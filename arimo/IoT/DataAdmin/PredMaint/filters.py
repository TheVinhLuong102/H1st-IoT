from rest_framework_filters import FilterSet

from .models import \
    EquipmentUniqueTypeGroupDataFieldProfile, \
    EquipmentUniqueTypeGroupServiceConfig, \
    EquipmentUniqueTypeGroupMonitoredDataFieldConfig, \
    Blueprint, \
    EquipmentUniqueTypeGroupDataFieldBlueprintBenchmarkMetricProfile, \
    EquipmentInstanceDailyRiskScore, \
    EquipmentProblemType, \
    EquipmentProblemPeriod, \
    AlertDiagnosisStatus, \
    Alert


class EquipmentUniqueTypeGroupDataFieldProfileFilter(FilterSet):
     class Meta:
         model = EquipmentUniqueTypeGroupDataFieldProfile

         fields = \
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


class EquipmentUniqueTypeGroupServiceConfigFilter(FilterSet):
    class Meta:
        model = EquipmentUniqueTypeGroupServiceConfig

        fields = \
            'equipment_general_type', \
            'equipment_unique_type_group', \
            'global_excluded_equipment_data_fields', \
            'active', \
            'comments', \
            'last_updated'
            # 'equipment_unique_type_group_monitored_data_field_configs'


class BlueprintFilter(FilterSet):
     class Meta:
         model = Blueprint

         fields = \
             'equipment_general_type', \
             'equipment_unique_type_group', \
             'trained_to_date', \
             'timestamp', \
             'uuid', \
             'active', \
             'last_updated'


class EquipmentUniqueTypeGroupDataFieldBlueprintBenchmarkMetricProfileFilter(FilterSet):
    class Meta:
        model = EquipmentUniqueTypeGroupDataFieldBlueprintBenchmarkMetricProfile

        fields = '__all__'


class EquipmentInstanceDailyRiskScoreFilter(FilterSet):
    class Meta:
        model = EquipmentInstanceDailyRiskScore

        fields = '__all__'


class EquipmentProblemTypeFilter(FilterSet):
    class Meta:
        model = EquipmentProblemType

        fields = '__all__'


class EquipmentProblemPeriodFilter(FilterSet):
     class Meta:
         model = EquipmentProblemPeriod

         fields = \
             'equipment_instance', \
             'from_date', \
             'to_date', \
             'dismissed', \
             'duration', \
             'ongoing', \
             'equipment_problem_types', \
             'comments', \
             'last_updated'


class AlertDiagnosisStatusFilter(FilterSet):
    class Meta:
        model = AlertDiagnosisStatus

        fields = '__all__'


class AlertFilter(FilterSet):
    class Meta:
        model = Alert
        fields = \
            'equipment_general_type', \
            'equipment_unique_type_group', \
            'equipment_instance', \
            'risk_score_name', \
            'threshold', \
            'from_date', \
            'to_date', \
            'duration', \
            'cumulative_excess_risk_score', \
            'approx_average_risk_score', \
            'last_risk_score', \
            'ongoing', \
            'diagnosis_status', \
            'last_updated'
