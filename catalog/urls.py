# from django.conf.urls import url
from django.urls import path, re_path
from .views import (
    CategoryListView,
    ProductDetailView,
    CatalogRootView,
    ManufacturerDetailView,
    ManufacturerListView,
)


urlpatterns = [
    path('', CatalogRootView.as_view(), name='catalog'),
    re_path(r'^category/(?P<pk>\d+)/$', CategoryListView.as_view(), name='catalog-category'),
    re_path(r'^manufacturer/(?P<pk>\d+)/$', ManufacturerDetailView.as_view(), name='catalog-manufacturer'),
    path('product/<slug:slug>/', ProductDetailView.as_view(), name='catalog-product'),
]
