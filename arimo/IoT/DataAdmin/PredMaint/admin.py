from django.contrib.admin import ModelAdmin, site

from .models import Blueprint


class BlueprintAdmin(ModelAdmin):
    list_display = 'uuid', 'timestamp', 'active'
    list_filter = 'active', 'timestamp'
    search_fields = 'uuid',


site.register(
    Blueprint,
    admin_class=BlueprintAdmin)
