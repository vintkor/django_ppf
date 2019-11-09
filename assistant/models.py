from django.db import models
from django_ppf.basemodel import BaseModel
from mptt.models import MPTTModel, TreeForeignKey
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils.crypto import get_random_string
from partners.models import Provider
from django.urls import reverse
from currency.models import Currency
from django.utils.html import format_html
from catalog.models import Manufacturer
from django.contrib.auth.models import User
from assistant.middleware import get_current_user
from django.utils.safestring import mark_safe


def set_image_name(instance, filename):
    name = get_random_string(40)
    ext = filename.split('.')[-1]
    path = 'images/{}.{}'.format(name, ext)
    return path


def set_file_name(instance, filename):
    name = get_random_string(40)
    ext = filename.split('.')[-1]
    path = 'files/{}.{}'.format(name, ext)
    return path


def set_code():
    last_product = Product.objects.first()
    if last_product is None:
        new_code = 'ПФ-10000'
    else:
        last_code = last_product.code.split('-')
        new_code = '{}-{}'.format(last_code[0], (int(last_code[1]) + 1))
    return new_code


class Unit(BaseModel):
    title = models.CharField(max_length=200, verbose_name='Название')
    short_title = models.CharField(max_length=10, verbose_name='Короткое обозначение')

    class Meta:
        verbose_name = 'Единица измерения'
        verbose_name_plural = 'Единицы измерения'
        ordering = ('title',)

    def __str__(self):
        return self.short_title


class Category(BaseModel, MPTTModel):
    title = models.CharField(verbose_name='Категория', max_length=255)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', db_index=True, on_delete=None)
    active = models.BooleanField(default=True, verbose_name="Вкл/Выкл")

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    class MPTTMeta:
        order_insertion_by = ['title']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('category', args=[self.id])

    def get_id(self):
        if self.parent:
            return self.parent.id
        return ''


class RozetkaCategory(BaseModel, MPTTModel):
    title = models.CharField(verbose_name='Категория розетка', max_length=255)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', db_index=True, on_delete=None)
    active = models.BooleanField(default=True, verbose_name="Вкл/Выкл")

    class Meta:
        verbose_name = "Категория розетка"
        verbose_name_plural = "Категории розетки"

    class MPTTMeta:
        order_insertion_by = ['title']

    def __str__(self):
        return "{}".format(self.title)

    def get_absolute_url(self):
        return reverse('category', args=[self.id])

    def get_id(self):
        if self.parent:
            return self.parent.id
        return ''


availability_prom_help_text = """
Наличие товара на складе
"+" — есть в наличии
"!" — гарантия наличия (для сертифицированных компаний)
"-" — нет в наличии
"&" — ожидается
"@" — услуга
цифра, например, "9" — кол-во дней на доставку, если товар под заказ
Важно! При пустом поле статус вашего товара станет «Нет в наличии».
"""

# availability_prom:
# НЕТ -
# Заканчивается +
# Львов (4 дня) +
# ЕСТЬ +


class Product(BaseModel):
    title = models.CharField(max_length=255, verbose_name="Заголовок")
    manufacturer = models.ForeignKey(Manufacturer, blank=True, null=True, on_delete=None, related_name="catalog_manufacturer")
    category = TreeForeignKey(Category, blank=True, null=True, verbose_name='Категория', on_delete=models.CASCADE)
    category_rozetka = TreeForeignKey(RozetkaCategory, blank=True, null=True, verbose_name='Категория розетка', on_delete=None)
    import_to_rozetka = models.BooleanField(verbose_name='На розетку', default=False)
    import_to_prom = models.BooleanField(verbose_name='На PROM', default=False)
    count_in_package = models.PositiveSmallIntegerField(verbose_name="Кол-во в упаковке", default=1)
    price = models.DecimalField(verbose_name="Цена", max_digits=8, decimal_places=2, blank=True, null=True)
    old_price_percent = models.DecimalField(
        verbose_name="Наценка в процентах для старай цены", max_digits=5, decimal_places=2, blank=True, null=True)
    discont = models.DecimalField(verbose_name='Скидка', decimal_places=2, max_digits=4, blank=True, null=True)
    stock_quantity = models.PositiveSmallIntegerField(default=100, verbose_name='Остаток')
    availability_prom = models.CharField(
        verbose_name='Наличие товара для прома', max_length=3,
        help_text=availability_prom_help_text,
        default='+', blank=True,
    )
    currency = models.ForeignKey(Currency, null=True, blank=True, default=None, on_delete=models.CASCADE)
    course = models.DecimalField(verbose_name='Курс', max_digits=12, decimal_places=5, blank=True, null=True, default=1)
    re_count = models.BooleanField(verbose_name="Пересчитывать в грн?", default=True)
    unit = models.ForeignKey(Unit, verbose_name='Единица измерения', blank=True, null=True, default=None, on_delete=models.CASCADE)
    step = models.DecimalField(verbose_name="Шаг", max_digits=8, decimal_places=3, default=1)
    text = RichTextUploadingField(verbose_name="Текст поста", blank=True, default="")
    image = models.ImageField(verbose_name="Изображение", blank=True, default='', upload_to=set_image_name)
    active = models.BooleanField(default=True, verbose_name="Вкл/Выкл")
    code = models.CharField(verbose_name="Артикул", max_length=20, default=set_code, unique=True, blank=True, null=True)

    vendor_id = models.CharField(blank=True, null=True, max_length=50)
    vendor_name = models.CharField(blank=True, null=True, max_length=200)

    author = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    is_checked = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
        ordering = ('-code',)
        permissions = (
            ('can_update_mizol', 'Может обновлять прайсы Мизол'),
            ('can_update_prom_parameters', 'Может обновлять параметры с прома'),
            ('Freelanser', 'freelanser'),
        )

    def __str__(self):
        return "{}".format(self.title)

    def save(self, *args, **kwargs):
        if not self.author:
            try:
                user = get_current_user()
                self.author = user
            except:
                self.user = None

        return super(Product, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('single-product', args=[str(self.id)])

    def import_for_admin(self):
        styles = "color: #fff; border-radius: 2px; padding: 3px 7px; min-width: 50px; display: block; text-align: center;"
        if self.import_to_rozetka:
            return mark_safe("<span style='background: green;{}'>Rozetka</span>".format(styles))
        elif self.import_to_prom:
            return mark_safe("<span style='background: linear-gradient(135deg,#4854a2,#772088);{}'>Prom</span>".format(styles))

    import_for_admin.short_description = 'Импорт'

    def get_currency_code(self):
        if self.currency:
            if self.re_count:
                return Currency.objects.get(code='UAH').code
            return self.currency.code
        return None
    get_currency_code.short_description = 'Валюта'

    def get_price(self):
        if not self.price:
            return None
        if self.discont:
            return self.price - (self.price * self.discont) / 100
        return self.price

    def get_price_UAH(self):
        price = self.get_price()
        if price:
            if self.re_count:
                return round(price * self.course * self.count_in_package, 3)
            else:
                return round(price * self.count_in_package, 3)
        return False
    get_price_UAH.short_description = 'Цена в валюте'

    def get_old_price(self):
        price_uah = self.get_price_UAH()
        old_price = (price_uah * self.old_price_percent) / 100 + price_uah
        return round(old_price, 2)

    def get_delivery_count(self):
        return self.delivery_set.count()

    def get_unit(self):
        if self.unit:
            return self.unit.short_title
        return 'шт.'

    def get_images_count(self):
        return Photo.objects.filter(product=self).count()

    get_images_count.short_description = 'Доп изобр.'

    def get_all_photo(self):
        images = list()
        other_photo = Photo.objects.filter(product=self)

        if self.image:
            images.append(self.image.url)

        for item in other_photo:
            images.append(item.image.url)

        return images

    def get_images(self):
        return Photo.objects.filter(product=self)


class Feature(BaseModel):
    product = models.ForeignKey(Product, verbose_name='Товар', default=None, on_delete=models.CASCADE)
    title = models.CharField(verbose_name="Характеристика", max_length=150)
    file = models.FileField(verbose_name='Файл', upload_to=set_file_name, default=None, blank=True, null=True)
    text = RichTextUploadingField(verbose_name="Текст поста", blank=True, default="")

    class Meta:
        verbose_name = "Характеристика"
        verbose_name_plural = "Характеристики"

    def __str__(self):
        return "{}".format(self.title)


class Delivery(BaseModel):
    product = models.ForeignKey(Product, verbose_name="Товар", on_delete=models.CASCADE)
    provider = models.ForeignKey(Provider, verbose_name="Поставщик", on_delete=models.CASCADE, blank=True, null=True)
    delivery = RichTextUploadingField(verbose_name="Доставка")
    delivery_my = RichTextUploadingField(verbose_name="Самовывоз")
    discount = RichTextUploadingField(verbose_name="Скидка")
    payment_cash = RichTextUploadingField(verbose_name="Оплата наличными")
    payment_card = RichTextUploadingField(verbose_name="Оплата картой")
    payment_bank = RichTextUploadingField(verbose_name="Оплата расчётный счёт")
    delivery_condition = RichTextUploadingField(verbose_name="Условие поставки", default=' ')
    return_product = RichTextUploadingField(verbose_name="Возврат", blank=True, null=True, default=None)

    class Meta:
        verbose_name = "Доп инфо"
        verbose_name_plural = "Доп инфо"

    def __str__(self):
        return "{} - {}".format(self.provider.title, self.product)


class Photo(BaseModel):
    product = models.ForeignKey(Product, verbose_name='Товар', on_delete=models.CASCADE)
    image = models.ImageField(verbose_name='Изображение', upload_to=set_image_name)
    weight = models.PositiveSmallIntegerField(verbose_name='Порядок', default=0)

    class Meta:
        verbose_name = "Изображение"
        verbose_name_plural = "Изображения"
        ordering = ['weight']

    def __str__(self):
        return "Image to product {}".format(self.product)

    def get_img_tag(self):
        return format_html("""<span style="
                                background-image: url('{}');
                                background-size: cover;
                                background-position: center;
                                width: 60px; height: 40px;
                                display: block;
                                position: relative;
                                "><span>""", self.image.url)

    get_img_tag.short_description = 'Preview'
    get_img_tag.allow_tags = True


class Parameter(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    parameter = models.CharField(max_length=200)
    value = models.CharField(max_length=500)
    is_dop_param_for_rozetka = models.BooleanField(default=False, verbose_name='Доп. параметр для розетки')

    def __str__(self):
        return self.parameter
