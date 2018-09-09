from django.contrib.admin import ModelAdmin, site, StackedInline

from .forms import \
    EquipmentUniqueTypeGroupServiceConfigForm, \
    EquipmentUniqueTypeGroupMonitoredDataFieldConfigForm, \
    EquipmentProblemPeriodForm, \
    AlertForm

from .models import \
    EquipmentUniqueTypeGroupDataFieldProfile, \
    EquipmentUniqueTypeGroupMonitoredDataFieldConfig, \
    EquipmentUniqueTypeGroupServiceConfig, \
    Blueprint, \
    EquipmentUniqueTypeGroupDataFieldBlueprintBenchmarkMetricProfile, \
    EquipmentProblemType, EquipmentProblemPeriod, AlertDiagnosisStatus, Alert


class EquipmentUniqueTypeGroupDataFieldProfileAdmin(ModelAdmin):
    list_display = \
        'equipment_general_type', \
        'equipment_unique_type_group', \
        'equipment_data_field', \
        'to_date', \
        'valid_proportion', \
        'n_distinct_values', \
        'sample_min', \
        'outlier_rst_min', \
        'sample_quartile', \
        'sample_median', \
        'sample_3rd_quartile', \
        'outlier_rst_max', \
        'sample_max', \
        'last_updated'

    list_filter = \
        'equipment_general_type', \
        'equipment_unique_type_group', \
        'to_date'

    list_select_related = \
        'equipment_general_type', \
        'equipment_unique_type_group', \
        'equipment_data_field'

    show_full_result_count = False   # too many

    search_fields = \
        'equipment_general_type__name', \
        'equipment_unique_type_group__name', \
        'equipment_data_field__name'

    readonly_fields = \
        'equipment_general_type', \
        'equipment_unique_type_group', \
        'equipment_data_field', \
        'to_date', \
        'valid_proportion', \
        'distinct_values', \
        'n_distinct_values', \
        'sample_min', \
        'outlier_rst_min', \
        'sample_quartile', \
        'sample_median', \
        'sample_3rd_quartile', \
        'outlier_rst_max', \
        'sample_max', \
        'last_updated'


site.register(
    EquipmentUniqueTypeGroupDataFieldProfile,
    admin_class=EquipmentUniqueTypeGroupDataFieldProfileAdmin)


class EquipmentUniqueTypeGroupMonitoredDataFieldConfigStackedInline(StackedInline):
    model = EquipmentUniqueTypeGroupMonitoredDataFieldConfig

    fields = \
        'monitored_equipment_data_field', \
        'excluded_equipment_data_fields', \
        'active', \
        'comments'

    form = EquipmentUniqueTypeGroupMonitoredDataFieldConfigForm

    extra = 0


class EquipmentUniqueTypeGroupServiceConfigAdmin(ModelAdmin):
    list_display = \
        'equipment_general_type', \
        'equipment_unique_type_group', \
        'monitored_and_excluded_equipment_data_fields', \
        'active', \
        'last_updated'

    list_filter = \
        'equipment_general_type', \
        'equipment_unique_type_group', \
        'active'

    list_select_related = \
        'equipment_general_type', \
        'equipment_unique_type_group',

    show_full_result_count = False   # too many

    search_fields = \
        'equipment_general_type__name', \
        'equipment_unique_type_group__name'

    form = EquipmentUniqueTypeGroupServiceConfigForm

    inlines = EquipmentUniqueTypeGroupMonitoredDataFieldConfigStackedInline,

    def monitored_and_excluded_equipment_data_fields(self, obj):
        return '{}{}'.format(
            '; '.join(
                '{}{}'.format(
                    equipment_unique_type_group_monitored_data_field_config.monitored_equipment_data_field.name.upper(),
                    ' (excl: {})'.format(
                        ', '.join(excluded_equipment_data_field.name
                                  for excluded_equipment_data_field in
                                    equipment_unique_type_group_monitored_data_field_config.excluded_equipment_data_fields.all()))
                        if equipment_unique_type_group_monitored_data_field_config.excluded_equipment_data_fields.count()
                        else '')
                for equipment_unique_type_group_monitored_data_field_config in
                    obj.equipment_unique_type_group_monitored_data_field_configs.filter(active=True)),
            ' | global excl: {}'.format(
                ', '.join(excluded_equipment_data_field.name
                          for excluded_equipment_data_field in obj.global_excluded_equipment_data_fields.all()))
                if obj.global_excluded_equipment_data_fields.count()
                else '')


site.register(
    EquipmentUniqueTypeGroupServiceConfig,
    admin_class=EquipmentUniqueTypeGroupServiceConfigAdmin)


class BlueprintAdmin(ModelAdmin):
    list_display = \
        'equipment_general_type', \
        'equipment_unique_type_group', \
        'trained_to_date', \
        'timestamp', \
        'uuid', \
        'active', \
        'last_updated'

    list_filter = \
        'equipment_general_type', \
        'equipment_unique_type_group', \
        'trained_to_date', \
        'timestamp', \
        'active'

    list_select_related = \
        'equipment_general_type', \
        'equipment_unique_type_group'

    show_full_result_count = False   # too many

    search_fields = \
        'equipment_general_type__name', \
        'equipment_unique_type_group__name', \
        'uuid'


site.register(
    Blueprint,
    admin_class=BlueprintAdmin)


class EquipmentUniqueTypeGroupDataFieldBlueprintBenchmarkMetricProfileAdmin(ModelAdmin):
    list_display = \
        'equipment_general_type', \
        'equipment_unique_type_group', \
        'equipment_data_field', \
        'trained_to_date', \
        'n', \
        'r2', \
        'mae', \
        'medae', \
        'rmse', \
        'last_updated'

    list_filter = \
        'equipment_general_type', \
        'equipment_unique_type_group', \
        'trained_to_date'

    list_select_related = \
        'equipment_general_type', \
        'equipment_unique_type_group', \
        'equipment_data_field'

    show_full_result_count = False   # too many

    search_fields = \
        'equipment_general_type__name', \
        'equipment_unique_type_group__name', \
        'equipment_data_field__name'

    readonly_fields = \
        'equipment_general_type', \
        'equipment_unique_type_group', \
        'equipment_data_field', \
        'trained_to_date', \
        'n', \
        'r2', \
        'mae', \
        'medae', \
        'rmse', \
        'last_updated'


site.register(
    EquipmentUniqueTypeGroupDataFieldBlueprintBenchmarkMetricProfile,
    admin_class=EquipmentUniqueTypeGroupDataFieldBlueprintBenchmarkMetricProfileAdmin)


class EquipmentProblemTypeAdmin(ModelAdmin):
    list_display = 'name',

    list_filter = 'name',

    show_full_result_count = False   # only a few, but skip counting anyway

    search_fields = 'name',


site.register(
    EquipmentProblemType,
    admin_class=EquipmentProblemTypeAdmin)


class EquipmentProblemPeriodAdmin(ModelAdmin):
    list_display = \
        'equipment_instance', \
        'from_date', \
        'to_date', \
        'equipment_problem_type_names', \
        'dismissed', \
        'comments', \
        'last_updated'

    list_filter = \
        'from_date', \
        'to_date', \
        'dismissed'

    list_select_related = 'equipment_instance',

    readonly_fields = 'alerts',   # too many alerts, so Select box would freeze

    show_full_result_count = False   # too many

    search_fields = 'equipment_instance__name',

    form = EquipmentProblemPeriodForm

    # ref: https://stackoverflow.com/questions/18108521/many-to-many-in-list-display-django
    def equipment_problem_type_names(self, obj):
        return ', '.join(equipment_problem_type.name
                         for equipment_problem_type in obj.equipment_problem_types.all())


site.register(
    EquipmentProblemPeriod,
    admin_class=EquipmentProblemPeriodAdmin)


class AlertDiagnosisStatusAdmin(ModelAdmin):
    list_display = \
        'index', \
        'name', \
        'last_updated'

    list_filter = 'name',

    show_full_result_count = False   # only a few, but skip counting anyway

    search_fields = 'name',


site.register(
    AlertDiagnosisStatus,
    admin_class=AlertDiagnosisStatusAdmin)


class AlertAdmin(ModelAdmin):
    list_display = \
        'equipment_general_type', \
        'equipment_unique_type_group', \
        'equipment_instance', \
        'risk_score_name', \
        'threshold', \
        'from_date', \
        'to_date', \
        'quantified_risk_degree', \
        'diagnosis_status'

    list_select_related = \
        'equipment_general_type', \
        'equipment_unique_type_group', \
        'equipment_instance', \
        'diagnosis_status'

    list_filter = \
        'equipment_general_type', \
        'equipment_unique_type_group', \
        'risk_score_name', \
        'threshold', \
        'from_date', \
        'to_date', \
        'diagnosis_status'

    show_full_result_count = False   # too many

    search_fields = \
        'equipment_general_type__name', \
        'equipment_unique_type_group__name', \
        'equipment_instance__name', \
        'risk_score_name'

    form = AlertForm


site.register(
    Alert,
    admin_class=AlertAdmin)
