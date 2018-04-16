import requests
from django.core.management.base import BaseCommand, CommandError
import csv
from django.utils.crypto import get_random_string
from catalog.models import Product, Category, Feature
from django.template.defaultfilters import slugify as django_slugify


class Command(BaseCommand):

    def handle(self, *args, **option):
        print('-'*150)

        with open('atmosfera.csv', 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file, delimiter=';')
            index = 0
            for row in reader:
                if row['Название_позиции'] \
                        and row['Описание'] \
                        and row['Название_позиции'] != row['Описание']:

                    print(' '*50, index)

                    url = row['Ссылка_изображения'].split(',')[0]

                    product = Product()

                    product.title = row['Название_позиции']
                    product.slug = self.slugify(row['Название_позиции'])
                    product.meta_keywords = row['Ключевые_слова']
                    product.description = row['Описание']
                    product.active = True

                    product.save()
                    product.category.add(Category.objects.get(title='Альтернативная энергетика').pk)

                    if row.get('Атрибут_Гарантийный срок(мес.)'):
                        feature_1 = Feature(
                            title='Гарантия',
                            value=row['Атрибут_Гарантийный срок(мес.)'],
                            product=product,
                        )
                        feature_1.save()

                    if row.get('Атрибут_Вес(кг)'):
                        feature_2 = Feature(
                            title='Вес',
                            value=row['Атрибут_Вес(кг)'],
                            product=product,
                        )
                        feature_2.save()

                    if row.get('Страна_производитель'):
                        feature_3 = Feature(
                            title='Страна производитель',
                            value=row['Страна_производитель'],
                            product=product,
                        )
                        feature_3.save()

                    if url:
                        ext = self.get_file_ext(url)
                        filename = self.make_filename(product.pk, ext)
                        self.get_and_save_image(url, filename)

                        product.image = filename
                        product.save(update_fields=('image',))
                    else:
                        product.delete()

                    index += 1

    @staticmethod
    def get_and_save_image(url, filename):
        r = requests.get(url)
        if r.status_code == 200:
            with open('media/' + filename, 'wb') as file:
                file.write(r.content)

    @staticmethod
    def make_filename(pk, ext):
        name = get_random_string(25)
        return 'images/catalog/product/{}__{}.{}'.format(pk, name, ext)

    @staticmethod
    def get_file_ext(url):
        return url.split('.')[-1]

    @staticmethod
    def slugify(s):
        alphabet = {'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'yo', 'ж': 'zh', 'з': 'z',
                    'и': 'i',
                    'й': 'j', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't',
                    'у': 'u', 'ф': 'f', 'х': 'kh', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'shch', 'ы': 'i', 'э': 'e',
                    'ю': 'yu',
                    'я': 'ya'}
        return django_slugify(''.join(alphabet.get(w, w) for w in s.lower()))

