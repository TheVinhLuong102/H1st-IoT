from django.contrib.admin import ModelAdmin, site

from .forms import BlueprintForm
from .models import Blueprint


class BlueprintAdmin(ModelAdmin):
    list_display = 'equipment_general_type', 'equipment_unique_type', 'uuid', 'timestamp', 'active'
    list_filter = 'equipment_general_type', 'equipment_unique_type', 'active', 'timestamp'
    search_fields = 'equipment_general_type', 'equipment_unique_type', 'uuid',

    form = BlueprintForm


site.register(
    Blueprint,
    admin_class=BlueprintAdmin)
