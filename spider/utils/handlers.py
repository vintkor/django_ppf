import requests
from bs4 import BeautifulSoup
from decimal import Decimal
import html
from assistant.models import Product, Photo, Category
from assistant.utils import get_file_ext, make_filename, get_and_save_image
from currency.models import Currency


class ProductTemplate:

    def __init__(self, title, price, images, text, vendor_id, currency_id, available):
        self.title = title
        self.price = price
        self.images = images
        self.text = text
        self.vendor_id = vendor_id
        self.currency_id = currency_id
        self.available = available


class BaseHandler:
    vendor_name = None
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                             '(KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'}
    category = Category.objects.get(title='TEST CATEGORY')

    def __init__(self, sourse):
        self.sourse = sourse
        self.content = None
        self.products = []
        self._set_currencies()

    def _set_currencies(self):
        self.currencies = {i.code.upper(): i.id for i in Currency.objects.all()}

    def download_content(self):
        r = requests.get(self.sourse.url, headers=self.headers)
        if r.status_code == 200:
            self.content = r.text
        else:
            print('[ERROR] response status: {}'.format(r.status_code))

    def prepare_content(self):
        raise NotImplementedError()

    @staticmethod
    def decimal_or_none(digit_text):
        try:
            return Decimal(digit_text)
        except:
            return None

    @staticmethod
    def _download_image(path, product_pk):
        ext = get_file_ext(path)
        filename = make_filename(product_pk, ext)
        get_and_save_image(path, filename)
        return filename

    @staticmethod
    def _update_product(product, product_in_db):
        product_in_db.availability_prom = '+' if product.available else '-'
        product_in_db.active = product.available or False
        product_in_db.price = product.price
        product_in_db.save(update_fields=('availability_prom', 'price', 'active'))

    def _create_product(self, product):
        new_product = Product()
        new_product.category = self.category
        new_product.title = product.title
        new_product.price = product.price
        new_product.text = product.text
        new_product.vendor_id = product.vendor_id
        new_product.vendor_name = self.vendor_name
        new_product.currency_id = product.currency_id
        new_product.availability_prom = '+' if product.available else '-'
        new_product.active = product.available
        try:
            new_product.image = self._download_image(product.images[0], new_product.pk)
        except IndexError:
            pass
        new_product.save()

        try:
            for i in product.images[1:]:
                image = Photo()
                image.product = new_product
                image.image = self._download_image(i, new_product.pk)
                image.save()
        except IndexError:
            pass

    def create_or_update(self):
        for product in self.products:
            products_in_db = Product.objects.filter(
                vendor_id=product.vendor_id,
                vendor_name=self.vendor_name.lower()
            )
            if len(products_in_db) > 0:
                for product_in_db in products_in_db:
                    self._update_product(product, product_in_db)
            else:
                self._create_product(product)

    def parse(self):
        print('[INFO] Parsing {}'.format(self.vendor_name))
        self.download_content()

        if self.content:
            self.prepare_content()
        else:
            print('[ERROR] Content is None in {}'.format(self.vendor_name))
            return False

        self.create_or_update()


class VitanHandler(BaseHandler):
    vendor_name = 'vitan'

    def prepare_content(self):
        soup = BeautifulSoup(self.content, 'html5lib')
        mapping = self.sourse.rules['mapping']

        for offer in soup.find_all(self.sourse.rules['cycle_tag']):
            try:
                product = ProductTemplate(
                    title=html.unescape(offer.find(mapping['get_title']).text),
                    price=self.decimal_or_none(offer.find(mapping['get_price']).text),
                    images=[i.text for i in offer.find_all(mapping['get_image'])],
                    text=html.unescape(offer.find(mapping['get_text']).text),
                    vendor_id=offer.find('vendorcode').text,
                    currency_id=self.currencies.get(offer.find('currencyid').text.upper()),
                    available=True if offer['available'] == 'true' else False,
                )
                self.products.append(product)
            except:
                print('[ERROR] Parsing error in VitanHandler')


class OptovikHandler(VitanHandler):
    vendor_name = 'optovik'
