# Generated by Django 2.0.2 on 2018-06-27 07:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assistant', '0012_parameter'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='stock_quantity',
            field=models.PositiveSmallIntegerField(default=100, verbose_name='Остаток'),
        ),
    ]
