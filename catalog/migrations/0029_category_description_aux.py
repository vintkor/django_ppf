# Generated by Django 2.0.2 on 2018-05-17 19:48

import ckeditor_uploader.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0028_category_is_auxpage'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='description_aux',
            field=ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True, verbose_name='Description aux'),
        ),
    ]
