from django.db import models
from django_ppf.basemodel import BaseModel
from django.utils.translation import ugettext as _


class Currency(BaseModel):
    title = models.CharField(max_length=100, verbose_name=_('Title'))
    code = models.CharField(max_length=3, verbose_name=_('Code'))
    active = models.BooleanField(default=True, verbose_name=_('Active'))

    class Meta:
        verbose_name = _('Currency')
        verbose_name_plural = _('Currencies')

    def __str__(self):
        return self.title
