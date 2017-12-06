from django.conf.urls import url
from .views import NewsListView, NewsDetailView

urlpatterns = [
    url(r'^$', NewsListView.as_view(), name='news-list'),
    url(r'^(?P<pk>\d+)/$', NewsDetailView.as_view(), name='news-detail'),
]
