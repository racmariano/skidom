# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-10-02 02:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resorts', '0003_auto_20171001_2037'),
    ]

    operations = [
        migrations.AddField(
            model_name='conditions',
            name='new_snow_24_hr',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='conditions',
            name='num_trails_open',
            field=models.IntegerField(default=0),
        ),
    ]
