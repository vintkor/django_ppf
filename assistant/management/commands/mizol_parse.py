from django.core.management.base import BaseCommand, CommandError
from assistant.utils import parse_mizol


class Command(BaseCommand):
    help = 'Parse Mizol'

    def handle(self, *args, **option):
        print('-' * 80)
        parse_mizol()
