# Generated by Django 2.0.2 on 2019-08-05 19:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('solutions', '0006_solproduct_description'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='solvariant',
            name='image',
        ),
    ]
