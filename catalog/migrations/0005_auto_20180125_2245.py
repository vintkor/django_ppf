# Generated by Django 2.0.1 on 2018-01-25 20:45

import catalog.models
from django.db import migrations
import sorl.thumbnail.fields


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0004_auto_20171216_1410'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='image',
            field=sorl.thumbnail.fields.ImageField(blank=True, null=True, upload_to=catalog.models.set_image_name, verbose_name='Изображение'),
        ),
        migrations.AlterField(
            model_name='product',
            name='image',
            field=sorl.thumbnail.fields.ImageField(blank=True, null=True, upload_to=catalog.models.set_product_image_name, verbose_name='Изображение'),
        ),
    ]