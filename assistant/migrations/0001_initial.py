# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2017-12-09 20:38
from __future__ import unicode_literals

import assistant.models
import ckeditor_uploader.fields
from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager
import mptt.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('currency', '0001_initial'),
        ('partners', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Updated')),
                ('title', models.CharField(max_length=255, verbose_name='Категория')),
                ('active', models.BooleanField(default=True, verbose_name='Вкл/Выкл')),
                ('lft', models.PositiveIntegerField(db_index=True, editable=False)),
                ('rght', models.PositiveIntegerField(db_index=True, editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(db_index=True, editable=False)),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='assistant.Category')),
            ],
            options={
                'verbose_name_plural': 'Категории',
                'verbose_name': 'Категория',
            },
            managers=[
                ('_tree_manager', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='Delivery',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Updated')),
                ('delivery', ckeditor_uploader.fields.RichTextUploadingField(verbose_name='Доставка')),
                ('delivery_my', ckeditor_uploader.fields.RichTextUploadingField(verbose_name='Самовывоз')),
                ('discount', ckeditor_uploader.fields.RichTextUploadingField(verbose_name='Скидка')),
                ('payment_cash', ckeditor_uploader.fields.RichTextUploadingField(verbose_name='Оплата наличными')),
                ('payment_card', ckeditor_uploader.fields.RichTextUploadingField(verbose_name='Оплата картой')),
                ('payment_bank', ckeditor_uploader.fields.RichTextUploadingField(verbose_name='Оплата расчётный счёт')),
                ('delivery_condition', ckeditor_uploader.fields.RichTextUploadingField(default=' ', verbose_name='Условие поставки')),
                ('branch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='partners.Branch', verbose_name='Филлиал')),
            ],
            options={
                'verbose_name_plural': 'Доп инфо',
                'verbose_name': 'Доп инфо',
            },
        ),
        migrations.CreateModel(
            name='Feature',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Updated')),
                ('title', models.CharField(max_length=150, verbose_name='Характеристика')),
                ('file', models.FileField(blank=True, default=None, null=True, upload_to=assistant.models.set_file_name, verbose_name='Файл')),
                ('text', ckeditor_uploader.fields.RichTextUploadingField(blank=True, default='', verbose_name='Текст поста')),
            ],
            options={
                'verbose_name_plural': 'Характеристики',
                'verbose_name': 'Характеристика',
            },
        ),
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Updated')),
                ('image', models.ImageField(upload_to=assistant.models.set_image_name, verbose_name='Изображение')),
                ('weight', models.PositiveSmallIntegerField(default=0, verbose_name='Порядок')),
            ],
            options={
                'ordering': ['weight'],
                'verbose_name_plural': 'Изображения',
                'verbose_name': 'Изображение',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Updated')),
                ('title', models.CharField(max_length=255, verbose_name='Заголовок')),
                ('price', models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True, verbose_name='Цена')),
                ('course', models.DecimalField(blank=True, decimal_places=5, default=1, max_digits=12, null=True, verbose_name='Курс')),
                ('re_count', models.BooleanField(default=True, verbose_name='Пересчитывать в грн?')),
                ('step', models.DecimalField(decimal_places=3, default=1, max_digits=8, verbose_name='Шаг')),
                ('text', ckeditor_uploader.fields.RichTextUploadingField(blank=True, default='', verbose_name='Текст поста')),
                ('image', models.ImageField(blank=True, default='', upload_to=assistant.models.set_image_name, verbose_name='Изображение')),
                ('active', models.BooleanField(default=True, verbose_name='Вкл/Выкл')),
                ('code', models.CharField(blank=True, default=assistant.models.set_code, max_length=20, null=True, unique=True, verbose_name='Артикул')),
                ('category', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='assistant.Category', verbose_name='Категория')),
                ('currency', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='currency.Currency')),
            ],
            options={
                'ordering': ('-code',),
                'verbose_name_plural': 'Товары',
                'verbose_name': 'Товар',
            },
        ),
        migrations.CreateModel(
            name='Unit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Updated')),
                ('title', models.CharField(max_length=200, verbose_name='Название')),
                ('short_title', models.CharField(max_length=10, verbose_name='Короткое обозначение')),
            ],
            options={
                'ordering': ('title',),
                'verbose_name_plural': 'Единицы измерения',
                'verbose_name': 'Единица измерения',
            },
        ),
        migrations.AddField(
            model_name='product',
            name='unit',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='assistant.Unit', verbose_name='Единица измерения'),
        ),
        migrations.AddField(
            model_name='photo',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='assistant.Product', verbose_name='Товар'),
        ),
        migrations.AddField(
            model_name='feature',
            name='product',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='assistant.Product', verbose_name='Товар'),
        ),
        migrations.AddField(
            model_name='delivery',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='assistant.Product', verbose_name='Товар'),
        ),
    ]