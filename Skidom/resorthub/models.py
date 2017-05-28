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

    def __str__(self):
        return self.resort_name

