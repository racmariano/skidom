# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-09-12 13:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resorthub', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trailpage',
            name='new_snow',
            field=models.IntegerField(default=0),
        ),
    ]
