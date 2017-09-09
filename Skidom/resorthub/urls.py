from django.conf.urls import url
from django.views.generic import ListView

from . import views

app_name = 'resorthub'
urlpatterns = [
    url(r'^$', views.index, name = 'index'),
    url(r'^signup/$', views.signup, name = 'signup'),
    url(r'^resorts/$', views.resort_listing, name= 'resorts'),
    url(r'^compare/$', views.compare_listing, name='compare'),
    url(r'^profile/$', views.profile_view, name='profile'),
]
