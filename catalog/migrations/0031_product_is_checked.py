# Generated by Django 2.0.2 on 2019-10-08 18:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0030_auto_20191008_2112'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='is_checked',
            field=models.BooleanField(default=False),
        ),
    ]
