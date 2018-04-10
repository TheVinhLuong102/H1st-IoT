from django.contrib.admin import ModelAdmin, site

from .models import Blueprint


class BlueprintAdmin(ModelAdmin):
    list_display = 'url', 'timestamp', 'active'
    list_filter = 'active', 'timestamp'
    search_fields = 'url',


site.register(
    Blueprint,
    admin_class=BlueprintAdmin)
