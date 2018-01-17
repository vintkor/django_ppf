from django.conf.urls import url
from .views import (
    AuthView,
    ProfileDetailView,
    user_logout,
)


urlpatterns = [
    # url(r'^register/$', UserSignupView.as_view(), name='dashboard-user-register'),
    url(r'^logout/$', user_logout, name='logout'),
    url(r'^login/$', AuthView.as_view(), name='login'),
    url(r'^profile/$', ProfileDetailView.as_view(), name='profile'),
]