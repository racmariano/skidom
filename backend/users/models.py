# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from address.models import AddressField

from django.db import models
from django import forms
from django.contrib.auth.models import AbstractUser

from resorts.models import Resort, SkiPass

# User model
class UserProfile(AbstractUser):
    address = AddressField(null = True, blank = True)
    email = models.EmailField(null = True, blank = True)

    favorite_resorts = forms.ModelMultipleChoiceField(queryset = Resort.objects.all())   

    pass_id = forms.ModelChoiceField(queryset = SkiPass.objects.all())
    own_equipment = models.BooleanField(default = False)