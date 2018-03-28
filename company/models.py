from django.db import models
from django_ppf.basemodel import BaseModel
from django.utils.translation import ugettext as _
from sorl.thumbnail import ImageField
from ckeditor_uploader.fields import RichTextUploadingField
from geo.models import Region


class Company(BaseModel):
    name = models.CharField(max_length=250, verbose_name=_('Company name'))
    description = RichTextUploadingField(verbose_name=_('Description'), blank=True, null=True)

    class Meta:
        verbose_name = _('Company')
        verbose_name_plural = _('Companies')

    def __str__(self):
        return self.name

    def get_office_count(self):
        return self.office_set.count()
    get_office_count.short_description = 'Кол-во филлиалов'


class Office(BaseModel):
    company = models.ForeignKey(Company, verbose_name=_('Company'), on_delete=models.CASCADE)
    region = models.ForeignKey(Region, on_delete=None, verbose_name=_('Country'))
    address = models.CharField(max_length=255, verbose_name=_('Address'))
    coordinates = models.CharField(max_length=50, verbose_name=_('Coordinates'))

    class Meta:
        verbose_name = _('Office')
        verbose_name_plural = _('Offices')

    def __str__(self):
        return '{} {}'.format(self.region.title, self.address)

    def get_images_count(self):
        return self.gallery_set.count()

    get_images_count.short_description = 'Кол-во изображений'


class Gallery(BaseModel):
    office = models.ForeignKey(Office, verbose_name=_('Office'), on_delete=models.CASCADE)
    image = ImageField(verbose_name=_('Image'), upload_to='images')
    alt = models.CharField(max_length=255, verbose_name=_('SEO Alt'), blank=True, null=True)

    class Meta:
        verbose_name = _('Office gallery')
        verbose_name_plural = _('Office galleries')

    def __str__(self):
        return str(self.office)


class Info(BaseModel):
    office = models.ForeignKey(Office, on_delete=models.CASCADE)
    label = models.CharField(max_length=100)
    field = models.CharField(max_length=100)
    fa_icon_class = models.CharField(max_length=60)

    class Meta:
        verbose_name = _('Office contact info')
        verbose_name_plural = _('Offices contact info')

    def __str__(self):
        return self.field
