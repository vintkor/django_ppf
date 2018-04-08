from django.urls import path
from .views import WebHookUpdate

app_name = 'telegram'
urlpatterns = [
    path('web-hook/<str:token>', WebHookUpdate.as_view(), name='webhook'),
]
