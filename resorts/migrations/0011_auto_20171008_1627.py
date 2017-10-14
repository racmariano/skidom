# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-10-08 20:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resorts', '0010_conditions_resort'),
    ]

    operations = [
        migrations.AddField(
            model_name='conditions',
            name='url',
            field=models.URLField(blank=True),
        ),
        migrations.AlterField(
            model_name='resort',
            name='conditions_page_url',
            field=models.URLField(blank=True),
        ),
    ]