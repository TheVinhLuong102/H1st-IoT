from django.contrib.admin import ModelAdmin, site

from .models import Blueprint


class BlueprintAdmin(ModelAdmin):
    list_display = 'equipment_general_type', 'equipment_unique_type_group', 'trained_to_date', 'timestamp', 'uuid', 'active'
    list_filter = 'equipment_general_type', 'equipment_unique_type_group', 'trained_to_date', 'timestamp', 'active'
    search_fields = 'equipment_general_type', 'equipment_unique_type_group', 'uuid',


site.register(
    Blueprint,
    admin_class=BlueprintAdmin)
