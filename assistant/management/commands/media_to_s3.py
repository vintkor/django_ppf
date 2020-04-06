from django.core.management.base import BaseCommand, CommandError
from django.core.files import File
from django.conf import settings
from django.apps import apps
import re
from django_ppf.storage_backends import PublicMediaStorage


class Command(BaseCommand):
    """
        python manage.py media_to_s3 catalog.Product description
        python manage.py media_to_s3 catalog.Product description_ru
        python manage.py media_to_s3 catalog.Product description_uk
        python manage.py catalog.Product use
        python manage.py catalog.Product use_ru
        python manage.py catalog.Product use_uk
    """

    def add_arguments(self, parser):
        parser.add_argument('app.model', type=str)
        parser.add_argument('field', type=str)

    def handle(self, *args, **options):
        app_name, model_name = options['app.model'].split('.')
        model = apps.get_model(app_label=app_name, model_name=model_name)

        field = options['field']
        pattern = r'src=\"\/media\/(.*?)\" '

        for item in model.objects.all().iterator():
            text = getattr(item, field)

            if not text:
                continue

            images = re.findall(pattern, text)
            if not images:
                continue

            templates = []

            for image in images:
                basename = '/media/{}'.format(image)
                full_path = '{}{}'.format(settings.BASE_DIR, basename)

                storage = PublicMediaStorage()

                if not storage.exists(image):
                    try:
                        with open(full_path, 'rb') as f:
                            storage.save(image, f)
                    except Exception as error:
                        print(error)

                file_url = storage.url(image)
                templates.append([basename, file_url])

            for i in templates:
                text = text.replace(i[0], i[1])

            setattr(item, field, text)
            item.save(update_fields=(field,))
