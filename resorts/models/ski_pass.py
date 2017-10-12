# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models;
from ..models import Resort;

class SkiPass(models.Model):

    name = models.CharField(max_length=50, default = '')
    price = models.DecimalField(max_digits = 6, decimal_places = 2, default = 0)
    resorts = models.ManyToManyField(Resort)

    class Meta:
        verbose_name_plural = "Ski passes"

    def __str__(self):
        return self.name
     