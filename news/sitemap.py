from django.contrib.sitemaps import Sitemap
from .models import News, Promo


class NewsSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.5

    def items(self):
        return News.objects.all()

    def lastmod(self, obj):
        return obj.created


class PromoSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.5

    def items(self):
        return Promo.objects.all()

    def lastmod(self, obj):
        return obj.created
