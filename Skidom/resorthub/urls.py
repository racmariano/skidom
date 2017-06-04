from django.conf.urls import url
from django.views.generic import ListView

from . import views

app_name = 'resorthub'
urlpatterns = [
    url(r'^$', views.index, name = 'index'),
    url(r'^signup/$', views.signup, name = 'signup')
]
