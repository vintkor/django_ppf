# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-01-15 18:44
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('assistant', '0003_auto_20180115_2044'),
        ('partners', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='branch',
            name='parent_provider',
        ),
        migrations.RemoveField(
            model_name='branch',
            name='region_for_work',
        ),
        migrations.DeleteModel(
            name='Branch',
        ),
        migrations.DeleteModel(
            name='Region',
        ),
    ]
