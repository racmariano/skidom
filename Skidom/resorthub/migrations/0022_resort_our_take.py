# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-07-18 15:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resorthub', '0021_auto_20170707_1718'),
    ]

    operations = [
        migrations.AddField(
            model_name='resort',
            name='our_take',
            field=models.CharField(default='This resort is so great! Yay, skiing!', max_length=1000),
        ),
    ]
