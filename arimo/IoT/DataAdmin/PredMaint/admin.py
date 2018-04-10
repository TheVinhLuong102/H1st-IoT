from django.contrib.admin import ModelAdmin, site

from .forms import BlueprintForm
from .models import Blueprint


class BlueprintAdmin(ModelAdmin):
    list_display = 'equipment_general_type', 'equipment_unique_type', 'trained_to_date', 'timestamp', 'uuid', 'active'
    list_filter = 'equipment_general_type', 'equipment_unique_type', 'trained_to_date', 'timestamp', 'active'
    search_fields = 'equipment_general_type', 'equipment_unique_type', 'uuid',

    form = BlueprintForm


site.register(
    Blueprint,
    admin_class=BlueprintAdmin)
