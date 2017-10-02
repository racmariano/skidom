# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from .resort import Resort

from django.db import models
from django.contrib.postgres.fields import ArrayField

from scrapy_djangoitem import DjangoItem

import datetime

# Past and forecasted conditions for a resort
class Conditions(models.Model):
    resort = models.ForeignKey(Resort)
    date = models.DateField(default = datetime.date.today)
    base_temp = models.DecimalField(max_digits = 6, decimal_places = 2, default = 0)
    summit_temp = models.DecimalField(max_digits = 6, decimal_places = 2, default = 0)
    wind_speed = models.DecimalField(max_digits = 6, decimal_places = 2, default = 0)
    base_depth = models.DecimalField(max_digits = 6, decimal_places = 2, default = 0)
    #past_n_day_snowfall = ArrayField(models.DecimalField(max_digits = 6, decimal_places = 2, default = 0), size = 15)
    #past_n_day_wind_speed = ArrayField(models.DecimalField(max_digits = 6, decimal_places = 2, default = 0), size = 15)
    #future_n_day_snowfall = ArrayField(models.DecimalField(max_digits = 6, decimal_places = 2, default = 0), size = 15)
    #future_n_day_wind_speed = ArrayField(models.DecimalField(max_digits = 6, decimal_places = 2, default = 0), size = 15)

    class Meta:
        verbose_name_plural = "Conditions"

class ConditionsItem(DjangoItem):
    django_model = Conditions