# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-10-08 18:16
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dynamic_scraper', '0025_new_follow_pages_page_xpath_pagination_attribute'),
        ('resorts', '0005_resort_condtions_page_url'),
    ]

    operations = [
        migrations.RenameField(
            model_name='resort',
            old_name='condtions_page_url',
            new_name='conditions_page_url',
        ),
        migrations.AddField(
            model_name='resort',
            name='scraper',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='dynamic_scraper.Scraper'),
        ),
        migrations.AddField(
            model_name='resort',
            name='scraper_runtime',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='dynamic_scraper.SchedulerRuntime'),
        ),
    ]