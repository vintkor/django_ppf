# Generated by Django 2.0.2 on 2018-05-17 19:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('geo', '0013_region_title_eng'),
    ]

    operations = [
        migrations.AddField(
            model_name='region',
            name='title_many',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Title many'),
        ),
    ]