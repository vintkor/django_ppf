from assistant.models import Product, Parameter, Category
from datetime import datetime
from xml.dom import minidom
from django.conf import settings
from bs4 import BeautifulSoup
import requests
from django.utils.crypto import get_random_string
import decimal
from currency.models import Currency
from openpyxl import load_workbook
from django.db.transaction import atomic
import csv
import os


class ExportFeatures:
    """
    Импорт параметров из прома на ассистант
    """

    def __init__(self, filename):
        self._filename = filename
        self.products = []

    def make_product_list(self):
        with open(self._filename, 'r', newline='') as file:
            reader = csv.reader(file)
            for idx, row in enumerate(reader):
                if idx == 0:
                    continue
                self.products.append([
                    i for index, i in enumerate(row) if index in range(34, len(row)+3) or index == 0
                ])

    def save_parameters(self):
        temp = []
        for product in self.products:
            temp_list = []
            count_parameters = (len(product) - 1)//3
            if count_parameters > 0:
                x, y, z = 1, 3, 2
                for i in range(count_parameters):
                    temp_list.append((product[x], product[y] + ' ' + product[z]))
                    x, y, z = x + 3, y + 3, z + 3
            temp.append({product[0]: temp_list})

        for i in temp:
            for product_code, v in i.items():
                try:
                    p = Product.objects.get(code=product_code)
                    param_list = []
                    for j in v:
                        if len(j[1]) > 1:
                            param_list.append(Parameter(
                                product=p,
                                parameter=j[0],
                                value=j[1],
                            ))
                    Parameter.objects.bulk_create(param_list)
                except:
                    pass


def clear_content(content):
    soup = BeautifulSoup(content, "html.parser")

    for img in soup('img'):
        img.decompose()

    for a in soup('a'):
        a.decompose()

    for iframe in soup('iframe'):
        iframe.decompose()

    return str(soup)


def make_xml(products=None):
    if products:
        products = products
    else:
        products = Product.objects.filter(import_to_rozetka=True)

    category_list = []
    for product in products:
        if product.import_to_rozetka:
            [
                category_list.append(j) for j in [
                    i for i in product.category_rozetka.get_ancestors(include_self=True, ascending=False)
                ]
            ]

    categories_list = [i for i in set(category_list)]

    imp = minidom.DOMImplementation()
    doctype = imp.createDocumentType(
        qualifiedName="yml_catalog",
        publicId="",
        systemId="shops.dtd",
    )

    doc = minidom.Document()
    doc.appendChild(doctype)

    yml_catalog = doc.createElement('yml_catalog')
    doc.appendChild(yml_catalog)
    yml_catalog.setAttribute('date', datetime.now().strftime("%Y-%m-%d %H:%M"))

    shop = doc.createElement('shop')
    yml_catalog.appendChild(shop)

    name = doc.createElement('name')
    name_text = doc.createTextNode('PPF Company')
    name.appendChild(name_text)
    shop.appendChild(name)

    company = doc.createElement('company')
    company_text = doc.createTextNode('PPF Company inc.')
    company.appendChild(company_text)
    shop.appendChild(company)

    url = doc.createElement('url')
    url_text = doc.createTextNode(settings.SITE_URL)
    url.appendChild(url_text)
    shop.appendChild(url)

    currencies = doc.createElement('currencies')
    shop.appendChild(currencies)

    currency = doc.createElement('currency')
    currency.setAttribute('id', 'UAH')
    currency.setAttribute('rate', '1')
    currencies.appendChild(currency)

    categories = doc.createElement('categories')
    shop.appendChild(categories)

    for cat in categories_list:
        category = doc.createElement('category')
        category_text = doc.createTextNode(cat.title)
        if cat.parent:
            category.setAttribute('parentId', str(cat.parent.id))
        category.setAttribute('id', str(cat.id))
        category.appendChild(category_text)
        categories.appendChild(category)

    offers = doc.createElement('offers')
    shop.appendChild(offers)

    for product in products:
        if product.import_to_rozetka:
            offer = doc.createElement('offer')
            offer.setAttribute('id', '{}'.format(product.id))
            offer.setAttribute('available', 'true')
            offers.appendChild(offer)

            offer_url = doc.createElement('url')
            offer_url_text = doc.createTextNode('{}{}'.format(settings.SITE_URL, product.get_absolute_url()))
            offer_url.appendChild(offer_url_text)
            offer.appendChild(offer_url)

            price = doc.createElement('price')
            price_text = doc.createTextNode(str(product.get_price_UAH()))
            price.appendChild(price_text)
            offer.appendChild(price)

            currencyId = doc.createElement('currencyId')
            currencyId_text = doc.createTextNode('UAH')
            currencyId.appendChild(currencyId_text)
            offer.appendChild(currencyId)

            categoryId = doc.createElement('categoryId')
            categoryId_text = doc.createTextNode(str(product.category_rozetka.id))  # <--
            categoryId.appendChild(categoryId_text)
            offer.appendChild(categoryId)

            if product.image:
                picture = doc.createElement('picture')
                picture_text = doc.createTextNode('{}{}'.format(settings.SITE_URL, product.image.url))
                picture.appendChild(picture_text)
                offer.appendChild(picture)

            for photo in product.get_images():
                picture_set = doc.createElement('picture')
                picture_set_text = doc.createTextNode('{}{}'.format(settings.SITE_URL, photo.image.url))
                picture_set.appendChild(picture_set_text)
                offer.appendChild(picture_set)

            vendor = doc.createElement('vendor')
            vendor_text = doc.createTextNode(product.manufacturer.title)
            vendor.appendChild(vendor_text)
            offer.appendChild(vendor)

            stock_quantity = doc.createElement('stock_quantity')
            stock_quantity_text = doc.createTextNode(str(product.stock_quantity))
            stock_quantity.appendChild(stock_quantity_text)
            offer.appendChild(stock_quantity)

            name = doc.createElement('name')
            name_text = doc.createTextNode('{title} ({code})'.format(
                title=product.title,
                code=product.code,
            ))
            name.appendChild(name_text)
            offer.appendChild(name)

            description = doc.createElement('description')
            cdata = doc.createCDATASection(clear_content(product.text))
            description.appendChild(cdata)
            offer.appendChild(description)

            # param1 = doc.createElement('param')
            # param1_text = doc.createTextNode(product.code)
            # param1.appendChild(param1_text)
            # param1.setAttribute('name', 'Артикул')
            # offer.appendChild(param1)

            for feature in product.parameter_set.filter(is_dop_param_for_rozetka=False):
                param2 = doc.createElement('param')
                param2_text = doc.createTextNode(feature.value)
                param2.appendChild(param2_text)
                param2.setAttribute('name', feature.parameter)
                offer.appendChild(param2)

            dop_parameters = []
            for dop_param in product.parameter_set.filter(is_dop_param_for_rozetka=True):
                dop_parameters.append('{}: {}<br/>'.format(dop_param.parameter, dop_param.value))

            param3 = doc.createElement('param')
            param3.setAttribute('name', 'Дополнительные характеристики')
            cdata2 = doc.createCDATASection(''.join(dop_parameters))
            param3.appendChild(cdata2)
            offer.appendChild(param3)

    file_handle = open("rozetka.xml", "w")
    doc.writexml(file_handle, encoding='UTF-8')
    file_handle.close()


def parse_atmosfera():
    file_path = 'http://www.atmosfera.ua/xport2shop/AtmosferaProds2exportUA.xml'
    r = requests.get(file_path)
    soup = BeautifulSoup(r.content, 'xml')

    categories = dict()
    for link in soup.find_all('category'):
        categories[link.get('id')] = {
            'parent_id': link.get('parentId'),
            'title': link.text,
        }

    products = list()
    for product in soup.find_all('item'):
        products.append({
            'id': product.find('Код_товара').text if product.find('Код_товара') else False,
            'price': product.find('Цена').text if product.find('Цена') else False,
            'category': product.find('parentId').text if product.find('parentId') else False,
            'currency': product.find('Валюта').text if product.find('Валюта') else False,
            'unit': product.find('Единица_измерения').text if product.find('Единица_измерения') else False,
            'images': product.find('Ссылка_изображения').text if product.find('Ссылка_изображения') else False,
            'title': product.find('Название_позиции').text if product.find('Название_позиции') else False,
            'vendor': product.find('Производитель').text if product.find('Производитель') else False,
            'country': product.find('Страна_производитель').text if product.find('Страна_производитель') else False,
            'desc': product.find('Описание').text if product.find('Описание') else False,
            'keywords': product.find('Ключевые_слова').text if product.find('Ключевые_слова') else False,
            'params': [{
                'name': p.get('name'),
                'value': p.text,
            } for p in product.find_all('param')],
        })

    print('-------------- CATEGORIES --------------')
    for k, v in categories.items():
        print(k, v)

    print('-------------- PRODUCTS --------------')
    for p in products:
        print(p)


def get_and_save_image(url, filename):
    r = requests.get(url)
    if r.status_code == 200:
        with open('media/' + filename, 'wb') as file:
            file.write(r.content)


def make_filename(pk, ext):
    name = get_random_string(25)
    return 'images/{}__{}'.format(pk, name)


def get_file_ext(url):
    return url.split('.')[-1]


def parse_yantarlk():
    """ Парсер сайта https://yantarlk.com.ua/ """

    try:
        test_category = Category.objects.get(title='TEST CATEGORY')
    except Category.DoesNotExist:
        test_category = Category(title='TEST CATEGORY')
        test_category.save()

    currency = Currency.objects.get(code='UAH')

    url = 'https://yantarlk.com.ua/'
    headers = requests.utils.default_headers()
    headers.update(
        {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
        }
    )
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.content, 'lxml')

    category_links = [
        i.find('a').get('href') for i in
        soup.find('div', attrs={'id': 'menu2'}).find_all('div', attrs={'class': 'title'})
    ]

    product_links = []
    for category_url in category_links:
        r = requests.get(category_url + '/?limit=2000', headers=headers)
        soup = BeautifulSoup(r.content, 'lxml')
        for i in soup.find_all('h4'):
            link = i.find('a').get('href')
            product_links.append(link)

    # product_links = ['https://yantarlk.com.ua/spec_sredstva_i_material/mastika_oz']
    products = []
    for index, product_link in enumerate(product_links):
        print('---------- Page {}'.format(index))
        r = requests.get(product_link, headers=headers)
        soup = BeautifulSoup(r.content, 'lxml')

        try:
            types_list = soup.find('div', attrs={'class', 'options_no_buy'}).find_all('div', attrs={'class': 'radio'})
        except:
            continue

        params_list = []
        for type in types_list:
            temp_types = type.find_all('span')
            params = dict()
            params['weight'] = temp_types[0].text
            try:
                params['plus_price'] = temp_types[1].text.split('+')[1].split(' ')[0]
            except IndexError:
                pass
            params_list.append(params)

        parameters = []
        for param_row in soup.find_all('tr', attrs={'itemprop': 'additionalProperty'}):
            row = param_row.find_all('td')
            try:
                parameters.append({
                    'name': row[0].text,
                    'value': row[1].text,
                })
            except IndexError:
                pass

        title = soup.find('title').text.split(' - купить ')[0]
        image_link = soup.find('a', attrs={'class': 'main-image'}).get('href')
        price = soup.find('span', attrs={'class': 'update_price'}).text.split('грн')[0]
        desc = soup.find('div', attrs={'id': 'tab-description'}).text

        for pl in params_list:
            prod_dict = {
                'title': title + ' ' + pl['weight'],
                'image': image_link,
                'description': desc,
                'parameters': parameters,
                'weight': pl['weight'],
                'vendor_name': 'ЯНТАРЬ',
            }
            # try:
            #     prod_dict['price'] = int(price) + int(pl.get('plus_price')) if pl.get('plus_price') else price
            # except:
            #     prod_dict['price'] = 0

            products.append(prod_dict)

    print('Finded', len(products), 'products')

    for ind, i in enumerate(products):
        product = Product()
        product.category = test_category
        product.vendor_name = i['vendor_name']
        product.title = i['title']
        product.text = i['description']
        # product.price = decimal.Decimal(i['price'])
        product.stock_quantity = 100
        product.active = True
        product.currency = currency
        product.save()

        parameter = Parameter()
        parameter.product = product
        parameter.parameter = 'Произвадитель'
        parameter.value = i['vendor_name']
        parameter.save()

        parameter2 = Parameter()
        parameter2.product = product
        parameter2.parameter = 'Страна'
        parameter2.value = 'Украина'
        parameter2.save()

        for param in i['parameters']:
            new_param = Parameter()
            new_param.product = product
            new_param.parameter = param['name']
            new_param.value = param['value'][:199]
            new_param.save()

        if i['image']:
            url = i['image']

            ext = get_file_ext(url)
            filename = make_filename(product.pk, ext)
            get_and_save_image(url, filename)

            product.image = filename
            product.save(update_fields=('image',))

        print('Saved', ind + 1, 'from', len(products), 'products')


def parse_mizol():
    file_path = 'http://api.mizol.ua/?modelName=Mizol_Characteristics&calledMethod=getProductCharacteristic&methodProperties[price]=RRC&apiKey=52542&hash=5398382aa014f0a06312ff751c5949c4cbb52f61ba02341dbf67ecedfab68bcf'
    r = requests.get(file_path)
    soup = BeautifulSoup(r.content, 'xml')
    vendor_name = 'Mizol'

    try:
        test_category = Category.objects.get(title='TEST CATEGORY')
    except Category.DoesNotExist:
        test_category = Category(title='TEST CATEGORY')
        test_category.save()

    products_id_in_db = [
        int(product['vendor_id']) for product in Product.objects.filter(vendor_name=vendor_name).values('vendor_id')
    ]

    new_products = list()
    products_for_update = list()

    for ind, product in enumerate(soup.find_all('offer')):
        print('----> finded', ind, 'products')

        if int(product['id']) in products_id_in_db:
            products_for_update.append({
                'vendor_id': int(product['id']),
                'price': decimal.Decimal(product.find('price').text) if product.find('price').text else 0,
            })
        else:
            new_products.append({
                'vendor_id': int(product['id']),
                'vendor_name': vendor_name,
                'title': product.find('name').text,
                'manufacturer': product.find('vendor').text if product.find('vendor').text else None,
                'country': product.find('country').text if product.find('country').text else None,
                'description': product.find('description').text,
                'active': True if product.find('available') == 'true' else False,
                'picture': product.find('picture').text if product.find('picture').text else None,
                'price': decimal.Decimal(product.find('price').text) if product.find('price').text else 0,
            })

    len_products_for_update = len(products_for_update)
    len_new_products = len(new_products)

    currency = Currency.objects.get(code='UAH')

    for ind, i in enumerate(new_products):
        product = Product()
        product.category = test_category
        product.vendor_id = i['vendor_id']
        product.vendor_name = i['vendor_name']
        product.title = i['title']
        product.text = i['description']
        product.active = True
        product.currency = currency
        product.save()

        if i['manufacturer']:
            parameter = Parameter()
            parameter.product = product
            parameter.parameter = 'Произвадитель'
            parameter.value = i['vendor_name']
            parameter.save()

        if i['country']:
            parameter2 = Parameter()
            parameter2.product = product
            parameter2.parameter = 'Страна'
            parameter2.value = i['country']
            parameter2.save()

        if i['picture']:
            url = i['picture']

            ext = get_file_ext(url)
            filename = make_filename(product.pk, ext)
            get_and_save_image(url, filename)

            product.image = filename
            product.save(update_fields=('image',))

        print('----> added', ind, 'items from', len_new_products)

    for ind, i in enumerate(products_for_update):
        product = Product.objects.get(vendor_name=vendor_name, vendor_id=i['vendor_id'])
        if product.price != i['price']:
            product.price = i['price']
            product.save(update_fields=('price',))

            print('----> updated', ind, 'items from', len_products_for_update)


def update_mizol_prices(filename):
    print('-'*80)
    wb = load_workbook(settings.MEDIA_ROOT + '/' +filename)
    sheet_name = wb.sheetnames[0]
    sheet = wb[sheet_name]

    data_list = []

    for row in sheet.rows:
        data_list.append({
            'id': row[1].value,
            'available': '-' if row[6].value == '-' else '+',
            'price': row[10].value,
        })

    data_update = []

    with atomic():
        for i in data_list:
            # try:
            #     # TODO Переписать на filter
            #     # product = Product.objects.get(vendor_id=i['id'], vendor_name='Mizol')
            # except:
            #     continue
            products = Product.objects.filter(vendor_id=i['id'], vendor_name='Mizol')

            for product in products:
                product.price = decimal.Decimal(i['price'])
                product.availability_prom = i['available']
                product.save(update_fields=('price', 'availability_prom',))

                data_update.append(product)


def import_parameters_form_prom(filename):
    import_csv = ExportFeatures(filename)
    import_csv.make_product_list()
    import_csv.save_parameters()

    os.remove(filename)
