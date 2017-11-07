"""Skidom URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import TemplateView

from django.conf.urls import url, include
from rest_framework import routers

from resorts.views import ResortViewSet

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'resorts', ResortViewSet)
# router.register(r'users', views.UserViewSet)

urlpatterns = [
    #url(r'^', include('resorthub.urls')),
    url(r'^', TemplateView.as_view(template_name="index.html")),
    url(r'^users/', include('users.urls')),
    url(r'^admin/', admin.site.urls), 
    url(r'^accounts/', include('django.contrib.auth.urls')),
    url(r'^api/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls')),
]
