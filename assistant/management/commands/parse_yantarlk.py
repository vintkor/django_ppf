from django.core.management.base import BaseCommand, CommandError
from assistant.utils import parse_yantarlk


class Command(BaseCommand):
    help = 'Parse yantarlk'

    def handle(self, *args, **option):
        print('-' * 80)
        parse_yantarlk()
