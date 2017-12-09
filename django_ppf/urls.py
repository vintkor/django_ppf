"""django_ppf URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django_ppf.settings import MEDIA_URL, MEDIA_ROOT
from django.conf.urls.static import static
from .views import HomeView
from django.conf import settings

urlpatterns = [
    url(r'^jet/', include('jet.urls', 'jet')),
    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^admin/', admin.site.urls),
    url(r'^catalog/', include('catalog.urls')),
    url(r'^assistant/', include('catalog_prom.urls')),
    url(r'^partners/', include('partners.urls')),
    url(r'^our-objects/', include('geo.urls')),
    url(r'^news/', include('news.urls')),
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),
] + static(MEDIA_URL, document_root=MEDIA_ROOT)


if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
