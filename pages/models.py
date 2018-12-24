from django.db import models
from django_ppf.basemodel import BaseModel
from django.utils.translation import ugettext as _
from ckeditor_uploader.fields import RichTextUploadingField
from django.shortcuts import reverse


class Page(BaseModel):
    title = models.CharField(max_length=200, verbose_name=_('Title'))
    slug = models.SlugField(null=True, max_length=170, unique=True)
    text = RichTextUploadingField(verbose_name=_('Text'))
    meta_description = models.CharField(max_length=200, verbose_name=_('META Description'), blank=True, null=True)
    meta_keywords = models.CharField(max_length=200, verbose_name=_('META Keywords'), blank=True, null=True)
    description = models.TextField(verbose_name=_('Description'), blank=True, null=True)

    class Meta:
        verbose_name = _('Page')
        verbose_name_plural = _('Pages')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('pages:page', args=[str(self.slug)])
