from django.views.decorators.csrf import csrf_exempt, csrf_protect, requires_csrf_token
from django.http import HttpResponse, Http404, JsonResponse

from rest_framework.decorators import api_view
from rest_framework.generics import GenericAPIView, \
    ListAPIView, CreateAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView, \
    ListCreateAPIView, RetrieveDestroyAPIView, RetrieveUpdateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.mixins import \
    ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin
from rest_framework.views import APIView
from rest_framework.renderers import \
    CoreJSONRenderer, JSONRenderer, \
    HTMLFormRenderer, StaticHTMLRenderer, TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.status import \
    HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_204_NO_CONTENT

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


@api_view(['GET'])
def api_root(request, format=None):
    return Response(dict(
            data_types=reverse('data-type-list', request=request, format=format),
            numeric_measurement_units=reverse('numeric-measurement-unit-list', request=request, format=format),
            equipment_data_field_types=reverse('equipment-data-field-type-list', request=request, format=format),
            equipment_general_types=reverse('equipment-general-type-list', request=request, format=format),
            equipment_unique_type_groups=reverse('equipment-unique-type-group-list', request=request, format=format),
            equipment_unique_types=reverse('equipment-unique-type-list', request=request, format=format),
            equipment_facilities=reverse('equipment-facility-list', request=request, format=format),
            equipment_instances=reverse('equipment-instance-list', request=request, format=format),
            equipment_systems=reverse('equipment-system-list', request=request, format=format)
        ))


class DataTypeList(ListCreateAPIView):
    queryset = DataType.objects.all()
    serializer_class = DataTypeSerializer
    renderer_classes = CoreJSONRenderer, JSONRenderer


class DataTypeDetail(RetrieveUpdateDestroyAPIView):
    queryset = DataType.objects.all()
    serializer_class = DataTypeSerializer
    renderer_classes = CoreJSONRenderer, JSONRenderer


class NumericMeasurementUnitList(ListCreateAPIView):
    queryset = NumericMeasurementUnit.objects.all()
    serializer_class = NumericMeasurementUnitSerializer
    renderer_classes = CoreJSONRenderer, JSONRenderer


class NumericMeasurementUnitDetail(RetrieveUpdateDestroyAPIView):
    queryset = NumericMeasurementUnit.objects.all()
    serializer_class = NumericMeasurementUnitSerializer
    renderer_classes = CoreJSONRenderer, JSONRenderer


class EquipmentDataFieldTypeList(ListCreateAPIView):
    queryset = EquipmentDataFieldType.objects.all()
    serializer_class = EquipmentDataFieldTypeSerializer
    renderer_classes = CoreJSONRenderer, JSONRenderer


class EquipmentDataFieldTypeDetail(RetrieveUpdateDestroyAPIView):
    queryset = EquipmentDataFieldType.objects.all()
    serializer_class = EquipmentDataFieldTypeSerializer
    renderer_classes = CoreJSONRenderer, JSONRenderer


class EquipmentGeneralTypeList(ListCreateAPIView):
    queryset = EquipmentGeneralType.objects.all()
    serializer_class = EquipmentGeneralTypeSerializer
    renderer_classes = CoreJSONRenderer, JSONRenderer


class EquipmentGeneralTypeDetail(RetrieveUpdateDestroyAPIView):
    queryset = EquipmentGeneralType.objects.all()
    serializer_class = EquipmentGeneralTypeSerializer
    renderer_classes = CoreJSONRenderer, JSONRenderer


class EquipmentDataFieldList(ListCreateAPIView):
    queryset = EquipmentDataField.objects.all()
    serializer_class = EquipmentDataFieldSerializer
    renderer_classes = CoreJSONRenderer, JSONRenderer


class EquipmentDataFieldDetail(RetrieveUpdateDestroyAPIView):
    queryset = EquipmentDataField.objects.all()
    serializer_class = EquipmentDataFieldSerializer
    renderer_classes = CoreJSONRenderer, JSONRenderer


class EquipmentUniqueTypeGroupList(ListCreateAPIView):
    queryset = EquipmentUniqueTypeGroup.objects.all()
    serializer_class = EquipmentUniqueTypeGroupSerializer
    renderer_classes = CoreJSONRenderer, JSONRenderer


class EquipmentUniqueTypeGroupDetail(RetrieveUpdateDestroyAPIView):
    queryset = EquipmentUniqueTypeGroup.objects.all()
    serializer_class = EquipmentUniqueTypeGroupSerializer
    renderer_classes = CoreJSONRenderer, JSONRenderer


class EquipmentUniqueTypeList(ListCreateAPIView):
    queryset = EquipmentUniqueType.objects.all()
    serializer_class = EquipmentUniqueTypeSerializer
    renderer_classes = CoreJSONRenderer, JSONRenderer


class EquipmentUniqueTypeDetail(RetrieveUpdateDestroyAPIView):
    queryset = EquipmentUniqueType.objects.all()
    serializer_class = EquipmentUniqueTypeSerializer
    renderer_classes = CoreJSONRenderer, JSONRenderer


class EquipmentFacilityList(ListCreateAPIView):
    queryset = EquipmentFacility.objects.all()
    serializer_class = EquipmentFacilitySerializer
    renderer_classes = CoreJSONRenderer, JSONRenderer


class EquipmentFacilityDetail(RetrieveUpdateDestroyAPIView):
    queryset = EquipmentFacility.objects.all()
    serializer_class = EquipmentFacilitySerializer
    renderer_classes = CoreJSONRenderer, JSONRenderer


class EquipmentInstanceList(ListCreateAPIView):
    queryset = EquipmentInstance.objects.all()
    serializer_class = EquipmentInstanceSerializer
    renderer_classes = CoreJSONRenderer, JSONRenderer


class EquipmentInstanceDetail(RetrieveUpdateDestroyAPIView):
    queryset = EquipmentInstance.objects.all()
    serializer_class = EquipmentInstanceSerializer
    renderer_classes = CoreJSONRenderer, JSONRenderer


class EquipmentSystemList(ListCreateAPIView):
    queryset = EquipmentSystem.objects.all()
    serializer_class = EquipmentSystemSerializer
    renderer_classes = CoreJSONRenderer, JSONRenderer


class EquipmentSystemDetail(RetrieveUpdateDestroyAPIView):
    queryset = EquipmentSystem.objects.all()
    serializer_class = EquipmentSystemSerializer
    renderer_classes = CoreJSONRenderer, JSONRenderer


# request.data
# Response(serializer.data, status=HTTP_201_CREATED)
# Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
