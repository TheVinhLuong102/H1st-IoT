from django.contrib.admin import ModelAdmin, site, TabularInline
from django.db.models.aggregates import Count
from django.db.models.query import Prefetch
from django.forms import BaseInlineFormSet

from silk.profiling.profiler import silk_profile

from .forms import \
    EquipmentUniqueTypeGroupForm, \
    EquipmentUniqueTypeForm, \
    EquipmentInstanceForm, \
    EquipmentSystemForm

from .models import \
    GlobalConfig, \
    NumericMeasurementUnit, \
    EquipmentGeneralType, \
    EquipmentDataField, \
    EquipmentUniqueTypeGroup, \
    EquipmentUniqueType, \
    EquipmentFacility, \
    EquipmentInstance, \
    EquipmentInstanceDailyMetadata, \
    EquipmentInstanceDataFieldDailyAgg, \
    EquipmentSystem


class GlobalConfigAdmin(ModelAdmin):
    list_display = \
        'key', \
        'value', \
        'last_updated'

    show_full_result_count = False

    @silk_profile(name='ADMIN: Global Configs')
    def changelist_view(self, *args, **kwargs):
        return super(type(self), self).changelist_view(*args, **kwargs)

    @silk_profile(name='ADMIN: Global Config')
    def changeform_view(self, *args, **kwargs):
        return super(type(self), self).changeform_view(*args, **kwargs)


site.register(
    GlobalConfig,
    admin_class=GlobalConfigAdmin)


class NumericMeasurementUnitAdmin(ModelAdmin):
    list_display = \
        'name', \
        'description'

    show_full_result_count = False

    @silk_profile(name='Admin: Numeric Measurement Units')
    def changelist_view(self, *args, **kwargs):
        return super(type(self), self).changelist_view(*args, **kwargs)

    @silk_profile(name='Admin: Numeric Measurement Unit')
    def changeform_view(self, *args, **kwargs):
        return super(type(self), self).changeform_view(*args, **kwargs)


site.register(
    NumericMeasurementUnit,
    admin_class=NumericMeasurementUnitAdmin)


class EquipmentGeneralTypeAdmin(ModelAdmin):
    list_display = 'name',

    show_full_result_count = False

    @silk_profile(name='Admin: Equipment General Types')
    def changelist_view(self, *args, **kwargs):
        return super(type(self), self).changelist_view(*args, **kwargs)

    @silk_profile(name='Admin: Equipment General Type')
    def changeform_view(self, *args, **kwargs):
        return super(type(self), self).changeform_view(*args, **kwargs)


site.register(
    EquipmentGeneralType,
    admin_class=EquipmentGeneralTypeAdmin)


class EquipmentDataFieldAdmin(ModelAdmin):
    list_display = \
        'equipment_general_type', \
        'name', \
        'description', \
        'equipment_data_field_type', \
        'data_type', \
        'numeric_measurement_unit', \
        'lower_numeric_null', \
        'upper_numeric_null', \
        'default_val', \
        'min_val', \
        'max_val', \
        'last_updated'

    list_filter = \
        'equipment_general_type__name', \
        'equipment_data_field_type__name', \
        'data_type__name', \
        'numeric_measurement_unit__name', \
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

    show_full_result_count = False

    search_fields = \
        'equipment_general_type__name', \
        'equipment_data_field_type__name', \
        'name', \
        'data_type__name', \
        'numeric_measurement_unit__name'

    readonly_fields = \
        'equipment_unique_types',

    @silk_profile(name='Admin: Equipment Data Fields')
    def changelist_view(self, *args, **kwargs):
        return super(type(self), self).changelist_view(*args, **kwargs)

    @silk_profile(name='Admin: Equipment Data Field')
    def changeform_view(self, *args, **kwargs):
        return super(type(self), self).changeform_view(*args, **kwargs)


site.register(
    EquipmentDataField,
    admin_class=EquipmentDataFieldAdmin)


class EquipmentUniqueTypeGroupAdmin(ModelAdmin):
    list_display = \
        'equipment_general_type', \
        'name', \
        'description', \
        'equipment_unique_type_names', \
        'n_equipment_data_fields', \
        'n_equipment_instances', \
        'last_updated'

    list_filter = 'equipment_general_type__name',

    show_full_result_count = False

    search_fields = \
        'equipment_general_type__name', \
        'name'

    form = EquipmentUniqueTypeGroupForm

    readonly_fields = 'equipment_data_fields',

    def equipment_unique_type_names(self, obj):
        return ', '.join(equipment_unique_type.name
                         for equipment_unique_type in obj.equipment_unique_types.all())

    def n_equipment_data_fields(self, obj):
        return obj.equipment_data_fields.count()

    def n_equipment_instances(self, obj):
        return sum(i['n_equipment_instances']
                   for i in obj.equipment_unique_types.annotate(n_equipment_instances=Count('equipment_instance')).values('n_equipment_instances')) \
            if obj.equipment_unique_types.count() \
          else 0

    def get_queryset(self, request):
        return super(type(self), self).get_queryset(request=request) \
                .select_related(
                    'equipment_general_type') \
                .prefetch_related(
                    'equipment_unique_types',
                    Prefetch(
                        lookup='equipment_data_fields',
                        queryset=
                            EquipmentDataField.objects
                            .select_related(
                                'equipment_general_type',
                                'equipment_data_field_type',
                                'data_type',
                                'numeric_measurement_unit')))

    @silk_profile(name='Admin: Equipment Unique Type Groups')
    def changelist_view(self, *args, **kwargs):
        return super(type(self), self).changelist_view(*args, **kwargs)

    @silk_profile(name='Admin: Equipment Unique Type Group')
    def changeform_view(self, *args, **kwargs):
        return super(type(self), self).changeform_view(*args, **kwargs)


site.register(
    EquipmentUniqueTypeGroup,
    admin_class=EquipmentUniqueTypeGroupAdmin)


class EquipmentUniqueTypeAdmin(ModelAdmin):
    list_display = \
        'equipment_general_type', \
        'name', \
        'description', \
        'n_equipment_data_fields', \
        'n_equipment_instances', \
        'equipment_unique_type_groups', \
        'last_updated'

    list_filter = 'equipment_general_type__name',

    show_full_result_count = False

    search_fields = \
        'equipment_general_type__name', \
        'name'

    form = EquipmentUniqueTypeForm

    readonly_fields = \
        'groups',

    def n_equipment_data_fields(self, obj):
        return obj.data_fields.count()

    def n_equipment_instances(self, obj):
        return obj.equipment_instances.count()

    def equipment_unique_type_groups(self, obj):
        return ', '.join(equipment_unique_type_group.name
                         for equipment_unique_type_group in obj.groups.all())

    def get_queryset(self, request):
        return super(type(self), self).get_queryset(request=request) \
                .select_related(
                    'equipment_general_type') \
                .prefetch_related(
                    'data_fields',
                    'equipment_instances',
                    'groups')

    @silk_profile(name='Admin: Equipment Unique Types')
    def changelist_view(self, *args, **kwargs):
        return super(type(self), self).changelist_view(*args, **kwargs)

    @silk_profile(name='Admin: Equipment Unique Type')
    def changeform_view(self, *args, **kwargs):
        return super(type(self), self).changeform_view(*args, **kwargs)


site.register(
    EquipmentUniqueType,
    admin_class=EquipmentUniqueTypeAdmin)


class EquipmentInstanceInLineFormSet(BaseInlineFormSet):
    model = EquipmentInstance

    # def get_queryset(self):
    #     return super(EquipmentInstanceInLineFormSet, self).get_queryset() \
    #         .select_related(
    #             'equipment_general_type',
    #             'equipment_unique_type', 'equipment_unique_type__equipment_general_type')


class EquipmentInstanceTabularInline(TabularInline):
    model = EquipmentInstance

    fields = \
        'equipment_general_type', \
        'equipment_unique_type', \
        'name'
        # 'last_updated' cannot be specified for EquipmentInstance model form as it is a non-editable field

    form = EquipmentInstanceForm

    formset = EquipmentInstanceInLineFormSet

    extra = 0

    def get_queryset(self, request):
        return super(type(self), self).get_queryset(request=request) \
                .select_related(
                    'equipment_general_type',
                    'equipment_unique_type', 'equipment_unique_type__equipment_general_type')


class EquipmentFacilityAdmin(ModelAdmin):
    list_display = \
        'name', \
        'info', \
        'n_equipment_instances', \
        'last_updated'

    show_full_result_count = False

    search_fields = 'name',

    inlines = EquipmentInstanceTabularInline,

    def n_equipment_instances(self, obj):
        return obj.equipment_instances.count()

    def get_queryset(self, request):
        return super(type(self), self).get_queryset(request=request) \
                .prefetch_related(
                    'equipment_instances')

    @silk_profile(name='Admin: Equipment Facilities')
    def changelist_view(self, *args, **kwargs):
        return super(type(self), self).changelist_view(*args, **kwargs)

    @silk_profile(name='Admin: Equipment Facility')
    def changeform_view(self, *args, **kwargs):
        return super(type(self), self).changeform_view(*args, **kwargs)


site.register(
    EquipmentFacility,
    admin_class=EquipmentFacilityAdmin)


class EquipmentInstanceAdmin(ModelAdmin):
    list_display = \
        'equipment_general_type', \
        'equipment_unique_type', \
        'equipment_facility', \
        'name', \
        'info', \
        'last_updated'

    list_filter = \
        'equipment_general_type__name', \
        'equipment_unique_type__name', \
        'equipment_facility__name'

    list_select_related = \
        'equipment_general_type', \
        'equipment_unique_type', 'equipment_unique_type__equipment_general_type', \
        'equipment_facility'

    show_full_result_count = False

    search_fields = \
        'equipment_general_type__name', \
        'equipment_unique_type__name', \
        'equipment_facility__name', \
        'name'

    form = EquipmentInstanceForm

    @silk_profile(name='Admin: Equipment Instances')
    def changelist_view(self, *args, **kwargs):
        return super(type(self), self).changelist_view(*args, **kwargs)

    @silk_profile(name='Admin: Equipment Instance')
    def changeform_view(self, *args, **kwargs):
        return super(type(self), self).changeform_view(*args, **kwargs)


site.register(
    EquipmentInstance,
    admin_class=EquipmentInstanceAdmin)


class EquipmentInstanceDailyMetadataAdmin(ModelAdmin):
    list_display = \
        'equipment_instance', \
        'date', \
        'url', \
        'n_columns', \
        'n_rows', \
        'last_updated'

    list_filter = \
        'equipment_instance__equipment_general_type__name', \
        'equipment_instance__equipment_unique_type__name'

    list_select_related = \
        'equipment_instance', \
        'equipment_instance__equipment_general_type', \
        'equipment_instance__equipment_unique_type'

    show_full_result_count = False

    search_fields = \
        'equipment_instance__equipment_general_type__name', \
        'equipment_instance__equipment_unique_type__name', \
        'equipment_instance__name'

    readonly_fields = \
        'equipment_instance', \
        'date', \
        'url', \
        'schema', \
        'n_columns', \
        'n_rows'

    @silk_profile(name='Admin: Equipment Instances Daily Metadata')
    def changelist_view(self, *args, **kwargs):
        return super(type(self), self).changelist_view(*args, **kwargs)

    @silk_profile(name='Admin: Equipment Instance Daily Metadata')
    def changeform_view(self, *args, **kwargs):
        return super(type(self), self).changeform_view(*args, **kwargs)


site.register(
    EquipmentInstanceDailyMetadata,
    admin_class=EquipmentInstanceDailyMetadataAdmin)


class EquipmentInstanceDataFieldDailyAggAdmin(ModelAdmin):
    list_display = \
        'equipment_instance', \
        'equipment_data_field', \
        'date', \
        'daily_count', \
        'daily_distinct_value_counts', \
        'daily_min', \
        'daily_outlier_rst_min', \
        'daily_quartile', \
        'daily_median', \
        'daily_mean', \
        'daily_3rd_quartile', \
        'daily_outlier_rst_max', \
        'daily_max', \
        'last_updated'

    list_select_related = \
        'equipment_instance', 'equipment_instance__equipment_general_type', 'equipment_instance__equipment_unique_type', \
        'equipment_data_field', 'equipment_data_field__equipment_general_type', 'equipment_data_field__equipment_data_field_type', \
                                'equipment_data_field__data_type', 'equipment_data_field__numeric_measurement_unit'

    show_full_result_count = False

    search_fields = \
        'equipment_instance__name', \
        'equipment_data_field__name'

    readonly_fields = \
        'equipment_instance', \
        'equipment_data_field', \
        'date', \
        'daily_count', \
        'daily_distinct_value_counts', \
        'daily_min', \
        'daily_outlier_rst_min', \
        'daily_quartile', \
        'daily_median', \
        'daily_mean', \
        'daily_3rd_quartile', \
        'daily_outlier_rst_max', \
        'daily_max'

    @silk_profile(name='Admin: Equipment Instance Data Field Daily Aggregates')
    def changelist_view(self, *args, **kwargs):
        return super(type(self), self).changelist_view(*args, **kwargs)

    @silk_profile(name='Admin: Equipment Instance Data Field Daily Aggregate')
    def changeform_view(self, *args, **kwargs):
        return super(type(self), self).changeform_view(*args, **kwargs)


site.register(
    EquipmentInstanceDataFieldDailyAgg,
    admin_class=EquipmentInstanceDataFieldDailyAggAdmin)


class EquipmentSystemAdmin(ModelAdmin):
    list_display = \
        'equipment_facility', \
        'name', \
        'date', \
        'n_equipment_instances', \
        'last_updated'

    list_filter = \
        'equipment_facility__name', \
        'name', \
        'date'

    show_full_result_count = False

    search_fields = \
        'equipment_facility__name', \
        'name',

    form = EquipmentSystemForm

    def n_equipment_instances(self, obj):
        return obj.equipment_instances.count()

    def get_queryset(self, request):
        return super(EquipmentSystemAdmin, self).get_queryset(request=request) \
            .select_related(
                'equipment_facility') \
            .prefetch_related(
                'equipment_instances')

    @silk_profile(name='Admin: Equipment Systems')
    def changelist_view(self, *args, **kwargs):
        return super(type(self), self).changelist_view(*args, **kwargs)

    @silk_profile(name='Admin: Equipment System')
    def changeform_view(self, *args, **kwargs):
        return super(type(self), self).changeform_view(*args, **kwargs)


site.register(
    EquipmentSystem,
    admin_class=EquipmentSystemAdmin)
