# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Resort
from .models import UserProfile

admin.site.register(Resort)
admin.site.register(UserProfile)    
