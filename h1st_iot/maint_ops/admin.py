from django.contrib.admin import ModelAdmin, site, StackedInline
from django.db.models import Prefetch

from silk.profiling.profiler import silk_profile

from h1st_iot.data_mgmt.querysets import \
    EQUIPMENT_DATA_FIELD_ID_ONLY_UNORDERED_QUERYSET, \
    EQUIPMENT_DATA_FIELD_NAME_ONLY_QUERYSET

from .models import \
    GlobalConfig, \
    EquipmentProblemType, \
    EquipmentInstanceAlarmPeriod, \
    EquipmentInstanceProblemDiagnosis, \
    EquipmentInstanceAlertPeriod, \
    AlertDiagnosisStatus

from .querysets import \
    EQUIPMENT_INSTANCE_ALARM_PERIOD_STR_QUERYSET, \
    EQUIPMENT_INSTANCE_ALERT_PERIOD_STR_QUERYSET, \
    EQUIPMENT_INSTANCE_PROBLEM_DIAGNOSIS_ID_ONLY_UNORDERED_QUERYSET, \
    EQUIPMENT_INSTANCE_PROBLEM_DIAGNOSIS_STR_QUERYSET


class GlobalConfigAdmin(ModelAdmin):
    list_display = \
        'key', \
        'value'

    show_full_result_count = False

    @silk_profile(name='Admin: Global Configs')
    def changelist_view(self, *args, **kwargs):
        return super().changelist_view(*args, **kwargs)

    @silk_profile(name='Admin: Global Config')
    def changeform_view(self, *args, **kwargs):
        return super().changeform_view(*args, **kwargs)


site.register(
    GlobalConfig,
    admin_class=GlobalConfigAdmin)


class EquipmentProblemTypeAdmin(ModelAdmin):
    list_display = 'name',

    search_fields = 'name',

    show_full_result_count = False

    @silk_profile(name='Admin: Equipment Problem Types')
    def changelist_view(self, *args, **kwargs):
        return super().changelist_view(*args, **kwargs)

    @silk_profile(name='Admin: Equipment Problem Type')
    def changeform_view(self, *args, **kwargs):
        return super().changeform_view(*args, **kwargs)


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
        'has_associated_equipment_instance_problem_diagnoses'

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
        QUERYSET = \
            super().get_queryset(request=request) \
            .select_related(
                'equipment_instance',
                'equipment_instance__equipment_general_type', 'equipment_instance__equipment_unique_type',
                'alarm_type') \
            .defer(
                'equipment_instance__equipment_unique_type__description', 'equipment_instance__equipment_unique_type__last_updated',
                'equipment_instance__equipment_facility', 'equipment_instance__info', 'equipment_instance__last_updated')

        return QUERYSET \
                .prefetch_related(
                    Prefetch(
                        lookup='equipment_instance_alert_periods',
                        queryset=EQUIPMENT_INSTANCE_ALERT_PERIOD_STR_QUERYSET),
                    Prefetch(
                        lookup='equipment_instance_problem_diagnoses',
                        queryset=EQUIPMENT_INSTANCE_PROBLEM_DIAGNOSIS_STR_QUERYSET)) \
            if request.resolver_match.url_name.endswith('_change') \
          else QUERYSET \
                .defer(
                    'date_range')

    @silk_profile(name='Admin: Equipment Instance Alarm Periods')
    def changelist_view(self, *args, **kwargs):
        return super().changelist_view(*args, **kwargs)

    @silk_profile(name='Admin: Equipment Instance Alarm Period')
    def changeform_view(self, *args, **kwargs):
        return super().changeform_view(*args, **kwargs)


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
        'has_associated_equipment_instance_alert_periods'

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

    # form = EquipmentInstanceProblemDiagnosisForm

    def equipment_problem_type_names(self, obj):
        return ', '.join(equipment_problem_type.name
                         for equipment_problem_type in obj.equipment_problem_types.all())

    def get_queryset(self, request):
        QUERYSET = \
            super().get_queryset(request) \
            .select_related(
                'equipment_instance',
                'equipment_instance__equipment_general_type', 'equipment_instance__equipment_unique_type') \
            .defer(
                'equipment_instance__equipment_unique_type__description', 'equipment_instance__equipment_unique_type__last_updated',
                'equipment_instance__equipment_facility', 'equipment_instance__info', 'equipment_instance__last_updated')

        return QUERYSET \
                .prefetch_related(
                    'equipment_problem_types',
                    Prefetch(
                        lookup='equipment_instance_alarm_periods',
                        queryset=EQUIPMENT_INSTANCE_ALARM_PERIOD_STR_QUERYSET),
                    Prefetch(
                        lookup='equipment_instance_alert_periods',
                        queryset=EQUIPMENT_INSTANCE_ALERT_PERIOD_STR_QUERYSET)) \
            if request.resolver_match.url_name.endswith('_change') \
          else QUERYSET \
                .defer(
                    'date_range') \
                .prefetch_related(
                    'equipment_problem_types')

    @silk_profile(name='Admin: Equipment Problem Diagnoses')
    def changelist_view(self, *args, **kwargs):
        return super().changelist_view(*args, **kwargs)

    @silk_profile(name='Admin: Equipment Problem Diagnosis')
    def changeform_view(self, *args, **kwargs):
        return super().changeform_view(*args, **kwargs)


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
        return super().changelist_view(*args, **kwargs)

    @silk_profile(name='Admin: Alert Diagnosis Status')
    def changeform_view(self, *args, **kwargs):
        return super().changeform_view(*args, **kwargs)


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
        'has_associated_equipment_instance_problem_diagnoses'

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

    # form = EquipmentInstanceAlertPeriodForm

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
        QUERYSET = \
            super().get_queryset(request) \
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

        return QUERYSET \
                .prefetch_related(
                    Prefetch(
                        lookup='equipment_instance_alarm_periods',
                        queryset=EQUIPMENT_INSTANCE_ALARM_PERIOD_STR_QUERYSET),
                    Prefetch(
                        lookup='equipment_instance_problem_diagnoses',
                        queryset=EQUIPMENT_INSTANCE_PROBLEM_DIAGNOSIS_ID_ONLY_UNORDERED_QUERYSET)) \
            if request.resolver_match.url_name.endswith('_change') \
          else QUERYSET \
                .defer(
                    'date_range',
                    'info')

    @silk_profile(name='Admin: Equipment Instance Alert Periods')
    def changelist_view(self, *args, **kwargs):
        return super().changelist_view(*args, **kwargs)

    @silk_profile(name='Admin: Equipment Instance Alert Period')
    def changeform_view(self, *args, **kwargs):
        return super().changeform_view(*args, **kwargs)


site.register(
    EquipmentInstanceAlertPeriod,
    admin_class=EquipmentInstanceAlertPeriodAdmin)
