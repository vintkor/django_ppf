from django.conf.urls import url
from .views import (
    NewsListView,
    NewsDetailView,
    PromoListView,
    PromoDetailView,
)
from django.urls import path, include

urlpatterns = [
    path('', NewsListView.as_view(), name='news-list'),
    path('<int:pk>/', NewsDetailView.as_view(), name='news-detail'),
    path('promo/', include([
        path('', PromoListView.as_view(), name='promo-list'),
        path('<slug:slug>/', PromoDetailView.as_view(), name='promo-detail'),
    ])),
]

