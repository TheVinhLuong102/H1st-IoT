from rest_framework.authentication import BasicAuthentication, RemoteUserAuthentication, SessionAuthentication, TokenAuthentication
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.renderers import CoreJSONRenderer, JSONRenderer
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from silk.profiling.profiler import silk_profile

from .filters import \
    GlobalConfigFilter, \
    EquipmentUniqueTypeGroupDataFieldProfileFilter, \
    EquipmentUniqueTypeGroupServiceConfigFilter, \
    BlueprintFilter, \
    EquipmentUniqueTypeGroupDataFieldBlueprintBenchmarkMetricProfileFilter, \
    EquipmentInstanceDailyRiskScoreFilter, \
    EquipmentProblemTypeFilter, \
    EquipmentInstanceAlarmPeriodFilter, \
    EquipmentInstanceProblemDiagnosisFilter, \
    AlertDiagnosisStatusFilter, \
    EquipmentInstanceAlertPeriodFilter

from .query_sets import \
    GLOBAL_CONFIG_QUERY_SET, \
    EQUIPMENT_UNIQUE_TYPE_GROUP_DATA_FIELD_PROFILE_REST_API_QUERY_SET, \
    EQUIPMENT_UNIQUE_TYPE_GROUP_SERVICE_CONFIG_REST_API_QUERY_SET, \
    BLUEPRINT_REST_API_QUERY_SET, \
    EQUIPMENT_UNIQUE_TYPE_GROUP_DATA_FIELD_BLUEPRINT_BENCHMARK_METRIC_PROFILE_REST_API_QUERY_SET, \
    EQUIPMENT_INSTANCE_DAILY_RISK_SCORE, \
    EQUIPMENT_PROBLEM_TYPE_QUERY_SET, \
    EQUIPMENT_INSTANCE_ALARM_PERIOD_REST_API_QUERY_SET, \
    ALERT_DIAGNOSIS_STATUS_REST_API_QUERY_SET, \
    EQUIPMENT_INSTANCE_ALERT_PERIOD_REST_API_QUERY_SET, \
    EQUIPMENT_INSTANCE_PROBLEM_DIAGNOSIS_REST_API_QUERY_SET

from .serializers import \
    GlobalConfigSerializer, \
    EquipmentUniqueTypeGroupDataFieldProfileSerializer, \
    EquipmentUniqueTypeGroupServiceConfigSerializer, \
    BlueprintSerializer, \
    EquipmentUniqueTypeGroupDataFieldBlueprintBenchmarkMetricProfileSerializer, \
    EquipmentInstanceDailyRiskScoreSerializer, \
    EquipmentProblemTypeSerializer, \
    EquipmentInstanceAlarmPeriodSerializer, \
    EquipmentInstanceProblemDiagnosisSerializer, \
    AlertDiagnosisStatusSerializer, \
    EquipmentInstanceAlertPeriodSerializer


class GlobalConfigViewSet(ModelViewSet):
    """
    list:
    `GET` a filterable, unpaginated list of Global Configs

    retrieve:
    `GET` the Global Config specified by `key`

    create:
    `POST` a new Global Config by `key`

    update:
    `PUT` updated data for the Global Config specified by `key`

    partial_update:
    `PATCH` the Global Config specified by `key`

    destroy:
    `DELETE` the Global Config specified by `key`
    """
    queryset = GLOBAL_CONFIG_QUERY_SET

    serializer_class = GlobalConfigSerializer

    authentication_classes = \
        BasicAuthentication, \
        RemoteUserAuthentication, \
        SessionAuthentication, \
        TokenAuthentication

    permission_classes = IsAuthenticated,

    filter_class = GlobalConfigFilter

    ordering_fields = 'key',

    ordering = 'key',

    pagination_class = None

    lookup_field = 'key'

    lookup_url_kwarg = 'global_config_key'

    renderer_classes = \
        CoreJSONRenderer, \
        JSONRenderer

    @silk_profile(name='API: Global Configs')
    def list(self, request, *args, **kwargs):
        return super(type(self), self).list(request, *args, **kwargs)

    @silk_profile(name='API: Global Config')
    def retrieve(self, request, *args, **kwargs):
        return super(type(self), self).retrieve(request, *args, **kwargs)


class EquipmentUniqueTypeGroupDataFieldProfileViewSet(ReadOnlyModelViewSet):
    """
    list:
    `GET` a filterable, paginated list of Equipment Unique Type Group Data Field Profiles

    retrieve:
    `GET` the Equipment Unique Type Group Data Field Profile specified by `id`
    """
    queryset = EQUIPMENT_UNIQUE_TYPE_GROUP_DATA_FIELD_PROFILE_REST_API_QUERY_SET

    serializer_class = EquipmentUniqueTypeGroupDataFieldProfileSerializer

    authentication_classes = \
        BasicAuthentication, \
        RemoteUserAuthentication, \
        SessionAuthentication, \
        TokenAuthentication

    permission_classes = IsAuthenticated,

    filter_class = EquipmentUniqueTypeGroupDataFieldProfileFilter

    ordering_fields = \
        'equipment_unique_type_group', \
        'equipment_data_field', \
        'to_date'

    ordering = \
        'equipment_unique_type_group', \
        'equipment_data_field', \
        '-to_date'

    pagination_class = LimitOffsetPagination

    renderer_classes = \
        CoreJSONRenderer, \
        JSONRenderer

    @silk_profile(name='API: Equipment Unique Type Group Data Field Profiles')
    def list(self, request, *args, **kwargs):
        return super(type(self), self).list(request, *args, **kwargs)

    @silk_profile(name='API: Equipment Unique Type Group Data Field Profile')
    def retrieve(self, request, *args, **kwargs):
        return super(type(self), self).retrieve(request, *args, **kwargs)


class EquipmentUniqueTypeGroupServiceConfigViewSet(ReadOnlyModelViewSet):
    """
    list:
    `GET` a filterable, unpaginated list of Equipment Unique Type Group Service Configs

    retrieve:
    `GET` the Equipment Unique Type Group Service Config specified by `id`
    """
    queryset = EQUIPMENT_UNIQUE_TYPE_GROUP_SERVICE_CONFIG_REST_API_QUERY_SET

    serializer_class = EquipmentUniqueTypeGroupServiceConfigSerializer

    authentication_classes = \
        BasicAuthentication, \
        RemoteUserAuthentication, \
        SessionAuthentication, \
        TokenAuthentication

    permission_classes = IsAuthenticated,

    filter_class = EquipmentUniqueTypeGroupServiceConfigFilter

    ordering_fields = \
        'active', \
        'equipment_unique_type_group'

    ordering = \
        '-active', \
        'equipment_unique_type_group'

    pagination_class = None

    renderer_classes = \
        CoreJSONRenderer, \
        JSONRenderer

    @silk_profile(name='API: Equipment Unique Type Group Service Configs')
    def list(self, request, *args, **kwargs):
        return super(type(self), self).list(request, *args, **kwargs)

    @silk_profile(name='API: Equipment Unique Type Group Service Config')
    def retrieve(self, request, *args, **kwargs):
        return super(type(self), self).retrieve(request, *args, **kwargs)


class BlueprintViewSet(ReadOnlyModelViewSet):
    """
    list:
    `GET` a filterable, paginated list of Blueprints

    retrieve:
    `GET` the Blueprint specified by `uuid`
    """
    queryset = BLUEPRINT_REST_API_QUERY_SET

    serializer_class = BlueprintSerializer

    authentication_classes = \
        BasicAuthentication, \
        RemoteUserAuthentication, \
        SessionAuthentication, \
        TokenAuthentication

    permission_classes = IsAuthenticated,

    filter_class = BlueprintFilter

    ordering_fields = \
        'equipment_unique_type_group', \
        'trained_to_date', \
        'timestamp'

    ordering = \
        'equipment_unique_type_group', \
        '-trained_to_date', \
        '-timestamp'

    pagination_class = LimitOffsetPagination

    lookup_field = 'uuid'

    lookup_url_kwarg = 'blueprint_uuid'

    renderer_classes = \
        CoreJSONRenderer, \
        JSONRenderer

    @silk_profile(name='API: Blueprints')
    def list(self, request, *args, **kwargs):
        return super(type(self), self).list(request, *args, **kwargs)

    @silk_profile(name='API: Blueprint')
    def retrieve(self, request, *args, **kwargs):
        return super(type(self), self).retrieve(request, *args, **kwargs)


class EquipmentUniqueTypeGroupDataFieldBlueprintBenchmarkMetricProfileViewSet(ReadOnlyModelViewSet):
    """
    list:
    `GET` a filterable, paginated list of Equipment Unique Type Group Data Field Blueprint Benchmark Metric Profiles

    retrieve:
    `GET` the Equipment Unique Type Group Data Field Blueprint Benchmark Metric Profile specified by `id`
    """
    queryset = EQUIPMENT_UNIQUE_TYPE_GROUP_DATA_FIELD_BLUEPRINT_BENCHMARK_METRIC_PROFILE_REST_API_QUERY_SET

    serializer_class = EquipmentUniqueTypeGroupDataFieldBlueprintBenchmarkMetricProfileSerializer

    authentication_classes = \
        BasicAuthentication, \
        RemoteUserAuthentication, \
        SessionAuthentication, \
        TokenAuthentication

    permission_classes = IsAuthenticated,

    filter_class = EquipmentUniqueTypeGroupDataFieldBlueprintBenchmarkMetricProfileFilter

    ordering_fields = \
        'equipment_unique_type_group', \
        'equipment_data_field', \
        'trained_to_date'

    ordering = \
        'equipment_unique_type_group', \
        'equipment_data_field', \
        '-trained_to_date'

    pagination_class = LimitOffsetPagination

    renderer_classes = \
        CoreJSONRenderer, \
        JSONRenderer

    @silk_profile(name='API: Equipment Unique Type Group Data Field Blueprint Benchmark Metric Profiles')
    def list(self, request, *args, **kwargs):
        return super(type(self), self).list(request, *args, **kwargs)

    @silk_profile(name='API: Equipment Unique Type Group Data Field Blueprint Benchmark Metric Profile')
    def retrieve(self, request, *args, **kwargs):
        return super(type(self), self).retrieve(request, *args, **kwargs)


class EquipmentInstanceDailyRiskScoreViewSet(ReadOnlyModelViewSet):
    """
    list:
    `GET` a filterable, paginated list of Equipment Instance Daily Risk Scores

    retrieve:
    `GET` the Equipment Instance Daily Risk Score specified by `id`
    """
    queryset = EQUIPMENT_INSTANCE_DAILY_RISK_SCORE

    serializer_class = EquipmentInstanceDailyRiskScoreSerializer

    authentication_classes = \
        BasicAuthentication, \
        RemoteUserAuthentication, \
        SessionAuthentication, \
        TokenAuthentication

    permission_classes = IsAuthenticated,

    filter_class = EquipmentInstanceDailyRiskScoreFilter

    ordering_fields = \
        'equipment_unique_type_group', \
        'equipment_instance', \
        'risk_score_name', \
        'date'

    pagination_class = LimitOffsetPagination

    renderer_classes = \
        CoreJSONRenderer, \
        JSONRenderer

    @silk_profile(name='API: Equipment Instance Daily Risk Scores')
    def list(self, request, *args, **kwargs):
        return super(type(self), self).list(request, *args, **kwargs)

    @silk_profile(name='API: Equipment Instance Daily Risk Score')
    def retrieve(self, request, *args, **kwargs):
        return super(type(self), self).retrieve(request, *args, **kwargs)


class EquipmentProblemTypeViewSet(ModelViewSet):
    """
    list:
    `GET` a filterable, unpaginated list of Equipment Problem Types

    retrieve:
    `GET` the Equipment Problem Type specified by `name`

    create:
    `POST` a new Equipment Problem Type by `name`

    update:
    `PUT` updated data for the Equipment Problem Type specified by `name`

    partial_update:
    `PATCH` the Equipment Problem Type specified by `name`

    destroy:
    `DELETE` the Equipment Problem Type specified by `name`
    """
    queryset = EQUIPMENT_PROBLEM_TYPE_QUERY_SET

    serializer_class = EquipmentProblemTypeSerializer

    authentication_classes = \
        BasicAuthentication, \
        RemoteUserAuthentication, \
        SessionAuthentication, \
        TokenAuthentication

    permission_classes = IsAuthenticated,

    filter_class = EquipmentProblemTypeFilter

    ordering_fields = 'name',

    ordering = 'name',

    pagination_class = None

    lookup_field = 'name'

    lookup_url_kwarg = 'equipment_problem_type_name'

    renderer_classes = \
        CoreJSONRenderer, \
        JSONRenderer

    @silk_profile(name='API: Equipment Problem Types')
    def list(self, request, *args, **kwargs):
        return super(type(self), self).list(request, *args, **kwargs)

    @silk_profile(name='API: Equipment Problem Type')
    def retrieve(self, request, *args, **kwargs):
        return super(type(self), self).retrieve(request, *args, **kwargs)


class EquipmentInstanceAlarmPeriodViewSet(ModelViewSet):
    queryset = EQUIPMENT_INSTANCE_ALARM_PERIOD_REST_API_QUERY_SET

    serializer_class = EquipmentInstanceAlarmPeriodSerializer

    authentication_classes = \
        BasicAuthentication, \
        RemoteUserAuthentication, \
        SessionAuthentication, \
        TokenAuthentication

    permission_classes = IsAuthenticated,

    filter_class = EquipmentInstanceAlarmPeriodFilter

    ordering_fields = \
        'equipment_instance', \
        'from_utc_date_time'

    ordering = \
        '-from_utc_date_time'

    pagination_class = LimitOffsetPagination

    renderer_classes = \
        CoreJSONRenderer, \
        JSONRenderer

    @silk_profile(name='API: Equipment Instance Alarm Periods')
    def list(self, request, *args, **kwargs):
        return super(type(self), self).list(request, *args, **kwargs)

    @silk_profile(name='API: Equipment Instance Alarm Period')
    def retrieve(self, request, *args, **kwargs):
        return super(type(self), self).retrieve(request, *args, **kwargs)


class EquipmentInstanceProblemDiagnosisViewSet(ModelViewSet):
    queryset = EQUIPMENT_INSTANCE_PROBLEM_DIAGNOSIS_REST_API_QUERY_SET

    serializer_class = EquipmentInstanceProblemDiagnosisSerializer

    authentication_classes = \
        BasicAuthentication, \
        RemoteUserAuthentication, \
        SessionAuthentication, \
        TokenAuthentication

    permission_classes = IsAuthenticated,

    filter_class = EquipmentInstanceProblemDiagnosisFilter

    ordering_fields = \
        'ongoing', \
        'from_date', \
        'to_date', \
        'equipment_instance', \
        'dismissed'

    ordering = \
        '-ongoing', \
        '-from_date', \
        '-to_date', \
        'dismissed'

    pagination_class = LimitOffsetPagination

    renderer_classes = \
        CoreJSONRenderer, \
        JSONRenderer

    @silk_profile(name='API: Equipment Instance Problem Diagnoses')
    def list(self, request, *args, **kwargs):
        return super(type(self), self).list(request, *args, **kwargs)

    @silk_profile(name='API: Equipment Instance Problem Diagnosis')
    def retrieve(self, request, *args, **kwargs):
        return super(type(self), self).retrieve(request, *args, **kwargs)


class AlertDiagnosisStatusViewSet(ReadOnlyModelViewSet):
    """
    list:
    `GET` a filterable, unpaginated list of Alert Diagnosis Statuses

    retrieve:
    `GET` the Alert Diagnosis Status specified by `name`
    """
    queryset = ALERT_DIAGNOSIS_STATUS_REST_API_QUERY_SET

    serializer_class = AlertDiagnosisStatusSerializer

    authentication_classes = \
        BasicAuthentication, \
        RemoteUserAuthentication, \
        SessionAuthentication, \
        TokenAuthentication

    permission_classes = IsAuthenticatedOrReadOnly,

    filter_class = AlertDiagnosisStatusFilter

    ordering_fields = 'index',

    ordering = 'index',

    pagination_class = None

    lookup_field = 'name'

    lookup_url_kwarg = 'alert_diagnosis_status_name'

    renderer_classes = \
        CoreJSONRenderer, \
        JSONRenderer

    @silk_profile(name='API: Alert Diagnosis Statuses')
    def list(self, request, *args, **kwargs):
        return super(type(self), self).list(request, *args, **kwargs)

    @silk_profile(name='API: Alert Diagnosis Status')
    def retrieve(self, request, *args, **kwargs):
        return super(type(self), self).retrieve(request, *args, **kwargs)


class EquipmentInstanceAlertPeriodViewSet(ModelViewSet):
    """
    list:
    `GET` a filterable, paginated list of Alerts

    retrieve:
    `GET` the Alert specified by `id`

    partial_update:
    `PATCH` the `diagnosis_status` of the Alert specified by `id`
    """
    queryset = EQUIPMENT_INSTANCE_ALERT_PERIOD_REST_API_QUERY_SET

    serializer_class = EquipmentInstanceAlertPeriodSerializer

    authentication_classes = \
        BasicAuthentication, \
        RemoteUserAuthentication, \
        SessionAuthentication, \
        TokenAuthentication

    permission_classes = \
        IsAuthenticated,

    filter_class = EquipmentInstanceAlertPeriodFilter

    ordering_fields = \
        'diagnosis_status', \
        'ongoing', \
        'risk_score_name', \
        'threshold', \
        'cumulative_excess_risk_score'

    ordering = \
        'diagnosis_status', \
        '-ongoing', \
        'risk_score_name', \
        '-threshold', \
        '-cumulative_excess_risk_score'

    pagination_class = LimitOffsetPagination

    renderer_classes = \
        CoreJSONRenderer, \
        JSONRenderer

    @silk_profile(name='API: Equipment Instance Alert Periods')
    def list(self, request, *args, **kwargs):
        return super(type(self), self).list(request, *args, **kwargs)

    @silk_profile(name='API: Equipment Instance Alert Period')
    def retrieve(self, request, *args, **kwargs):
        return super(type(self), self).retrieve(request, *args, **kwargs)
