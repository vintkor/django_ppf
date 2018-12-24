from django.conf.urls import url, include
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django_ppf.settings import MEDIA_URL, MEDIA_ROOT
from django.conf.urls.static import static
from .views import HomeView, ContactsView
from django.conf import settings
from django.contrib import sitemaps
from catalog.sitemap import ProductSitemap, CategorySitemap, AuxPageSitemap
from geo.sitemap import RegionSitemap, ObjectPPFSitemap
from news.sitemap import NewsSitemap, PromoSitemap
from django.contrib.sitemaps.views import sitemap
from django.urls import path, reverse
import sys


class StaticViewSitemap(sitemaps.Sitemap):
    priority = 0.5
    changefreq = 'daily'

    def items(self):
        return (
            'home', 'contacts', 'news-list', 'geo-root', 'catalog',
        )

    def location(self, item):
        return reverse(item)


sitemap_dict = {
    'pages': StaticViewSitemap,
    'aux_page': AuxPageSitemap,
    'categories': CategorySitemap,
    'products': ProductSitemap,
    'regions': RegionSitemap,
    'objects': ObjectPPFSitemap,
    'news': NewsSitemap,
    'promo': PromoSitemap,
}


urlpatterns = [
    url(r'^i18n/', include('django.conf.urls.i18n')),
    url(r'^admin/', admin.site.urls),
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),
    url(r'^telegram/', include('telegram_bot.urls')),
] + static(MEDIA_URL, document_root=MEDIA_ROOT)


urlpatterns += i18n_patterns(
    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^catalog/', include('catalog.urls')),
    url(r'^assistant/', include('assistant.urls')),
    url(r'^our-objects/', include('geo.urls')),
    url(r'^news/', include('news.urls')),
    url(r'^contacts/', ContactsView.as_view(), name='contacts'),
    url(r'^accounts/', include('user_profile.urls')),
    url(r'^library/', include('library.urls')),
    url(r'^pages/', include('pages.urls')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemap_dict}, name='django.contrib.sitemaps.views.sitemap'),
    prefix_default_language=False
)


if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
