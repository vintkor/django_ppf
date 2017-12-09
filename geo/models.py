from django.db import models
from django_ppf.basemodel import BaseModel
from django.utils.translation import ugettext as _
from django.utils.crypto import get_random_string
from mptt.models import MPTTModel, TreeForeignKey
from django.shortcuts import reverse
from catalog.models import Product


def set_region_image_name(instanse, filename):
    name = get_random_string(40)
    ext = filename.split('.')[-1]
    path = 'images/catalog/region/{}.{}'.format(name, ext)
    return path


def set_object_image_name(instanse, filename):
    name = get_random_string(40)
    ext = filename.split('.')[-1]
    path = 'images/catalog/object/{}.{}'.format(name, ext)
    return path


class Region(BaseModel, MPTTModel):
    parent = TreeForeignKey(
        'self', verbose_name=_('Parent region'), null=True, blank=True,
        related_name='children', db_index=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, verbose_name=_('Title'))
    code = models.CharField(max_length=15, blank=True, null=True, default=None, unique=True)
    image = models.ImageField(verbose_name=_('Image'), upload_to=set_region_image_name, blank=True, null=True)
    meta_description = models.CharField(max_length=200, verbose_name=_('META Description'), blank=True, null=True)
    meta_keywords = models.CharField(max_length=200, verbose_name=_('META Keywords'), blank=True, null=True)
    description = models.TextField(verbose_name=_('Description'), blank=True, null=True)

    class MPTTMeta:
        order_insertion_by = ['title']

    class Meta:
        verbose_name = _('Region')
        verbose_name_plural = _('Regions')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('geo-region', args=[str(self.id)])

    def count_objects(self):
        objects = ObjectPPF.objects.all()
        return len([obj for obj in objects if obj.region.get_ancestors(ascending=False).first() == self])


class ObjectPPF(BaseModel):
    region = models.ForeignKey(Region, verbose_name=_('Region'), on_delete=models.CASCADE)
    title = models.CharField(max_length=250, verbose_name=_('Title'))
    text = models.TextField(verbose_name=_('Text'), blank=True, null=True)
    meta_description = models.CharField(max_length=200, verbose_name=_('META Description'), blank=True, null=True)
    meta_keywords = models.CharField(max_length=200, verbose_name=_('META Keywords'), blank=True, null=True)
    description = models.TextField(verbose_name=_('Description'), blank=True, null=True)
    products = models.ManyToManyField(Product, verbose_name=_('Products'))
    favorite = models.BooleanField(verbose_name=_('Favorite objects'), default=False)

    class Meta:
        verbose_name = _('Object')
        verbose_name_plural = _('Objects')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('geo-object', args=[str(self.id)])


class ObjectImage(BaseModel):
    object_ppf = models.ForeignKey(ObjectPPF, verbose_name=_('Object'), on_delete=models.CASCADE)
    title = models.CharField(max_length=250, verbose_name=_('Title'))
    image = models.ImageField(verbose_name=_('Image'), upload_to=set_object_image_name, blank=True, null=True)
    weight = models.PositiveSmallIntegerField(verbose_name=_('Weight'), default=0)

    class Meta:
        verbose_name = _('Image')
        verbose_name_plural = _('Images')

    def __str__(self):
        return self.title
