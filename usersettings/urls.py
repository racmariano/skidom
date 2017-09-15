from django.conf.urls import url
from django.views.generic import ListView

from . import views

app_name = 'usersettings'

urlpatterns = [
    url(r'^profile/$', views.profile_view, name = 'profile'),
    url(r'^signup/$', views.signup, name='signup'),
]
