from django.contrib.sitemaps import Sitemap
from .models import SolProduct


class SolProductSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.5

    def items(self):
        return SolProduct.objects.filter(is_active=True)

    def lastmod(self, obj):
        return obj.created
