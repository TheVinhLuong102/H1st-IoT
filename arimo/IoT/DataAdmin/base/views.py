from django.db.models import Prefetch
from django.http import HttpResponse, Http404, JsonResponse
from django.views.decorators.csrf import csrf_exempt, csrf_protect, requires_csrf_token

from rest_framework.authentication import \
    BasicAuthentication, RemoteUserAuthentication, SessionAuthentication, TokenAuthentication
from rest_framework.decorators import action, api_view
from rest_framework.generics import GenericAPIView, \
    ListAPIView, CreateAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView, \
    ListCreateAPIView, RetrieveDestroyAPIView, RetrieveUpdateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.mixins import \
    ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin
from rest_framework.pagination import CursorPagination, LimitOffsetPagination, PageNumberPagination
from rest_framework.permissions import IsAdminUser, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.renderers import CoreJSONRenderer, JSONRenderer, \
    HTMLFormRenderer, StaticHTMLRenderer, TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.status import \
    HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_204_NO_CONTENT
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet, ModelViewSet, ReadOnlyModelViewSet

from silk.profiling.profiler import silk_profile

from .filters import \
    DataTypeFilter, \
    NumericMeasurementUnitFilter, \
    EquipmentDataFieldTypeFilter, \
    EquipmentGeneralTypeFilter, \
    EquipmentDataFieldFilter, \
    EquipmentUniqueTypeGroupFilter, \
    EquipmentUniqueTypeFilter, \
    EquipmentFacilityFilter, \
    EquipmentInstanceFilter, \
    EquipmentSystemFilter
from .models import \
    DataType, \
    NumericMeasurementUnit, \
    EquipmentDataFieldType, \
    EquipmentGeneralType, \
    EquipmentDataField, \
    EquipmentUniqueTypeGroup, \
    EquipmentUniqueType, \
    EquipmentFacility, \
    EquipmentInstance, \
    EquipmentSystem
from .serializers import \
    DataTypeSerializer, \
    NumericMeasurementUnitSerializer, \
    EquipmentDataFieldTypeSerializer, \
    EquipmentGeneralTypeSerializer, \
    EquipmentDataFieldSerializer, \
    EquipmentUniqueTypeGroupSerializer, \
    EquipmentUniqueTypeSerializer, \
    EquipmentFacilitySerializer, \
    EquipmentInstanceSerializer, \
    EquipmentSystemSerializer


class DataTypeViewSet(ReadOnlyModelViewSet):
    queryset = DataType.objects.all()

    serializer_class = DataTypeSerializer

    authentication_classes = \
        BasicAuthentication, \
        RemoteUserAuthentication, \
        SessionAuthentication, \
        TokenAuthentication

    permission_classes = IsAuthenticatedOrReadOnly,

    lookup_field = 'name'

    lookup_url_kwarg = 'data_type_name___cat_or_num'

    filter_class = pagination_class = None

    renderer_classes = \
        CoreJSONRenderer, \
        JSONRenderer


class NumericMeasurementUnitViewSet(ModelViewSet):
    queryset = NumericMeasurementUnit.objects.all()

    serializer_class = NumericMeasurementUnitSerializer

    authentication_classes = \
        BasicAuthentication, \
        RemoteUserAuthentication, \
        SessionAuthentication, \
        TokenAuthentication

    permission_classes = IsAuthenticatedOrReadOnly,

    lookup_field = 'name'

    lookup_url_kwarg = 'numeric_measurement_unit_name'

    filter_class = NumericMeasurementUnitFilter

    pagination_class = None

    renderer_classes = \
        CoreJSONRenderer, \
        JSONRenderer


class EquipmentDataFieldTypeViewSet(ReadOnlyModelViewSet):
    queryset = EquipmentDataFieldType.objects.all()

    serializer_class = EquipmentDataFieldTypeSerializer

    authentication_classes = \
        BasicAuthentication, \
        RemoteUserAuthentication, \
        SessionAuthentication, \
        TokenAuthentication

    permission_classes = IsAuthenticatedOrReadOnly,

    lookup_field = 'name'

    lookup_url_kwarg = 'equipment_data_field_type_name___control_or_measure'

    filter_class = pagination_class = None

    renderer_classes = \
        CoreJSONRenderer, \
        JSONRenderer


class EquipmentGeneralTypeViewSet(ModelViewSet):
    queryset = EquipmentGeneralType.objects.all()

    serializer_class = EquipmentGeneralTypeSerializer

    authentication_classes = \
        BasicAuthentication, \
        RemoteUserAuthentication, \
        SessionAuthentication, \
        TokenAuthentication

    permission_classes = IsAuthenticated,

    lookup_field = 'name'

    lookup_url_kwarg = 'equipment_general_type_name'

    filter_class = EquipmentGeneralTypeFilter

    pagination_class = None

    renderer_classes = \
        CoreJSONRenderer, \
        JSONRenderer


class EquipmentDataFieldViewSet(ModelViewSet):
    queryset = EquipmentDataField.objects \
        .select_related(
            'equipment_general_type',
            'equipment_data_field_type',
            'data_type',
            'numeric_measurement_unit') \
        .prefetch_related(
            Prefetch(
                'equipment_unique_types',
                queryset=EquipmentUniqueType.objects.select_related('equipment_general_type')))

    serializer_class = EquipmentDataFieldSerializer

    authentication_classes = \
        BasicAuthentication, \
        RemoteUserAuthentication, \
        SessionAuthentication, \
        TokenAuthentication

    permission_classes = IsAuthenticated,

    filter_class = EquipmentDataFieldFilter

    pagination_class = None

    renderer_classes = \
        CoreJSONRenderer, \
        JSONRenderer

    @silk_profile('equipment-data-field-list')
    def list(self, request, *args, **kwargs):
        return super(EquipmentDataFieldViewSet, self).list(request, *args, **kwargs)


class EquipmentUniqueTypeGroupViewSet(ModelViewSet):
    queryset = EquipmentUniqueTypeGroup.objects \
        .select_related(
            'equipment_general_type') \
        .prefetch_related(
            Prefetch(
                'equipment_unique_types',
                queryset=EquipmentUniqueType.objects.select_related('equipment_general_type')),
            Prefetch(
                'equipment_data_fields',
                queryset=EquipmentDataField.objects.select_related('equipment_general_type', 'equipment_data_field_type')))

    serializer_class = EquipmentUniqueTypeGroupSerializer

    authentication_classes = \
        BasicAuthentication, \
        RemoteUserAuthentication, \
        SessionAuthentication, \
        TokenAuthentication

    permission_classes = IsAuthenticated,

    lookup_field = 'name'

    lookup_url_kwarg = 'equipment_unique_type_group_name'

    filter_class = EquipmentUniqueTypeGroupFilter

    pagination_class = None

    renderer_classes = \
        CoreJSONRenderer, \
        JSONRenderer

    @silk_profile('equipment-unique-type-group-list')
    def list(self, request, *args, **kwargs):
        return super(EquipmentUniqueTypeGroupViewSet, self).list(request, *args, **kwargs)


class EquipmentUniqueTypeViewSet(ModelViewSet):
    queryset = EquipmentUniqueType.objects \
        .select_related(
            'equipment_general_type') \
        .prefetch_related(
            Prefetch(
                'data_fields',
                queryset=EquipmentDataField.objects.select_related('equipment_general_type', 'equipment_data_field_type')),
            Prefetch(
                'groups',
                queryset=EquipmentUniqueTypeGroup.objects.select_related('equipment_general_type')))

    serializer_class = EquipmentUniqueTypeSerializer

    authentication_classes = \
        BasicAuthentication, \
        RemoteUserAuthentication, \
        SessionAuthentication, \
        TokenAuthentication

    permission_classes = IsAuthenticated,

    filter_class = EquipmentUniqueTypeFilter

    pagination_class = None

    renderer_classes = \
        CoreJSONRenderer, \
        JSONRenderer

    @silk_profile('equipment-unique-type-list')
    def list(self, request, *args, **kwargs):
        return super(EquipmentUniqueTypeViewSet, self).list(request, *args, **kwargs)


class EquipmentFacilityViewSet(ModelViewSet):
    queryset = EquipmentFacility.objects.all()

    serializer_class = EquipmentFacilitySerializer

    authentication_classes = \
        BasicAuthentication, \
        RemoteUserAuthentication, \
        SessionAuthentication, \
        TokenAuthentication

    permission_classes = IsAuthenticated,

    lookup_field = 'name'

    lookup_url_kwarg = 'equipment_facility_name'

    filter_class = EquipmentFacilityFilter

    pagination_class = None

    renderer_classes = \
        CoreJSONRenderer, \
        JSONRenderer


class EquipmentInstanceViewSet(ModelViewSet):
    queryset = EquipmentInstance.objects \
        .select_related('equipment_general_type', 'equipment_unique_type', 'equipment_unique_type__equipment_general_type', 'equipment_facility')

    serializer_class = EquipmentInstanceSerializer

    authentication_classes = \
        BasicAuthentication, \
        RemoteUserAuthentication, \
        SessionAuthentication, \
        TokenAuthentication

    permission_classes = IsAuthenticated,

    lookup_field = 'name'

    lookup_url_kwarg = 'equipment_instance_name'

    filter_class = EquipmentInstanceFilter

    pagination_class = LimitOffsetPagination

    renderer_classes = \
        CoreJSONRenderer, \
        JSONRenderer

    @silk_profile('equipment-instance-list')
    def list(self, request, *args, **kwargs):
        return super(EquipmentInstanceViewSet, self).list(request, *args, **kwargs)


class EquipmentSystemViewSet(ModelViewSet):
    queryset = EquipmentSystem.objects.all()

    serializer_class = EquipmentSystemSerializer

    authentication_classes = \
        BasicAuthentication, \
        RemoteUserAuthentication, \
        SessionAuthentication, \
        TokenAuthentication

    permission_classes = IsAuthenticated,

    filter_class = EquipmentSystemFilter

    pagination_class = LimitOffsetPagination

    renderer_classes = \
        CoreJSONRenderer, \
        JSONRenderer


# request.data
# Response(serializer.data, status=HTTP_201_CREATED)
# Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
