import logging
import os

from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters

from services import start, info, all_news, message, all_auctions, all_adverts, adverts_bmw

logger = logging.getLogger(__name__)


BOT_TOKEN = os.getenv("BOT_TOKEN")


if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("info", info))
    app.add_handler(CommandHandler("news", all_news))
    app.add_handler(CommandHandler("all_auctions", all_auctions))
    app.add_handler(CommandHandler("bmw_adverts", adverts_bmw))
    app.add_handler(CommandHandler("all_adverts", all_adverts))
    app.add_handler(MessageHandler(~filters.COMMAND, message))
    app.run_polling()
