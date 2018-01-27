from django.contrib.sitemaps import Sitemap
from .models import Region, ObjectPPF


class RegionSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.5

    def items(self):
        return Region.objects.all()

    def lastmod(self, obj):
        return obj.created


class ObjectPPFSitemap(Sitemap):
    changefreq = "never"
    priority = 0.5

    def items(self):
        return ObjectPPF.objects.all()

    def lastmod(self, obj):
        return obj.created