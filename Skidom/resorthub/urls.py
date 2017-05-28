from django.conf.urls import url
from django.views.generic import ListView

from . import views

app_name = 'resorthub'
urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name = 'index'),
    url(r'^userinfo/$', views.userinfo, name='userinfo')
]
