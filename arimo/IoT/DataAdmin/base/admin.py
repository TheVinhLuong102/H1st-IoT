from django.contrib.admin import ModelAdmin, site, TabularInline
from django.db.models.aggregates import Count
from django.db.models.query import Prefetch
from django.forms import BaseInlineFormSet

from silk.profiling.profiler import silk_profile

from .forms import \
    EquipmentComponentForm, \
    EquipmentDataFieldForm, \
    EquipmentUniqueTypeGroupForm, \
    EquipmentUniqueTypeForm, \
    EquipmentInstanceForm, \
    EquipmentSystemForm

from .models import \
    GlobalConfig, \
    NumericMeasurementUnit, \
    EquipmentGeneralType, \
    EquipmentComponent, \
    EquipmentDataField, \
    EquipmentUniqueTypeGroup, \
    EquipmentUniqueType, \
    EquipmentFacility, \
    EquipmentInstance, \
    EquipmentInstanceDailyMetadata, \
    EquipmentInstanceDataFieldDailyAgg, \
    EquipmentSystem, \
    Error


class GlobalConfigAdmin(ModelAdmin):
    list_display = \
        'key', \
        'value'

    show_full_result_count = False

    @silk_profile(name='Admin: Global Configs')
    def changelist_view(self, *args, **kwargs):
        return super(type(self), self).changelist_view(*args, **kwargs)

    @silk_profile(name='Admin: Global Config')
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


class EquipmentComponentAdmin(ModelAdmin):
    list_display = \
        'equipment_general_type', \
        'name', \
        'description', \
        'equipment_data_field_list', \
        'n_equipment_unique_types', \
        'last_updated'

    list_filter = 'equipment_general_type__name',

    search_fields = \
        'equipment_general_type__name', \
        'name', \
        'description'

    show_full_result_count = False

    form = EquipmentComponentForm

    def equipment_data_field_list(self, obj):
        n = obj.equipment_data_fields.count()
        return '{}: {}'.format(
                n, '; '.join(str(equipment_data_field)
                             for equipment_data_field in obj.equipment_data_fields.all())) \
            if n \
          else ''

    def n_equipment_unique_types(self, obj):
        return obj.equipment_unique_types.count()

    def get_queryset(self, request):
        return super(type(self), self).get_queryset(request=request) \
                .select_related(
                    'equipment_general_type') \
                .prefetch_related(
                    Prefetch(
                        lookup='equipment_data_fields',
                        queryset=
                            EquipmentDataField.objects.only('id').order_by()
                            if request.resolver_match.url_name.endswith('_change')
                            else EquipmentDataField.objects
                                    .defer('description', 'last_updated')
                                    .select_related(
                                        'equipment_general_type',
                                        'equipment_data_field_type',
                                        'data_type',
                                        'numeric_measurement_unit')
                                    .defer(
                                        'numeric_measurement_unit__description')),
                    Prefetch(
                        lookup='equipment_unique_types',
                        queryset=EquipmentUniqueType.objects.only('id').order_by()))

    @silk_profile(name='Admin: Equipment Components')
    def changelist_view(self, *args, **kwargs):
        return super(type(self), self).changelist_view(*args, **kwargs)

    @silk_profile(name='Admin: Equipment Component')
    def changeform_view(self, *args, **kwargs):
        return super(type(self), self).changeform_view(*args, **kwargs)


site.register(
    EquipmentComponent,
    admin_class=EquipmentComponentAdmin)


class EquipmentDataFieldAdmin(ModelAdmin):
    list_display = \
        'equipment_general_type', \
        'equipment_component_list', \
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
        'n_equipment_unique_types', \
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

    search_fields = \
        'equipment_general_type__name', \
        'equipment_data_field_type__name', \
        'name', \
        'description', \
        'data_type__name', \
        'numeric_measurement_unit__name'

    show_full_result_count = False

    form = EquipmentDataFieldForm

    def equipment_component_list(self, obj):
        n = obj.equipment_components.count()
        return '{}: {}'.format(
                n, ', '.join(equipment_component.name
                             for equipment_component in obj.equipment_components.all())) \
            if n \
          else ''

    def n_equipment_unique_types(self, obj):
        return obj.equipment_unique_types.count()

    def get_queryset(self, request):
        return super(type(self), self).get_queryset(request=request) \
                .select_related(
                    'equipment_general_type',
                    'equipment_data_field_type',
                    'data_type',
                    'numeric_measurement_unit') \
                .defer(
                    'numeric_measurement_unit__description') \
                .prefetch_related(
                    Prefetch(
                        lookup='equipment_components',
                        queryset=
                            EquipmentComponent.objects.only('id').order_by()
                            if request.resolver_match.url_name.endswith('_change')
                            else EquipmentComponent.objects.only('name').order_by('name')),
                    Prefetch(
                        lookup='equipment_unique_types',
                        queryset=EquipmentUniqueType.objects.only('id').order_by()))

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
        'equipment_unique_type_list', \
        'equipment_component_list', \
        'n_equipment_data_fields', \
        'n_equipment_instances', \
        'last_updated'

    list_filter = 'equipment_general_type__name',

    search_fields = \
        'equipment_general_type__name', \
        'name', \
        'description'

    show_full_result_count = False

    form = EquipmentUniqueTypeGroupForm

    readonly_fields = \
        'equipment_components', \
        'equipment_data_fields',

    def equipment_unique_type_list(self, obj):
        n = obj.equipment_unique_types.count()
        return '{}: {}'.format(
                n, ', '.join(equipment_unique_type.name
                             for equipment_unique_type in obj.equipment_unique_types.all())) \
            if n \
          else ''

    def equipment_component_list(self, obj):
        n = obj.equipment_components.count()
        return '{}: {}'.format(
                n, ', '.join(equipment_component.name
                             for equipment_component in obj.equipment_components.all())) \
            if n \
          else ''

    def n_equipment_data_fields(self, obj):
        return obj.equipment_data_fields.count()

    def n_equipment_instances(self, obj):
        return sum(equipment_unique_type.equipment_instances.count()
                   for equipment_unique_type in obj.equipment_unique_types.all()) \
            if obj.equipment_unique_types.count() \
          else ''

    def get_queryset(self, request):
        query_set = \
            super(type(self), self).get_queryset(request=request) \
            .select_related(
                'equipment_general_type')

        return query_set \
                .prefetch_related(
                    Prefetch(
                        lookup='equipment_unique_types',
                        queryset=EquipmentUniqueType.objects.only('id').order_by()),
                    Prefetch(
                        lookup='equipment_components',
                        queryset=
                            EquipmentComponent.objects
                            .defer('description', 'last_updated')
                            .select_related(
                                'equipment_general_type')),
                    Prefetch(
                        lookup='equipment_data_fields',
                        queryset=
                            EquipmentDataField.objects
                            .select_related(
                                'equipment_general_type',
                                'equipment_data_field_type',
                                'data_type',
                                'numeric_measurement_unit')
                            .defer(
                                'numeric_measurement_unit__description'))) \
            if request.resolver_match.url_name.endswith('_change') \
          else query_set \
                .prefetch_related(
                    Prefetch(
                        lookup='equipment_unique_types',
                        queryset=
                            EquipmentUniqueType.objects
                            .defer('description', 'last_updated')
                            .order_by('name')
                            .prefetch_related(
                                Prefetch(
                                    lookup='equipment_instances',
                                    queryset=EquipmentInstance.objects.only('id', 'equipment_unique_type').order_by()))),
                    Prefetch(
                        lookup='equipment_components',
                        queryset=EquipmentComponent.objects.only('name').order_by('name')),
                    Prefetch(
                        lookup='equipment_data_fields',
                        queryset=EquipmentDataField.objects.only('id').order_by()))

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
        'equipment_component_list', \
        'n_equipment_data_fields', \
        'equipment_unique_type_group_list', \
        'n_equipment_instances', \
        'last_updated'

    list_filter = 'equipment_general_type__name',

    show_full_result_count = False

    search_fields = \
        'equipment_general_type__name', \
        'name', \
        'description'

    form = EquipmentUniqueTypeForm

    def equipment_component_list(self, obj):
        n = obj.equipment_components.count()
        return '{}: {}'.format(
                n, ', '.join(equipment_component.name
                             for equipment_component in obj.equipment_components.all())) \
            if n \
          else ''

    def n_equipment_data_fields(self, obj):
        return obj.equipment_data_fields.count()

    def n_equipment_instances(self, obj):
        return obj.equipment_instances.count()

    def equipment_unique_type_group_list(self, obj):
        n = obj.equipment_unique_type_groups.count()
        return '{}: {}'.format(
                n, ', '.join(equipment_unique_type_group.name
                             for equipment_unique_type_group in obj.equipment_unique_type_groups.all())) \
            if n \
          else ''

    def get_queryset(self, request):
        query_set = \
            super(type(self), self).get_queryset(request=request) \
            .select_related(
                'equipment_general_type') \
            .prefetch_related(
                Prefetch(
                    lookup='equipment_data_fields',
                    queryset=EquipmentDataField.objects.only('id').order_by()))

        return query_set \
                .prefetch_related(
                    Prefetch(
                        lookup='equipment_components',
                        queryset=EquipmentComponent.objects.only('id').order_by()),
                    Prefetch(
                        lookup='equipment_unique_type_groups',
                        queryset=EquipmentUniqueTypeGroup.objects.only('id').order_by())) \
            if request.resolver_match.url_name.endswith('_change') \
          else query_set \
                .prefetch_related(
                    Prefetch(
                        lookup='equipment_components',
                        queryset=EquipmentComponent.objects.only('name').order_by('name')),
                    Prefetch(
                        lookup='equipment_instances',
                        queryset=EquipmentInstance.objects.only('id', 'equipment_unique_type').order_by()),
                    Prefetch(
                        lookup='equipment_unique_type_groups',
                        queryset=
                            EquipmentUniqueTypeGroup.objects.only('name').order_by('name')))

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
    #     return super(type(self), self).get_queryset() \
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

    search_fields = \
        'name', \
        'info'

    show_full_result_count = False

    # inlines = EquipmentInstanceTabularInline,

    def n_equipment_instances(self, obj):
        return obj.equipment_instances.count()

    def get_queryset(self, request):
        query_set = super(type(self), self).get_queryset(request=request)

        return query_set \
            if request.resolver_match.url_name.endswith('_change') \
          else query_set \
                .prefetch_related(
                    Prefetch(
                        lookup='equipment_instances',
                        queryset=EquipmentInstance.objects.only('id', 'equipment_facility').order_by()))

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

    search_fields = \
        'equipment_general_type__name', \
        'equipment_unique_type__name', \
        'equipment_facility__name', \
        'name', \
        'info'

    show_full_result_count = False

    form = EquipmentInstanceForm

    def get_queryset(self, request):
        query_set = super(type(self), self).get_queryset(request=request)

        return query_set \
                .select_related(
                    'equipment_general_type',
                    'equipment_unique_type') \
                .defer(
                    'equipment_unique_type__description', 'equipment_unique_type__last_updated') \
            if request.resolver_match.url_name.endswith('_change') \
          else query_set \
                .select_related(
                    'equipment_general_type',
                    'equipment_unique_type', 'equipment_unique_type__equipment_general_type',
                    'equipment_facility') \
                .defer(
                    'equipment_unique_type__description', 'equipment_unique_type__last_updated',
                    'equipment_facility__info', 'equipment_facility__last_updated')

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
        'equipment_instance__equipment_unique_type__name', \
        'date'

    search_fields = \
        'equipment_instance__equipment_general_type__name', \
        'equipment_instance__equipment_unique_type__name', \
        'equipment_instance__name'

    show_full_result_count = False

    readonly_fields = \
        'equipment_instance', \
        'date', \
        'url', \
        'schema', \
        'n_columns', \
        'n_rows'

    def get_queryset(self, request):
        return super(type(self), self).get_queryset(request=request) \
                .defer('schema') \
                .select_related(
                    'equipment_instance',
                    'equipment_instance__equipment_general_type', 'equipment_instance__equipment_unique_type')

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

    search_fields = \
        'equipment_instance__name', \
        'equipment_data_field__name'

    show_full_result_count = False

    list_select_related = \
        'equipment_instance', 'equipment_instance__equipment_general_type', 'equipment_instance__equipment_unique_type', \
        'equipment_data_field', 'equipment_data_field__equipment_general_type', 'equipment_data_field__equipment_data_field_type', \
                                'equipment_data_field__data_type', 'equipment_data_field__numeric_measurement_unit'

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
        'date'

    search_fields = \
        'equipment_facility__name', \
        'name',

    show_full_result_count = False

    form = EquipmentSystemForm

    def n_equipment_instances(self, obj):
        return obj.equipment_instances.count()

    def get_queryset(self, request):
        return super(type(self), self).get_queryset(request=request) \
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


class ErrorAdmin(ModelAdmin):
    list_display = \
        'key', \
        'value', \
        'last_updated'

    search_fields = \
        'key', \
        'value'

    show_full_result_count = False

    readonly_fields = \
        'key', \
        'value'

    @silk_profile(name='Admin: Errors')
    def changelist_view(self, *args, **kwargs):
        return super(type(self), self).changelist_view(*args, **kwargs)

    @silk_profile(name='Admin: Error')
    def changeform_view(self, *args, **kwargs):
        return super(type(self), self).changeform_view(*args, **kwargs)


site.register(
    Error,
    admin_class=ErrorAdmin)
