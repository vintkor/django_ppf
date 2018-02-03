from django.db import models
from django_ppf.basemodel import BaseModel
from django.utils.translation import ugettext as _
from django.utils.crypto import get_random_string
from mptt.models import MPTTModel, TreeForeignKey
from django.shortcuts import reverse
from ckeditor_uploader.fields import RichTextUploadingField
from sorl.thumbnail import ImageField


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


class Category(BaseModel, MPTTModel):
    parent = TreeForeignKey(
        'self', verbose_name=_('Parent category'), null=True, blank=True,
        related_name='children', db_index=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, verbose_name=_('Title'))
    image = ImageField(verbose_name=_('Image'), upload_to=set_image_name, blank=True, null=True)
    meta_description = models.CharField(max_length=200, verbose_name=_('META Description'), blank=True, null=True)
    meta_keywords = models.CharField(max_length=200, verbose_name=_('META Keywords'), blank=True, null=True)
    description = RichTextUploadingField(verbose_name=_('Description'), blank=True, null=True)

    class MPTTMeta:
        order_insertion_by = ['title']

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')

    def __str__(self):
        categories = ' > '.join([i.title for i in self.get_ancestors(include_self=True)])
        return categories

    def get_absolute_url(self):
        return reverse('catalog-category', args=[str(self.id)])

    def get_count_products(self):
        categories = self.get_descendants(include_self=True)
        return Product.objects.select_related('category').filter(category__in=categories).count()


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
    category = models.ForeignKey(Category, verbose_name=_('Category'), on_delete=models.CASCADE)
    manufacturer = models.ForeignKey(Manufacturer, verbose_name=_('Manufacturer'), on_delete=None, blank=True, null=True, default=None)
    title = models.CharField(max_length=250, verbose_name=_('Title'))
    image = ImageField(verbose_name=_('Image'), upload_to=set_product_image_name, blank=True, null=True)
    text = models.TextField(verbose_name=_('Text'), blank=True, null=True)
    meta_description = models.CharField(max_length=200, verbose_name=_('META Description'), blank=True, null=True)
    meta_keywords = models.CharField(max_length=200, verbose_name=_('META Keywords'), blank=True, null=True)
    description = models.TextField(verbose_name=_('Description'), blank=True, null=True)

    class Meta:
        verbose_name = _('Product')
        verbose_name_plural = _('Products')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('catalog-product', args=[str(self.id)])
