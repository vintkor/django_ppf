from django.core.management.base import BaseCommand, CommandError
from assistant.utils import ExportFeatures


class Command(BaseCommand):
    help = 'Импорт характеристик с прома на ассистант через .csv файл'

    def handle(self, *args, **option):
        export = ExportFeatures('prom.csv')
        export.make_product_list()
        export.save_parameters()
