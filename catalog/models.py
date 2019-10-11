from django.db import models
from assistant.middleware import get_current_user
from django_ppf.basemodel import BaseModel
from django.utils.translation import ugettext as _
from django.utils.crypto import get_random_string
from mptt.models import MPTTModel, TreeForeignKey
from django.shortcuts import reverse
from ckeditor_uploader.fields import RichTextUploadingField
from sorl.thumbnail import ImageField
from phonenumber_field.modelfields import PhoneNumberField
from .utils import FileUtil
from django.contrib.auth.models import User


def set_image_name(instanse, filename):
    name = get_random_string(40)
    ext = filename.split('.')[-1]
    path = 'images/catalog/category/{}.{}'.format(name, ext)
    return path


def set_image_logo_name(instanse, filename):
    name = get_random_string(40)
    ext = filename.split('.')[-1]
    path = 'images/catalog/manufacturer/{}.{}'.format(name, ext)
    return path


def set_product_image_name(instanse, filename):
    name = get_random_string(40)
    ext = filename.split('.')[-1]
    path = 'images/catalog/product/{}.{}'.format(name, ext)
    return path


def set_icons_name(instanse, filename):
    name = get_random_string(40)
    ext = filename.split('.')[-1]
    path = 'images/catalog/icons/{}.{}'.format(name, ext)
    return path


def set_file_name(instanse, filename):
    name = get_random_string(40)
    ext = filename.split('.')[-1]
    path = 'files/catalog/{}.{}'.format(name, ext)
    return path


class Category(BaseModel, MPTTModel):
    parent = TreeForeignKey(
        'self', verbose_name=_('Parent category'), null=True, blank=True,
        related_name='children', db_index=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, verbose_name=_('Title'))
    slug = models.SlugField(null=True, max_length=170, unique=True)
    image = ImageField(verbose_name=_('Image'), upload_to=set_image_name, blank=True, null=True)
    meta_description = models.CharField(max_length=200, verbose_name=_('META Description'), blank=True, null=True)
    meta_keywords = models.CharField(max_length=200, verbose_name=_('META Keywords'), blank=True, null=True)
    description = RichTextUploadingField(verbose_name=_('Description'), blank=True, null=True)
    sort = models.PositiveSmallIntegerField(verbose_name='Сортировка', default=10)
    is_auxpage = models.BooleanField(default=False)
    description_aux = RichTextUploadingField(verbose_name=_('Description aux'), blank=True, null=True)

    class MPTTMeta:
        order_insertion_by = ['title']

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')
        ordering = ('sort',)

    def __str__(self):
        categories = ' > '.join([i.title for i in self.get_ancestors(include_self=True)])
        return categories

    def get_absolute_url(self):
        return reverse('catalog-category', args=[str(self.slug)])

    def get_count_products(self):
        categories = self.get_descendants(include_self=True)
        return Product.objects.select_related('category').filter(
            category__in=categories,
            active=True,
        ).count()

    def get_children_with_products(self):
        return (i for i in self.get_children() if i.get_count_products() > 0)


class Manufacturer(BaseModel):
    title = models.CharField(max_length=250, verbose_name=_('Title'))
    logo = ImageField(verbose_name=_('Logo'), upload_to=set_image_logo_name, blank=True, null=True)
    meta_description = models.CharField(max_length=200, verbose_name=_('META Description'), blank=True, null=True)
    meta_keywords = models.CharField(max_length=200, verbose_name=_('META Keywords'), blank=True, null=True)
    description = RichTextUploadingField(verbose_name=_('Description'), blank=True, null=True)

    class Meta:
        verbose_name = _('Manufacturer')
        verbose_name_plural = _('Manufacturers')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('catalog-manufacturer', args=[str(self.id)])

    def get_count_product(self):
        return Product.objects.select_related('manufacturer').filter(manufacturer=self).count()


class Product(BaseModel):
    category = models.ManyToManyField(Category, verbose_name=_('Category'))
    manufacturer = models.ForeignKey(Manufacturer, verbose_name=_('Manufacturer'), on_delete=None, blank=True, null=True, default=None)
    title = models.CharField(max_length=250, verbose_name=_('Title'))
    slug = models.SlugField(null=True, max_length=170, unique=True)
    image = ImageField(verbose_name=_('Image'), upload_to=set_product_image_name, blank=True, null=True)
    meta_description = models.CharField(max_length=200, verbose_name=_('META Description'), blank=True, null=True)
    meta_keywords = models.CharField(max_length=200, verbose_name=_('META Keywords'), blank=True, null=True)
    description = RichTextUploadingField(verbose_name=_('Description'), blank=True, null=True)
    use = RichTextUploadingField(verbose_name=_('Use'), blank=True, null=True)
    countries = models.ManyToManyField('geo.Region', blank=True)

    title_color = models.CharField(max_length=250, verbose_name=_('Color block title'), blank=True, null=True)
    title_use = models.CharField(max_length=250, verbose_name=_('Use block title'), blank=True, null=True)
    title_features = models.CharField(max_length=250, verbose_name=_('Feature block title'), blank=True, null=True)
    title_benefit = models.CharField(max_length=250, verbose_name=_('Benefit block title'), blank=True, null=True)
    title_gallery = models.CharField(max_length=250, verbose_name=_('Gallery block title'), blank=True, null=True)
    title_documents = models.CharField(max_length=250, verbose_name=_('Documents block title'), blank=True, null=True)
    title_digits = models.CharField(max_length=250, verbose_name=_('Digits block title'), blank=True, null=True)
    title_video = models.CharField(max_length=250, verbose_name=_('Video block title'), blank=True, null=True)
    title_country = models.CharField(max_length=250, verbose_name=_('Map block title'), blank=True, null=True)

    active = models.BooleanField(default=False)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name='author')
    is_checked = models.BooleanField(default=False)

    class Meta:
        verbose_name = _('Product')
        verbose_name_plural = _('Products')
        permissions = (
            ('Freelanser', 'freelanser'),
        )

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.author:
            try:
                self.author = get_current_user()
            except:
                self.user = None
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('catalog-product', args=[str(self.slug)])

    def is_documents(self):
        return Document.objects.filter(product=self).exists()

    def is_features(self):
        return Feature.objects.filter(product=self).exists()

    def is_benefits(self):
        return Benefit.objects.filter(product=self).exists()

    def is_galleries(self):
        return Gallery.objects.filter(product=self).exists()

    def is_videos(self):
        return Video.objects.filter(product=self).exists()

    def is_digits(self):
        return Digits.objects.filter(product=self).exists()

    def is_colors(self):
        return Color.objects.filter(product=self).exists()


class Order(BaseModel):
    product = models.ForeignKey(Product, on_delete=None, verbose_name=_('Product'))
    phone = PhoneNumberField(verbose_name=_('Phone number'))

    class Meta:
        verbose_name = _('Order')
        verbose_name_plural = _('Orders')

    def __str__(self):
        return str(self.phone)


class Feature(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name=_('Product'))
    title = models.CharField(max_length=150, verbose_name=_('Title'))
    value = models.CharField(max_length=150, verbose_name=_('Value'))

    class Meta:
        verbose_name = _('Feature')
        verbose_name_plural = _('Features')

    def __str__(self):
        return '{} - {}'.format(self.product, self.title)


class Benefit(BaseModel):
    product = models.ForeignKey(Product, on_delete=None, verbose_name=_('Product'))
    image = ImageField(verbose_name=_('Image'), upload_to=set_icons_name, blank=True, null=True)
    title = models.CharField(max_length=150, verbose_name=_('Title'))
    subtitle = models.CharField(max_length=150, verbose_name=_('Subtitle'), blank=True, null=True)
    text = models.TextField(verbose_name=_('Text'), blank=True, null=True)

    class Meta:
        verbose_name = _('Benefit')
        verbose_name_plural = _('Benefits')

    def __str__(self):
        return '{} - {}'.format(self.product, self.title)


class Gallery(BaseModel):
    product = models.ForeignKey(Product, on_delete=None, verbose_name=_('Product'))
    image = ImageField(verbose_name=_('Image'), upload_to=set_product_image_name)
    alt = models.CharField(max_length=150, verbose_name=_('SEO alt'), blank=True, null=True)

    class Meta:
        verbose_name = _('Gallery')
        verbose_name_plural = _('Galleries')

    def __str__(self):
        return '{} - {}'.format(self.product, self.alt)


class Document(BaseModel):
    product = models.ForeignKey(Product, on_delete=None, verbose_name=_('Product'))
    title = models.CharField(max_length=150, verbose_name=_('Title'))
    file = models.FileField(verbose_name=_('File'), upload_to=set_file_name)

    class Meta:
        verbose_name = _('Document')
        verbose_name_plural = _('Documents')

    def __str__(self):
        return '{} - {}'.format(self.product, self.title)

    def get_file_type(self):
        return FileUtil(self).get_file_type()


class Video(BaseModel):
    product = models.ForeignKey(Product, on_delete=None, verbose_name=_('Product'))
    title = models.CharField(max_length=250, verbose_name=_('Title'))
    link = models.URLField(verbose_name=_('Link to youtube video'))

    class Meta:
        verbose_name = _('Video')
        verbose_name_plural = _('Videos')

    def __str__(self):
        return '{} - {}'.format(self.product, self.title)

    def get_video_id(self):
        return self.link.split('=')[1]


class Digits(BaseModel):
    product = models.ForeignKey(Product, on_delete=None, verbose_name=_('Product'))
    digit = models.CharField(max_length=150, verbose_name=_('Digit'))
    title = models.CharField(max_length=150, verbose_name=_('Title'))
    subtitle = models.CharField(max_length=150, verbose_name=_('Subtitle'), blank=True, null=True)
    text = models.TextField(verbose_name=_('Text'), blank=True, null=True)

    class Meta:
        verbose_name = _('Digit')
        verbose_name_plural = _('Digits')

    def __str__(self):
        return '{} - {} - {}'.format(self.product, self.digit, self.title)


class Color(BaseModel):
    product = models.ForeignKey(Product, on_delete=None, verbose_name=_('Product'))
    image = ImageField(verbose_name=_('Image'), upload_to=set_product_image_name)
    alt = models.CharField(max_length=150, verbose_name=_('SEO alt'), blank=True, null=True)

    class Meta:
        verbose_name = _('Color')
        verbose_name_plural = _('Colors')

    def __str__(self):
        return '{} - {}'.format(self.product, self.alt)
