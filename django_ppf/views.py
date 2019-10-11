from django.views.generic import View
from catalog.models import Category
from django.shortcuts import render
from django.urls import reverse
from company.models import Company
from django.contrib import sitemaps


class HomeView(View):

    def get(self, request):
        categories = Category.objects.filter(level=0)
        company = Company.objects.first()
        context = {
            'categories': categories,
            'company': company,
        }
        return render(request, 'django_ppf/home.html', context)


class ContactsView(View):

    def get(self, request):
        categories = Category.objects.filter(level=0)
        company = Company.objects.prefetch_related(
            'office_set',
            'office_set__gallery_set',
            'office_set__info_set',
        ).first()
        context = {
            'categories': categories,
            'company': company,
        }
        return render(request, 'django_ppf/contacts.html', context)


class StaticViewSitemap(sitemaps.Sitemap):
    priority = 0.5
    changefreq = 'daily'

    def items(self):
        return (
            'home', 'contacts', 'news-list', 'geo-root', 'catalog',
        )

    def location(self, item):
        return reverse(item)
