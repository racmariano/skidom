# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from multiselectfield import MultiSelectField
from address.models import AddressField


from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver

from dynamic_scraper.models import Scraper, SchedulerRuntime
from scrapy_djangoitem import DjangoItem

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
    web_home = models.URLField(default = '')

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

    # Slope information
    num_slopes = models.IntegerField(default = 0)
    num_green = models.IntegerField(default = 0)
    num_blue = models.IntegerField(default = 0)
    num_black = models.IntegerField(default = 0)
    num_doubb = models.IntegerField(default = 0)

    # Short 'our take' description
    our_take = models.CharField(max_length = 1000, default = "This resort is so great! Yay, skiing!")


    # To mine num_open information from trail info page (url refers to trail info page) 
    url = models.URLField(blank=True)
    scraper = models.ForeignKey(Scraper, blank = True, null = True, on_delete = models.SET_NULL)
    scraper_runtime = models.ForeignKey(SchedulerRuntime, blank = True, null = True, on_delete = models.SET_NULL)

    def __str__(self):
        return self.name

# Ski website model for scraping
class TrailPage(models.Model):
    resort = models.ForeignKey(Resort, null = True, default=4)
    url = models.URLField(blank=True)

    num_open = models.IntegerField(default = 999)
    base_temp = models.DecimalField(max_digits = 3, decimal_places = 1, default = 0)
    summit_temp = models.DecimalField(max_digits = 3, decimal_places = 1, default = 0)
    new_snow =  models.CharField(default = "", max_length = 100)

    checker_runtime = models.ForeignKey(SchedulerRuntime, blank = True, null = True, on_delete = models.SET_NULL)

    def __init__(self, *args, **kwargs):
        super(TrailPage, self).__init__(*args, **kwargs)
        if not self.id:
            self.url = self.resort.url

    def __unicode__(self):
        return self.url

class TrailPageItem(DjangoItem):
    django_model = TrailPage

# User model
class UserProfile(AbstractUser):
    address = AddressField(null = True, blank = True)
    email = models.EmailField(null = True, blank = True)

    RUN_CHOICES = (("BE", "Beginner"),
                     ("IN", "Intermediate"),
                     ("EX", "Expert"),
                     ("TE", "Freestyle"),
                     ("GL", "Glades"))
        
    favorite_runs = MultiSelectField(choices = RUN_CHOICES, default = "BE")
    favorite_resorts = models.ManyToManyField(Resort, null = True, blank = True)    

    pass_type = models.CharField(max_length = 20, choices = PASS_CHOICES, default = "NON")
    own_equipment = models.BooleanField(default = False) 

