# Generated by Django 2.0 on 2017-12-09 11:49

from django.db import migrations, models
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('geo', '0003_auto_20171209_1206'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='region',
            managers=[
                ('_tree_manager', django.db.models.manager.Manager()),
            ],
        ),
        migrations.AlterField(
            model_name='region',
            name='code',
            field=models.CharField(blank=True, default=None, max_length=15, null=True, unique=True),
        ),
    ]
