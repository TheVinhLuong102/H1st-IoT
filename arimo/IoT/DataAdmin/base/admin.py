from django.contrib.admin import ModelAdmin, site, TabularInline

from silk.profiling.profiler import silk_profile

from .forms import \
    EquipmentDataFieldForm, \
    EquipmentUniqueTypeGroupForm, \
    EquipmentUniqueTypeForm, \
    EquipmentInstanceForm, \
    EquipmentSystemForm

from .models import \
    NumericMeasurementUnit, \
    EquipmentGeneralType, \
    EquipmentDataField, \
    EquipmentUniqueTypeGroup, \
    EquipmentUniqueType, \
    EquipmentFacility, \
    EquipmentInstance, \
    EquipmentSystem


class NumericMeasurementUnitAdmin(ModelAdmin):
    list_display = 'name',

    list_filter = 'name',

    show_full_result_count = False   # only a few, but skip counting anyway

    search_fields = 'name',

    @silk_profile(name='Admin: Numeric Measurement Units')
    def changelist_view(self, request, extra_context=None):
        return super(NumericMeasurementUnitAdmin, self).changelist_view(
                request=request,
                extra_context=extra_context)

    @silk_profile(name='Admin: Numeric Measurement Unit')
    def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
        return super(NumericMeasurementUnitAdmin, self).changelist_view(
                request=request,
                object_id=object_id,
                form_url=form_url,
                extra_context=extra_context)


site.register(
    NumericMeasurementUnit,
    admin_class=NumericMeasurementUnitAdmin)


class EquipmentGeneralTypeAdmin(ModelAdmin):
    list_display = 'name',

    list_filter = 'name',

    show_full_result_count = False   # only a few, but skip counting anyway

    search_fields = 'name',

    @silk_profile(name='Admin: Equipment General Types')
    def changelist_view(self, request, extra_context=None):
        return super(EquipmentGeneralTypeAdmin, self).changelist_view(
                request=request,
                extra_context=extra_context)

    @silk_profile(name='Admin: Equipment General Type')
    def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
        return super(EquipmentGeneralTypeAdmin, self).changelist_view(
                request=request,
                object_id=object_id,
                form_url=form_url,
                extra_context=extra_context)


site.register(
    EquipmentGeneralType,
    admin_class=EquipmentGeneralTypeAdmin)


class EquipmentDataFieldAdmin(ModelAdmin):
    list_display = \
        'equipment_general_type', \
        'equipment_data_field_type', \
        'name', \
        'data_type', \
        'numeric_measurement_unit', \
        'lower_numeric_null', \
        'upper_numeric_null', \
        'default_val', \
        'min_val', \
        'max_val', \
        'last_updated'

    list_filter = \
        'equipment_general_type', \
        'equipment_data_field_type', \
        'data_type', \
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

    @silk_profile(name='Admin: Equipment Data Fields')
    def changelist_view(self, request, extra_context=None):
        return super(EquipmentDataFieldAdmin, self).changelist_view(
                request=request,
                extra_context=extra_context)

    @silk_profile(name='Admin: Equipment Data Field')
    def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
        return super(EquipmentDataFieldAdmin, self).changelist_view(
                request=request,
                object_id=object_id,
                form_url=form_url,
                extra_context=extra_context)


site.register(
    EquipmentDataField,
    admin_class=EquipmentDataFieldAdmin)


class EquipmentUniqueTypeGroupAdmin(ModelAdmin):
    list_display = \
        'equipment_general_type', \
        'name', \
        'last_updated'

    list_filter = 'equipment_general_type',

    list_select_related = 'equipment_general_type',

    show_full_result_count = False   # only a few, but skip counting anyway

    search_fields = \
        'equipment_general_type__name', \
        'name'

    form = EquipmentUniqueTypeGroupForm

    readonly_fields = 'equipment_data_fields',   # *** UGLY READ-ONLY DISPLAY ***

    @silk_profile(name='Admin: Equipment Unique Type Groups')
    def changelist_view(self, request, extra_context=None):
        return super(EquipmentUniqueTypeGroupAdmin, self).changelist_view(
                request=request,
                extra_context=extra_context)

    @silk_profile(name='Admin: Equipment Unique Type Group')
    def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
        return super(EquipmentUniqueTypeGroupAdmin, self).changelist_view(
                request=request,
                object_id=object_id,
                form_url=form_url,
                extra_context=extra_context)


site.register(
    EquipmentUniqueTypeGroup,
    admin_class=EquipmentUniqueTypeGroupAdmin)


class EquipmentUniqueTypeAdmin(ModelAdmin):
    list_display = \
        'equipment_general_type', \
        'name', \
        'last_updated'

    list_filter = 'equipment_general_type',

    list_select_related = 'equipment_general_type',

    show_full_result_count = False   # too many

    search_fields = \
        'equipment_general_type__name', \
        'name'

    form = EquipmentUniqueTypeForm

    @silk_profile(name='Admin: Equipment Unique Types')
    def changelist_view(self, request, extra_context=None):
        return super(EquipmentUniqueTypeAdmin, self).changelist_view(
                request=request,
                extra_context=extra_context)

    @silk_profile(name='Admin: Equipment Unique Type')
    def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
        return super(EquipmentUniqueTypeAdmin, self).changelist_view(
                request=request,
                object_id=object_id,
                form_url=form_url,
                extra_context=extra_context)


site.register(
    EquipmentUniqueType,
    admin_class=EquipmentUniqueTypeAdmin)


class EquipmentInstanceTabularInline(TabularInline):
    model = EquipmentInstance

    fields = \
        'equipment_general_type', \
        'equipment_unique_type', \
        'name'
        # 'last_updated' cannot be specified for EquipmentInstance model form as it is a non-editable field

    form = EquipmentInstanceForm

    extra = 0


class EquipmentFacilityAdmin(ModelAdmin):
    list_display = \
        'name', \
        'last_updated'

    list_filter = 'name',

    show_full_result_count = False   # too many

    search_fields = 'name',

    inlines = EquipmentInstanceTabularInline,

    @silk_profile(name='Admin: Equipment Facilities')
    def changelist_view(self, request, extra_context=None):
        return super(EquipmentFacilityAdmin, self).changelist_view(
                request=request,
                extra_context=extra_context)

    @silk_profile(name='Admin: Equipment Facility')
    def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
        return super(EquipmentFacilityAdmin, self).changelist_view(
                request=request,
                object_id=object_id,
                form_url=form_url,
                extra_context=extra_context)


site.register(
    EquipmentFacility,
    admin_class=EquipmentFacilityAdmin)


class EquipmentInstanceAdmin(ModelAdmin):
    list_display = \
        'equipment_general_type', \
        'equipment_unique_type', \
        'equipment_facility', \
        'name', \
        'last_updated'

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

    @silk_profile(name='Admin: Equipment Instances')
    def changelist_view(self, request, extra_context=None):
        return super(EquipmentInstanceAdmin, self).changelist_view(
                request=request,
                extra_context=extra_context)

    @silk_profile(name='Admin: Equipment Instance')
    def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
        return super(EquipmentInstanceAdmin, self).changelist_view(
                request=request,
                object_id=object_id,
                form_url=form_url,
                extra_context=extra_context)


site.register(
    EquipmentInstance,
    admin_class=EquipmentInstanceAdmin)


class EquipmentSystemAdmin(ModelAdmin):
    list_display = \
        'equipment_facility', \
        'name', \
        'date', \
        'last_updated'

    list_filter = \
        'equipment_facility', \
        'name', \
        'date'

    list_select_related = 'equipment_facility',

    show_full_result_count = False   # too many

    search_fields = \
        'equipment_facility__name', \
        'name',

    form = EquipmentSystemForm

    @silk_profile(name='Admin: Equipment Systems')
    def changelist_view(self, request, extra_context=None):
        return super(EquipmentSystemAdmin, self).changelist_view(
                request=request,
                extra_context=extra_context)

    @silk_profile(name='Admin: Equipment System')
    def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
        return super(EquipmentSystemAdmin, self).changelist_view(
                request=request,
                object_id=object_id,
                form_url=form_url,
                extra_context=extra_context)


site.register(
    EquipmentSystem,
    admin_class=EquipmentSystemAdmin)
