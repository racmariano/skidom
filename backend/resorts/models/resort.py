# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from address.models import AddressField
from dynamic_scraper.models import Scraper, SchedulerRuntime
from scrapy_djangoitem import DjangoItem

# Basic resort model
class Resort(models.Model):

    # Basic resort information
    name = models.CharField(max_length=50, default = '')
    address = AddressField(blank = True)
    website = models.URLField(default = '')

    # Prices for lift and rentals
    adult_lift_ticket = models.DecimalField(max_digits = 6, decimal_places = 2, default = 0)
    combo_rental = models.DecimalField(max_digits = 6, decimal_places = 2, default = 0)

    # Season information
    opening_date = models.DateField(auto_now = True)

    # Slope information
    num_slopes = models.IntegerField(default = 0)
    num_beginner = models.IntegerField(default = 0)
    num_intermediate = models.IntegerField(default = 0)
    num_advanced = models.IntegerField(default = 0)
    num_expert = models.IntegerField(default = 0)
    num_terrain = models.IntegerField(default = 0)

    # Short 'our take' description
    our_take = models.CharField(max_length = 1000, default = "This resort is great! Yay, skiing!")


    # Fields for scraper support 
    conditions_page_url = models.URLField(blank = True)
    scraper = models.ForeignKey(Scraper, blank = True, null = True, on_delete = models.SET_NULL)
    scraper_runtime = models.ForeignKey(SchedulerRuntime, blank = True, null = True, on_delete = models.SET_NULL)



    def __str__(self):
        return self.name
