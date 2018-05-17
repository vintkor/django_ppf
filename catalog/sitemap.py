import datetime
from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from geo.models import Region
from .models import Product, Category


class ProductSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.5

    def items(self):
        return Product.objects.filter(active=True)

    def lastmod(self, obj):
        return obj.created


class CategorySitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.5

    def items(self):
        return Category.objects.all()

    def lastmod(self, obj):
        return obj.created


class AuxPageSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.5

    def items(self):
        regions = Region.objects.filter(is_auxpage=True)
        categories = Category.objects.filter(is_auxpage=True)
        list_objects = []
        for reg in regions:
            for cat in categories:
                list_objects.append(
                    '{}___{}___{}'.format(cat.slug, reg.title_eng, str(cat.updated.date()))
                )
        return list_objects

    def location(self, obj):
        item = obj.split('___')
        return reverse('catalog-category-aux', kwargs={'slug': item[0], 'region': item[1].lower()})

    def lastmod(self, obj):
        item = obj.split('___')[2].split('-')
        return datetime.date(int(item[0]), int(item[1]), int(item[2]))
