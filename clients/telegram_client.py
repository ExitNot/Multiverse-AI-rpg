import logging as log

from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

from config import TELEGRAM_BOT_TOKEN
from clients.base_client import BaseClient

# set higher logging level for httpx to avoid all GET and POST requests being logged
log.getLogger("httpx").setLevel(log.WARNING)

logger = log.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context.
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    '''Send a message when the command /start is issued.'''
    user = update.effective_user
    await update.message.reply_html(
        rf"Hi {user.mention_html()}!",
        reply_markup=ForceReply(selective=True),
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    '''Send a message when the command /help is issued.'''
    await update.message.reply_text("Help!")


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    '''Echo the user message.'''
    await update.message.reply_text(update.message.text)


class TelegramClient(BaseClient):
    def __init__(self):
        self.application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
        
        # on different commands - answer in Telegram
        self.application.add_handler(CommandHandler("start", start))
        self.application.add_handler(CommandHandler("help", help_command))
        
        # on non command i.e message - echo the message on Telegram
        self.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    def start(self) -> None:
        """Start the telegram bot"""
        self.application.run_polling(allowed_updates=Update.ALL_TYPES)

    def stop(self) -> None:
        """Stop the telegram bot"""
        self.application.stop()