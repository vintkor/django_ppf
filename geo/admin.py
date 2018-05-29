from django.contrib import admin
from .models import Region, ObjectPPF, ObjectImage
from mptt.admin import DraggableMPTTAdmin
from sorl.thumbnail.admin import AdminImageMixin


class ObjectImageInline(AdminImageMixin, admin.TabularInline):
    model = ObjectImage
    exclude = ('',)
    extra = 0


@admin.register(Region)
class RegionAdmin(AdminImageMixin, DraggableMPTTAdmin):
    list_display = ('tree_actions', 'indented_title', 'title', 'title_many', 'title_eng', 'code', 'count_objects', 'is_auxpage')
    readonly_fields = ('code',)
    list_editable = ('title', 'title_eng', 'title_many')


@admin.register(ObjectPPF)
class ObjectPPFAdmin(admin.ModelAdmin):
    list_display = ('title', 'region', 'favorite')
    list_filter = ('region', 'favorite')
    search_fields = ('title',)
    inlines = (ObjectImageInline,)
    list_editable = ('favorite',)
    filter_horizontal = ('products',)
