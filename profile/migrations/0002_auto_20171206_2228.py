# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2017-12-06 20:28
from __future__ import unicode_literals

from django.db import migrations, models
import profile.models


class Migration(migrations.Migration):

    dependencies = [
        ('profile', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='avatar',
            field=models.ImageField(blank=True, default=None, null=True, upload_to=profile.models.set_profile_image_name, verbose_name='Avatar'),
        ),
        migrations.AddField(
            model_name='profile',
            name='birthday',
            field=models.DateField(blank=True, default=None, null=True, verbose_name='Birthday'),
        ),
    ]