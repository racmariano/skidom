from django.conf.urls import url

from . import views

app_name = 'resorthub'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^userinfo/$', views.userinfo, name='userinfo')
]
