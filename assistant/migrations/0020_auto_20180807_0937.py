# Generated by Django 2.0.2 on 2018-08-07 06:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assistant', '0019_product_discont'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='discont',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=4, null=True, verbose_name='Скидка'),
        ),
    ]
