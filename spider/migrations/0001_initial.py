# Generated by Django 2.0.2 on 2019-10-17 19:06

from django.db import migrations, models
import jsonfield.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Source',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('url', models.URLField()),
                ('rules', jsonfield.fields.JSONField(default=dict)),
                ('for_assistant', models.BooleanField(default=True)),
                ('active', models.BooleanField()),
            ],
            options={
                'verbose_name': 'Источник',
                'verbose_name_plural': 'Источники',
            },
        ),
    ]