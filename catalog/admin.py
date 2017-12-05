from django.contrib import admin
from .models import Category, Product
from mptt.admin import DraggableMPTTAdmin


@admin.register(Category)
class CategoryAdmin(DraggableMPTTAdmin):
    list_display = ('tree_actions', 'indented_title',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'category')
    list_filter = ('category',)
    search_fields = ('title',)
