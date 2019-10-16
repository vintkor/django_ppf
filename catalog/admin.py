from django.contrib import admin
from .models import Category, Product, Manufacturer, Order, Feature, Benefit, Gallery, Document, Video, Digits, Color
from mptt.admin import DraggableMPTTAdmin
from django.utils.translation import ugettext_lazy as _
from modeltranslation.admin import (
    TabbedTranslationAdmin,
    TabbedDjangoJqueryTranslationAdmin,
    TranslationTabularInline,
    TranslationStackedInline,
)
import catalog.translation
from assistant.admin import set_author


class FrelancerTranslatorAccessMixin:

    def get_queryset(self, request):
        user = request.user
        qs = self.model._default_manager.select_related('product__author').all()
        ordering = self.get_ordering(request)
        if ordering:
            qs = qs.order_by(*ordering)
        if user.is_superuser:
            return qs
        elif user.has_perm('catalog.Freelanser'):
            qs = qs.filter(product__author=user, product__is_checked=False)
            return qs
        else:
            return qs


class ColorInline(TranslationTabularInline):
    extra = 0
    model = Color


class DigitsInline(TranslationTabularInline):
    extra = 0
    model = Digits


class VideoInline(TranslationTabularInline):
    extra = 0
    model = Video


class FeatureInline(TranslationTabularInline):
    extra = 0
    model = Feature


class BenefitInline(TranslationStackedInline):
    extra = 0
    model = Benefit


class GalleryInline(TranslationTabularInline):
    extra = 0
    model = Gallery


class DocumentInline(TranslationTabularInline):
    extra = 0
    model = Document


@admin.register(Category)
class CategoryAdmin(DraggableMPTTAdmin, TabbedTranslationAdmin):
    list_display = ('tree_actions',  'indented_title', 'get_count_products', 'sort', 'is_auxpage',)
    prepopulated_fields = {'slug': ('title',)}
    Category.get_count_products.short_description = _('Products')


def reverse_active(modeladmin, request, queryset):
    for item in queryset:
        item.active = not item.active
        item.save(update_fields=('active',))


def reverse_is_checked(modeladmin, request, queryset):
    for item in queryset:
        item.is_checked = not item.is_checked
        item.save(update_fields=('is_checked',))


@admin.register(Product)
class ProductAdmin(TabbedDjangoJqueryTranslationAdmin):
    list_display = ('title', 'manufacturer', 'author', 'is_checked', 'active')
    list_filter = ('category',)
    search_fields = ('title',)
    inlines = (FeatureInline, BenefitInline, GalleryInline, ColorInline, DocumentInline, VideoInline, DigitsInline)
    save_on_top = True
    list_editable = ('active',)
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ('countries', 'category',)
    actions = (
        reverse_active,
        set_author,
        reverse_is_checked,
    )

    def get_queryset(self, request):
        user = request.user
        qs = super(ProductAdmin, self).get_queryset(request)
        if user.is_superuser:
            return qs
        elif user.has_perm('catalog.Freelanser'):
            return qs.filter(author=user, is_checked=False)
        else:
            return qs


@admin.register(Manufacturer)
class ManufacturerAdmin(TabbedTranslationAdmin):
    list_display = ('title', 'get_count_product')
    search_fields = ('title',)

    Manufacturer.get_count_product.short_description = _('Products')


@admin.register(Order)
class OrderAdmin(FrelancerTranslatorAccessMixin, admin.ModelAdmin):
    list_display = ('phone', 'product', 'created')


@admin.register(Video)
class VideoAdmin(FrelancerTranslatorAccessMixin, TabbedTranslationAdmin):
    list_display = ('title', 'product', 'created')


@admin.register(Digits)
class DigitsAdmin(FrelancerTranslatorAccessMixin, TabbedTranslationAdmin):
    list_display = ('digit', 'title', 'product', 'created')


@admin.register(Gallery)
class GalleryAdmin(FrelancerTranslatorAccessMixin, TabbedTranslationAdmin):
    list_display = ('alt', 'product', 'created')


@admin.register(Color)
class ColorAdmin(FrelancerTranslatorAccessMixin, TabbedTranslationAdmin):
    list_display = ('alt', 'product', 'created')

