# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

class Resort(models.Model):
    resort_name = models.CharField(max_length=200)
    resort_address = models.CharField(max_length=400)
    lift_ticket_price = models.DecimalField(max_digits = 5, decimal_places = 2)
    rental_price = models.DecimalField(max_digits = 5, decimal_places = 2)
    season_begins = models.DateField(auto_now = True)
    maxx_pass = models.BooleanField(default = True) 
    one_day_snowfall = models.IntegerField(default = 0)
    two_day_snowfall = models.IntegerField(default = 0)
    three_day_snowfall = models.IntegerField(default = 0)
    four_day_snowfall = models.IntegerField(default = 0)
    five_day_snowfall = models.IntegerField(default = 0)
    six_day_snowfall = models.IntegerField(default = 0)
    seven_day_snowfall = models.IntegerField(default = 0)
    eight_day_snowfall = models.IntegerField(default = 0)
    nine_day_snowfall = models.IntegerField(default = 0)
    ten_day_snowfall = models.IntegerField(default = 0)

    def __str__(self):
        return self.resort_name


