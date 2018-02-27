# Generated by Django 2.0.1 on 2018-02-27 19:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0020_auto_20180226_2132'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='title_benefit',
            field=models.CharField(blank=True, max_length=250, null=True, verbose_name='Benefit block title'),
        ),
        migrations.AddField(
            model_name='product',
            name='title_country',
            field=models.CharField(blank=True, max_length=250, null=True, verbose_name='Map block title'),
        ),
        migrations.AddField(
            model_name='product',
            name='title_digits',
            field=models.CharField(blank=True, max_length=250, null=True, verbose_name='Digits block title'),
        ),
        migrations.AddField(
            model_name='product',
            name='title_documents',
            field=models.CharField(blank=True, max_length=250, null=True, verbose_name='Documents block title'),
        ),
        migrations.AddField(
            model_name='product',
            name='title_features',
            field=models.CharField(blank=True, max_length=250, null=True, verbose_name='Feature block title'),
        ),
        migrations.AddField(
            model_name='product',
            name='title_gallery',
            field=models.CharField(blank=True, max_length=250, null=True, verbose_name='Gallery block title'),
        ),
        migrations.AddField(
            model_name='product',
            name='title_video',
            field=models.CharField(blank=True, max_length=250, null=True, verbose_name='Video block title'),
        ),
    ]
