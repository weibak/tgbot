from django.conf import settings
from asgiref.sync import sync_to_async
from telegram import Bot
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
from zetter.models import Message
import logging

logger = logging.getLogger(__name__)


def run_bot():
    logger.info(settings.BOT_TOKEN)
    app = ApplicationBuilder().token(settings.BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(~filters.COMMAND, message))
    app.run_polling()


@sync_to_async
def create_message(action: str, text: str):
    Message.objects.create(action=action, text=text, message={})


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f"Start {update.effective_user.first_name}")


async def message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await create_message(action="message", text=update.message.text)
    await update.message.reply_text(f"Message {update.effective_user.first_name}")


async def send_message(chat_id: int, text: str) -> None:
    bot = Bot(settings.BOT_TOKEN)
    await bot.send_message(chat_id=chat_id, text=text)
