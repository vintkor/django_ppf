# Generated by Django 2.0.2 on 2019-08-24 17:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('solutions', '0008_solproduct_created'),
    ]

    operations = [
        migrations.AddField(
            model_name='soloffer',
            name='text',
            field=models.TextField(blank=True, null=True, verbose_name='Текст'),
        ),
        migrations.AddField(
            model_name='solproduct',
            name='text',
            field=models.TextField(blank=True, null=True, verbose_name='Текст'),
        ),
    ]
