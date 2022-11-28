from django.core.management.base import BaseCommand

from zetter.zetter_bot import message, send_message, run_bot


class Command(BaseCommand):
    help = "Run telegram bot"

    def handle(self, *args, **options):
        run_bot()
