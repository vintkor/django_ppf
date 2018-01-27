from django.conf.urls import url, include
from django.contrib import admin
from django_ppf.settings import MEDIA_URL, MEDIA_ROOT
from django.conf.urls.static import static
from .views import HomeView, ContactsView
from django.conf import settings
from django.contrib import sitemaps
from catalog.sitemap import ProductSitemap, CategorySitemap
from geo.sitemap import RegionSitemap, ObjectPPFSitemap
from news.sitemap import NewsSitemap
from django.contrib.sitemaps.views import sitemap
from django.urls import path, reverse


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
    'categories': CategorySitemap,
    'products': ProductSitemap,
    'regions': RegionSitemap,
    'objects': ObjectPPFSitemap,
    'news': NewsSitemap,
}


urlpatterns = [
    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^admin/', admin.site.urls),
    url(r'^catalog/', include('catalog.urls')),
    url(r'^assistant/', include('assistant.urls')),
    url(r'^our-objects/', include('geo.urls')),
    url(r'^news/', include('news.urls')),
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),
    url(r'^accounts/', include('profile.urls')),
    url(r'^contacts/', ContactsView.as_view(), name='contacts'),
    path('sitemap.xml', sitemap, {'sitemaps': sitemap_dict}, name='django.contrib.sitemaps.views.sitemap'),
] + static(MEDIA_URL, document_root=MEDIA_ROOT)


if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
