import logging as log
import json
import os
import uuid
from datetime import datetime

from telegram import ForceReply, Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters, CallbackQueryHandler

from config import TELEGRAM_BOT_TOKEN
from clients.base_client import BaseClient
from services.user_service import UserService

# set higher logging level for httpx to avoid all GET and POST requests being logged
log.getLogger("httpx").setLevel(log.WARNING)

logger = log.getLogger(__name__)

# Initialize services
user_service = UserService()

def get_user_info(user) -> dict:
    """
    Extract essential user information from Telegram user object
    
    Args:
        user: Telegram user object
        
    Returns:
        dict: User information dictionary
    """
    return {
        "telegram_id": str(user.id),
        "username": user.username,
        "language_code": user.language_code,
        "game_settings": {
            "language": user.language_code or "en"  # Use Telegram language code or default to English
        }
    }

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    '''Send a message with language selection buttons when the command /start is issued.'''
    user = update.effective_user
    telegram_id = str(user.id)
    
    try:
        # Check if user already exists
        existing_account = await user_service.get_user_by_telegram_id(telegram_id)
        
        if existing_account:
            # User exists, show welcome back message
            welcome_message = user_service.get_localized_message(
                existing_account,
                "welcome_back",
                language=existing_account.get('game_settings', {}).get('language', 'en')
            )
            await update.message.reply_text(welcome_message)
            return
        
        # Create new account with default settings
        user_info = get_user_info(user)
        new_user = await user_service.create_user(
            telegram_id=user_info['telegram_id'],
            username=user_info['username'],
            language_code=user_info['game_settings']['language']
        )
        
        # Show language selection for new user
        reply_markup = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("English 🇬🇧", callback_data="lang_selected_en"),
                InlineKeyboardButton("Ukrainian 🇺🇦", callback_data="lang_selected_uk"),
            ],
            [
                InlineKeyboardButton("Russian 🇷🇺", callback_data="lang_selected_ru"),
                InlineKeyboardButton("Czech 🇨🇿", callback_data="lang_selected_cs"),
            ],
        ])
        
        welcome_message = user_service.get_localized_message(
            new_user,
            "welcome_new",
            language=new_user['game_settings']['language']
        )
        
        await update.message.reply_text(
            welcome_message,
            reply_markup=reply_markup
        )
    except Exception as e:
        logger.error(f"Error in start command: {str(e)}")
        error_message = user_service.get_localized_message(
            {"game_settings": {"language": "en"}},
            "error_generic"
        )
        await update.message.reply_text(error_message)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    '''Send a message when the command /help is issued.'''
    user = update.effective_user
    telegram_id = str(user.id)
    
    try:
        user_account = await user_service.get_user_by_telegram_id(telegram_id)
        if not user_account:
            user_account = {"game_settings": {"language": "en"}}
            
        help_message = user_service.get_localized_message(
            user_account,
            "help_message"
        )
        await update.message.reply_text(help_message)
    except Exception as e:
        logger.error(f"Error in help command: {str(e)}")
        error_message = user_service.get_localized_message(
            {"game_settings": {"language": "en"}},
            "error_generic"
        )
        await update.message.reply_text(error_message)

def get_user_logger(user_id: int) -> log.Logger:
    """Create or get a logger for specific user"""
    logger = log.getLogger(f'user_{user_id}')
    
    if not logger.handlers:
        os.makedirs('logs/users', exist_ok=True)
        handler = log.FileHandler(f'logs/users/user_{user_id}.log')
        formatter = log.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(log.INFO)
    
    return logger

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    '''Echo the user message and log it'''
    user_id = update.effective_user.id
    user_logger = get_user_logger(user_id)
    user_logger.info(f"Message: {update.message.text}")
    await update.message.reply_text(update.message.text)


def load_locale(lang_code: str) -> dict:
    """Load localization strings for the specified language."""
    # TODO: Implement proper locale loading
    return {
        'language_name': {
            'en': 'English',
            'uk': 'Ukrainian',
            'ru': 'Russian',
            'cs': 'Czech'
        }.get(lang_code, 'English'),
        'language_selected': 'You have selected {language}'
    }


async def language_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    '''Handle the language selection callback.'''
    query = update.callback_query
    await query.answer()
    
    try:
        # Get the selected language from callback data
        lang_code = query.data.split('_')[2]  # lang_selected_en -> en
        
        user = update.effective_user
        telegram_id = str(user.id)
        
        # Update existing account with new language
        existing_account = await user_service.get_user_by_telegram_id(telegram_id)
        if existing_account:
            await user_service.update_user_language(
                account_id=existing_account.get('account_id'),
                language_code=lang_code
            )
            
            # Get localized message for language change
            success_message = user_service.get_localized_message(
                {"game_settings": {"language": lang_code}},
                "language_changed",
                language=lang_code
            )
            await query.edit_message_text(success_message)
    except Exception as e:
        logger.error(f"Error in language callback: {str(e)}")
        error_message = user_service.get_localized_message(
            {"game_settings": {"language": "en"}},
            "error_language_change"
        )
        await query.edit_message_text(error_message)


class TelegramClient(BaseClient):
    def __init__(self):
        self.application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
        
        # on different commands - answer in Telegram
        self.application.add_handler(CommandHandler("start", start))
        self.application.add_handler(CommandHandler("help", help_command))
        
        # Add callback handler for language selection with pattern
        self.application.add_handler(CallbackQueryHandler(language_callback, pattern="^lang_selected_"))
        
        # on non command i.e message - echo the message on Telegram
        self.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    def start(self) -> None:
        """Start the telegram bot"""
        self.application.run_polling(allowed_updates=Update.ALL_TYPES)

    def stop(self) -> None:
        """Stop the telegram bot"""
        self.application.stop()