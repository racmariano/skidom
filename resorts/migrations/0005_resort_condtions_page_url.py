# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-10-08 16:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resorts', '0004_auto_20171001_2228'),
    ]

    operations = [
        migrations.AddField(
            model_name='resort',
            name='condtions_page_url',
            field=models.URLField(default=''),
        ),
    ]
