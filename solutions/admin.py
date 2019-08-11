from django.contrib import admin
from .models import (
    SolOffer,
    SolProduct,
    SolVariant,
)


class SolVariantInline(admin.TabularInline):
    extra = 0
    model = SolVariant
    filter_vertical = ('products',)


@admin.register(SolProduct)
class SolProductAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'category',
        'is_active',
    )
    prepopulated_fields = {'slug': ('title',)}
    save_on_top = True
    save_as = True


@admin.register(SolOffer)
class SolOfferAdmin(admin.ModelAdmin):
    list_display = (
        '__str__',
        'product',
    )
    inlines = (SolVariantInline,)
    save_on_top = True
    save_as = True


@admin.register(SolVariant)
class SolVariantAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'price',
    )
    save_on_top = True
    save_as = True
