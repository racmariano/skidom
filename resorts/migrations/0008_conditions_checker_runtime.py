# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-10-08 20:09
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dynamic_scraper', '0025_new_follow_pages_page_xpath_pagination_attribute'),
        ('resorts', '0007_auto_20171008_1424'),
    ]

    operations = [
        migrations.AddField(
            model_name='conditions',
            name='checker_runtime',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='dynamic_scraper.SchedulerRuntime'),
        ),
    ]