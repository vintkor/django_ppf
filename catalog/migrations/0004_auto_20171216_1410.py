# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2017-12-16 12:10
from __future__ import unicode_literals

import ckeditor_uploader.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0003_auto_20171206_2139'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='description',
            field=ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True, verbose_name='Description'),
        ),
    ]