from django.contrib.admin import ModelAdmin, site, StackedInline
from django.db.models import Prefetch

from silk.profiling.profiler import silk_profile

from ..base.query_sets import \
    EQUIPMENT_DATA_FIELD_ID_ONLY_UNORDERED_QUERY_SET, \
    EQUIPMENT_DATA_FIELD_NAME_ONLY_QUERY_SET

from .forms import \
    EquipmentUniqueTypeGroupServiceConfigForm, \
    EquipmentUniqueTypeGroupMonitoredDataFieldConfigForm, \
    EquipmentInstanceProblemDiagnosisForm, \
    EquipmentInstanceAlertPeriodForm

from .models import \
    GlobalConfig, \
    EquipmentUniqueTypeGroupDataFieldProfile, \
    EquipmentUniqueTypeGroupDataFieldPairwiseCorrelation, \
    EquipmentUniqueTypeGroupMonitoredDataFieldConfig, \
    EquipmentUniqueTypeGroupServiceConfig, \
    Blueprint, \
    EquipmentUniqueTypeGroupDataFieldBlueprintBenchmarkMetricProfile, \
    EquipmentProblemType, \
    EquipmentInstanceAlarmPeriod, \
    EquipmentInstanceProblemDiagnosis, \
    EquipmentInstanceAlertPeriod, \
    AlertDiagnosisStatus

from .query_sets import \
    EQUIPMENT_INSTANCE_ALARM_PERIOD_STR_QUERY_SET, \
    EQUIPMENT_INSTANCE_ALERT_PERIOD_STR_QUERY_SET, \
    EQUIPMENT_INSTANCE_PROBLEM_DIAGNOSIS_ID_ONLY_UNORDERED_QUERY_SET, \
    EQUIPMENT_INSTANCE_PROBLEM_DIAGNOSIS_STR_QUERY_SET


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
        'sample_max', \
        'last_updated'

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
        return super(type(self), self).get_queryset(request=request) \
                .select_related(
                    'equipment_unique_type_group', 'equipment_unique_type_group__equipment_general_type',
                    'equipment_data_field',
                    'equipment_data_field__equipment_general_type', 'equipment_data_field__equipment_data_field_type',
                    'equipment_data_field__data_type', 'equipment_data_field__numeric_measurement_unit') \
                .defer(
                    'equipment_unique_type_group__description', 'equipment_unique_type_group__last_updated',
                    'equipment_data_field__description', 'equipment_data_field__last_updated',
                    'equipment_data_field__numeric_measurement_unit__description')

    @silk_profile(name='Admin: Equipment Unique Type Group Data Field Profiles')
    def changelist_view(self, *args, **kwargs):
        return super(type(self), self).changelist_view(*args, **kwargs)

    @silk_profile(name='Admin: Equipment Unique Type Group Data Field Profile')
    def changeform_view(self, *args, **kwargs):
        return super(type(self), self).changeform_view(*args, **kwargs)


site.register(
    EquipmentUniqueTypeGroupDataFieldProfile,
    admin_class=EquipmentUniqueTypeGroupDataFieldProfileAdmin)


class EquipmentUniqueTypeGroupDataFieldPairwiseCorrelationAdmin(ModelAdmin):
    list_display = \
        'equipment_unique_type_group', \
        'equipment_data_field', \
        'equipment_data_field_2', \
        'sample_correlation', \
        'last_updated'

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
        return super(type(self), self).get_queryset(request=request) \
                .select_related(
                    'equipment_unique_type_group', 'equipment_unique_type_group__equipment_general_type',
                    'equipment_data_field',
                    'equipment_data_field__equipment_general_type', 'equipment_data_field__equipment_data_field_type',
                    'equipment_data_field__data_type', 'equipment_data_field__numeric_measurement_unit',
                    'equipment_data_field_2',
                    'equipment_data_field_2__equipment_general_type', 'equipment_data_field_2__equipment_data_field_type',
                    'equipment_data_field_2__data_type', 'equipment_data_field_2__numeric_measurement_unit') \
                .defer(
                    'equipment_unique_type_group__description', 'equipment_unique_type_group__last_updated',
                    'equipment_data_field__description', 'equipment_data_field__last_updated',
                    'equipment_data_field__numeric_measurement_unit__description',
                    'equipment_data_field_2__description', 'equipment_data_field_2__last_updated',
                    'equipment_data_field_2__numeric_measurement_unit__description')

    @silk_profile(name='Admin: Equipment Unique Type Group Data Field Pairwise Correlations')
    def changelist_view(self, *args, **kwargs):
        return super(type(self), self).changelist_view(*args, **kwargs)

    @silk_profile(name='Admin: Equipment Unique Type Group Data Field Pairwise Correlation')
    def changeform_view(self, *args, **kwargs):
        return super(type(self), self).changeform_view(*args, **kwargs)


site.register(
    EquipmentUniqueTypeGroupDataFieldPairwiseCorrelation,
    admin_class=EquipmentUniqueTypeGroupDataFieldPairwiseCorrelationAdmin)


class EquipmentUniqueTypeGroupMonitoredDataFieldConfigStackedInline(StackedInline):
    model = EquipmentUniqueTypeGroupMonitoredDataFieldConfig

    fields = \
        'monitored_equipment_data_field', \
        'highly_correlated_numeric_equipment_data_fields', \
        'auto_included_numeric_equipment_data_fields', \
        'lowly_correlated_numeric_equipment_data_fields', \
        'manually_included_equipment_data_fields', \
        'manually_excluded_equipment_data_fields', \
        'active', \
        'comments'

    form = EquipmentUniqueTypeGroupMonitoredDataFieldConfigForm

    extra = 0

    readonly_fields = \
        'highly_correlated_numeric_equipment_data_fields', \
        'auto_included_numeric_equipment_data_fields', \
        'lowly_correlated_numeric_equipment_data_fields'
    
    def get_queryset(self, request):
        return super(type(self), self).get_queryset(request=request) \
                .select_related(
                    'monitored_equipment_data_field') \
                .defer(
                    'monitored_equipment_data_field__equipment_general_type',
                    'monitored_equipment_data_field__name',
                    'monitored_equipment_data_field__description',
                    'monitored_equipment_data_field__equipment_data_field_type',
                    'monitored_equipment_data_field__data_type',
                    'monitored_equipment_data_field__numeric_measurement_unit',
                    'monitored_equipment_data_field__lower_numeric_null',
                    'monitored_equipment_data_field__upper_numeric_null',
                    'monitored_equipment_data_field__default_val',
                    'monitored_equipment_data_field__min_val',
                    'monitored_equipment_data_field__max_val',
                    'monitored_equipment_data_field__last_updated') \
                .prefetch_related(
                    Prefetch(
                        lookup='manually_included_equipment_data_fields',
                        queryset=EQUIPMENT_DATA_FIELD_ID_ONLY_UNORDERED_QUERY_SET),
                    Prefetch(
                        lookup='manually_excluded_equipment_data_fields',
                        queryset=EQUIPMENT_DATA_FIELD_ID_ONLY_UNORDERED_QUERY_SET))


class EquipmentUniqueTypeGroupServiceConfigAdmin(ModelAdmin):
    list_display = \
        'equipment_unique_type_group', \
        'include_categorical_equipment_data_fields', \
        'monitored_and_excluded_equipment_data_fields', \
        'active', \
        'from_date', \
        'to_date', \
        'configs', \
        'comments', \
        'last_updated'

    list_filter = \
        'equipment_unique_type_group__equipment_general_type__name', \
        'equipment_unique_type_group__name', \
        'active'

    search_fields = \
        'equipment_unique_type_group__equipment_general_type__name', \
        'equipment_unique_type_group__name',

    show_full_result_count = False

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
                                        equipment_unique_type_group_monitored_data_field_config.manually_excluded_equipment_data_fields.all()))
                            if equipment_unique_type_group_monitored_data_field_config.manually_excluded_equipment_data_fields.count()
                            else '')
                    for equipment_unique_type_group_monitored_data_field_config in
                        obj.equipment_unique_type_group_monitored_data_field_configs.all()
                    if equipment_unique_type_group_monitored_data_field_config.active),
                ' | global excl: {}'.format(
                    ', '.join(excluded_equipment_data_field.name
                              for excluded_equipment_data_field in obj.global_excluded_equipment_data_fields.all()))
                    if obj.global_excluded_equipment_data_fields.count()
                    else '')

    def get_queryset(self, request):
        query_set = super(type(self), self).get_queryset(request=request) \

        return query_set \
                .select_related(
                    'equipment_unique_type_group') \
                .defer(
                    'equipment_unique_type_group__equipment_general_type',
                    # 'equipment_unique_type_group__name',
                    'equipment_unique_type_group__description',
                    'equipment_unique_type_group__last_updated') \
                .prefetch_related(
                    Prefetch(
                        lookup='global_excluded_equipment_data_fields',
                        queryset=EQUIPMENT_DATA_FIELD_ID_ONLY_UNORDERED_QUERY_SET)) \
            if request.resolver_match.url_name.endswith('_change') \
          else query_set \
                .select_related(
                    'equipment_unique_type_group', 'equipment_unique_type_group__equipment_general_type') \
                .defer(
                    'equipment_unique_type_group__description', 'equipment_unique_type_group__last_updated') \
                .prefetch_related(
                    Prefetch(
                        lookup='equipment_unique_type_group_monitored_data_field_configs',
                        queryset=
                            EquipmentUniqueTypeGroupMonitoredDataFieldConfig.objects
                            .defer(
                                'highly_correlated_numeric_equipment_data_fields',
                                'auto_included_numeric_equipment_data_fields',
                                'lowly_correlated_numeric_equipment_data_fields',
                                'comments')
                            .select_related(
                                'monitored_equipment_data_field')
                            .defer(
                                'monitored_equipment_data_field__equipment_general_type',
                                'monitored_equipment_data_field__description',
                                'monitored_equipment_data_field__equipment_data_field_type',
                                'monitored_equipment_data_field__data_type',
                                'monitored_equipment_data_field__numeric_measurement_unit',
                                'monitored_equipment_data_field__lower_numeric_null',
                                'monitored_equipment_data_field__upper_numeric_null',
                                'monitored_equipment_data_field__default_val',
                                'monitored_equipment_data_field__min_val',
                                'monitored_equipment_data_field__max_val',
                                'monitored_equipment_data_field__last_updated')
                            .prefetch_related(
                                Prefetch(
                                    lookup='manually_excluded_equipment_data_fields',
                                    queryset=EQUIPMENT_DATA_FIELD_NAME_ONLY_QUERY_SET))),
                    Prefetch(
                        lookup='global_excluded_equipment_data_fields',
                        queryset=EQUIPMENT_DATA_FIELD_NAME_ONLY_QUERY_SET))

    @silk_profile(name='Admin: Equipment Unique Type Group Service Configs')
    def changelist_view(self, *args, **kwargs):
        return super(type(self), self).changelist_view(*args, **kwargs)

    @silk_profile(name='Admin: Equipment Unique Type Group Service Config')
    def changeform_view(self, *args, **kwargs):
        return super(type(self), self).changeform_view(*args, **kwargs)


site.register(
    EquipmentUniqueTypeGroupServiceConfig,
    admin_class=EquipmentUniqueTypeGroupServiceConfigAdmin)


class BlueprintAdmin(ModelAdmin):
    list_display = \
        'equipment_unique_type_group', \
        'trained_to_date', \
        'uuid', \
        'timestamp', \
        'active', \
        'benchmark_metrics_summary', \
        'last_updated'

    list_filter = \
        'equipment_unique_type_group__equipment_general_type__name', \
        'equipment_unique_type_group__name', \
        'trained_to_date', \
        'timestamp', \
        'active'

    search_fields = \
        'equipment_unique_type_group__equipment_general_type__name', \
        'equipment_unique_type_group__name', \
        'uuid'

    show_full_result_count = False

    readonly_fields = \
        'equipment_unique_type_group', \
        'trained_to_date', \
        'uuid', \
        'timestamp'

    def benchmark_metrics_summary(self, obj):
        if obj.benchmark_metrics:
            d = {}

            for label_var_name, benchmark_metrics in obj.benchmark_metrics.items():
                global_benchmark_metrics = benchmark_metrics['GLOBAL']

                good = True

                r2 = global_benchmark_metrics['R2']

                if r2 is not None:
                    r2_text = '{:.1f}%'.format(100 * r2)
                    if r2 < .68:
                        good = False
                        r2_text += ' (< 68%)'

                else:
                    r2_text = 'na'
                    good = False

                mae = global_benchmark_metrics['MAE']
                medae = global_benchmark_metrics['MedAE']
                mae_medae_ratio = mae / medae
                mae_medae_ratio_text = '{:.3g}x'.format(mae_medae_ratio)
                if mae_medae_ratio > 3:
                    good = False
                    mae_medae_ratio_text += ' (> 3x)'

                d[label_var_name.upper()
                  if good
                  else label_var_name] = \
                    dict(good=good,
                         R2_text=r2_text,
                         MAE=mae,
                         MedAE=medae,
                         MAE_MedAE_ratio_text=mae_medae_ratio_text)

            return '; '.join(
                '{}: R2 {}, MAE {:.3g} / MedAE {:.3g} = {}'.format(
                    k,
                    v['R2_text'],
                    v['MAE'],
                    v['MedAE'],
                    v['MAE_MedAE_ratio_text'])
                for k, v in sorted(d.items(), key=lambda i: i[1]['good'], reverse=True))

    def get_queryset(self, request):
        return super(type(self), self).get_queryset(request=request) \
                .select_related(
                    'equipment_unique_type_group', 'equipment_unique_type_group__equipment_general_type') \
                .defer(
                    'equipment_unique_type_group__description', 'equipment_unique_type_group__last_updated')

    @silk_profile(name='Admin: Blueprints')
    def changelist_view(self, *args, **kwargs):
        return super(type(self), self).changelist_view(*args, **kwargs)

    @silk_profile(name='Admin: Blueprint')
    def changeform_view(self, *args, **kwargs):
        return super(type(self), self).changeform_view(*args, **kwargs)


site.register(
    Blueprint,
    admin_class=BlueprintAdmin)


class EquipmentUniqueTypeGroupDataFieldBlueprintBenchmarkMetricProfileAdmin(ModelAdmin):
    list_display = \
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
        'equipment_unique_type_group__equipment_general_type__name', \
        'equipment_unique_type_group__name', \
        'trained_to_date'

    search_fields = \
        'equipment_unique_type_group__equipment_general_type__name', \
        'equipment_unique_type_group__name', \
        'equipment_data_field__name'

    show_full_result_count = False

    readonly_fields = \
        'equipment_unique_type_group', \
        'equipment_data_field', \
        'trained_to_date', \
        'n', \
        'r2', \
        'mae', \
        'medae', \
        'rmse'

    def get_queryset(self, request):
        return super(type(self), self).get_queryset(request=request) \
                .select_related(
                    'equipment_unique_type_group', 'equipment_unique_type_group__equipment_general_type',
                    'equipment_data_field',
                    'equipment_data_field__equipment_general_type', 'equipment_data_field__equipment_data_field_type',
                    'equipment_data_field__data_type', 'equipment_data_field__numeric_measurement_unit') \
                .defer(
                    'equipment_unique_type_group__description', 'equipment_unique_type_group__last_updated',
                    'equipment_data_field__description', 'equipment_data_field__last_updated',
                    'equipment_data_field__numeric_measurement_unit__description')

    @silk_profile(name='Admin: Equipment Unique Type Group Data Field Blueprint Benchmark Metric Profiles')
    def changelist_view(self, *args, **kwargs):
        return super(type(self), self).changelist_view(*args, **kwargs)

    @silk_profile(name='Admin: Equipment Unique Type Group Data Field Blueprint Benchmark Metric Profile')
    def changeform_view(self, *args, **kwargs):
        return super(type(self), self).changeform_view(*args, **kwargs)


site.register(
    EquipmentUniqueTypeGroupDataFieldBlueprintBenchmarkMetricProfile,
    admin_class=EquipmentUniqueTypeGroupDataFieldBlueprintBenchmarkMetricProfileAdmin)


class EquipmentProblemTypeAdmin(ModelAdmin):
    list_display = 'name',

    search_fields = 'name',

    show_full_result_count = False

    @silk_profile(name='Admin: Equipment Problem Types')
    def changelist_view(self, *args, **kwargs):
        return super(type(self), self).changelist_view(*args, **kwargs)

    @silk_profile(name='Admin: Equipment Problem Type')
    def changeform_view(self, *args, **kwargs):
        return super(type(self), self).changeform_view(*args, **kwargs)


site.register(
    EquipmentProblemType,
    admin_class=EquipmentProblemTypeAdmin)


class EquipmentInstanceAlarmPeriodAdmin(ModelAdmin):
    list_display = \
        'equipment_instance', \
        'alarm_type', \
        'from_utc_date_time', \
        'to_utc_date_time', \
        'duration_in_days', \
        'has_associated_equipment_instance_alert_periods', \
        'has_associated_equipment_instance_problem_diagnoses', \
        'last_updated'

    list_filter = \
        'equipment_instance__equipment_general_type__name', \
        'alarm_type__name', \
        'from_utc_date_time', \
        'to_utc_date_time', \
        'has_associated_equipment_instance_alert_periods', \
        'has_associated_equipment_instance_problem_diagnoses'

    search_fields = \
        'equipment_instance__equipment_general_type__name', \
        'equipment_instance__equipment_unique_type__name', \
        'equipment_instance__name'

    show_full_result_count = False

    readonly_fields = \
        'equipment_instance', \
        'alarm_type', \
        'from_utc_date_time', \
        'to_utc_date_time', \
        'duration_in_days', \
        'date_range', \
        'has_associated_equipment_instance_alert_periods', \
        'equipment_instance_alert_periods', \
        'has_associated_equipment_instance_problem_diagnoses', \
        'equipment_instance_problem_diagnoses'

    def get_queryset(self, request):
        query_set = \
            super(type(self), self).get_queryset(request=request) \
            .select_related(
                'equipment_instance',
                'equipment_instance__equipment_general_type', 'equipment_instance__equipment_unique_type',
                'alarm_type') \
            .defer(
                'equipment_instance__equipment_unique_type__description', 'equipment_instance__equipment_unique_type__last_updated',
                'equipment_instance__equipment_facility', 'equipment_instance__info', 'equipment_instance__last_updated')

        return query_set \
                .prefetch_related(
                    Prefetch(
                        lookup='equipment_instance_alert_periods',
                        queryset=EQUIPMENT_INSTANCE_ALERT_PERIOD_STR_QUERY_SET),
                    Prefetch(
                        lookup='equipment_instance_problem_diagnoses',
                        queryset=EQUIPMENT_INSTANCE_PROBLEM_DIAGNOSIS_STR_QUERY_SET)) \
            if request.resolver_match.url_name.endswith('_change') \
          else query_set \
                .defer(
                    'date_range')

    @silk_profile(name='Admin: Equipment Instance Alarm Periods')
    def changelist_view(self, *args, **kwargs):
        return super(type(self), self).changelist_view(*args, **kwargs)

    @silk_profile(name='Admin: Equipment Instance Alarm Period')
    def changeform_view(self, *args, **kwargs):
        return super(type(self), self).changeform_view(*args, **kwargs)


site.register(
    EquipmentInstanceAlarmPeriod,
    admin_class=EquipmentInstanceAlarmPeriodAdmin)


class EquipmentInstanceProblemDiagnosisAdmin(ModelAdmin):
    list_display = \
        'equipment_instance', \
        'from_date', \
        'to_date', \
        'duration', \
        'equipment_problem_type_names', \
        'dismissed', \
        'comments', \
        'has_associated_equipment_instance_alarm_periods', \
        'has_associated_equipment_instance_alert_periods', \
        'last_updated'

    list_filter = \
        'equipment_instance__equipment_general_type__name', \
        'from_date', \
        'to_date', \
        'dismissed'

    readonly_fields = \
        'date_range', \
        'duration', \
        'has_equipment_problems', \
        'has_associated_equipment_instance_alarm_periods', \
        'equipment_instance_alarm_periods', \
        'has_associated_equipment_instance_alert_periods', \
        'equipment_instance_alert_periods'

    show_full_result_count = False

    search_fields = \
        'equipment_instance__equipment_general_type__name', \
        'equipment_instance__equipment_unique_type__name', \
        'equipment_instance__name'

    form = EquipmentInstanceProblemDiagnosisForm

    def equipment_problem_type_names(self, obj):
        return ', '.join(equipment_problem_type.name
                         for equipment_problem_type in obj.equipment_problem_types.all())

    def get_queryset(self, request):
        query_set = \
            super(type(self), self).get_queryset(request) \
            .select_related(
                'equipment_instance',
                'equipment_instance__equipment_general_type', 'equipment_instance__equipment_unique_type') \
            .defer(
                'equipment_instance__equipment_unique_type__description', 'equipment_instance__equipment_unique_type__last_updated',
                'equipment_instance__equipment_facility', 'equipment_instance__info', 'equipment_instance__last_updated')

        return query_set \
                .prefetch_related(
                    'equipment_problem_types',
                    Prefetch(
                        lookup='equipment_instance_alarm_periods',
                        queryset=EQUIPMENT_INSTANCE_ALARM_PERIOD_STR_QUERY_SET),
                    Prefetch(
                        lookup='equipment_instance_alert_periods',
                        queryset=EQUIPMENT_INSTANCE_ALERT_PERIOD_STR_QUERY_SET)) \
            if request.resolver_match.url_name.endswith('_change') \
          else query_set \
                .defer(
                    'date_range') \
                .prefetch_related(
                    'equipment_problem_types')

    @silk_profile(name='Admin: Equipment Problem Diagnoses')
    def changelist_view(self, *args, **kwargs):
        return super(type(self), self).changelist_view(*args, **kwargs)

    @silk_profile(name='Admin: Equipment Problem Diagnosis')
    def changeform_view(self, *args, **kwargs):
        return super(type(self), self).changeform_view(*args, **kwargs)


site.register(
    EquipmentInstanceProblemDiagnosis,
    admin_class=EquipmentInstanceProblemDiagnosisAdmin)


class AlertDiagnosisStatusAdmin(ModelAdmin):
    list_display = \
        'index', \
        'name'

    show_full_result_count = False

    @silk_profile(name='Admin: Alert Diagnosis Statuses')
    def changelist_view(self, *args, **kwargs):
        return super(type(self), self).changelist_view(*args, **kwargs)

    @silk_profile(name='Admin: Alert Diagnosis Status')
    def changeform_view(self, *args, **kwargs):
        return super(type(self), self).changeform_view(*args, **kwargs)


site.register(
    AlertDiagnosisStatus,
    admin_class=AlertDiagnosisStatusAdmin)


class EquipmentInstanceAlertPeriodAdmin(ModelAdmin):
    list_display = \
        'equipment_unique_type_group', \
        'equipment_instance', \
        'risk_score_name', \
        'threshold', \
        'from_date', \
        'to_date', \
        'duration', \
        'approx_average_risk_score', \
        'last_risk_score', \
        'cumulative_excess_risk_score', \
        'ongoing', \
        'diagnosis_status', \
        'has_associated_equipment_instance_alarm_periods', \
        'has_associated_equipment_instance_problem_diagnoses', \
        'last_updated'

    list_filter = \
        'equipment_unique_type_group__equipment_general_type__name', \
        'equipment_unique_type_group__name', \
        'risk_score_name', \
        'threshold', \
        'from_date', \
        'to_date', \
        'ongoing', \
        'diagnosis_status', \
        'has_associated_equipment_instance_alarm_periods', \
        'has_associated_equipment_instance_problem_diagnoses'

    search_fields = \
        'equipment_unique_type_group__equipment_general_type__name', \
        'equipment_unique_type_group__name', \
        'equipment_instance__name', \
        'risk_score_name'

    show_full_result_count = False

    form = EquipmentInstanceAlertPeriodForm

    readonly_fields = \
        'equipment_unique_type_group', \
        'equipment_instance', \
        'risk_score_name', \
        'threshold', \
        'from_date', \
        'to_date', \
        'date_range', \
        'duration', \
        'approx_average_risk_score', \
        'last_risk_score', \
        'cumulative_excess_risk_score', \
        'ongoing', \
        'info', \
        'has_associated_equipment_instance_alarm_periods', \
        'equipment_instance_alarm_periods', \
        'has_associated_equipment_instance_problem_diagnoses'

    def get_queryset(self, request):
        query_set = \
            super(type(self), self).get_queryset(request) \
            .select_related(
                'equipment_unique_type_group', 'equipment_unique_type_group__equipment_general_type',
                'equipment_instance',
                'equipment_instance__equipment_general_type', 'equipment_instance__equipment_unique_type',
                'diagnosis_status') \
            .defer(
                'equipment_unique_type_group__description', 'equipment_unique_type_group__last_updated',
                'equipment_instance__equipment_unique_type__description',
                'equipment_instance__equipment_unique_type__last_updated',
                'equipment_instance__equipment_facility', 'equipment_instance__info', 'equipment_instance__last_updated')

        return query_set \
                .prefetch_related(
                    Prefetch(
                        lookup='equipment_instance_alarm_periods',
                        queryset=EQUIPMENT_INSTANCE_ALARM_PERIOD_STR_QUERY_SET),
                    Prefetch(
                        lookup='equipment_instance_problem_diagnoses',
                        queryset=EQUIPMENT_INSTANCE_PROBLEM_DIAGNOSIS_ID_ONLY_UNORDERED_QUERY_SET)) \
            if request.resolver_match.url_name.endswith('_change') \
          else query_set \
                .defer(
                    'date_range',
                    'info')

    @silk_profile(name='Admin: Equipment Instance Alert Periods')
    def changelist_view(self, *args, **kwargs):
        return super(type(self), self).changelist_view(*args, **kwargs)

    @silk_profile(name='Admin: Equipment Instance Alert Period')
    def changeform_view(self, *args, **kwargs):
        return super(type(self), self).changeform_view(*args, **kwargs)


site.register(
    EquipmentInstanceAlertPeriod,
    admin_class=EquipmentInstanceAlertPeriodAdmin)
