from django.contrib import admin
from .models import News, Promo


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'created')


@admin.register(Promo)
class PromoAdmin(admin.ModelAdmin):
    list_display = ('title', 'created')
    prepopulated_fields = {'slug': ('title',)}
