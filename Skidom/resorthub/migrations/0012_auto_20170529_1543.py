# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-29 19:43
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('resorthub', '0011_remove_resort_maxx_pass'),
    ]

    operations = [
        migrations.RenameField(
            model_name='resort',
            old_name='resort_address',
            new_name='address',
        ),
        migrations.RenameField(
            model_name='resort',
            old_name='resort_name',
            new_name='name',
        ),
    ]
