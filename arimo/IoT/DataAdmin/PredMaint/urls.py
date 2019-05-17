from django.conf.urls import include, url

from rest_framework.routers import DefaultRouter

from .autocompletes import \
    EquipmentProblemTypeAutoComplete, \
    EquipmentInstanceProblemDiagnosisAutoComplete

from .views import \
    GlobalConfigViewSet, \
    EquipmentUniqueTypeGroupDataFieldProfileViewSet, \
    EquipmentUniqueTypeGroupServiceConfigViewSet, \
    BlueprintViewSet, \
    EquipmentUniqueTypeGroupDataFieldBlueprintBenchmarkMetricProfileViewSet, \
    EquipmentInstanceDailyRiskScoreViewSet, \
    EquipmentProblemTypeViewSet, \
    EquipmentInstanceProblemDiagnosisViewSet, \
    AlertDiagnosisStatusViewSet, \
    EquipmentInstanceAlertPeriodViewSet


ROUTER = DefaultRouter()

ROUTER.register(
    'global-configs',
    GlobalConfigViewSet)

ROUTER.register(
    'equipment-unique-type-group-data-field-profiles',
    EquipmentUniqueTypeGroupDataFieldProfileViewSet)

ROUTER.register(
    'equipment-unique-type-group-service-configs',
    EquipmentUniqueTypeGroupServiceConfigViewSet)

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
    'equipment-problem-types',
    EquipmentProblemTypeViewSet)

ROUTER.register(
    'equipment-instance-problem-diagnoses',
    EquipmentInstanceProblemDiagnosisViewSet)

ROUTER.register(
    'alert-diagnosis-statuses',
    AlertDiagnosisStatusViewSet)

ROUTER.register(
    'equipment-instance-alert-periods',
    EquipmentInstanceAlertPeriodViewSet)


URL_PATTERNS = [
    # API URLs
    url(r'^api/pred-maint/', include(ROUTER.urls)),

    # Auto-Complete URLs
    url(r'^{}/$'.format(EquipmentProblemTypeAutoComplete.name),
        EquipmentProblemTypeAutoComplete.as_view(),
        name=EquipmentProblemTypeAutoComplete.name),

    url(r'^{}/$'.format(EquipmentInstanceProblemDiagnosisAutoComplete.name),
        EquipmentInstanceProblemDiagnosisAutoComplete.as_view(),
        name=EquipmentInstanceProblemDiagnosisAutoComplete.name)
]
