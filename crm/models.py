from django.db import models
from django_ppf.basemodel import BaseModel


class UserRole(BaseModel):
    title = models.CharField(max_length=255, verbose_name='Роль')
