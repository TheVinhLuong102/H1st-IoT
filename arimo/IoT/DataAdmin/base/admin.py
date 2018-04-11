from django.contrib.admin import ModelAdmin, site

from .forms import EquipmentDataFieldForm, EquipmentUniqueTypeGroupForm, EquipmentUniqueTypeForm, EquipmentInstanceForm
from .models import EquipmentGeneralType, EquipmentDataField, EquipmentUniqueTypeGroup, EquipmentUniqueType, EquipmentInstance


class EquipmentGeneralTypeAdmin(ModelAdmin):
    list_display = 'name',
    list_filter = 'name',
    search_fields = 'name',


site.register(
    EquipmentGeneralType,
    admin_class=EquipmentGeneralTypeAdmin)


class EquipmentDataFieldAdmin(ModelAdmin):
    list_display = \
        'equipment_general_type', \
        'equipment_data_field_type', \
        'name', \
        'data_type', \
        'nullable', \
        'lower_numeric_null', \
        'upper_numeric_null', \
        'default_val', \
        'min_val', \
        'max_val'

    list_filter = \
        'equipment_general_type', \
        'equipment_data_field_type', \
        'name', \
        'data_type', \
        'nullable', \
        'lower_numeric_null', \
        'upper_numeric_null', \
        'default_val', \
        'min_val', \
        'max_val'

    search_fields = \
        'equipment_general_type', \
        'equipment_data_field_type', \
        'name', \
        'data_type', \
        'nullable', \
        'lower_numeric_null', \
        'upper_numeric_null', \
        'default_val', \
        'min_val', \
        'max_val'

    form = EquipmentDataFieldForm


site.register(
    EquipmentDataField,
    admin_class=EquipmentDataFieldAdmin)


class EquipmentUniqueTypeGroupAdmin(ModelAdmin):
    list_display = 'equipment_general_type', 'name'
    list_filter = 'equipment_general_type', 'name'
    search_fields = 'equipment_general_type', 'name'

    form = EquipmentUniqueTypeGroupForm


site.register(
    EquipmentUniqueTypeGroup,
    admin_class=EquipmentUniqueTypeGroupAdmin)


class EquipmentUniqueTypeAdmin(ModelAdmin):
    list_display = 'equipment_general_type', 'name'
    list_filter = 'equipment_general_type', 'name'
    search_fields = 'equipment_general_type', 'name'

    form = EquipmentUniqueTypeForm


site.register(
    EquipmentUniqueType,
    admin_class=EquipmentUniqueTypeAdmin)


class EquipmentInstanceAdmin(ModelAdmin):
    list_display = 'equipment_general_type', 'equipment_unique_type', 'name'
    list_filter = 'equipment_general_type', 'equipment_unique_type', 'name'
    search_fields = 'equipment_general_type', 'equipment_unique_type', 'name'

    form = EquipmentInstanceForm


site.register(
    EquipmentInstance,
    admin_class=EquipmentInstanceAdmin)
