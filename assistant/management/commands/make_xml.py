from django.core.management.base import BaseCommand, CommandError
from assistant.utils import make_xml


class Command(BaseCommand):
    help = 'Импорт товаров без категорий из файла экспорта prom.ua'

    def handle(self, *args, **option):
        make_xml()
