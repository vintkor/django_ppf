from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class GeoConfig(AppConfig):
    name = 'geo'
    verbose_name = _('Geo')
