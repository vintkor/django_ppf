from django.contrib import admin
from .models import Category, Product, Manufacturer
from mptt.admin import DraggableMPTTAdmin
from sorl.thumbnail.admin import AdminImageMixin
from django.utils.translation import ugettext_lazy as _
# import catalog.translation
# from modeltranslation.admin import TranslationAdmin


@admin.register(Category)
class CategoryAdmin(AdminImageMixin, DraggableMPTTAdmin):
    list_display = ('tree_actions', 'indented_title',)


@admin.register(Product)
class ProductAdmin(AdminImageMixin, admin.ModelAdmin):
    list_display = ('title', 'category', 'manufacturer')
    list_filter = ('category',)
    search_fields = ('title',)


@admin.register(Manufacturer)
class ManufacturerAdmin(admin.ModelAdmin):
    list_display = ('title', 'get_count_product')
    search_fields = ('title',)

    def get_count_product(self, obj):
        return obj.get_count_product()
    get_count_product.short_description = _('Products')
