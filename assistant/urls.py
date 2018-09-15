from django.conf.urls import url
from assistant.views import (
    CatalogList,
    CatalogDetail,
    CatalogSearch,
    CatalogForPromXLSX,
    CatalogCategoryList,
    CatalogForRozetkaXML,
    UpdateMizolPriceView,
    ImportParametersFormPromView,
)


urlpatterns = [
    url(r'^$', CatalogList.as_view(), name='all-catalog'),
    url(r'^search/$', CatalogSearch.as_view(), name='search-catalog'),
    url(r'^update-mizol-prices/$', UpdateMizolPriceView.as_view(), name='update-mizol-prices'),
    url(r'^import-parameters-from-prom/$', ImportParametersFormPromView.as_view(), name='import-parameters-from-prom'),
    url(r'^(?P<pk>\d+)$', CatalogDetail.as_view(), name='single-product'),
    url(r'^category/(?P<pk>\d+)$', CatalogCategoryList.as_view(), name='category'),
    url(r'^prom-xlsx/$', CatalogForPromXLSX.as_view(), name='catalog-prom'),
    url(r'^rozetka-xml/$', CatalogForRozetkaXML.as_view(), name='catalog-rozetka'),
]
