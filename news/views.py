from django.views.generic import ListView, DetailView
from .models import News, Promo
from catalog.models import Category


class NewsListView(ListView):
    template_name = 'news/news-list.html'
    context_object_name = 'news_list'
    model = News

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['categories'] = Category.objects.filter(level=0)
        return context


class NewsDetailView(DetailView):
    template_name = 'news/news-detail.html'
    context_object_name = 'news'
    model = News

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['categories'] = Category.objects.filter(level=0)
        return context


class PromoListView(ListView):
    template_name = 'news/promo-list.html'
    context_object_name = 'promos'
    model = Promo


class PromoDetailView(DetailView):
    template_name = 'news/promo-detail.html'
    context_object_name = 'promo'
    model = Promo
