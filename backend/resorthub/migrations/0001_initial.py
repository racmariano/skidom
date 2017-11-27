# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-09-11 01:22
from __future__ import unicode_literals

import address.models
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import multiselectfield.db.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('dynamic_scraper', '0025_new_follow_pages_page_xpath_pagination_attribute'),
        ('address', '0001_initial'),
        ('auth', '0008_alter_user_username_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.ASCIIUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=30, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('favorite_runs', multiselectfield.db.fields.MultiSelectField(choices=[('BE', 'Beginner'), ('IN', 'Intermediate'), ('EX', 'Expert'), ('TE', 'Freestyle'), ('GL', 'Glades')], default='BE', max_length=14)),
                ('pass_type', models.CharField(choices=[('NON', 'None'), ('EPI', 'Epic Pass'), ('MAX', 'Max Pass'), ('MOC', 'Mountain Collective Pass'), ('NEP', 'New England Pass'), ('PEA', 'Peak Pass'), ('POW', 'Powder Alliance Pass'), ('ROC', 'Rocky Mountain Super Pass')], default='NON', max_length=20)),
                ('own_equipment', models.BooleanField(default=False)),
                ('address', address.models.AddressField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='address.Address')),
            ],
            options={
                'abstract': False,
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Resort',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=200)),
                ('web_home', models.URLField(default='')),
                ('lift_ticket_price', models.DecimalField(decimal_places=2, default=100.0, max_digits=6)),
                ('rental_price', models.DecimalField(decimal_places=2, default=50.0, max_digits=5)),
                ('season_begins', models.DateField(auto_now=True)),
                ('available_passes', multiselectfield.db.fields.MultiSelectField(choices=[('NON', 'None'), ('EPI', 'Epic Pass'), ('MAX', 'Max Pass'), ('MOC', 'Mountain Collective Pass'), ('NEP', 'New England Pass'), ('PEA', 'Peak Pass'), ('POW', 'Powder Alliance Pass'), ('ROC', 'Rocky Mountain Super Pass')], default='NON', max_length=31)),
                ('one_day_snowfall', models.DecimalField(decimal_places=1, default=0, max_digits=3)),
                ('two_day_snowfall', models.DecimalField(decimal_places=1, default=0, max_digits=3)),
                ('three_day_snowfall', models.DecimalField(decimal_places=1, default=0, max_digits=3)),
                ('four_day_snowfall', models.DecimalField(decimal_places=1, default=0, max_digits=3)),
                ('five_day_snowfall', models.DecimalField(decimal_places=1, default=0, max_digits=3)),
                ('six_day_snowfall', models.DecimalField(decimal_places=1, default=0, max_digits=3)),
                ('seven_day_snowfall', models.DecimalField(decimal_places=1, default=0, max_digits=3)),
                ('eight_day_snowfall', models.DecimalField(decimal_places=1, default=0, max_digits=3)),
                ('nine_day_snowfall', models.DecimalField(decimal_places=1, default=0, max_digits=3)),
                ('ten_day_snowfall', models.DecimalField(decimal_places=1, default=0, max_digits=3)),
                ('num_slopes', models.IntegerField(default=0)),
                ('num_green', models.IntegerField(default=0)),
                ('num_blue', models.IntegerField(default=0)),
                ('num_black', models.IntegerField(default=0)),
                ('num_doubb', models.IntegerField(default=0)),
                ('our_take', models.CharField(default='This resort is so great! Yay, skiing!', max_length=1000)),
                ('url', models.URLField(blank=True)),
                ('address', address.models.AddressField(blank=True, on_delete=django.db.models.deletion.CASCADE, to='address.Address')),
                ('scraper', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='dynamic_scraper.Scraper')),
                ('scraper_runtime', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='dynamic_scraper.SchedulerRuntime')),
            ],
        ),
        migrations.CreateModel(
            name='TrailPage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField(blank=True)),
                ('num_open', models.IntegerField(default=999)),
                ('base_temp', models.DecimalField(decimal_places=2, default=0, max_digits=6)),
                ('summit_temp', models.DecimalField(decimal_places=2, default=0, max_digits=6)),
                ('new_snow', models.CharField(default='', max_length=100)),
                ('checker_runtime', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='dynamic_scraper.SchedulerRuntime')),
                ('resort', models.ForeignKey(default=4, null=True, on_delete=django.db.models.deletion.CASCADE, to='resorthub.Resort')),
            ],
        ),
        migrations.AddField(
            model_name='userprofile',
            name='favorite_resorts',
            field=models.ManyToManyField(blank=True, null=True, to='resorthub.Resort'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='groups',
            field=models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions'),
        ),
    ]