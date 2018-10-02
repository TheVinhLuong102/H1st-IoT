from rest_framework.authentication import \
    BasicAuthentication, RemoteUserAuthentication, SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.renderers import CoreJSONRenderer, JSONRenderer
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet


from .filters import \
    EquipmentUniqueTypeGroupServiceConfigFilter, \
    EquipmentUniqueTypeGroupMonitoredDataFieldConfigFilter, \
    EquipmentUniqueTypeGroupDataFieldBlueprintBenchmarkMetricProfileFilter, \
    EquipmentInstanceDailyRiskScoreFilter, \
    EquipmentProblemTypeFilter, \
    AlertDiagnosisStatusFilter
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
from .serializers import \
    EquipmentUniqueTypeGroupDataFieldProfileSerializer, \
    EquipmentUniqueTypeGroupServiceConfigSerializer, \
    EquipmentUniqueTypeGroupMonitoredDataFieldConfigSerializer, \
    BlueprintSerializer, \
    EquipmentUniqueTypeGroupDataFieldBlueprintBenchmarkMetricProfileSerializer, \
    EquipmentInstanceDailyRiskScoreSerializer, \
    EquipmentProblemTypeSerializer, \
    EquipmentProblemPeriodSerializer, \
    AlertDiagnosisStatusSerializer, \
    AlertSerializer


class EquipmentUniqueTypeGroupDataFieldProfileViewSet(ModelViewSet):
    queryset = EquipmentUniqueTypeGroupDataFieldProfile.objects.all()

    serializer_class = EquipmentUniqueTypeGroupDataFieldProfileSerializer

    authentication_classes = \
        BasicAuthentication, \
        RemoteUserAuthentication, \
        SessionAuthentication, \
        TokenAuthentication

    renderer_classes = \
        CoreJSONRenderer, \
        JSONRenderer

    permission_classes = \
        IsAuthenticated, \
        IsAuthenticatedOrReadOnly


class EquipmentUniqueTypeGroupServiceConfigViewSet(ModelViewSet):
    queryset = EquipmentUniqueTypeGroupServiceConfig.objects.all()

    serializer_class = EquipmentUniqueTypeGroupServiceConfigSerializer

    authentication_classes = \
        BasicAuthentication, \
        RemoteUserAuthentication, \
        SessionAuthentication, \
        TokenAuthentication

    renderer_classes = \
        CoreJSONRenderer, \
        JSONRenderer

    permission_classes = \
        IsAuthenticated, \
        IsAuthenticatedOrReadOnly


class EquipmentUniqueTypeGroupMonitoredDataFieldConfigViewSet(ModelViewSet):
    queryset = EquipmentUniqueTypeGroupMonitoredDataFieldConfig.objects.all()

    serializer_class = EquipmentUniqueTypeGroupMonitoredDataFieldConfigSerializer

    authentication_classes = \
        BasicAuthentication, \
        RemoteUserAuthentication, \
        SessionAuthentication, \
        TokenAuthentication

    renderer_classes = \
        CoreJSONRenderer, \
        JSONRenderer

    permission_classes = \
        IsAuthenticated, \
        IsAuthenticatedOrReadOnly


class BlueprintViewSet(ModelViewSet):
    queryset = Blueprint.objects.all()

    serializer_class = BlueprintSerializer

    authentication_classes = \
        BasicAuthentication, \
        RemoteUserAuthentication, \
        SessionAuthentication, \
        TokenAuthentication

    renderer_classes = \
        CoreJSONRenderer, \
        JSONRenderer

    permission_classes = \
        IsAuthenticated, \
        IsAuthenticatedOrReadOnly


class EquipmentUniqueTypeGroupDataFieldBlueprintBenchmarkMetricProfileViewSet(ModelViewSet):
    queryset = EquipmentUniqueTypeGroupDataFieldBlueprintBenchmarkMetricProfile.objects.all()

    serializer_class = EquipmentUniqueTypeGroupDataFieldBlueprintBenchmarkMetricProfileSerializer

    authentication_classes = \
        BasicAuthentication, \
        RemoteUserAuthentication, \
        SessionAuthentication, \
        TokenAuthentication

    renderer_classes = \
        CoreJSONRenderer, \
        JSONRenderer

    permission_classes = \
        IsAuthenticated, \
        IsAuthenticatedOrReadOnly


class EquipmentInstanceDailyRiskScoreViewSet(ModelViewSet):
    queryset = EquipmentInstanceDailyRiskScore.objects.all()

    serializer_class = EquipmentInstanceDailyRiskScoreSerializer

    authentication_classes = \
        BasicAuthentication, \
        RemoteUserAuthentication, \
        SessionAuthentication, \
        TokenAuthentication

    renderer_classes = \
        CoreJSONRenderer, \
        JSONRenderer

    permission_classes = \
        IsAuthenticated, \
        IsAuthenticatedOrReadOnly


class EquipmentProblemTypeViewSet(ModelViewSet):
    queryset = EquipmentProblemType.objects.all()

    serializer_class = EquipmentProblemTypeSerializer

    authentication_classes = \
        BasicAuthentication, \
        RemoteUserAuthentication, \
        SessionAuthentication, \
        TokenAuthentication

    renderer_classes = \
        CoreJSONRenderer, \
        JSONRenderer

    permission_classes = \
        IsAuthenticated, \
        IsAuthenticatedOrReadOnly


class EquipmentProblemPeriodViewSet(ModelViewSet):
    queryset = EquipmentProblemPeriod.objects.all()

    serializer_class = EquipmentProblemPeriodSerializer

    authentication_classes = \
        BasicAuthentication, \
        RemoteUserAuthentication, \
        SessionAuthentication, \
        TokenAuthentication

    renderer_classes = \
        CoreJSONRenderer, \
        JSONRenderer

    permission_classes = \
        IsAuthenticated, \
        IsAuthenticatedOrReadOnly


class AlertDiagnosisStatusViewSet(ModelViewSet):
    queryset = AlertDiagnosisStatus.objects.all()

    serializer_class = AlertDiagnosisStatusSerializer

    authentication_classes = \
        BasicAuthentication, \
        RemoteUserAuthentication, \
        SessionAuthentication, \
        TokenAuthentication

    renderer_classes = \
        CoreJSONRenderer, \
        JSONRenderer

    permission_classes = \
        IsAuthenticated, \
        IsAuthenticatedOrReadOnly


class AlertViewSet(ModelViewSet):
    queryset = Alert.objects.all()

    serializer_class = AlertSerializer

    authentication_classes = \
        BasicAuthentication, \
        RemoteUserAuthentication, \
        SessionAuthentication, \
        TokenAuthentication

    renderer_classes = \
        CoreJSONRenderer, \
        JSONRenderer

    permission_classes = \
        IsAuthenticated, \
        IsAuthenticatedOrReadOnly
