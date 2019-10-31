from django.contrib import admin
from .models import Source
import jsonfield
from django_json_widget.widgets import JSONEditorWidget


@admin.register(Source)
class SourceAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'url',
        'for_assistant',
        'active',
    )
    formfield_overrides = {
        jsonfield.JSONField: {'widget': JSONEditorWidget()},
    }
