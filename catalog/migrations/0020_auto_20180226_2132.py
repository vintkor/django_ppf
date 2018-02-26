# Generated by Django 2.0.1 on 2018-02-26 19:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0019_auto_20180226_2120'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='category',
        ),
        migrations.AddField(
            model_name='product',
            name='category',
            field=models.ManyToManyField(to='catalog.Category', verbose_name='Категория'),
        ),
    ]
