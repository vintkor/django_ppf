from django.conf.urls import url
from .views import (
    SolProductDetailView,
    SolProductListView,
)
from django.urls import path, include


app_name = 'solutions'
urlpatterns = [
    path('', SolProductListView.as_view(), name='list'),
    path('<slug:slug>/', SolProductDetailView.as_view(), name='detail'),
]
