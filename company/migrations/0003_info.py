# Generated by Django 2.0.3 on 2018-03-23 18:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0002_auto_20180323_1956'),
    ]

    operations = [
        migrations.CreateModel(
            name='Info',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Дата обновления')),
                ('label', models.CharField(max_length=100)),
                ('field', models.CharField(max_length=100)),
                ('fa_icon_class', models.CharField(max_length=60)),
                ('office', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='company.Office')),
            ],
            options={
                'verbose_name': 'Office contact info',
                'verbose_name_plural': 'Offices contact info',
            },
        ),
    ]
