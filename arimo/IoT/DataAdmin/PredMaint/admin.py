from django.contrib.admin import ModelAdmin, site

from .models import Blueprint


class BlueprintAdmin(ModelAdmin):
    list_display = 'equipment_general_type', 'uuid', 'timestamp', 'active'
    list_filter = 'equipment_general_type', 'active', 'timestamp'
    search_fields = 'equipment_general_type', 'uuid',


site.register(
    Blueprint,
    admin_class=BlueprintAdmin)
