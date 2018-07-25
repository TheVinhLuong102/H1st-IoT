from django.contrib.admin import ModelAdmin, site

from .forms import \
    EquipmentDataFieldForm, \
    EquipmentUniqueTypeGroupForm, \
    EquipmentUniqueTypeForm, \
    EquipmentInstanceForm, \
    EquipmentInstanceAssociationForm

from .models import \
    NumericMeasurementUnit, \
    EquipmentGeneralType, \
    EquipmentDataField, \
    EquipmentUniqueTypeGroup, \
    EquipmentUniqueType, \
    EquipmentInstance, \
    EquipmentInstanceAssociation


class NumericMeasurementUnitAdmin(ModelAdmin):
    list_display = 'name',

    list_filter = 'name',

    show_full_result_count = False   # only a few, but skip counting anyway

    search_fields = 'name',


site.register(
    NumericMeasurementUnit,
    admin_class=NumericMeasurementUnitAdmin)


class EquipmentGeneralTypeAdmin(ModelAdmin):
    list_display = 'name',

    list_filter = 'name',

    show_full_result_count = False   # only a few, but skip counting anyway

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
        'data_type', \
        'nullable', \
        'lower_numeric_null', \
        'upper_numeric_null', \
        'default_val', \
        'name', \
        'min_val', \
        'max_val'

    list_select_related = \
        'equipment_general_type', \
        'equipment_data_field_type', \
        'data_type'

    show_full_result_count = False   # too many

    search_fields = \
        'equipment_general_type__name', \
        'equipment_data_field_type__name', \
        'name', \
        'data_type__name'

    form = EquipmentDataFieldForm


site.register(
    EquipmentDataField,
    admin_class=EquipmentDataFieldAdmin)


class EquipmentUniqueTypeGroupAdmin(ModelAdmin):
    list_display = 'equipment_general_type', 'name'

    list_filter = 'equipment_general_type',

    list_select_related = 'equipment_general_type',

    show_full_result_count = False   # only a few, but skip counting anyway

    search_fields = \
        'equipment_general_type__name', \
        'name'

    form = EquipmentUniqueTypeGroupForm


site.register(
    EquipmentUniqueTypeGroup,
    admin_class=EquipmentUniqueTypeGroupAdmin)


class EquipmentUniqueTypeAdmin(ModelAdmin):
    list_display = 'equipment_general_type', 'name'

    list_filter = 'equipment_general_type',

    list_select_related = 'equipment_general_type',

    show_full_result_count = False   # too many

    search_fields = \
        'equipment_general_type__name', \
        'name'

    form = EquipmentUniqueTypeForm


site.register(
    EquipmentUniqueType,
    admin_class=EquipmentUniqueTypeAdmin)


class EquipmentInstanceAdmin(ModelAdmin):
    list_display = 'equipment_general_type', 'equipment_unique_type', 'name'

    list_filter = 'equipment_general_type', 'equipment_unique_type'

    list_select_related = 'equipment_general_type', 'equipment_unique_type'

    show_full_result_count = False   # too many

    search_fields = \
        'equipment_general_type__name', \
        'equipment_unique_type__name', \
        'name'

    form = EquipmentInstanceForm


site.register(
    EquipmentInstance,
    admin_class=EquipmentInstanceAdmin)


class EquipmentInstanceAssociationAdmin(ModelAdmin):
    list_display = 'name', 'date'

    list_filter = 'name', 'date'

    show_full_result_count = False   # too many

    search_fields = 'name',

    form = EquipmentInstanceAssociationForm


site.register(
    EquipmentInstanceAssociation,
    admin_class=EquipmentInstanceAssociationAdmin)
