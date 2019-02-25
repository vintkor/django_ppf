from django.db import models
from django_ppf.basemodel import BaseModel
from django.utils.translation import ugettext as _
from django.utils.crypto import get_random_string
from django.shortcuts import reverse
from ckeditor_uploader.fields import RichTextUploadingField
from django_ppf.settings import SITE_URL

from telegram_bot.models import TelegramBot, TelegramUser
from telegram_bot.utils import Telegram


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

    def save(self, *args, **kwargs):
        new_news = False
        if not self.pk:
            new_news = True

        super(News, self).save(args, kwargs)

        if new_news:
            bot = TelegramBot.objects.first()
            users = TelegramUser.objects.all()

            text = '📢 {} \n\n 🔗 Читать новость {}{}'.format(
                self.title,
                SITE_URL,
                self.get_absolute_url(),
            )

            telegram = Telegram(bot.token)
            for user in users:
                telegram.send_message(user.user_id, text)


class Promo(BaseModel):
    title = models.CharField(max_length=255, verbose_name=_('Title'))
    slug = models.SlugField(null=True, max_length=170, unique=True)
    image = models.ImageField(verbose_name=_('Image'), upload_to=set_news_image_name, blank=True, null=True)
    small_image = models.ImageField(verbose_name=_('Small image'), upload_to=set_news_image_name, blank=True, null=True)
    text = RichTextUploadingField(verbose_name=_('Text'))
    meta_description = models.CharField(max_length=200, verbose_name=_('META Description'), blank=True, null=True)
    meta_keywords = models.CharField(max_length=200, verbose_name=_('META Keywords'), blank=True, null=True)
    description = models.TextField(verbose_name=_('Description'), blank=True, null=True)

    class Meta:
        verbose_name = _('Promo')
        verbose_name_plural = _('Promo')
        ordering = ('-created',)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        new_promo = False
        if not self.pk:
            new_promo = True

        super(Promo, self).save(args, kwargs)

        if new_promo:
            bot = TelegramBot.objects.first()
            users = TelegramUser.objects.all()

            text = '📢 {} \n\n 🔗 Читать о новой акции {}{}'.format(
                self.title,
                SITE_URL,
                self.get_absolute_url(),
            )

            telegram = Telegram(bot.token)
            for user in users:
                telegram.send_message(user.user_id, text)

    def get_absolute_url(self):
        return reverse('promo-detail', args=[str(self.slug)])
