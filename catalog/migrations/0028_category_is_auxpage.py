# Generated by Django 2.0.2 on 2018-05-17 19:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0027_auto_20180416_2313'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='is_auxpage',
            field=models.BooleanField(default=False),
        ),
    ]
