from django.contrib.admin import ModelAdmin, site, StackedInline, TabularInline

from .forms import \
    EquipmentDataFieldForm, \
    EquipmentUniqueTypeGroupForm, \
    EquipmentUniqueTypeForm, \
    EquipmentInstanceForm, \
    EquipmentEnsembleForm

from .models import \
    NumericMeasurementUnit, \
    EquipmentGeneralType, \
    EquipmentDataField, \
    EquipmentUniqueTypeGroup, \
    EquipmentUniqueType, \
    EquipmentFacility, \
    EquipmentInstance, \
    EquipmentEnsemble


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
        'numeric_measurement_unit', \
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
        'numeric_measurement_unit', \
        'lower_numeric_null', \
        'upper_numeric_null', \
        'default_val', \
        'name', \
        'min_val', \
        'max_val'

    list_select_related = \
        'equipment_general_type', \
        'equipment_data_field_type', \
        'data_type', \
        'numeric_measurement_unit'

    show_full_result_count = False   # too many

    search_fields = \
        'equipment_general_type__name', \
        'equipment_data_field_type__name', \
        'name', \
        'data_type__name', \
        'numeric_measurement_unit__name'

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


class EquipmentInstanceTabularInline(TabularInline):
    model = EquipmentInstance

    fields = \
        'equipment_general_type', \
        'equipment_unique_type', \
        'name'

    form = EquipmentInstanceForm


class EquipmentFacilityAdmin(ModelAdmin):
    list_display = 'name',

    list_filter = 'name',

    show_full_result_count = False   # too many

    search_fields = 'name',

    inlines = EquipmentInstanceTabularInline,


site.register(
    EquipmentFacility,
    admin_class=EquipmentFacilityAdmin)


class EquipmentInstanceAdmin(ModelAdmin):
    list_display = \
        'equipment_general_type', \
        'equipment_unique_type', \
        'equipment_facility', \
        'name'

    list_filter = \
        'equipment_general_type', \
        'equipment_unique_type', \
        'equipment_facility'

    list_select_related = \
        'equipment_general_type', \
        'equipment_unique_type', \
        'equipment_facility'

    show_full_result_count = False   # too many

    search_fields = \
        'equipment_general_type__name', \
        'equipment_unique_type__name', \
        'equipment_facility__name', \
        'name'

    form = EquipmentInstanceForm


site.register(
    EquipmentInstance,
    admin_class=EquipmentInstanceAdmin)


class EquipmentEnsembleAdmin(ModelAdmin):
    list_display = \
        'equipment_facility', \
        'name', \
        'date'

    list_filter = \
        'equipment_facility', \
        'name', \
        'date'

    list_select_related = 'equipment_facility',

    show_full_result_count = False   # too many

    search_fields = \
        'equipment_facility__name', \
        'name',

    form = EquipmentEnsembleForm


site.register(
    EquipmentEnsemble,
    admin_class=EquipmentEnsembleAdmin)
