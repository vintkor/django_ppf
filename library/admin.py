from django.contrib import admin
from .models import Category, Document
from mptt.admin import DraggableMPTTAdmin


@admin.register(Category)
class CategoryAdmin(DraggableMPTTAdmin):
    list_display = ('tree_actions', 'indented_title',)
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'category',
    )
    prepopulated_fields = {'slug': ('title',)}
