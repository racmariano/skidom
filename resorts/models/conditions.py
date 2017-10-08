# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from .resort import Resort

from django.db import models
from django.contrib.postgres.fields import ArrayField

from dynamic_scraper.models import Scraper, SchedulerRuntime
from scrapy_djangoitem import DjangoItem

import datetime

# Past and forecasted conditions for a resort
class Conditions(models.Model):

    # Hard-coded attributes needed for scraping
    resort = models.ForeignKey(Resort, null = True, default=6)
    conditions_page_url = models.URLField(blank = True)
    checker_runtime = models.ForeignKey(SchedulerRuntime, blank = True, null = True, on_delete = models.SET_NULL)

    # Attributes collected during scraping
    date = models.DateField(default = datetime.date.today)
    base_temp = models.DecimalField(max_digits = 6, decimal_places = 2, default = 0)
    summit_temp = models.DecimalField(max_digits = 6, decimal_places = 2, default = 0)
    wind_speed = models.DecimalField(max_digits = 6, decimal_places = 2, default = 0)
    base_depth = models.DecimalField(max_digits = 6, decimal_places = 2, default = 0)
    num_trails_open = models.IntegerField(default = 0)
    new_snow_24_hr = models.IntegerField(default = 0)
    #past_n_day_snowfall = ArrayField(models.DecimalField(max_digits = 6, decimal_places = 2, default = 0), size = 15)
    #past_n_day_wind_speed = ArrayField(models.DecimalField(max_digits = 6, decimal_places = 2, default = 0), size = 15)
    #future_n_day_snowfall = ArrayField(models.DecimalField(max_digits = 6, decimal_places = 2, default = 0), size = 15)
    #future_n_day_wind_speed = ArrayField(models.DecimalField(max_digits = 6, decimal_places = 2, default = 0), size = 15)


    def __init__(self, *args, **kwargs):
        super(Conditions, self).__init__(*args, **kwargs)
        if not self.id:
            self.conditions_page_url = self.resort.conditions_page_url

    def __unicode__(self):
        return self.resort.name+(" Scraper")

    def __str__(self):
        return self.resort.name+(" Scraper")

    class Meta:
        verbose_name_plural = "Conditions"

class ConditionsItem(DjangoItem):
    django_model = Conditions
