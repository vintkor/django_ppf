from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.crypto import get_random_string
from django.utils.translation import ugettext as _


def set_profile_image_name(instanse, filename):
    name = get_random_string(40)
    ext = filename.split('.')[-1]
    path = 'images/profile/{}.{}'.format(name, ext)
    return path


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(verbose_name=_('Avatar'),
                               upload_to=set_profile_image_name, blank=True, null=True, default=None)
    birthday = models.DateField(verbose_name=_('Birthday'), blank=True, null=True, default=None)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
