# Generated by Django 2.0.2 on 2018-09-15 11:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('assistant', '0023_parameter_is_dop_param_for_rozetka'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ('-code',), 'permissions': (('can_update_mizol_prices', 'Can update mizol prices'), ('Freelanser', 'freelanser')), 'verbose_name': 'Товар', 'verbose_name_plural': 'Товары'},
        ),
    ]
