from django.db.models import Prefetch

from rest_framework.authentication import \
    BasicAuthentication, RemoteUserAuthentication, SessionAuthentication, TokenAuthentication
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.renderers import CoreJSONRenderer, JSONRenderer
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from silk.profiling.profiler import silk_profile

from .filters import \
    EquipmentUniqueTypeGroupDataFieldProfileFilter, \
    EquipmentUniqueTypeGroupServiceConfigFilter, \
    BlueprintFilter, \
    EquipmentUniqueTypeGroupDataFieldBlueprintBenchmarkMetricProfileFilter, \
    EquipmentInstanceDailyRiskScoreFilter, \
    EquipmentProblemTypeFilter, \
    EquipmentDiagnosisFilter, \
    AlertDiagnosisStatusFilter, \
    AlertFilter
from .models import \
    EquipmentUniqueTypeGroupDataFieldProfile, \
    EquipmentUniqueTypeGroupServiceConfig, \
    EquipmentUniqueTypeGroupMonitoredDataFieldConfig, \
    Blueprint, \
    EquipmentUniqueTypeGroupDataFieldBlueprintBenchmarkMetricProfile, \
    EquipmentInstanceDailyRiskScore, \
    EquipmentProblemType, \
    EquipmentProblemPeriod as EquipmentDiagnosis, \
    AlertDiagnosisStatus, \
    Alert
from .serializers import \
    EquipmentUniqueTypeGroupDataFieldProfileSerializer, \
    EquipmentUniqueTypeGroupServiceConfigSerializer, \
    BlueprintSerializer, \
    EquipmentUniqueTypeGroupDataFieldBlueprintBenchmarkMetricProfileSerializer, \
    EquipmentInstanceDailyRiskScoreSerializer, \
    EquipmentProblemTypeSerializer, \
    EquipmentDiagnosisSerializer, \
    AlertDiagnosisStatusSerializer, \
    AlertSerializer

from ..base.models import EquipmentDataField


class EquipmentUniqueTypeGroupDataFieldProfileViewSet(ReadOnlyModelViewSet):
    queryset = EquipmentUniqueTypeGroupDataFieldProfile.objects \
        .select_related(
            'equipment_general_type',
            'equipment_unique_type_group', 'equipment_unique_type_group__equipment_general_type',
            'equipment_data_field', 'equipment_data_field__equipment_general_type', 'equipment_data_field__equipment_data_field_type')

    serializer_class = EquipmentUniqueTypeGroupDataFieldProfileSerializer

    authentication_classes = \
        BasicAuthentication, \
        RemoteUserAuthentication, \
        SessionAuthentication, \
        TokenAuthentication

    renderer_classes = \
        CoreJSONRenderer, \
        JSONRenderer

    permission_classes = IsAuthenticated,

    filter_class = EquipmentUniqueTypeGroupDataFieldProfileFilter

    pagination_class = LimitOffsetPagination

    @silk_profile('equipment-unique-type-group-data-field-profile-list')
    def list(self, request, *args, **kwargs):
        return super(EquipmentUniqueTypeGroupDataFieldProfileViewSet, self).list(request, *args, **kwargs)


class EquipmentUniqueTypeGroupServiceConfigViewSet(ReadOnlyModelViewSet):
    queryset = EquipmentUniqueTypeGroupServiceConfig.objects \
        .select_related(
            'equipment_general_type',
            'equipment_unique_type_group', 'equipment_unique_type_group__equipment_general_type') \
        .prefetch_related(
            Prefetch(
                'equipment_unique_type_group_monitored_data_field_configs',
                queryset=EquipmentUniqueTypeGroupMonitoredDataFieldConfig.objects
                    .select_related(
                        'monitored_equipment_data_field',
                        'monitored_equipment_data_field__equipment_general_type',
                        'monitored_equipment_data_field__equipment_data_field_type')
                    .prefetch_related(
                        Prefetch(
                            'excluded_equipment_data_fields',
                            queryset=EquipmentDataField.objects
                                .select_related(
                                'equipment_general_type',
                                'equipment_data_field_type')))),

            Prefetch(
                'global_excluded_equipment_data_fields',
                queryset=EquipmentDataField.objects
                    .select_related(
                        'equipment_general_type',
                        'equipment_data_field_type')))

    serializer_class = EquipmentUniqueTypeGroupServiceConfigSerializer

    authentication_classes = \
        BasicAuthentication, \
        RemoteUserAuthentication, \
        SessionAuthentication, \
        TokenAuthentication

    permission_classes = IsAuthenticated,

    filter_class = EquipmentUniqueTypeGroupServiceConfigFilter

    pagination_class = None

    renderer_classes = \
        CoreJSONRenderer, \
        JSONRenderer

    @silk_profile('equipment-unique-type-group-service-config-list')
    def list(self, request, *args, **kwargs):
        return super(EquipmentUniqueTypeGroupServiceConfigViewSet, self).list(request, *args, **kwargs)


class BlueprintViewSet(ReadOnlyModelViewSet):
    queryset = Blueprint.objects \
        .select_related(
            'equipment_general_type',
            'equipment_unique_type_group', 'equipment_unique_type_group__equipment_general_type')

    serializer_class = BlueprintSerializer

    authentication_classes = \
        BasicAuthentication, \
        RemoteUserAuthentication, \
        SessionAuthentication, \
        TokenAuthentication

    permission_classes = IsAuthenticated,

    lookup_field = 'uuid'

    lookup_url_kwarg = 'blueprint_uuid'

    renderer_classes = \
        CoreJSONRenderer, \
        JSONRenderer

    filter_class = BlueprintFilter

    pagination_class = LimitOffsetPagination

    @silk_profile('blueprint-list')
    def list(self, request, *args, **kwargs):
        return super(BlueprintViewSet, self).list(request, *args, **kwargs)


class EquipmentUniqueTypeGroupDataFieldBlueprintBenchmarkMetricProfileViewSet(ReadOnlyModelViewSet):
    queryset = \
        EquipmentUniqueTypeGroupDataFieldBlueprintBenchmarkMetricProfile.objects \
        .select_related(
            'equipment_general_type',
            'equipment_unique_type_group', 'equipment_unique_type_group__equipment_general_type',
            'equipment_data_field', 'equipment_data_field__equipment_general_type', 'equipment_data_field__equipment_data_field_type')

    serializer_class = EquipmentUniqueTypeGroupDataFieldBlueprintBenchmarkMetricProfileSerializer

    authentication_classes = \
        BasicAuthentication, \
        RemoteUserAuthentication, \
        SessionAuthentication, \
        TokenAuthentication

    permission_classes = IsAuthenticated,

    filter_class = EquipmentUniqueTypeGroupDataFieldBlueprintBenchmarkMetricProfileFilter

    pagination_class = LimitOffsetPagination

    renderer_classes = \
        CoreJSONRenderer, \
        JSONRenderer

    @silk_profile('equipment-unique-type-group-data-field-blueprint-benchmark-metric-profile-list')
    def list(self, request, *args, **kwargs):
        return super(EquipmentUniqueTypeGroupDataFieldBlueprintBenchmarkMetricProfileViewSet, self).list(request, *args, **kwargs)


class EquipmentInstanceDailyRiskScoreViewSet(ReadOnlyModelViewSet):
    queryset = EquipmentInstanceDailyRiskScore.objects.all()

    serializer_class = EquipmentInstanceDailyRiskScoreSerializer

    authentication_classes = \
        BasicAuthentication, \
        RemoteUserAuthentication, \
        SessionAuthentication, \
        TokenAuthentication

    permission_classes = IsAuthenticated,

    filter_class = EquipmentInstanceDailyRiskScoreFilter

    pagination_class = LimitOffsetPagination

    renderer_classes = \
        CoreJSONRenderer, \
        JSONRenderer


class EquipmentProblemTypeViewSet(ModelViewSet):
    queryset = EquipmentProblemType.objects.all()

    serializer_class = EquipmentProblemTypeSerializer

    authentication_classes = \
        BasicAuthentication, \
        RemoteUserAuthentication, \
        SessionAuthentication, \
        TokenAuthentication

    permission_classes = IsAuthenticated,

    renderer_classes = \
        CoreJSONRenderer, \
        JSONRenderer

    filter_class = EquipmentProblemTypeFilter

    pagination_class = None

    @silk_profile('equipment-problem-type-list')
    def list(self, request, *args, **kwargs):
        return super(EquipmentProblemTypeViewSet, self).list(request, *args, **kwargs)


class EquipmentDiagnosisViewSet(ModelViewSet):
    queryset = \
        EquipmentDiagnosis.objects \
        .select_related('equipment_instance') \
        .prefetch_related('equipment_problem_types')

    serializer_class = EquipmentDiagnosisSerializer

    authentication_classes = \
        BasicAuthentication, \
        RemoteUserAuthentication, \
        SessionAuthentication, \
        TokenAuthentication

    permission_classes = IsAuthenticated,

    renderer_classes = \
        CoreJSONRenderer, \
        JSONRenderer

    filter_class = EquipmentDiagnosisFilter

    pagination_class = LimitOffsetPagination

    @silk_profile('equipment-problem-period-list')
    def list(self, request, *args, **kwargs):
        return super(EquipmentDiagnosisViewSet, self).list(request, *args, **kwargs)


class AlertDiagnosisStatusViewSet(ReadOnlyModelViewSet):
    queryset = AlertDiagnosisStatus.objects.all()

    serializer_class = AlertDiagnosisStatusSerializer

    authentication_classes = \
        BasicAuthentication, \
        RemoteUserAuthentication, \
        SessionAuthentication, \
        TokenAuthentication

    permission_classes = IsAuthenticatedOrReadOnly,

    renderer_classes = \
        CoreJSONRenderer, \
        JSONRenderer

    filter_class = AlertDiagnosisStatusFilter

    pagination_class = None

    @silk_profile('alert-diagnosis-status-list')
    def list(self, request, *args, **kwargs):
        return super(AlertDiagnosisStatusViewSet, self).list(request, *args, **kwargs)


class AlertViewSet(ReadOnlyModelViewSet):
    queryset = \
        Alert.objects \
        .select_related(
            'equipment_general_type',
            'equipment_unique_type_group',
            'equipment_instance',
            'diagnosis_status')

    serializer_class = AlertSerializer

    authentication_classes = \
        BasicAuthentication, \
        RemoteUserAuthentication, \
        SessionAuthentication, \
        TokenAuthentication

    permission_classes = \
        IsAuthenticated,

    renderer_classes = \
        CoreJSONRenderer, \
        JSONRenderer

    filter_class = AlertFilter

    pagination_class = LimitOffsetPagination

    @silk_profile('alert-list')
    def list(self, request, *args, **kwargs):
        return super(AlertViewSet, self).list(request, *args, **kwargs)
