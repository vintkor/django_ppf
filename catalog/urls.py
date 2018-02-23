# from django.conf.urls import url
from django.urls import path, re_path
from .views import (
    ProductDetailView,
    CatalogRootView,
    ManufacturerDetailView,
    ManufacturerListView,
    ProductListView,
)


urlpatterns = [
    path('', CatalogRootView.as_view(), name='catalog'),
    path('category/<slug:slug>/', ProductListView.as_view(), name='catalog-category'),
    re_path(r'^manufacturer/(?P<pk>\d+)/$', ManufacturerDetailView.as_view(), name='catalog-manufacturer'),
    path('product/<slug:slug>/', ProductDetailView.as_view(), name='catalog-product'),
]
