from django.contrib import admin
from .models import Category, Product, Manufacturer, Order, Feature, Benefit, Gallery, Document, Video, Digits
from mptt.admin import DraggableMPTTAdmin
from sorl.thumbnail.admin import AdminImageMixin, AdminInlineImageMixin
from django.utils.translation import ugettext_lazy as _
# import catalog.translation
# from modeltranslation.admin import TranslationAdmin


class DigitsInline(admin.StackedInline):
    extra = 0
    model = Digits


class VideoInline(admin.TabularInline):
    extra = 0
    model = Video


class FeatureInline(admin.TabularInline):
    extra = 0
    model = Feature


class BenefitInline(AdminInlineImageMixin, admin.StackedInline):
    extra = 0
    model = Benefit


class GalleryInline(AdminInlineImageMixin, admin.TabularInline):
    extra = 0
    model = Gallery


class DocumentInline(admin.TabularInline):
    extra = 0
    model = Document


@admin.register(Category)
class CategoryAdmin(AdminImageMixin, DraggableMPTTAdmin):
    list_display = ('tree_actions',  'indented_title', 'get_count_products')
    prepopulated_fields = {'slug': ('title',)}
    Category.get_count_products.short_description = _('Products')


@admin.register(Product)
class ProductAdmin(AdminImageMixin, admin.ModelAdmin):
    list_display = ('title', 'category', 'manufacturer', 'active')
    list_filter = ('category',)
    search_fields = ('title',)
    inlines = (FeatureInline, BenefitInline, GalleryInline, DocumentInline, VideoInline, DigitsInline)
    save_on_top = True
    list_editable = ('active',)
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ('countries',)


@admin.register(Manufacturer)
class ManufacturerAdmin(admin.ModelAdmin):
    list_display = ('title', 'get_count_product')
    search_fields = ('title',)

    Manufacturer.get_count_product.short_description = _('Products')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('phone', 'product', 'created')


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'product', 'created')


@admin.register(Digits)
class DigitsAdmin(admin.ModelAdmin):
    list_display = ('digit', 'title', 'product', 'created')
