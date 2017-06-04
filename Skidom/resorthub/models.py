# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from multiselectfield import MultiSelectField
from address.models import AddressField

from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver

PASS_CHOICES = (("NON", "None"),
                ("EPI", "Epic Pass"),
                ("MAX", "Max Pass"),
                ("MOC", "Mountain Collective Pass"),
                ("NEP", "New England Pass"),
                ("PEA", "Peak Pass"),
                ("POW", "Powder Alliance Pass"),
                ("ROC", "Rocky Mountain Super Pass"))

# Basic resort model
class Resort(models.Model):

    # Basic resort information
    name = models.CharField(max_length=200, default = "")
    address = AddressField(blank = True)

    # Prices for lift and rentals
    lift_ticket_price = models.DecimalField(max_digits = 6, decimal_places = 2, default = 100.00)
    rental_price = models.DecimalField(max_digits = 5, decimal_places = 2, default = 50.00)

    # Season information
    season_begins = models.DateField(auto_now = True)

    # Pass information
    available_passes = MultiSelectField(choices = PASS_CHOICES, default = "NON")

    # Snow predictions
    one_day_snowfall = models.DecimalField(max_digits = 3, decimal_places = 1, default = 0)
    two_day_snowfall = models.DecimalField(max_digits = 3, decimal_places = 1, default = 0)
    three_day_snowfall = models.DecimalField(max_digits = 3, decimal_places = 1, default = 0)
    four_day_snowfall = models.DecimalField(max_digits = 3, decimal_places = 1, default = 0)
    five_day_snowfall = models.DecimalField(max_digits = 3, decimal_places = 1, default = 0)
    six_day_snowfall = models.DecimalField(max_digits = 3, decimal_places = 1, default = 0)
    seven_day_snowfall = models.DecimalField(max_digits = 3, decimal_places = 1, default = 0)
    eight_day_snowfall = models.DecimalField(max_digits = 3, decimal_places = 1, default = 0)
    nine_day_snowfall = models.DecimalField(max_digits = 3, decimal_places = 1, default = 0)
    ten_day_snowfall = models.DecimalField(max_digits = 3, decimal_places = 1, default = 0)

    def __str__(self):
        return self.name


# User model
class UserProfile(AbstractUser):
    address = AddressField(null = True, blank = True)

    RUN_CHOICES = (("BE", "Beginner"),
                     ("IN", "Intermediate"),
                     ("EX", "Expert"),
                     ("TE", "Freestyle"),
                     ("GL", "Glades"))
        
    favorite_runs = MultiSelectField(choices = RUN_CHOICES, default = "BE")
    pass_type = models.CharField(max_length = 20, choices = PASS_CHOICES, default = "NON")
    own_equipment = models.BooleanField(default = False) 

