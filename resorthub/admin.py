# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import OldResort
from .models import UserProfile
from .models import TrailPage

admin.site.register(OldResort)
admin.site.register(UserProfile)  
admin.site.register(TrailPage)  
