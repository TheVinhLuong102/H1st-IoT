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


# class EquipmentUniqueTypeGroupDataFieldProfileFilter(FilterSet):
#     class Meta:
#         model = EquipmentUniqueTypeGroupDataFieldProfile
#         fields = '__all__'


class EquipmentUniqueTypeGroupServiceConfigFilter(FilterSet):
    class Meta:
        model = EquipmentUniqueTypeGroupServiceConfig

        fields = '__all__'


class EquipmentUniqueTypeGroupMonitoredDataFieldConfigFilter(FilterSet):
    class Meta:
        model = EquipmentUniqueTypeGroupMonitoredDataFieldConfig

        fields = '__all__'


# class BlueprintFilter(FilterSet):
#     class Meta:
#         model = Blueprint
#         fields = '__all__'


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


# class EquipmentProblemPeriodFilter(FilterSet):
#     class Meta:
#         model = EquipmentProblemPeriod
#         fields = '__all__'


class AlertDiagnosisStatusFilter(FilterSet):
    class Meta:
        model = AlertDiagnosisStatus

        fields = '__all__'


# class AlertFilter(FilterSet):
#     class Meta:
#         model = Alert
#         fields = '__all__'
