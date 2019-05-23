from django.db.models import Prefetch

from ..base.query_sets import \
    EQUIPMENT_DATA_FIELD_NAME_ONLY_QUERY_SET, \
    EQUIPMENT_DATA_FIELD_INCL_DESCRIPTION_QUERY_SET

from .models import \
    GlobalConfig, \
    EquipmentUniqueTypeGroupDataFieldProfile, \
    EquipmentUniqueTypeGroupServiceConfig, \
    EquipmentUniqueTypeGroupMonitoredDataFieldConfig, \
    Blueprint, \
    EquipmentUniqueTypeGroupDataFieldBlueprintBenchmarkMetricProfile, \
    EquipmentInstanceDailyRiskScore, \
    EquipmentProblemType, \
    EquipmentInstanceAlarmPeriod, \
    AlertDiagnosisStatus, \
    EquipmentInstanceAlertPeriod, \
    EquipmentInstanceProblemDiagnosis


GLOBAL_CONFIG_QUERY_SET = \
    GlobalConfig.objects.all()


EQUIPMENT_UNIQUE_TYPE_GROUP_DATA_FIELD_PROFILE_REST_API_QUERY_SET = \
    EquipmentUniqueTypeGroupDataFieldProfile.objects \
    .select_related(
        'equipment_unique_type_group',
        'equipment_data_field',
        'equipment_data_field__equipment_general_type', 'equipment_data_field__equipment_data_field_type',
        'equipment_data_field__data_type', 'equipment_data_field__numeric_measurement_unit') \
    .defer(
        'equipment_unique_type_group__equipment_general_type',
        'equipment_unique_type_group__description',
        'equipment_unique_type_group__last_updated',
        'equipment_data_field__last_updated',
        'equipment_data_field__numeric_measurement_unit__description')


EQUIPMENT_UNIQUE_TYPE_GROUP_SERVICE_CONFIG_REST_API_QUERY_SET = \
    EquipmentUniqueTypeGroupServiceConfig.objects \
    .defer(
        'last_updated') \
    .select_related(
        'equipment_unique_type_group') \
    .defer(
        'equipment_unique_type_group__equipment_general_type',
        'equipment_unique_type_group__description',
        'equipment_unique_type_group__last_updated') \
    .prefetch_related(
        Prefetch(
            lookup='equipment_unique_type_group_monitored_data_field_configs',
            queryset=
                EquipmentUniqueTypeGroupMonitoredDataFieldConfig.objects
                .defer(
                    'highly_correlated_numeric_equipment_data_fields',
                    'auto_included_numeric_equipment_data_fields',
                    'lowly_correlated_numeric_equipment_data_fields')
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
                        lookup='manually_included_equipment_data_fields',
                        queryset=EQUIPMENT_DATA_FIELD_NAME_ONLY_QUERY_SET),
                    Prefetch(
                        lookup='manually_excluded_equipment_data_fields',
                        queryset=EQUIPMENT_DATA_FIELD_NAME_ONLY_QUERY_SET))),
        Prefetch(
            lookup='global_excluded_equipment_data_fields',
            queryset=EQUIPMENT_DATA_FIELD_INCL_DESCRIPTION_QUERY_SET))


BLUEPRINT_REST_API_QUERY_SET = \
    Blueprint.objects \
    .defer(
        'last_updated') \
    .select_related(
        'equipment_unique_type_group') \
    .defer(
        'equipment_unique_type_group__equipment_general_type',
        'equipment_unique_type_group__description',
        'equipment_unique_type_group__last_updated')


EQUIPMENT_UNIQUE_TYPE_GROUP_DATA_FIELD_BLUEPRINT_BENCHMARK_METRIC_PROFILE_REST_API_QUERY_SET = \
    EquipmentUniqueTypeGroupDataFieldBlueprintBenchmarkMetricProfile.objects \
    .defer(
        'last_updated') \
    .select_related(
        'equipment_unique_type_group',
        'equipment_data_field') \
    .defer(
        'equipment_unique_type_group__equipment_general_type',
        'equipment_unique_type_group__description',
        'equipment_unique_type_group__last_updated',
        'equipment_data_field__equipment_general_type',
        'equipment_data_field__description',
        'equipment_data_field__equipment_data_field_type',
        'equipment_data_field__data_type',
        'equipment_data_field__numeric_measurement_unit',
        'equipment_data_field__lower_numeric_null',
        'equipment_data_field__upper_numeric_null',
        'equipment_data_field__default_val',
        'equipment_data_field__min_val',
        'equipment_data_field__max_val',
        'equipment_data_field__last_updated')


EQUIPMENT_INSTANCE_DAILY_RISK_SCORE = \
    EquipmentInstanceDailyRiskScore.objects \
    .defer(
        'last_updated') \
    .select_related(
        'equipment_unique_type_group',
        'equipment_instance') \
    .defer(
        'equipment_unique_type_group__equipment_general_type',
        'equipment_unique_type_group__description',
        'equipment_unique_type_group__last_updated',
        'equipment_instance__equipment_general_type',
        'equipment_instance__equipment_unique_type',
        'equipment_instance__equipment_facility',
        'equipment_instance__info',
        'equipment_instance__last_updated')


EQUIPMENT_PROBLEM_TYPE_REST_API_QUERY_SET = \
    EquipmentProblemType.objects.all()


EQUIPMENT_INSTANCE_ALARM_PERIOD_FULL_QUERY_SET = \
    EquipmentInstanceAlarmPeriod.objects \
    .select_related(
        'equipment_instance',
        'alarm_type') \
    .defer


EQUIPMENT_INSTANCE_ALARM_PERIOD_REST_API_QUERY_SET = \
    EQUIPMENT_INSTANCE_ALARM_PERIOD_FULL_QUERY_SET \
    .prefetch_related(
    Prefetch(
        lookup='equipment_instance_alert_periods',
        queryset=
        EquipmentInstanceAlertPeriod.objects
            .select_related(
            'equipment_unique_type_group',
            'equipment_instance',
            'diagnosis_status')),
    Prefetch(
        lookup='equipment_instance_problem_diagnoses',
        queryset=
        EquipmentInstanceProblemDiagnosis.objects
            .select_related(
            'equipment_instance')
            .prefetch_related(
            'equipment_problem_types')))


ALERT_DIAGNOSIS_STATUS_REST_API_QUERY_SET = \
    AlertDiagnosisStatus.objects.all()


EQUIPMENT_INSTANCE_ALERT_PERIOD_REST_API_QUERY_SET = \
    EquipmentInstanceAlertPeriod.objects \
    .select_related(
        'equipment_unique_type_group',
        'equipment_instance',
        'diagnosis_status') \
    .prefetch_related(
        Prefetch(
            lookup='equipment_instance_alarm_periods',
            queryset=
            EquipmentInstanceAlarmPeriod.objects
                .select_related(
                'equipment_instance',
                'alarm_type')),
        Prefetch(
            lookup='equipment_instance_problem_diagnoses',
            queryset=
            EquipmentInstanceProblemDiagnosis.objects
                .select_related(
                'equipment_instance')
                .prefetch_related(
                'equipment_problem_types')))


EQUIPMENT_INSTANCE_PROBLEM_DIAGNOSIS_REST_API_QUERY_SET = \
EquipmentInstanceProblemDiagnosis.objects \
    .select_related(
    'equipment_instance') \
    .prefetch_related(
    'equipment_problem_types',
    Prefetch(
        lookup='equipment_instance_alarm_periods',
        queryset=
        EquipmentInstanceAlarmPeriod.objects
            .select_related(
            'equipment_instance',
            'alarm_type')),
    Prefetch(
        lookup='equipment_instance_alert_periods',
        queryset=
        EquipmentInstanceAlertPeriod.objects
            .select_related(
            'equipment_unique_type_group',
            'equipment_instance',
            'diagnosis_status')))
