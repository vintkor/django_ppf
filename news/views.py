from django.views.generic import ListView, DetailView
from .models import News


class NewsListView(ListView):
    template_name = 'news/news-list.html'
    context_object_name = 'news_list'
    model = News


class NewsDetailView(DetailView):
    template_name = 'news/news-detail.html'
    context_object_name = 'news'
    model = News
