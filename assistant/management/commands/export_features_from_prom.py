from django.core.management.base import BaseCommand, CommandError
from assistant.utils import ExportFeatures


class Command(BaseCommand):
    help = 'Импорт характеристик с прома на ассистант через .csv файл'

    def handle(self, *args, **option):
        export = ExportFeatures('media/yandex_market.xml')
        export.parse_features()
        export.save_params()
