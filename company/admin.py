from django.contrib import admin
from .models import (
    Company,
    Office,
    Gallery,
    Info,
)


class InfoInline(admin.StackedInline):
    model = Info
    extra = 0


class GalleryInline(admin.StackedInline):
    model = Gallery
    extra = 0


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_office_count',)


@admin.register(Office)
class Office(admin.ModelAdmin):
    inlines = (InfoInline, GalleryInline,)
    list_display = ('company', 'region', 'address', 'get_images_count',)


@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    pass


@admin.register(Info)
class InfoAdmin(admin.ModelAdmin):
    list_display = ('office', 'label', 'field',)
