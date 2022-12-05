import logging
import os

from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters

from services import start, info, all_news, message, all_auctions, all_adverts, adverts_bmw, adverts_merc, adverts_toyo, \
    adverts_before_3000, adverts_3000_6000, adverts_6000_9000, adverts_up_9000

logger = logging.getLogger(__name__)


BOT_TOKEN = os.getenv("BOT_TOKEN")


if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("info", info))
    app.add_handler(CommandHandler("news", all_news))
    app.add_handler(CommandHandler("all_auctions", all_auctions))
    app.add_handler(CommandHandler("bmw_adverts", adverts_bmw))
    app.add_handler(CommandHandler("merc_adverts", adverts_merc))
    app.add_handler(CommandHandler("toyo_adverts", adverts_toyo))
    app.add_handler(CommandHandler("bef_3000", adverts_before_3000))
    app.add_handler(CommandHandler("from_3000_to_6000", adverts_3000_6000))
    app.add_handler(CommandHandler("from_6000_to_9000", adverts_6000_9000))
    app.add_handler(CommandHandler("up_to_9000", adverts_up_9000))
    app.add_handler(CommandHandler("all_adverts", all_adverts))
    app.add_handler(MessageHandler(~filters.COMMAND, message))
    app.run_polling()
