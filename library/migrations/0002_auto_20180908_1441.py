# Generated by Django 2.0.2 on 2018-09-08 11:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='document',
            unique_together={('id', 'slug')},
        ),
    ]
