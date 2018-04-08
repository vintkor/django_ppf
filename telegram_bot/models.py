from django_ppf.basemodel import BaseModel
from django.db import models
from django.contrib.auth.models import User


class TelegramBot(BaseModel):
    title = models.CharField(max_length=200)
    token = models.CharField(max_length=200)

    def __str__(self):
        return self.title


class TelegramUser(BaseModel):
    username = models.CharField(max_length=200)
    user_id = models.BigIntegerField()
    system_user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    send_message = models.BooleanField(default=False)

    def __str__(self):
        return self.username
