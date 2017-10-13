# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-10-12 02:40
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('resorthub', '0003_auto_20170916_1225'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='oldresort',
            name='address',
        ),
        migrations.RemoveField(
            model_name='oldresort',
            name='scraper',
        ),
        migrations.RemoveField(
            model_name='oldresort',
            name='scraper_runtime',
        ),
        migrations.RemoveField(
            model_name='trailpage',
            name='checker_runtime',
        ),
        migrations.RemoveField(
            model_name='trailpage',
            name='resort',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='favorite_resorts',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='favorite_runs',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='pass_type',
        ),
        migrations.DeleteModel(
            name='OldResort',
        ),
        migrations.DeleteModel(
            name='TrailPage',
        ),
    ]
