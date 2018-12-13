from django.core.management.base import BaseCommand, CommandError
from assistant.utils import ParseHoroz


class Command(BaseCommand):
    help = 'Parse Horoz'

    def handle(self, *args, **option):
        print('-' * 80)
        ph = ParseHoroz(link='https://horozua.com/index.php?route=feed/yandex_yml', my_currency_code='USD')
        ph.set_products()
        ph.add_or_update_products_in_db()
