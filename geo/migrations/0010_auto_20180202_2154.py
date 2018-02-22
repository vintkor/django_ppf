# Generated by Django 2.0.1 on 2018-02-02 19:54

import ckeditor_uploader.fields
from django.db import migrations, models
import django.db.models.deletion
import mptt.fields


class Migration(migrations.Migration):

    dependencies = [
        ('geo', '0009_auto_20180125_2247'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='objectimage',
            options={'verbose_name': 'Изображение', 'verbose_name_plural': 'Изображения'},
        ),
        migrations.AlterModelOptions(
            name='objectppf',
            options={'verbose_name': 'Объект', 'verbose_name_plural': 'Объекты'},
        ),
        migrations.AlterModelOptions(
            name='region',
            options={'verbose_name': 'Регион', 'verbose_name_plural': 'Регионы'},
        ),
        migrations.AlterField(
            model_name='objectimage',
            name='created',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Дата создания'),
        ),
        migrations.AlterField(
            model_name='objectimage',
            name='object_ppf',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='geo.ObjectPPF', verbose_name='Объект'),
        ),
        migrations.AlterField(
            model_name='objectimage',
            name='title',
            field=models.CharField(max_length=250, verbose_name='Заголовок'),
        ),
        migrations.AlterField(
            model_name='objectimage',
            name='updated',
            field=models.DateTimeField(auto_now=True, verbose_name='Дата обновления'),
        ),
        migrations.AlterField(
            model_name='objectimage',
            name='weight',
            field=models.PositiveSmallIntegerField(default=0, verbose_name='Вес'),
        ),
        migrations.AlterField(
            model_name='objectppf',
            name='created',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Дата создания'),
        ),
        migrations.AlterField(
            model_name='objectppf',
            name='description',
            field=models.TextField(blank=True, null=True, verbose_name='Описание'),
        ),
        migrations.AlterField(
            model_name='objectppf',
            name='favorite',
            field=models.BooleanField(default=False, verbose_name='Избранные объекты'),
        ),
        migrations.AlterField(
            model_name='objectppf',
            name='meta_description',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='META Описание'),
        ),
        migrations.AlterField(
            model_name='objectppf',
            name='meta_keywords',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='META Ключевые слова'),
        ),
        migrations.AlterField(
            model_name='objectppf',
            name='products',
            field=models.ManyToManyField(to='catalog.Product', verbose_name='Продукты'),
        ),
        migrations.AlterField(
            model_name='objectppf',
            name='region',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='geo.Region', verbose_name='Регион'),
        ),
        migrations.AlterField(
            model_name='objectppf',
            name='title',
            field=models.CharField(max_length=250, verbose_name='Заголовок'),
        ),
        migrations.AlterField(
            model_name='objectppf',
            name='updated',
            field=models.DateTimeField(auto_now=True, verbose_name='Дата обновления'),
        ),
        migrations.AlterField(
            model_name='region',
            name='created',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Дата создания'),
        ),
        migrations.AlterField(
            model_name='region',
            name='description',
            field=ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True, verbose_name='Описание'),
        ),
        migrations.AlterField(
            model_name='region',
            name='meta_description',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='META Описание'),
        ),
        migrations.AlterField(
            model_name='region',
            name='meta_keywords',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='META Ключевые слова'),
        ),
        migrations.AlterField(
            model_name='region',
            name='parent',
            field=mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='geo.Region', verbose_name='Родительский регион'),
        ),
        migrations.AlterField(
            model_name='region',
            name='title',
            field=models.CharField(max_length=200, verbose_name='Заголовок'),
        ),
        migrations.AlterField(
            model_name='region',
            name='updated',
            field=models.DateTimeField(auto_now=True, verbose_name='Дата обновления'),
        ),
    ]
