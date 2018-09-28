from rest_framework.routers import DefaultRouter

from .views import \
    EquipmentUniqueTypeGroupDataFieldProfileViewSet, \
    EquipmentUniqueTypeGroupServiceConfigViewSet, \
    EquipmentUniqueTypeGroupMonitoredDataFieldConfigViewSet, \
    BlueprintViewSet, \
    EquipmentUniqueTypeGroupDataFieldBlueprintBenchmarkMetricProfileViewSet, \
    EquipmentInstanceDailyRiskScoreViewSet, \
    EquipmentProblemTypeViewSet, \
    EquipmentProblemPeriodViewSet, \
    AlertDiagnosisStatusViewSet, \
    AlertViewSet


ROUTER = DefaultRouter()

ROUTER.register(
    'equipment-unique-type-group-data-field-profiles',
    EquipmentUniqueTypeGroupDataFieldProfileViewSet)

ROUTER.register(
    'equipment-unique-type-group-service-configs',
    EquipmentUniqueTypeGroupServiceConfigViewSet)

ROUTER.register(
    'equipment-unique-type-group-monitored-data-field-configs',
    EquipmentUniqueTypeGroupMonitoredDataFieldConfigViewSet)

ROUTER.register(
    'blueprints',
    BlueprintViewSet)

ROUTER.register(
    'equipment-unique-type-group-data-field-blueprint-benchmark-metric-profiles',
    EquipmentUniqueTypeGroupDataFieldBlueprintBenchmarkMetricProfileViewSet)

ROUTER.register(
    'equipment-instance-daily-risk-scores',
    EquipmentInstanceDailyRiskScoreViewSet)

ROUTER.register(
    'equipment-problem-type',
    EquipmentProblemTypeViewSet)

ROUTER.register(
    'equipment-problem-periods',
    EquipmentProblemPeriodViewSet)

ROUTER.register(
    'alert-diagnosis-statuses',
    AlertDiagnosisStatusViewSet)

ROUTER.register(
    'alerts',
    AlertViewSet)


URL_PATTERNS = []
