from .views import PageDetailView
from django.urls import path


app_name = 'pages'
urlpatterns = [
    path('<str:slug>/', PageDetailView.as_view(), name='page'),
]
