from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from django.utils.translation import ugettext as _
from django_ppf.basemodel import BaseModel


class Category(BaseModel, MPTTModel):
    parent = TreeForeignKey(
        'self', verbose_name=_('Parent category'), null=True, blank=True,
        related_name='children', db_index=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, verbose_name=_('Title'))
    slug = models.SlugField(null=True, max_length=170, unique=True)

    class MPTTMeta:
        order_insertion_by = ['title']

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')

    def __str__(self):
        categories = ' > '.join([i.title for i in self.get_ancestors(include_self=True)])
        return categories


class Document(BaseModel):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name=_('Category'))
    title = models.CharField(max_length=250, verbose_name=_('Title'))
    slug = models.SlugField(null=True, max_length=170, unique=True)
    file = models.FileField(upload_to='media/library/', verbose_name=_('File'))

    class Meta:
        verbose_name = _('Product')
        verbose_name_plural = _('Products')
        unique_together = ('id', 'slug')

    def __str__(self):
        return self.title
