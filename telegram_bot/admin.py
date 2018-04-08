from django.contrib import admin
from .models import TelegramBot, TelegramUser


@admin.register(TelegramBot)
class TelegramBotAdmin(admin.ModelAdmin):
    pass


@admin.register(TelegramUser)
class TelegramUserAdmin(admin.ModelAdmin):
    pass
