# Generated by Django 2.0.2 on 2018-08-19 13:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assistant', '0022_auto_20180809_2222'),
    ]

    operations = [
        migrations.AddField(
            model_name='parameter',
            name='is_dop_param_for_rozetka',
            field=models.BooleanField(default=False, verbose_name='Доп. параметр для розетки'),
        ),
    ]