# Generated by Django 2.0.1 on 2018-01-25 20:47

from django.db import migrations
import geo.models
import sorl.thumbnail.fields


class Migration(migrations.Migration):

    dependencies = [
        ('geo', '0008_auto_20180122_2151'),
    ]

    operations = [
        migrations.AlterField(
            model_name='objectimage',
            name='image',
            field=sorl.thumbnail.fields.ImageField(blank=True, null=True, upload_to=geo.models.set_object_image_name, verbose_name='Изображение'),
        ),
        migrations.AlterField(
            model_name='region',
            name='image',
            field=sorl.thumbnail.fields.ImageField(blank=True, null=True, upload_to=geo.models.set_region_image_name, verbose_name='Изображение'),
        ),
    ]
