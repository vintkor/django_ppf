from django.core.management.base import BaseCommand, CommandError
from bs4 import BeautifulSoup
import requests
from assistant.models import Product
from django.utils.crypto import get_random_string


class Command(BaseCommand):
    help = 'Spider http://rainway-shop.com.ua'

    def handle(self, *args, **option):
        site_url = 'http://rainway-shop.com.ua'
        product_postfix = ''
        links = [
            '{}/podshivka_kryshi'.format(site_url),
        ]

        product_links = []

        for link in links:
            r = requests.get(link)

            soup = BeautifulSoup(r.content, 'html.parser')
            pages = soup.find_all('figcaption', attrs={'class': 'figcaption'})
            for page in pages:
                product_links.append(site_url + page.find('a')['href'])

        products = []

        for i, link in enumerate(product_links):
            r = requests.get(link)
            soup = BeautifulSoup(r.content, 'html.parser')
            base_title = soup.find('h1')['data-orig']
            variants = soup.find_all('a', attrs={'class': '__listImg'})
            for variant in variants:
                products.append({
                    'title': '{}, {}'.format(base_title, variant['data-colorname']),
                    'image': site_url + variant['data-imgn'],
                    'description': '<p>{}</p>'.format(soup.find('div', attrs={'id': 'tab1'}).text),
                })

        for i in products:
            product = Product()
            product.title = i['title'] + product_postfix
            product.text = i['description']
            product.save()

            url = i['image']

            ext = self.get_file_ext(url)
            filename = self.make_filename(product.pk, ext)
            self.get_and_save_image(url, filename)

            product.image = filename
            product.save(update_fields=('image',))

    @staticmethod
    def get_and_save_image(url, filename):
        r = requests.get(url)
        if r.status_code == 200:
            with open('media/' + filename, 'wb') as file:
                file.write(r.content)

    @staticmethod
    def make_filename(pk, ext):
        name = get_random_string(25)
        return 'images/{}__{}.{}'.format(pk, name, ext)

    @staticmethod
    def get_file_ext(url):
        return url.split('.')[-1]
