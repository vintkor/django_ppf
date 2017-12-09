from django.contrib import admin
from .models import Region, ObjectPPF, ObjectImage
from mptt.admin import DraggableMPTTAdmin


class ObjectImageInline(admin.TabularInline):
    model = ObjectImage
    exclude = ('',)
    extra = 0


@admin.register(Region)
class RegionAdmin(DraggableMPTTAdmin):
    list_display = ('tree_actions', 'indented_title', 'code', 'count_objects')


@admin.register(ObjectPPF)
class ObjectPPFAdmin(admin.ModelAdmin):
    list_display = ('title', 'region', 'favorite')
    list_filter = ('region', 'favorite')
    search_fields = ('title',)
    inlines = (ObjectImageInline,)
    list_editable = ('favorite',)
