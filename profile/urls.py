from django.conf.urls import url
from .views import (
    AuthView,
)


urlpatterns = [
    # url(r'^register/$', UserSignupView.as_view(), name='dashboard-user-register'),
    url(r'^login/$', AuthView.as_view(), name='login'),
]