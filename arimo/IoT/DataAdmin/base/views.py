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
from rest_framework.permissions import IsAdminUser, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.renderers import CoreJSONRenderer, JSONRenderer, \
    HTMLFormRenderer, StaticHTMLRenderer, TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.status import \
    HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_204_NO_CONTENT
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet, ModelViewSet, ReadOnlyModelViewSet

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

    permission_classes = \
        IsAuthenticatedOrReadOnly,

    lookup_field = 'name'

    lookup_url_kwarg = 'data_type_name___cat_or_num'

    renderer_classes = \
        CoreJSONRenderer, \
        JSONRenderer

    filter_class = pagination_class = None


class NumericMeasurementUnitViewSet(ModelViewSet):
    queryset = NumericMeasurementUnit.objects.all()

    serializer_class = NumericMeasurementUnitSerializer

    authentication_classes = \
        BasicAuthentication, \
        RemoteUserAuthentication, \
        SessionAuthentication, \
        TokenAuthentication

    permission_classes = \
        IsAuthenticatedOrReadOnly,

    lookup_field = 'name'

    lookup_url_kwarg = 'numeric_measurement_unit_name'

    renderer_classes = \
        CoreJSONRenderer, \
        JSONRenderer

    filter_class = NumericMeasurementUnitFilter

    pagination_class = None


class EquipmentDataFieldTypeViewSet(ReadOnlyModelViewSet):
    queryset = EquipmentDataFieldType.objects.all()

    serializer_class = EquipmentDataFieldTypeSerializer

    authentication_classes = \
        BasicAuthentication, \
        RemoteUserAuthentication, \
        SessionAuthentication, \
        TokenAuthentication

    permission_classes = \
        IsAuthenticatedOrReadOnly,

    lookup_field = 'name'

    lookup_url_kwarg = 'equipment_data_field_type_name___control_or_measure'

    renderer_classes = \
        CoreJSONRenderer, \
        JSONRenderer

    filter_class = pagination_class = None


class EquipmentGeneralTypeViewSet(ModelViewSet):
    queryset = EquipmentGeneralType.objects.all()

    serializer_class = EquipmentGeneralTypeSerializer

    authentication_classes = \
        BasicAuthentication, \
        RemoteUserAuthentication, \
        SessionAuthentication, \
        TokenAuthentication

    permission_classes = \
        IsAuthenticated,

    lookup_field = 'name'

    lookup_url_kwarg = 'equipment_general_type_name'

    renderer_classes = \
        CoreJSONRenderer, \
        JSONRenderer

    filter_class = EquipmentGeneralTypeFilter

    pagination_class = None


class EquipmentDataFieldViewSet(ModelViewSet):
    queryset = EquipmentDataField.objects \
        .select_related('equipment_general_type', 'equipment_data_field_type', 'data_type', 'numeric_measurement_unit') \
        .prefetch_related('equipment_unique_types')

    serializer_class = EquipmentDataFieldSerializer

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

    filter_class = EquipmentDataFieldFilter

    pagination_class = None


class EquipmentUniqueTypeGroupViewSet(ModelViewSet):
    queryset = EquipmentUniqueTypeGroup.objects.all()

    serializer_class = EquipmentUniqueTypeGroupSerializer

    authentication_classes = \
        BasicAuthentication, \
        RemoteUserAuthentication, \
        SessionAuthentication, \
        TokenAuthentication

    permission_classes = \
        IsAuthenticated,

    lookup_field = 'name'

    lookup_url_kwarg = 'equipment_unique_type_group_name'

    # filter_class = EquipmentUniqueTypeGroupFilter

    renderer_classes = \
        CoreJSONRenderer, \
        JSONRenderer

    pagination_class = None


class EquipmentUniqueTypeViewSet(ModelViewSet):
    queryset = EquipmentUniqueType.objects.all()

    serializer_class = EquipmentUniqueTypeSerializer

    authentication_classes = \
        BasicAuthentication, \
        RemoteUserAuthentication, \
        SessionAuthentication, \
        TokenAuthentication

    permission_classes = \
        IsAuthenticated,

    # filter_class = EquipmentUniqueTypeFilter

    renderer_classes = \
        CoreJSONRenderer, \
        JSONRenderer

    pagination_class = None


class EquipmentFacilityViewSet(ModelViewSet):
    queryset = EquipmentFacility.objects.all()

    serializer_class = EquipmentFacilitySerializer

    authentication_classes = \
        BasicAuthentication, \
        RemoteUserAuthentication, \
        SessionAuthentication, \
        TokenAuthentication

    permission_classes = \
        IsAuthenticated,

    lookup_field = 'name'

    lookup_url_kwarg = 'equipment_facility_name'

    # filter_class = EquipmentFacilityFilter

    renderer_classes = \
        CoreJSONRenderer, \
        JSONRenderer

    pagination_class = None


class EquipmentInstanceViewSet(ModelViewSet):
    queryset = EquipmentInstance.objects.all()

    serializer_class = EquipmentInstanceSerializer

    authentication_classes = \
        BasicAuthentication, \
        RemoteUserAuthentication, \
        SessionAuthentication, \
        TokenAuthentication

    permission_classes = \
        IsAuthenticated,

    lookup_field = 'name'

    lookup_url_kwarg = 'equipment_instance_name'

    # filter_class = EquipmentInstanceFilter

    renderer_classes = \
        CoreJSONRenderer, \
        JSONRenderer


class EquipmentSystemViewSet(ModelViewSet):
    queryset = EquipmentSystem.objects.all()

    serializer_class = EquipmentSystemSerializer

    authentication_classes = \
        BasicAuthentication, \
        RemoteUserAuthentication, \
        SessionAuthentication, \
        TokenAuthentication

    permission_classes = \
        IsAuthenticated,

    # filter_class = EquipmentSystemFilter

    renderer_classes = \
        CoreJSONRenderer, \
        JSONRenderer


# request.data
# Response(serializer.data, status=HTTP_201_CREATED)
# Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
