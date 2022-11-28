import asyncio

from django.conf import settings
from django.core.management.base import BaseCommand

from zetter.zetter_bot import send_message


class Command(BaseCommand):
    help = " send message"

    def handle(self, *args, **options):
        asyncio.run(send_message(chat_id=settings.CHAT_ID, text="Test notification"))
