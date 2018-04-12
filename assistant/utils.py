from assistant.models import Product
from datetime import datetime
from xml.dom import minidom
from django.conf import settings
from bs4 import BeautifulSoup


def clear_content(content):
    soup = BeautifulSoup(content, "html.parser")

    for img in soup('img'):
        img.decompose()

    for a in soup('a'):
        a.decompose()

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

    currency = doc.createElement('url')
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
            offer.setAttribute('id', '2322')
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
            stock_quantity_text = doc.createTextNode('100')
            stock_quantity.appendChild(stock_quantity_text)
            offer.appendChild(stock_quantity)

            name = doc.createElement('name')
            name_text = doc.createTextNode(product.title)
            name.appendChild(name_text)
            offer.appendChild(name)

            description = doc.createElement('description')
            cdata = doc.createCDATASection(clear_content(product.text))
            description.appendChild(cdata)
            offer.appendChild(description)

            param1 = doc.createElement('param')
            param1_text = doc.createTextNode(product.code)
            param1.appendChild(param1_text)
            param1.setAttribute('name', 'Артикул')
            offer.appendChild(param1)

            for feature in product.parameter_set.all():
                param2 = doc.createElement('param')
                param2_text = doc.createTextNode(feature.value)
                param2.appendChild(param2_text)
                param2.setAttribute('name', feature.parameter)
                offer.appendChild(param2)

    file_handle = open("rozetka.xml", "w")
    doc.writexml(file_handle, encoding='UTF-8')
    file_handle.close()
