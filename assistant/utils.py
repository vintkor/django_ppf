from assistant.models import Product
from datetime import datetime
from xml.dom import minidom
from django.conf import settings


def make_xml(products=None):
    if products:
        products = products
    else:
        products = Product.objects.all()

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

    category = doc.createElement('category')
    category_text = doc.createTextNode('Женская одежда')
    category.setAttribute('id', '2')
    category.appendChild(category_text)
    categories.appendChild(category)

    category2 = doc.createElement('category')
    category2_text = doc.createTextNode('Платья')
    category2.setAttribute('id', '22')
    category2.setAttribute('parentId', '2')
    category2.appendChild(category2_text)
    categories.appendChild(category2)

    offers = doc.createElement('offers')
    shop.appendChild(offers)

    for product in products:
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
        categoryId_text = doc.createTextNode('2')
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
        cdata = doc.createCDATASection(product.text)
        description.appendChild(cdata)
        offer.appendChild(description)

        param1 = doc.createElement('param')
        param1_text = doc.createTextNode(product.code)
        param1.appendChild(param1_text)
        param1.setAttribute('name', 'Артикул')
        offer.appendChild(param1)

        param = doc.createElement('param')
        param_text = doc.createTextNode('XL')
        param.appendChild(param_text)
        param.setAttribute('name', 'Размер')
        offer.appendChild(param)

    file_handle = open("rozetka.xml", "w")
    doc.writexml(file_handle, encoding='UTF-8')
    file_handle.close()
