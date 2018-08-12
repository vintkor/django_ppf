# Generated by Django 2.0.2 on 2018-08-11 21:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import user_profile.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('user_profile', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('avatar', models.ImageField(blank=True, default=None, null=True, upload_to=user_profile.models.set_profile_image_name, verbose_name='Аватар')),
                ('birthday', models.DateField(blank=True, default=None, null=True, verbose_name='Дата рождения')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='user',
        ),
        migrations.DeleteModel(
            name='UserProfile',
        ),
    ]
