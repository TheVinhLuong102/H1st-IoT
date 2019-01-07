from django.conf.urls import include, url

from rest_framework.routers import DefaultRouter

from .autocompletes import \
    EquipmentProblemTypeAutoComplete, \
    EquipmentProblemDiagnosisAutoComplete

from .views import \
    GlobalConfigViewSet, \
    EquipmentUniqueTypeGroupDataFieldProfileViewSet, \
    EquipmentUniqueTypeGroupServiceConfigViewSet, \
    BlueprintViewSet, \
    EquipmentUniqueTypeGroupDataFieldBlueprintBenchmarkMetricProfileViewSet, \
    EquipmentInstanceDailyRiskScoreViewSet, \
    EquipmentProblemTypeViewSet, \
    EquipmentProblemDiagnosisViewSet, \
    AlertDiagnosisStatusViewSet, \
    AlertViewSet


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
    'equipment-problem-diagnoses',
    EquipmentProblemDiagnosisViewSet)

ROUTER.register(
    'alert-diagnosis-statuses',
    AlertDiagnosisStatusViewSet)

ROUTER.register(
    'alerts',
    AlertViewSet)


URL_PATTERNS = [
    # API URLs
    url(r'^api/pred-maint/', include(ROUTER.urls)),

    # Auto-Complete URLs
    url(r'^{}/$'.format(EquipmentProblemTypeAutoComplete.name),
        EquipmentProblemTypeAutoComplete.as_view(),
        name=EquipmentProblemTypeAutoComplete.name),

    url(r'^{}/$'.format(EquipmentProblemDiagnosisAutoComplete.name),
        EquipmentProblemDiagnosisAutoComplete.as_view(),
        name=EquipmentProblemDiagnosisAutoComplete.name)
]
