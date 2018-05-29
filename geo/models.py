from django.db import models
from django_ppf.basemodel import BaseModel
from django.utils.translation import ugettext as _
from django.utils.crypto import get_random_string
from mptt.models import MPTTModel, TreeForeignKey
from django.shortcuts import reverse
from catalog.models import Product
from ckeditor_uploader.fields import RichTextUploadingField
from sorl.thumbnail import ImageField


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
    title_many = models.CharField(max_length=200, verbose_name=_('Title many'), blank=True, null=True)
    title_eng = models.CharField(max_length=200, verbose_name=_('Title eng'), blank=True, null=True)
    code = models.CharField(max_length=15, blank=True, null=True, default=None, unique=True)
    image = ImageField(verbose_name=_('Image'), upload_to=set_region_image_name, blank=True, null=True)
    meta_description = models.CharField(max_length=200, verbose_name=_('META Description'), blank=True, null=True)
    meta_keywords = models.CharField(max_length=200, verbose_name=_('META Keywords'), blank=True, null=True)
    description = RichTextUploadingField(verbose_name=_('Description'), blank=True, null=True)
    is_auxpage = models.BooleanField(default=False)

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
        children = (i.id for i in self.get_descendants(include_self=True))
        return ObjectPPF.objects.filter(region__id__in=children).count()


class ObjectPPF(BaseModel):
    region = models.ForeignKey(Region, verbose_name=_('Region'), on_delete=models.CASCADE)
    title = models.CharField(max_length=250, verbose_name=_('Title'))
    text = RichTextUploadingField(verbose_name=_('Text'), blank=True, null=True)
    meta_description = models.CharField(max_length=200, verbose_name=_('META Description'), blank=True, null=True)
    meta_keywords = models.CharField(max_length=200, verbose_name=_('META Keywords'), blank=True, null=True)
    products = models.ManyToManyField(Product, verbose_name=_('Products'))
    favorite = models.BooleanField(verbose_name=_('Favorite objects'), default=False)

    class Meta:
        verbose_name = _('Object')
        verbose_name_plural = _('Objects')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('geo-object', args=[str(self.id)])

    def get_main_or_first_image(self):
        try:
            return self.objectimage_set.get(is_main=True).image
        except ObjectImage.DoesNotExist:
            return self.objectimage_set.first().image


class ObjectImage(BaseModel):
    object_ppf = models.ForeignKey(ObjectPPF, verbose_name=_('Object'), on_delete=models.CASCADE)
    title = models.CharField(max_length=250, verbose_name=_('Title'))
    image = ImageField(verbose_name=_('Image'), upload_to=set_object_image_name, blank=True, null=True)
    weight = models.PositiveSmallIntegerField(verbose_name=_('Weight'), default=0)
    is_main = models.BooleanField(default=False)

    class Meta:
        verbose_name = _('Image')
        verbose_name_plural = _('Images')

    def __str__(self):
        return self.title
