from django.contrib.admin import ModelAdmin, site

from .models import Blueprint


class BlueprintAdmin(ModelAdmin):
    list_display = 'url',
    list_filter = 'url',
    search_fields = 'url',


site.register(
    Blueprint,
    admin_class=BlueprintAdmin)
