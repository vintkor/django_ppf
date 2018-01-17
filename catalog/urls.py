from django.conf.urls import url
from .views import CategoryListView, ProductDetailView, CatalogRootView, ProductEditView

urlpatterns = [
    url(r'^$', CatalogRootView.as_view(), name='catalog'),
    url(r'^category/(?P<pk>\d+)/$', CategoryListView.as_view(), name='catalog-category'),
    url(r'^product/(?P<pk>\d+)/$', ProductDetailView.as_view(), name='catalog-product'),
    url(r'^product/(?P<pk>\d+)/edit/$', ProductEditView.as_view(), name='catalog-product-edit'),
]
