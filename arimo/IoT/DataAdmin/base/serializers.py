from rest_framework.serializers import \
    Serializer, CharField, ListField, \
    ModelSerializer, RelatedField, ManyRelatedField, PrimaryKeyRelatedField, SlugRelatedField, StringRelatedField, \
    HyperlinkedModelSerializer, HyperlinkedIdentityField, HyperlinkedRelatedField

from drf_writable_nested.serializers import WritableNestedModelSerializer

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
from ..util import clean_lower_str


class DataTypeSerializer(ModelSerializer):
    class Meta:
        model = DataType
        fields = 'name',


class NumericMeasurementUnitSerializer(ModelSerializer):
    class Meta:
        model = NumericMeasurementUnit
        fields = 'name',


class EquipmentDataFieldTypeSerializer(ModelSerializer):
    class Meta:
        model = EquipmentDataFieldType
        fields = 'name',


class EquipmentGeneralTypeSerializer(ModelSerializer):
    class Meta:
        model = EquipmentGeneralType
        fields = 'name',


class EquipmentUniqueTypeShortFormRelatedField(RelatedField):
    def to_internal_value(self, data):
        return EquipmentUniqueType.objects.get_or_create(
            equipment_general_type=EquipmentGeneralType.objects.get_or_create(name=clean_lower_str(data['equipment_general_type']))[0],
            name=clean_lower_str(data['name']))[0]

    def to_representation(self, value):
        return dict(
            # equipment_general_type=value.equipment_general_type.name,
            name=value.name)


class EquipmentDataFieldSerializer(WritableNestedModelSerializer):
    equipment_general_type = \
        SlugRelatedField(
            queryset=EquipmentGeneralType.objects.all(), read_only=False,
            slug_field='name',
            many=False,
            required=True)

    equipment_data_field_type = \
        SlugRelatedField(
            queryset=EquipmentDataFieldType.objects.all(), read_only=False,
            slug_field='name',
            many=False,
            required=True)

    data_type = \
        SlugRelatedField(
            queryset=DataType.objects.all(), read_only=False,
            slug_field='name',
            many=False,
            required=False)

    numeric_measurement_unit = \
        SlugRelatedField(
            queryset=NumericMeasurementUnit.objects.all(), read_only=False,
            slug_field='name',
            many=False,
            required=False)

    equipment_unique_types = \
        EquipmentUniqueTypeShortFormRelatedField(
            queryset=EquipmentUniqueType.objects.all(), read_only=False,   # .all()
            many=True,
            required=False)

    class Meta:
        model = EquipmentDataField

        fields = \
            'id', \
            'equipment_general_type', \
            'equipment_data_field_type', \
            'name', \
            'data_type', \
            'nullable', \
            'numeric_measurement_unit', \
            'lower_numeric_null', \
            'upper_numeric_null', \
            'default_val', \
            'min_val', \
            'max_val', \
            'equipment_unique_types', \
            'last_updated'


class EquipmentDataFieldShortFormRelatedField(RelatedField):
    def to_representation(self, value):
        return dict(
            equipment_general_type=value.equipment_general_type.name,
            equipment_data_field_type=value.equipment_data_field_type.name,
            name=value.name)


class EquipmentUniqueTypeGroupSerializer(WritableNestedModelSerializer):
    equipment_general_type = \
        SlugRelatedField(
            queryset=EquipmentGeneralType.objects.all(), read_only=False,
            slug_field='name',
            many=False)

    equipment_unique_types = \
        EquipmentUniqueTypeShortFormRelatedField(
            queryset=EquipmentUniqueType.objects.all(), read_only=False,
            many=True)

    equipment_data_fields = \
        EquipmentDataFieldShortFormRelatedField(
            queryset=EquipmentDataField.objects.all(), read_only=False,
            many=True)

    class Meta:
        model = EquipmentUniqueTypeGroup

        fields = \
            'equipment_general_type', \
            'name', \
            'equipment_unique_types', \
            'equipment_data_fields', \
            'last_updated'


class EquipmentUniqueTypeSerializer(WritableNestedModelSerializer):
    equipment_general_type = \
        SlugRelatedField(
            queryset=EquipmentGeneralType.objects.all(), read_only=False,
            slug_field='name',
            many=False)

    data_fields = \
        EquipmentDataFieldShortFormRelatedField(
            queryset=EquipmentDataField.objects.all(), read_only=False,
            many=True)

    groups = \
        SlugRelatedField(
            queryset=EquipmentUniqueTypeGroup.objects.all(), read_only=False,
            slug_field='name',
            many=True)

    class Meta:
        model = EquipmentUniqueType

        fields = \
            'equipment_general_type', \
            'name', \
            'data_fields', \
            'groups', \
            'last_updated'


class EquipmentInstanceSerializer(WritableNestedModelSerializer):
    equipment_general_type = \
        SlugRelatedField(
            queryset=EquipmentGeneralType.objects.all(), read_only=False,
            slug_field='name',
            many=False)

    equipment_unique_type = \
        EquipmentUniqueTypeShortFormRelatedField(
            queryset=EquipmentUniqueType.objects.all(), read_only=False,
            many=False)

    equipment_facility = \
        SlugRelatedField(
            queryset=EquipmentFacility.objects.all(), read_only=False,
            slug_field='name')

    class Meta:
        model = EquipmentInstance

        fields = \
            'equipment_general_type', \
            'equipment_unique_type', \
            'equipment_facility', \
            'name', \
            'last_updated', \
            'data_file_url', \
            'control_data_file_url', \
            'measure_data_file_url'


class EquipmentFacilitySerializer(WritableNestedModelSerializer):
    equipment_instances = \
        SlugRelatedField(
            queryset=EquipmentInstance.objects.all(), read_only=False,
            slug_field='name')

    class Meta:
        model = EquipmentFacility

        fields = \
            'name', \
            'equipment_instances', \
            'last_updated'


class EquipmentSystemSerializer(WritableNestedModelSerializer):
    class Meta:
        model = EquipmentSystem

        fields = '__all__'


# serializer(obj)
# serializer(data=data)
# serializer(objs, many=True)
# serializer.data
# serializer.errors
# serializer.save()
