from django.contrib.sitemaps import Sitemap
from .models import Product, Category


class ProductSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.5

    def items(self):
        return Product.objects.all()

    def lastmod(self, obj):
        return obj.created


class CategorySitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.5

    def items(self):
        return Category.objects.all()

    def lastmod(self, obj):
        return obj.created