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

    renderer_classes = \
        CoreJSONRenderer, \
        JSONRenderer

    permission_classes = \
        IsAuthenticatedOrReadOnly,


class NumericMeasurementUnitViewSet(ModelViewSet):
    queryset = NumericMeasurementUnit.objects.all()

    serializer_class = NumericMeasurementUnitSerializer

    authentication_classes = \
        BasicAuthentication, \
        RemoteUserAuthentication, \
        SessionAuthentication, \
        TokenAuthentication

    renderer_classes = \
        CoreJSONRenderer, \
        JSONRenderer

    permission_classes = \
        IsAuthenticatedOrReadOnly,


class EquipmentDataFieldTypeViewSet(ReadOnlyModelViewSet):
    queryset = EquipmentDataFieldType.objects.all()

    serializer_class = EquipmentDataFieldTypeSerializer

    authentication_classes = \
        BasicAuthentication, \
        RemoteUserAuthentication, \
        SessionAuthentication, \
        TokenAuthentication

    renderer_classes = \
        CoreJSONRenderer, \
        JSONRenderer

    permission_classes = \
        IsAuthenticatedOrReadOnly,


class EquipmentGeneralTypeViewSet(ModelViewSet):
    queryset = EquipmentGeneralType.objects.all()

    serializer_class = EquipmentGeneralTypeSerializer

    authentication_classes = \
        BasicAuthentication, \
        RemoteUserAuthentication, \
        SessionAuthentication, \
        TokenAuthentication

    renderer_classes = \
        CoreJSONRenderer, \
        JSONRenderer

    permission_classes = \
        IsAuthenticated,


class EquipmentDataFieldViewSet(ModelViewSet):
    queryset = EquipmentDataField.objects.all()

    serializer_class = EquipmentDataFieldSerializer

    authentication_classes = \
        BasicAuthentication, \
        RemoteUserAuthentication, \
        SessionAuthentication, \
        TokenAuthentication

    renderer_classes = \
        CoreJSONRenderer, \
        JSONRenderer

    permission_classes = \
        IsAuthenticated,


class EquipmentUniqueTypeGroupViewSet(ModelViewSet):
    queryset = EquipmentUniqueTypeGroup.objects.all()

    serializer_class = EquipmentUniqueTypeGroupSerializer

    authentication_classes = \
        BasicAuthentication, \
        RemoteUserAuthentication, \
        SessionAuthentication, \
        TokenAuthentication

    renderer_classes = \
        CoreJSONRenderer, \
        JSONRenderer

    permission_classes = \
        IsAuthenticated,


class EquipmentUniqueTypeViewSet(ModelViewSet):
    queryset = EquipmentUniqueType.objects.all()

    serializer_class = EquipmentUniqueTypeSerializer

    authentication_classes = \
        BasicAuthentication, \
        RemoteUserAuthentication, \
        SessionAuthentication, \
        TokenAuthentication

    renderer_classes = \
        CoreJSONRenderer, \
        JSONRenderer

    permission_classes = \
        IsAuthenticated,


class EquipmentFacilityViewSet(ModelViewSet):
    queryset = EquipmentFacility.objects.all()

    serializer_class = EquipmentFacilitySerializer

    authentication_classes = \
        BasicAuthentication, \
        RemoteUserAuthentication, \
        SessionAuthentication, \
        TokenAuthentication

    renderer_classes = \
        CoreJSONRenderer, \
        JSONRenderer

    permission_classes = \
        IsAuthenticated,


class EquipmentInstanceViewSet(ModelViewSet):
    queryset = EquipmentInstance.objects.all()

    serializer_class = EquipmentInstanceSerializer

    authentication_classes = \
        BasicAuthentication, \
        RemoteUserAuthentication, \
        SessionAuthentication, \
        TokenAuthentication

    renderer_classes = \
        CoreJSONRenderer, \
        JSONRenderer

    permission_classes = \
        IsAuthenticated,


class EquipmentSystemViewSet(ModelViewSet):
    queryset = EquipmentSystem.objects.all()

    serializer_class = EquipmentSystemSerializer

    authentication_classes = \
        BasicAuthentication, \
        RemoteUserAuthentication, \
        SessionAuthentication, \
        TokenAuthentication

    renderer_classes = \
        CoreJSONRenderer, \
        JSONRenderer

    permission_classes = \
        IsAuthenticated,


# request.data
# Response(serializer.data, status=HTTP_201_CREATED)
# Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
