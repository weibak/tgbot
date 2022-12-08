import os

import aiohttp
import aioredis
import logging
from telegram import Update, Bot
from telegram.ext import ContextTypes


BOT_TOKEN = os.getenv("BOT_TOKEN")
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")

redis = aioredis.from_url(f"redis://{REDIS_HOST}")
logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)


async def get_chat_ids():
    chat_ids = []
    chat_len = await redis.llen("chats")
    for index in range(chat_len):
        chat_id = await redis.lindex("chats", index)
        chat_ids.append(chat_id.decode())
    return list(set(chat_ids))


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await redis.lpush("chats", update.effective_chat.id)
    logger.info(await get_chat_ids())
    await update.message.reply_text("Welcome, I can show you some information about auctions and adverts\nPress /info "
                                    "and take a list of commands")


async def info(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(" Commands\n Start: /start\n News: /news\n All auctions: /all_auctions\n "
                                    "All adverts: /all_adverts\n")


async def message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await redis.publish("messages", update.message.text)


async def all_auctions(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await get_cars_auctions("http://127.0.0.1:8000/api/auctions/", update, context)


async def all_adverts(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await get_cars_adverts("http://127.0.0.1:8000/api/adverts/", update, context)


async def all_news(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await get_news("http://127.0.0.1:8000/api/news/", update, context)


async def adverts_bmw(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await get_cars_adverts("http://127.0.0.1:8000/api/adverts/?mark=BMW", update, context)


async def adverts_merc(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await get_cars_adverts("http://127.0.0.1:8000/api/adverts/?mark=MERCEDES", update, context)


async def adverts_toyo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await get_cars_adverts("http://127.0.0.1:8000/api/adverts/?mark=TOYOTA", update, context)


async def adverts_before_3000(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await get_cars_adverts("http://127.0.0.1:8000/api/adverts/?max_price=3000", update, context)


async def adverts_3000_6000(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await get_cars_adverts("http://127.0.0.1:8000/api/adverts/?min_price=3000&max_price=6000", update, context)


async def adverts_6000_9000(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await get_cars_adverts("http://127.0.0.1:8000/api/adverts/?min_price=6000&max_price=9000", update, context)


async def adverts_up_9000(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await get_cars_adverts("http://127.0.0.1:8000/api/adverts/?min_price=9000", update, context)


async def get_cars_adverts(url: str, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            cars = await response.json()
    result = ""
    for car in cars["results"]:
        result += f"Mark: {car['car_']['car_model']['mark']['car_mark']}\n" \
                  f"Model: {car['car_']['car_model']['car_model']}\n"\
                  f"Year: {car['car_']['year']}\n"\
                  f"Engine: {car['engine_type']}\nCapacity: {car['engine_capacity']}\n"\
                  f"Drive: {car['drive']}\nGear box: {car['gear_box']}\nDescription: {car['description']}\n"\
                  f"Image: {car['image']}\nWin: {car['win']}\nPrice: {car['price']}\nPrice USD: {car['price_usd']}\n"\
                  f"Phone number: {car['phone_number']}\n\n"
    await update.message.reply_text(result)


async def get_cars_auctions(url: str, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            cars = await response.json()
    result = ""
    for car in cars["results"]:
        result += f"Car: {car['car_id']}\nEngine: {car['engine_type']}\nCapacity: {car['engine_capacity']}\n" \
                  f"Drive: {car['drive']}\nGear box: {car['gear_box']}\nDescription: {car['description']}\n" \
                  f"Image: {car['image']}\nWin: {car['win']}\nPrice: {car['price']}\n\n"
    await update.message.reply_text(result)


async def get_news(url: str, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            news = await response.json()
    result = ""
    for new in news["results"]:
        result += f"{new['title']}\n{new['image']}\n{new['text']}\n{new['created_at']}\n"
    await update.message.reply_text(result)


async def send_message(text: str, chat_id: int = None) -> None:
    bot = Bot(BOT_TOKEN)
    if chat_id is not None:
        await bot.send_message(chat_id=chat_id, text=text)
        return
    for chat_id in await get_chat_ids():
        await bot.send_message(chat_id=chat_id, text=text)


async def redis_subscriber(ws):
    async with redis.pubsub() as channel:
        await channel.subscribe("messages")
        async for response in channel.listen():
            if isinstance(response.get("data"), bytes):
                await ws.send_str(response.get('data').decode())
            else:
                await ws.send_str(f"Pubsub channel: {response.get('data')}")
