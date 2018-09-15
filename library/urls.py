from django.urls import re_path
from .views import DocumentListView

app_name = 'library'
urlpatterns = [
    re_path(r'^', DocumentListView.as_view(), name='list'),
    re_path(r'^(?P<slug>[\w-]+)/$', DocumentListView.as_view(), name='list'),
]
