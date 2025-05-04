import logging as log
import json
import os

from telegram import ForceReply, Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters, CallbackQueryHandler

from config import TELEGRAM_BOT_TOKEN
from clients.base_client import BaseClient

# set higher logging level for httpx to avoid all GET and POST requests being logged
log.getLogger("httpx").setLevel(log.WARNING)

logger = log.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context.
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    '''Send a message with language selection buttons when the command /start is issued.'''
    keyboard = [
        [
            InlineKeyboardButton("English 🇬🇧", callback_data="lang_selected_en"),
            InlineKeyboardButton("Ukrainian 🇺🇦", callback_data="lang_selected_uk"),
        ],
        [
            InlineKeyboardButton("Russian 🇷🇺", callback_data="lang_selected_ru"),
            InlineKeyboardButton("Czech 🇨🇿", callback_data="lang_selected_cs"),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Choose your language:", reply_markup=reply_markup)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    '''Send a message when the command /help is issued.'''
    await update.message.reply_text("Help!")


def get_user_logger(user_id: int) -> logging.Logger:
    """Create or get a logger for specific user"""
    logger = logging.getLogger(f'user_{user_id}')
    
    if not logger.handlers:
        os.makedirs('logs/users', exist_ok=True)
        handler = logging.FileHandler(f'logs/users/user_{user_id}.log')
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
    
    return logger

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    '''Echo the user message and log it'''
    user_id = update.effective_user.id
    user_logger = get_user_logger(user_id)
    user_logger.info(f"Message: {update.message.text}")
    await update.message.reply_text(update.message.text)


def load_locale(lang_code: str) -> dict:
    """Load localization strings for the specified language to user settings (DB)."""
    # TODO: DB insertion of language setting 


async def language_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    '''Handle the language selection callback.'''
    query = update.callback_query
    await query.answer()
    
    # Get the selected language from callback data
    lang_code = query.data.split('_')[2]  # lang_selected_en -> en
    locale = load_locale(lang_code)
    
    language_names = {
        'en': locale.get('language_name', 'English'),
        'uk': locale.get('language_name', 'Ukrainian'),
        'ru': locale.get('language_name', 'Russian'),
        'cs': locale.get('language_name', 'Czech')
    }
    
    await query.edit_message_text(locale.get('language_selected', 'You have selected {language}')
                                  .format(language=language_names[lang_code]))


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