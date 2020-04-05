from django.core.management.base import BaseCommand, CommandError
from django.core.files import File
from django.conf import settings
from django.apps import apps


class Command(BaseCommand):
    """
        python manage.py catalog.Category image
        python manage.py catalog.Manufacturer logo
        python manage.py catalog.Product image
        python manage.py catalog.Benefit image
        python manage.py catalog.Gallery image
        python manage.py catalog.Document file
        python manage.py catalog.Color image

        python manage.py assistant.Product image
        python manage.py assistant.Feature file
        python manage.py assistant.Photo image

        python manage.py company.Gallery image

        python manage.py geo.Region image
        python manage.py geo.ObjectImage image

        python manage.py library.Document file

        python manage.py news.News image
        python manage.py news.Promo image
        python manage.py news.Promo small_image

        python manage.py partners.File file

        python manage.py solutions.SolProduct image
        python manage.py solutions.SolOffer image

        python manage.py user_profile.Profile avatar
    """

    def add_arguments(self, parser):
        parser.add_argument('app.model', type=str)
        parser.add_argument('image_field', type=str)

    def handle(self, *args, **options):
        app_name, model_name = options['app.model'].split('.')
        model = apps.get_model(app_label=app_name, model_name=model_name)

        image_field = options['image_field']

        for item in model.objects.all().iterator():
            mediafile = getattr(item, image_field)
            if not mediafile:
                continue

            filename = '{}/media/{}'.format(settings.BASE_DIR, mediafile)
            try:
                with open(filename, 'rb') as f:
                    myfile = File(f)
                    setattr(item, image_field, myfile)
                    item.save()
            except Exception as error:
                print(error)
