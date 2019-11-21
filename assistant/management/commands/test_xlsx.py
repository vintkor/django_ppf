from django.core.management.base import BaseCommand, CommandError
from assistant.utils import make_xlsx_for_prom


class Command(BaseCommand):

    def handle(self, *args, **option):
        make_xlsx_for_prom()