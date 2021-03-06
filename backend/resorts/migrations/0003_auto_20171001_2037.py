# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-10-02 00:37
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('resorts', '0002_auto_20170916_1541'),
    ]

    operations = [
        migrations.AddField(
            model_name='conditions',
            name='base_depth',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=6),
        ),
        migrations.AddField(
            model_name='conditions',
            name='date',
            field=models.DateField(default=datetime.date.today),
        ),
        migrations.AddField(
            model_name='conditions',
            name='wind_speed',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=6),
        ),
        migrations.AlterField(
            model_name='conditions',
            name='resort',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='resorts.Resort'),
        ),
    ]
