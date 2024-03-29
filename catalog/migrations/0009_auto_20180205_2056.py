# Generated by Django 2.0.1 on 2018-02-05 18:56

import catalog.models
from django.db import migrations, models
import sorl.thumbnail.fields


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0008_auto_20180205_2055'),
    ]

    operations = [
        migrations.AlterField(
            model_name='benefit',
            name='subtitle',
            field=models.CharField(blank=True, max_length=150, null=True, verbose_name='Subtitle'),
        ),
        migrations.AlterField(
            model_name='benefit',
            name='text',
            field=models.TextField(blank=True, null=True, verbose_name='Текст'),
        ),
        migrations.AlterField(
            model_name='document',
            name='file',
            field=sorl.thumbnail.fields.ImageField(upload_to=catalog.models.set_file_name, verbose_name='Файл'),
        ),
        migrations.AlterField(
            model_name='gallery',
            name='alt',
            field=models.CharField(max_length=150, verbose_name='SEO alt'),
        ),
    ]
