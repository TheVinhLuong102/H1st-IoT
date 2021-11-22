"""H1st IoT Data Management (Base) Admin."""


from django.contrib.admin import ModelAdmin, site, TabularInline
from django.db.models.query import Prefetch
from django.forms import BaseInlineFormSet

from silk.profiling.profiler import silk_profile

from h1st_iot.data_mgmt.base.models import (
    GlobalConfig,
    NumericMeasurementUnit,
    EquipmentGeneralType,
    EquipmentDataField,
    EquipmentUniqueTypeGroup,
    EquipmentUniqueType,
    EquipmentFacility,
    EquipmentInstance,
    EquipmentSystem,
    EquipmentUniqueTypeGroupDataFieldProfile,
    EquipmentUniqueTypeGroupDataFieldPairwiseCorrelation,
)
from h1st_iot.data_mgmt.base.query_sets import (
    EQUIPMENT_DATA_FIELD_ID_ONLY_UNORDERED_QUERY_SET,
    EQUIPMENT_DATA_FIELD_STR_QUERY_SET,
    EQUIPMENT_UNIQUE_TYPE_GROUP_ID_ONLY_UNORDERED_QUERY_SET,
    EQUIPMENT_UNIQUE_TYPE_GROUP_NAME_ONLY_QUERY_SET,
    EQUIPMENT_UNIQUE_TYPE_ID_ONLY_UNORDERED_QUERY_SET,
    EQUIPMENT_UNIQUE_TYPE_NAME_ONLY_QUERY_SET,
    EQUIPMENT_INSTANCE_ID_ONLY_UNORDERED_QUERY_SET,
    EQUIPMENT_INSTANCE_RELATED_TO_EQUIPMENT_UNIQUE_TYPE_ID_ONLY_UNORDERED_QUERY_SET,   # noqa: E501
    EQUIPMENT_INSTANCE_RELATED_TO_EQUIPMENT_FACILITY_ID_ONLY_UNORDERED_QUERY_SET,   # noqa: E501
)


class GlobalConfigAdmin(ModelAdmin):
    """GlobalConfigAdmin."""

    list_display = 'key', 'value'

    show_full_result_count = False

    @silk_profile(name='Admin: Global Configs')
    def changelist_view(self, *args, **kwargs):
        return super().changelist_view(*args, **kwargs)

    @silk_profile(name='Admin: Global Config')
    def changeform_view(self, *args, **kwargs):
        return super().changeform_view(*args, **kwargs)


site.register(GlobalConfig, admin_class=GlobalConfigAdmin)


class NumericMeasurementUnitAdmin(ModelAdmin):
    """NumericMeasurementUnitAdmin."""

    list_display = ('name',)

    show_full_result_count = False

    @silk_profile(name='Admin: Numeric Measurement Units')
    def changelist_view(self, *args, **kwargs):
        return super().changelist_view(*args, **kwargs)

    @silk_profile(name='Admin: Numeric Measurement Unit')
    def changeform_view(self, *args, **kwargs):
        return super().changeform_view(*args, **kwargs)


site.register(NumericMeasurementUnit, admin_class=NumericMeasurementUnitAdmin)


class EquipmentGeneralTypeAdmin(ModelAdmin):
    """EquipmentGeneralTypeAdmin."""

    list_display = ('name',)

    show_full_result_count = False

    @silk_profile(name='Admin: Equipment General Types')
    def changelist_view(self, *args, **kwargs):
        return super().changelist_view(*args, **kwargs)

    @silk_profile(name='Admin: Equipment General Type')
    def changeform_view(self, *args, **kwargs):
        return super().changeform_view(*args, **kwargs)


site.register(EquipmentGeneralType, admin_class=EquipmentGeneralTypeAdmin)


class EquipmentDataFieldAdmin(ModelAdmin):
    """EquipmentDataFieldAdmin."""

    list_display = \
        'equipment_general_type', \
        'name', \
        'equipment_data_field_type', \
        'data_type', \
        'numeric_measurement_unit', \
        'lower_numeric_null', \
        'upper_numeric_null', \
        'min_val', \
        'max_val', \
        'n_equipment_unique_types'

    list_filter = \
        'equipment_general_type__name', \
        'equipment_data_field_type__name', \
        'data_type__name', \
        'numeric_measurement_unit__name', \
        'lower_numeric_null', \
        'upper_numeric_null', \
        'name', \
        'min_val', \
        'max_val'

    search_fields = \
        'equipment_general_type__name', \
        'equipment_data_field_type__name', \
        'name', \
        'data_type__name', \
        'numeric_measurement_unit__name'

    show_full_result_count = False

    # form = EquipmentDataFieldForm

    def n_equipment_unique_types(self, obj):
        return obj.equipment_unique_types.count()

    def get_queryset(self, request):
        return super().get_queryset(request=request) \
                .select_related(
                    'equipment_general_type',
                    'equipment_data_field_type',
                    'data_type',
                    'numeric_measurement_unit') \
                .prefetch_related(
                    Prefetch(
                        lookup='equipment_unique_types',
                        queryset=EQUIPMENT_UNIQUE_TYPE_ID_ONLY_UNORDERED_QUERY_SET))

    @silk_profile(name='Admin: Equipment Data Fields')
    def changelist_view(self, *args, **kwargs):
        return super().changelist_view(*args, **kwargs)

    @silk_profile(name='Admin: Equipment Data Field')
    def changeform_view(self, *args, **kwargs):
        return super().changeform_view(*args, **kwargs)


site.register(EquipmentDataField, admin_class=EquipmentDataFieldAdmin)


class EquipmentUniqueTypeGroupAdmin(ModelAdmin):
    """EquipmentUniqueTypeGroupAdmin."""

    list_display = \
        'equipment_general_type', \
        'name', \
        'equipment_unique_type_list', \
        'n_equipment_data_fields', \
        'n_equipment_instances'

    list_filter = 'equipment_general_type__name',

    search_fields = 'equipment_general_type__name', 'name',

    show_full_result_count = False

    # form = EquipmentUniqueTypeGroupForm

    readonly_fields = ('equipment_data_fields',)

    def equipment_unique_type_list(self, obj):
        n = obj.equipment_unique_types.count()
        return '{}: {}'.format(
                n, ', '.join(equipment_unique_type.name
                             for equipment_unique_type in obj.equipment_unique_types.all())) \
            if n \
          else ''

    def n_equipment_data_fields(self, obj):
        return obj.equipment_data_fields.count()

    def n_equipment_instances(self, obj):
        return obj.equipment_instances.count()

    def get_queryset(self, request):
        query_set = \
            super().get_queryset(request=request) \
            .select_related(
                'equipment_general_type')

        return query_set \
                .prefetch_related(
                    Prefetch(
                        lookup='equipment_unique_types',
                        queryset=EQUIPMENT_UNIQUE_TYPE_ID_ONLY_UNORDERED_QUERY_SET),
                    Prefetch(
                        lookup='equipment_data_fields',
                        queryset=EQUIPMENT_DATA_FIELD_STR_QUERY_SET)) \
            if request.resolver_match.url_name.endswith('_change') \
          else query_set \
                .prefetch_related(
                    Prefetch(
                        lookup='equipment_unique_types',
                        queryset=EQUIPMENT_UNIQUE_TYPE_NAME_ONLY_QUERY_SET),
                    Prefetch(
                        lookup='equipment_data_fields',
                        queryset=EQUIPMENT_DATA_FIELD_ID_ONLY_UNORDERED_QUERY_SET),
                    Prefetch(
                        lookup='equipment_instances',
                        queryset=EQUIPMENT_INSTANCE_ID_ONLY_UNORDERED_QUERY_SET))

    @silk_profile(name='Admin: Equipment Unique Type Groups')
    def changelist_view(self, *args, **kwargs):
        return super().changelist_view(*args, **kwargs)

    @silk_profile(name='Admin: Equipment Unique Type Group')
    def changeform_view(self, *args, **kwargs):
        return super().changeform_view(*args, **kwargs)


site.register(EquipmentUniqueTypeGroup,
              admin_class=EquipmentUniqueTypeGroupAdmin)


class EquipmentUniqueTypeAdmin(ModelAdmin):
    """EquipmentUniqueTypeAdmin."""

    list_display = \
        'equipment_general_type', \
        'name', \
        'n_equipment_data_fields', \
        'equipment_unique_type_group_list', \
        'n_equipment_instances'

    list_filter = 'equipment_general_type__name',

    show_full_result_count = False

    search_fields = 'equipment_general_type__name', 'name'

    # form = EquipmentUniqueTypeForm

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
            super().get_queryset(request=request) \
            .select_related(
                'equipment_general_type') \
            .prefetch_related(
                Prefetch(
                    lookup='equipment_data_fields',
                    queryset=EQUIPMENT_DATA_FIELD_ID_ONLY_UNORDERED_QUERY_SET))

        return query_set \
                .prefetch_related(
                    Prefetch(
                        lookup='equipment_unique_type_groups',
                        queryset=EQUIPMENT_UNIQUE_TYPE_GROUP_ID_ONLY_UNORDERED_QUERY_SET)) \
            if request.resolver_match.url_name.endswith('_change') \
          else query_set \
                .prefetch_related(
                    Prefetch(
                        lookup='equipment_instances',
                        queryset=EQUIPMENT_INSTANCE_RELATED_TO_EQUIPMENT_UNIQUE_TYPE_ID_ONLY_UNORDERED_QUERY_SET),
                    Prefetch(
                        lookup='equipment_unique_type_groups',
                        queryset=EQUIPMENT_UNIQUE_TYPE_GROUP_NAME_ONLY_QUERY_SET))

    @silk_profile(name='Admin: Equipment Unique Types')
    def changelist_view(self, *args, **kwargs):
        return super().changelist_view(*args, **kwargs)

    @silk_profile(name='Admin: Equipment Unique Type')
    def changeform_view(self, *args, **kwargs):
        return super().changeform_view(*args, **kwargs)


site.register(
    EquipmentUniqueType,
    admin_class=EquipmentUniqueTypeAdmin)


class EquipmentInstanceInLineFormSet(BaseInlineFormSet):
    model = EquipmentInstance

    # def get_queryset(self):
    #     return super().get_queryset() \
    #         .select_related(
    #             'equipment_general_type',
    #             'equipment_unique_type', 'equipment_unique_type__equipment_general_type')


class EquipmentInstanceTabularInline(TabularInline):
    model = EquipmentInstance

    fields = \
        'equipment_general_type', \
        'equipment_unique_type', \
        'name'

    # form = EquipmentInstanceForm

    formset = EquipmentInstanceInLineFormSet

    extra = 0

    def get_queryset(self, request):
        return super().get_queryset(request=request) \
                .select_related(
                    'equipment_general_type',
                    'equipment_unique_type', 'equipment_unique_type__equipment_general_type')


class EquipmentFacilityAdmin(ModelAdmin):
    list_display = \
        'name', \
        'info', \
        'n_equipment_instances'

    search_fields = \
        'name', \
        'info'

    show_full_result_count = False

    # inlines = EquipmentInstanceTabularInline,

    def n_equipment_instances(self, obj):
        return obj.equipment_instances.count()

    def get_queryset(self, request):
        query_set = super().get_queryset(request=request)

        return query_set \
            if request.resolver_match.url_name.endswith('_change') \
          else query_set \
                .prefetch_related(
                    Prefetch(
                        lookup='equipment_instances',
                        queryset=EQUIPMENT_INSTANCE_RELATED_TO_EQUIPMENT_FACILITY_ID_ONLY_UNORDERED_QUERY_SET))

    @silk_profile(name='Admin: Equipment Facilities')
    def changelist_view(self, *args, **kwargs):
        return super().changelist_view(*args, **kwargs)

    @silk_profile(name='Admin: Equipment Facility')
    def changeform_view(self, *args, **kwargs):
        return super().changeform_view(*args, **kwargs)


site.register(
    EquipmentFacility,
    admin_class=EquipmentFacilityAdmin)


class EquipmentInstanceAdmin(ModelAdmin):
    list_display = \
        'equipment_general_type', \
        'equipment_unique_type', \
        'equipment_facility', \
        'name', \
        'info'

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

    # form = EquipmentInstanceForm

    def get_queryset(self, request):
        query_set = super().get_queryset(request=request)

        return query_set \
                .select_related(
                    'equipment_general_type',
                    'equipment_unique_type') \
                .defer(
                    'equipment_unique_type__equipment_general_type') \
                .prefetch_related(
                    Prefetch(
                        lookup='equipment_unique_type_groups',
                        queryset=EQUIPMENT_UNIQUE_TYPE_GROUP_ID_ONLY_UNORDERED_QUERY_SET)) \
            if request.resolver_match.url_name.endswith('_change') \
          else query_set \
                .select_related(
                    'equipment_general_type',
                    'equipment_unique_type', 'equipment_unique_type__equipment_general_type',
                    'equipment_facility') \
                .defer(
                    'equipment_facility__info')

    @silk_profile(name='Admin: Equipment Instances')
    def changelist_view(self, *args, **kwargs):
        return super().changelist_view(*args, **kwargs)

    @silk_profile(name='Admin: Equipment Instance')
    def changeform_view(self, *args, **kwargs):
        return super().changeform_view(*args, **kwargs)


site.register(
    EquipmentInstance,
    admin_class=EquipmentInstanceAdmin)


class EquipmentSystemAdmin(ModelAdmin):
    list_display = \
        'equipment_facility', \
        'name', \
        'date', \
        'n_equipment_instances'

    list_filter = \
        'equipment_facility__name', \
        'date'

    search_fields = \
        'equipment_facility__name', \
        'name',

    show_full_result_count = False

    # form = EquipmentSystemForm

    def n_equipment_instances(self, obj):
        return obj.equipment_instances.count()

    def get_queryset(self, request):
        return super().get_queryset(request=request) \
                .select_related(
                    'equipment_facility') \
                .defer(
                    'equipment_facility__info') \
                .prefetch_related(
                    Prefetch(
                        lookup='equipment_instances',
                        queryset=EQUIPMENT_INSTANCE_ID_ONLY_UNORDERED_QUERY_SET))

    @silk_profile(name='Admin: Equipment Systems')
    def changelist_view(self, *args, **kwargs):
        return super().changelist_view(*args, **kwargs)

    @silk_profile(name='Admin: Equipment System')
    def changeform_view(self, *args, **kwargs):
        return super().changeform_view(*args, **kwargs)


site.register(
    EquipmentSystem,
    admin_class=EquipmentSystemAdmin)


class EquipmentUniqueTypeGroupDataFieldProfileAdmin(ModelAdmin):
    list_display = \
        'equipment_unique_type_group', \
        'equipment_data_field', \
        'to_date', \
        'valid_proportion', \
        'n_distinct_values', \
        'distinct_values', \
        'sample_min', \
        'outlier_rst_min', \
        'sample_quartile', \
        'sample_median', \
        'sample_3rd_quartile', \
        'outlier_rst_max', \
        'sample_max'

    list_filter = \
        'equipment_unique_type_group__equipment_general_type__name', \
        'equipment_unique_type_group__name', \
        'to_date', \
        'equipment_data_field__name'

    search_fields = \
        'equipment_unique_type_group__equipment_general_type__name', \
        'equipment_unique_type_group__name', \
        'equipment_data_field__name'

    show_full_result_count = False

    ordering = \
        'equipment_unique_type_group', \
        '-to_date', \
        '-n_distinct_values'

    readonly_fields = \
        'equipment_unique_type_group', \
        'equipment_data_field', \
        'to_date', \
        'valid_proportion', \
        'n_distinct_values', \
        'distinct_values', \
        'sample_min', \
        'outlier_rst_min', \
        'sample_quartile', \
        'sample_median', \
        'sample_3rd_quartile', \
        'outlier_rst_max', \
        'sample_max'

    def get_queryset(self, request):
        return super().get_queryset(request=request) \
                .select_related(
                    'equipment_unique_type_group', 'equipment_unique_type_group__equipment_general_type',
                    'equipment_data_field',
                    'equipment_data_field__equipment_general_type', 'equipment_data_field__equipment_data_field_type',
                    'equipment_data_field__data_type', 'equipment_data_field__numeric_measurement_unit')

    @silk_profile(name='Admin: Equipment Unique Type Group Data Field Profiles')
    def changelist_view(self, *args, **kwargs):
        return super().changelist_view(*args, **kwargs)

    @silk_profile(name='Admin: Equipment Unique Type Group Data Field Profile')
    def changeform_view(self, *args, **kwargs):
        return super().changeform_view(*args, **kwargs)


site.register(
    EquipmentUniqueTypeGroupDataFieldProfile,
    admin_class=EquipmentUniqueTypeGroupDataFieldProfileAdmin)


class EquipmentUniqueTypeGroupDataFieldPairwiseCorrelationAdmin(ModelAdmin):
    list_display = \
        'equipment_unique_type_group', \
        'equipment_data_field', \
        'equipment_data_field_2', \
        'sample_correlation'

    list_filter = \
        'equipment_unique_type_group__equipment_general_type__name', \
        'equipment_unique_type_group__name', \
        'equipment_data_field__name'

    search_fields = \
        'equipment_unique_type_group__equipment_general_type__name', \
        'equipment_unique_type_group__name', \
        'equipment_data_field__name'

    show_full_result_count = False

    ordering = \
        'equipment_unique_type_group', \
        '-sample_correlation'

    readonly_fields = \
        'equipment_unique_type_group', \
        'equipment_data_field', \
        'equipment_data_field_2', \
        'sample_correlation'

    def get_queryset(self, request):
        return super().get_queryset(request=request) \
                .select_related(
                    'equipment_unique_type_group', 'equipment_unique_type_group__equipment_general_type',
                    'equipment_data_field',
                    'equipment_data_field__equipment_general_type', 'equipment_data_field__equipment_data_field_type',
                    'equipment_data_field__data_type', 'equipment_data_field__numeric_measurement_unit',
                    'equipment_data_field_2',
                    'equipment_data_field_2__equipment_general_type', 'equipment_data_field_2__equipment_data_field_type',
                    'equipment_data_field_2__data_type', 'equipment_data_field_2__numeric_measurement_unit')

    @silk_profile(name='Admin: Equipment Unique Type Group Data Field Pairwise Correlations')
    def changelist_view(self, *args, **kwargs):
        return super().changelist_view(*args, **kwargs)

    @silk_profile(name='Admin: Equipment Unique Type Group Data Field Pairwise Correlation')
    def changeform_view(self, *args, **kwargs):
        return super().changeform_view(*args, **kwargs)


site.register(
    EquipmentUniqueTypeGroupDataFieldPairwiseCorrelation,
    admin_class=EquipmentUniqueTypeGroupDataFieldPairwiseCorrelationAdmin)
