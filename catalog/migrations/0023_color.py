# Generated by Django 2.0.1 on 2018-02-27 20:45

import catalog.models
from django.db import migrations, models
import sorl.thumbnail.fields


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0022_product_title_use'),
    ]

    operations = [
        migrations.CreateModel(
            name='Color',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Дата обновления')),
                ('image', sorl.thumbnail.fields.ImageField(upload_to=catalog.models.set_product_image_name, verbose_name='Изображение')),
                ('alt', models.CharField(blank=True, max_length=150, null=True, verbose_name='SEO alt')),
                ('product', models.ForeignKey(on_delete=None, to='catalog.Product', verbose_name='Продукт')),
            ],
            options={
                'verbose_name': 'Color',
                'verbose_name_plural': 'Colors',
            },
        ),
    ]
