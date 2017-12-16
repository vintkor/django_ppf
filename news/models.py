from django.db import models
from django_ppf.basemodel import BaseModel
from django.utils.translation import ugettext as _
from django.utils.crypto import get_random_string
from django.shortcuts import reverse
from ckeditor_uploader.fields import RichTextUploadingField


def set_news_image_name(instanse, filename):
    name = get_random_string(40)
    ext = filename.split('.')[-1]
    path = 'images/catalog/news/{}.{}'.format(name, ext)
    return path


class News(BaseModel):
    title = models.CharField(max_length=200, verbose_name=_('Title'))
    image = models.ImageField(verbose_name=_('Image'), upload_to=set_news_image_name, blank=True, null=True)
    text = RichTextUploadingField(verbose_name=_('Text'))
    meta_description = models.CharField(max_length=200, verbose_name=_('META Description'), blank=True, null=True)
    meta_keywords = models.CharField(max_length=200, verbose_name=_('META Keywords'), blank=True, null=True)
    description = models.TextField(verbose_name=_('Description'), blank=True, null=True)

    class Meta:
        verbose_name = _('News')
        verbose_name_plural = _('News')
        ordering = ('-created',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('news-detail', args=[str(self.id)])
