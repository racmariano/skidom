# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import Resort
from .models import SkiPass

# Register your models here.
admin.site.register(Resort)
admin.site.register(SkiPass)
