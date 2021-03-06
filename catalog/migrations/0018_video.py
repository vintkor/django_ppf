# Generated by Django 2.0.1 on 2018-02-24 20:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0017_auto_20180224_1535'),
    ]

    operations = [
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Дата обновления')),
                ('title', models.CharField(max_length=250, verbose_name='Заголовок')),
                ('link', models.URLField(verbose_name='Link to youtube video')),
                ('product', models.ForeignKey(on_delete=None, to='catalog.Product', verbose_name='Продукт')),
            ],
            options={
                'verbose_name': 'Video',
                'verbose_name_plural': 'Videos',
            },
        ),
    ]
