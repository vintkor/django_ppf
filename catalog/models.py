from django.db import models
from django_ppf.basemodel import BaseModel
from django.utils.translation import ugettext as _
from django.utils.crypto import get_random_string
from mptt.models import MPTTModel, TreeForeignKey
from django.shortcuts import reverse

def set_image_name(instanse, filename):
    name = get_random_string(40)
    ext = filename.split('.')[-1]
    path = 'images/catalog/category/{}.{}'.format(name, ext)
    return path


class Category(BaseModel, MPTTModel):
    parent = TreeForeignKey('self', verbose_name=_('Parent category'), null=True, blank=True, related_name='children', db_index=True)
    title = models.CharField(max_length=200, verbose_name=_('Category'))
    image = models.ImageField(verbose_name=_('Image'), upload_to=set_image_name, blank=True, null=True)
    meta_description = models.CharField(max_length=200, verbose_name=_('META Description'), blank=True, null=True)
    meta_keywords = models.CharField(max_length=200, verbose_name=_('META Keywords'), blank=True, null=True)
    description = models.TextField(verbose_name=_('Description'), blank=True, null=True)

    class MPTTMeta:
        order_insertion_by = ['title']

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('catalog-category', args=[str(self.id)])
