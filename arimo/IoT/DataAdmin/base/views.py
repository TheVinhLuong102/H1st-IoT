from django.db.models import Prefetch

from rest_framework.authentication import BasicAuthentication, RemoteUserAuthentication, SessionAuthentication, TokenAuthentication
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.renderers import CoreJSONRenderer, JSONRenderer
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from silk.profiling.profiler import silk_profile

from .filters import \
    GlobalConfigFilter, \
    DataTypeFilter, \
    NumericMeasurementUnitFilter, \
    EquipmentDataFieldTypeFilter, \
    EquipmentGeneralTypeFilter, \
    EquipmentComponentFilter, \
    EquipmentDataFieldFilter, \
    EquipmentUniqueTypeGroupFilter, \
    EquipmentUniqueTypeFilter, \
    EquipmentFacilityFilter, \
    EquipmentInstanceFilter, \
    EquipmentInstanceDataFieldDailyAggFilter, \
    EquipmentSystemFilter, \
    ErrorFilter

from .models import \
    GlobalConfig, \
    DataType, \
    NumericMeasurementUnit, \
    EquipmentDataFieldType, \
    EquipmentGeneralType, \
    EquipmentComponent, \
    EquipmentDataField, \
    EquipmentUniqueTypeGroup, \
    EquipmentUniqueType, \
    EquipmentFacility, \
    EquipmentInstance, \
    EquipmentInstanceDataFieldDailyAgg, \
    EquipmentSystem, \
    Error

from .serializers import \
    GlobalConfigSerializer, \
    DataTypeSerializer, \
    NumericMeasurementUnitSerializer, \
    EquipmentDataFieldTypeSerializer, \
    EquipmentGeneralTypeSerializer, \
    EquipmentComponentSerializer, \
    EquipmentDataFieldSerializer, \
    EquipmentUniqueTypeGroupSerializer, \
    EquipmentUniqueTypeSerializer, \
    EquipmentFacilitySerializer, \
    EquipmentInstanceSerializer, \
    EquipmentInstanceDataFieldDailyAggSerializer, \
    EquipmentSystemSerializer, \
    ErrorSerializer


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
    queryset = GlobalConfig.objects.all()

    serializer_class = GlobalConfigSerializer

    authentication_classes = \
        BasicAuthentication, \
        RemoteUserAuthentication, \
        SessionAuthentication, \
        TokenAuthentication

    permission_classes = IsAuthenticated,

    lookup_field = 'key'

    lookup_url_kwarg = 'global_config_key'

    filter_class = GlobalConfigFilter

    ordering_fields = 'key',

    ordering = 'key',

    pagination_class = None

    renderer_classes = \
        CoreJSONRenderer, \
        JSONRenderer

    @silk_profile(name='REST API: Global Configs')
    def list(self, request, *args, **kwargs):
        return super(type(self), self).list(request, *args, **kwargs)

    @silk_profile(name='REST API: Global Config')
    def retrieve(self, request, *args, **kwargs):
        return super(type(self), self).retrieve(request, *args, **kwargs)


class DataTypeViewSet(ReadOnlyModelViewSet):
    """
    list:
    `GET` an filterable, unpaginated list of 2 Data Types named "cat" and "num"

    retrieve:
    `GET` the Data Type specified by `name` "cat" or "num"
    """
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

    filter_class = DataTypeFilter

    ordering_fields = 'name',

    ordering = 'name',

    pagination_class = None

    renderer_classes = \
        CoreJSONRenderer, \
        JSONRenderer

    @silk_profile(name='REST API: Data Types')
    def list(self, request, *args, **kwargs):
        return super(type(self), self).list(request, *args, **kwargs)

    @silk_profile(name='REST API: Data Type')
    def retrieve(self, request, *args, **kwargs):
        return super(type(self), self).retrieve(request, *args, **kwargs)


class NumericMeasurementUnitViewSet(ModelViewSet):
    """
    list:
    `GET` a filterable, unpaginated list of Numeric Measurement Units

    retrieve:
    `GET` the Numeric Measurement Unit specified by `name`

    create:
    `POST` a new Numeric Measurement Unit by `name`

    update:
    `PUT` updated data for the Numeric Measurement Unit specified by `name`

    partial_update:
    `PATCH` the Numeric Measurement Unit specified by `name`

    destroy:
    `DELETE` the Numeric Measurement Unit specified by `name`
    """
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

    ordering_fields = 'name',

    ordering = 'name',

    pagination_class = None

    renderer_classes = \
        CoreJSONRenderer, \
        JSONRenderer

    @silk_profile(name='REST API: Numeric Measurement Units')
    def list(self, request, *args, **kwargs):
        return super(type(self), self).list(request, *args, **kwargs)

    @silk_profile(name='REST API: Numeric Measurement Unit')
    def retrieve(self, request, *args, **kwargs):
        return super(type(self), self).retrieve(request, *args, **kwargs)


class EquipmentDataFieldTypeViewSet(ReadOnlyModelViewSet):
    """
    list:
    `GET` an unfiltered, unpaginated list of Equipment Data Field Types

    retrieve:
    `GET` the Equipment Data Field Type specified by `name`
    """
    queryset = EquipmentDataFieldType.objects.all()

    serializer_class = EquipmentDataFieldTypeSerializer

    authentication_classes = \
        BasicAuthentication, \
        RemoteUserAuthentication, \
        SessionAuthentication, \
        TokenAuthentication

    permission_classes = IsAuthenticatedOrReadOnly,

    lookup_field = 'name'

    lookup_url_kwarg = 'equipment_data_field_type_name'

    filter_class = EquipmentDataFieldTypeFilter

    ordering_fields = 'name',

    ordering = 'name',

    pagination_class = None

    renderer_classes = \
        CoreJSONRenderer, \
        JSONRenderer

    @silk_profile(name='REST API: Equipment Data Field Types')
    def list(self, request, *args, **kwargs):
        return super(type(self), self).list(request, *args, **kwargs)

    @silk_profile(name='REST API: Equipment Data Field Type')
    def retrieve(self, request, *args, **kwargs):
        return super(type(self), self).retrieve(request, *args, **kwargs)


class EquipmentGeneralTypeViewSet(ModelViewSet):
    """
    list:
    `GET` a filterable, unpaginated list of Equipment General Types

    retrieve:
    `GET` the Equipment General Type specified by `name`

    create:
    `POST` a new Equipment General Type by `name`

    update:
    `PUT` updated data for the Equipment General Type specified by `name`

    partial_update:
    `PATCH` the Equipment General Type specified by `name`

    destroy:
    `DELETE` the Equipment General Type specified by `name`
    """
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

    ordering_fields = 'name',

    ordering = 'name',

    pagination_class = None

    renderer_classes = \
        CoreJSONRenderer, \
        JSONRenderer

    @silk_profile(name='REST API: Equipment General Types')
    def list(self, request, *args, **kwargs):
        return super(type(self), self).list(request, *args, **kwargs)

    @silk_profile(name='REST API: Equipment General Type')
    def retrieve(self, request, *args, **kwargs):
        return super(type(self), self).retrieve(request, *args, **kwargs)


class EquipmentComponentViewSet(ModelViewSet):
    """
    list:
    `GET` a filterable, unpaginated list of Equipment Components

    retrieve:
    `GET` the Equipment Component specified by `id`

    create:
    `POST` a new Equipment Component

    update:
    `PUT` updated data for the Equipment Component specified by `id`

    partial_update:
    `PATCH` the Equipment Component specified by `id`

    destroy:
    `DELETE` the Equipment Component specified by `id`
    """
    queryset = \
        EquipmentComponent.objects \
        .select_related(
            'equipment_general_type') \
        .prefetch_related(
            Prefetch(
                lookup='equipment_data_fields',
                queryset=
                    EquipmentDataField.objects
                    .select_related(
                        'equipment_general_type',
                        'equipment_data_field_type')),
            Prefetch(
                lookup='equipment_unique_types',
                queryset=
                    EquipmentUniqueType.objects
                    .select_related(
                        'equipment_general_type')))

    serializer_class = EquipmentComponentSerializer

    authentication_classes = \
        BasicAuthentication, \
        RemoteUserAuthentication, \
        SessionAuthentication, \
        TokenAuthentication

    permission_classes = IsAuthenticated,

    filter_class = EquipmentComponentFilter

    ordering_fields = \
        'equipment_general_type', \
        'name'

    ordering = \
        'equipment_general_type', \
        'name'

    pagination_class = None

    renderer_classes = \
        CoreJSONRenderer, \
        JSONRenderer

    @silk_profile(name='REST API: Equipment Components')
    def list(self, request, *args, **kwargs):
        return super(type(self), self).list(request, *args, **kwargs)

    @silk_profile(name='REST API: Equipment Component')
    def retrieve(self, request, *args, **kwargs):
        return super(type(self), self).retrieve(request, *args, **kwargs)


class EquipmentDataFieldViewSet(ModelViewSet):
    """
    list:
    `GET` a filterable, unpaginated list of Equipment Data Fields

    retrieve:
    `GET` the Equipment Data Field specified by `id`

    create:
    `POST` a new Equipment Data Field

    update:
    `PUT` updated data for the Equipment Data Field specified by `id`

    partial_update:
    `PATCH` the Equipment Data Field specified by `id`

    destroy:
    `DELETE` the Equipment Data Field specified by `id`
    """
    queryset = \
        EquipmentDataField.objects \
        .select_related(
            'equipment_general_type',
            'equipment_data_field_type',
            'data_type',
            'numeric_measurement_unit') \
        .prefetch_related(
            Prefetch(
                lookup='equipment_components',
                queryset=
                    EquipmentUniqueType.objects
                    .select_related(
                        'equipment_general_type')),
            Prefetch(
                lookup='equipment_unique_types',
                queryset=
                    EquipmentUniqueType.objects
                    .select_related(
                        'equipment_general_type')))

    serializer_class = EquipmentDataFieldSerializer

    authentication_classes = \
        BasicAuthentication, \
        RemoteUserAuthentication, \
        SessionAuthentication, \
        TokenAuthentication

    permission_classes = IsAuthenticated,

    filter_class = EquipmentDataFieldFilter

    ordering_fields = \
        'equipment_general_type', \
        'name', \
        'equipment_data_field_type'

    ordering = \
        'equipment_general_type', \
        'name'

    pagination_class = None

    renderer_classes = \
        CoreJSONRenderer, \
        JSONRenderer

    @silk_profile(name='REST API: Equipment Data Fields')
    def list(self, request, *args, **kwargs):
        return super(type(self), self).list(request, *args, **kwargs)

    @silk_profile(name='REST API: Equipment Data Field')
    def retrieve(self, request, *args, **kwargs):
        return super(type(self), self).retrieve(request, *args, **kwargs)


class EquipmentUniqueTypeGroupViewSet(ModelViewSet):
    """
    list:
    `GET` a filterable, unpaginated list of Equipment Unique Type Groups

    retrieve:
    `GET` the Equipment Unique Type Group specified by `name`

    create:
    `POST` a new Equipment Unique Type Group

    update:
    `PUT` updated data for the Equipment Unique Type Group specified by `name`

    partial_update:
    `PATCH` the Equipment Unique Type Group specified by `name`

    destroy:
    `DELETE` the Equipment Unique Type Group specified by `name`
    """
    queryset = \
        EquipmentUniqueTypeGroup.objects \
        .select_related(
            'equipment_general_type') \
        .prefetch_related(
            Prefetch(
                lookup='equipment_unique_types',
                queryset=
                    EquipmentUniqueType.objects
                    .select_related(
                        'equipment_general_type')),
            Prefetch(
                lookup='equipment_data_fields',
                queryset=
                    EquipmentDataField.objects
                    .select_related(
                        'equipment_general_type',
                        'equipment_data_field_type')))

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

    ordering_fields = \
        'equipment_general_type', \
        'name'

    ordering = \
        'equipment_general_type', \
        'name'

    pagination_class = None

    renderer_classes = \
        CoreJSONRenderer, \
        JSONRenderer

    @silk_profile(name='REST API: Equipment Unique Type Groups')
    def list(self, request, *args, **kwargs):
        return super(type(self), self).list(request, *args, **kwargs)

    @silk_profile(name='REST API: Equipment Unique Type Group')
    def retrieve(self, request, *args, **kwargs):
        return super(type(self), self).retrieve(request, *args, **kwargs)


class EquipmentUniqueTypeViewSet(ModelViewSet):
    """
    list:
    `GET` a filterable, unpaginated list of Equipment Unique Types

    retrieve:
    `GET` the Equipment Unique Type specified by `id`

    create:
    `POST` a new Equipment Unique Type

    update:
    `PUT` updated data for the Equipment Unique Type specified by `id`

    partial_update:
    `PATCH` the Equipment Unique Type specified by `id`

    destroy:
    `DELETE` the Equipment Unique Type specified by `id`
    """
    queryset = \
        EquipmentUniqueType.objects \
        .select_related(
            'equipment_general_type') \
        .prefetch_related(
            Prefetch(
                lookup='data_fields',
                queryset=
                    EquipmentDataField.objects
                    .select_related(
                        'equipment_general_type',
                        'equipment_data_field_type')),
            'groups')

    serializer_class = EquipmentUniqueTypeSerializer

    authentication_classes = \
        BasicAuthentication, \
        RemoteUserAuthentication, \
        SessionAuthentication, \
        TokenAuthentication

    permission_classes = IsAuthenticated,

    filter_class = EquipmentUniqueTypeFilter

    ordering_fields = \
        'equipment_general_type', \
        'name'

    ordering = \
        'equipment_general_type', \
        'name'

    pagination_class = None

    renderer_classes = \
        CoreJSONRenderer, \
        JSONRenderer

    @silk_profile(name='REST API: Equipment Unique Types')
    def list(self, request, *args, **kwargs):
        return super(type(self), self).list(request, *args, **kwargs)

    @silk_profile(name='REST API: Equipment Unique Type')
    def retrieve(self, request, *args, **kwargs):
        return super(type(self), self).retrieve(request, *args, **kwargs)


class EquipmentFacilityViewSet(ModelViewSet):
    """
    list:
    `GET` a filterable, paginated list of Equipment Facilities

    retrieve:
    `GET` the Equipment Facility specified by `name`

    create:
    `POST` a new Equipment Facility

    update:
    `PUT` updated data for the Equipment Facility specified by `name`

    partial_update:
    `PATCH` the Equipment Facility specified by `name`

    destroy:
    `DELETE` the Equipment Facility specified by `name`
    """
    queryset = \
        EquipmentFacility.objects \
        .prefetch_related(
            'equipment_instances')

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

    ordering_fields = 'name',

    ordering = 'name',

    pagination_class = LimitOffsetPagination

    renderer_classes = \
        CoreJSONRenderer, \
        JSONRenderer

    @silk_profile(name='REST API: Equipment Facilities')
    def list(self, request, *args, **kwargs):
        return super(type(self), self).list(request, *args, **kwargs)

    @silk_profile(name='REST API: Equipment Facility')
    def retrieve(self, request, *args, **kwargs):
        return super(type(self), self).retrieve(request, *args, **kwargs)


class EquipmentInstanceViewSet(ModelViewSet):
    """
    list:
    `GET` a filterable, paginated list of Equipment Instances

    retrieve:
    `GET` the Equipment Instance specified by `name`

    create:
    `POST` a new Equipment Instance

    update:
    `PUT` updated data for the Equipment Instance specified by `name`

    partial_update:
    `PATCH` the Equipment Instance specified by `name`

    destroy:
    `DELETE` the Equipment Instance specified by `name`
    """
    queryset = \
        EquipmentInstance.objects \
        .select_related(
            'equipment_general_type',
            'equipment_unique_type', 'equipment_unique_type__equipment_general_type',
            'equipment_facility')

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

    ordering_fields = \
        'equipment_general_type', \
        'equipment_unique_type', \
        'name'

    ordering = \
        'equipment_general_type', \
        'equipment_unique_type', \
        'name'

    pagination_class = LimitOffsetPagination

    renderer_classes = \
        CoreJSONRenderer, \
        JSONRenderer

    @silk_profile(name='REST API: Equipment Instances')
    def list(self, request, *args, **kwargs):
        return super(type(self), self).list(request, *args, **kwargs)

    @silk_profile(name='REST API: Equipment Instance')
    def retrieve(self, request, *args, **kwargs):
        return super(type(self), self).retrieve(request, *args, **kwargs)


class EquipmentInstanceDataFieldDailyAggViewSet(ReadOnlyModelViewSet):
    """
    list:
    `GET` a filterable, paginated list of Equipment Instance Data Field Daily Aggs

    retrieve:
    `GET` the Equipment Instance Data Field Daily Agg specified by `id`
    """
    queryset = \
        EquipmentInstanceDataFieldDailyAgg.objects \
        .select_related(
            'equipment_instance',
            'equipment_data_field', 'equipment_data_field__equipment_general_type', 'equipment_data_field__equipment_data_field_type')

    serializer_class = EquipmentInstanceDataFieldDailyAggSerializer

    authentication_classes = \
        BasicAuthentication, \
        RemoteUserAuthentication, \
        SessionAuthentication, \
        TokenAuthentication

    permission_classes = IsAuthenticated,

    filter_class = EquipmentInstanceDataFieldDailyAggFilter

    ordering_fields = \
        'equipment_instance', \
        'equipment_data_field', \
        'date'

    # ordering = ()   # too numerous to order by default

    pagination_class = LimitOffsetPagination

    renderer_classes = \
        CoreJSONRenderer, \
        JSONRenderer

    @silk_profile(name='REST API: Equipment Instance Data Field Daily Aggregates')
    def list(self, request, *args, **kwargs):
        return super(type(self), self).list(request, *args, **kwargs)

    @silk_profile(name='REST API: Equipment Instance Data Field Daily Aggregate')
    def retrieve(self, request, *args, **kwargs):
        return super(type(self), self).retrieve(request, *args, **kwargs)


class EquipmentSystemViewSet(ModelViewSet):
    """
    list:
    `GET` a filterable, paginated list of Equipment Systems

    retrieve:
    `GET` the Equipment System specified by `id`

    create:
    `POST` a new Equipment System

    update:
    `PUT` updated data for the Equipment System specified by `id`

    partial_update:
    `PATCH` the Equipment System specified by `id`

    destroy:
    `DELETE` the Equipment System specified by `id`
    """
    queryset = \
        EquipmentSystem.objects \
        .select_related(
            'equipment_facility') \
        .prefetch_related(
            'equipment_instances')

    serializer_class = EquipmentSystemSerializer

    authentication_classes = \
        BasicAuthentication, \
        RemoteUserAuthentication, \
        SessionAuthentication, \
        TokenAuthentication

    permission_classes = IsAuthenticated,

    filter_class = EquipmentSystemFilter

    ordering_fields = \
        'name', \
        'date'

    ordering = \
        'name', \
        'date'

    pagination_class = LimitOffsetPagination

    renderer_classes = \
        CoreJSONRenderer, \
        JSONRenderer

    @silk_profile(name='REST API: Equipment Systems')
    def list(self, request, *args, **kwargs):
        return super(type(self), self).list(request, *args, **kwargs)

    @silk_profile(name='REST API: Equipment System')
    def retrieve(self, request, *args, **kwargs):
        return super(type(self), self).retrieve(request, *args, **kwargs)


class ErrorViewSet(ReadOnlyModelViewSet):
    """
    list:
    `GET` a filterable, paginated list of Errors

    retrieve:
    `GET` the Error specified by `key`
    """
    queryset = Error.objects.all()

    serializer_class = ErrorSerializer

    authentication_classes = \
        BasicAuthentication, \
        RemoteUserAuthentication, \
        SessionAuthentication, \
        TokenAuthentication

    permission_classes = IsAuthenticated,

    lookup_field = 'key'

    lookup_url_kwarg = 'error_key'

    filter_class = ErrorFilter

    ordering_fields = 'key',

    ordering = 'key',

    pagination_class = LimitOffsetPagination

    renderer_classes = \
        CoreJSONRenderer, \
        JSONRenderer

    @silk_profile(name='REST API: Errors')
    def list(self, request, *args, **kwargs):
        return super(type(self), self).list(request, *args, **kwargs)

    @silk_profile(name='REST API: Error')
    def retrieve(self, request, *args, **kwargs):
        return super(type(self), self).retrieve(request, *args, **kwargs)
