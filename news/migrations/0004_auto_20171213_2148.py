# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2017-12-13 19:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0003_auto_20171209_1849'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='title',
            field=models.CharField(max_length=200, verbose_name='Название'),
        ),
    ]
