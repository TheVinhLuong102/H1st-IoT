from rest_framework.serializers import \
    Serializer, CharField, ListField, \
    ModelSerializer, RelatedField, ManyRelatedField, PrimaryKeyRelatedField, SlugRelatedField, StringRelatedField, \
    HyperlinkedModelSerializer, HyperlinkedIdentityField, HyperlinkedRelatedField

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


class EquipmentDataFieldSerializer(ModelSerializer):
    equipment_general_type = \
        SlugRelatedField(
            read_only=True,
            slug_field='name')

    equipment_data_field_type = \
        SlugRelatedField(
            read_only=True,
            slug_field='name')

    data_type = \
        SlugRelatedField(
            read_only=True,
            slug_field='name')

    numeric_measurement_unit = \
        SlugRelatedField(
            read_only=True,
            slug_field='name')

    equipment_unique_types = \
        SlugRelatedField(
            many=True,
            read_only=True,
            slug_field='name')

    class Meta:
        model = EquipmentDataField

        fields = \
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

        # depth = 1


class EquipmentDataFieldShortFormRelatedField(RelatedField):
    def to_internal_value(self, data):
        # TODO
        pass

    def to_representation(self, value):
        return dict(
            # equipment_general_type=value.equipment_general_type.name,
            equipment_data_field_type=value.equipment_data_field_type.name,
            name=value.name)


class EquipmentUniqueTypeGroupSerializer(ModelSerializer):
    equipment_general_type = \
        SlugRelatedField(
            read_only=True,
            slug_field='name')

    equipment_unique_types = \
        SlugRelatedField(
            many=True,
            read_only=True,
            slug_field='name')

    equipment_data_fields = \
        EquipmentDataFieldShortFormRelatedField(
            many=True,
            read_only=True)

    class Meta:
        model = EquipmentUniqueTypeGroup

        fields = \
            'equipment_general_type', \
            'name', \
            'equipment_unique_types', \
            'equipment_data_fields', \
            'last_updated'


class EquipmentUniqueTypeSerializer(ModelSerializer):
    equipment_general_type = \
        SlugRelatedField(
            read_only=True,
            slug_field='name')

    data_fields = \
        EquipmentDataFieldShortFormRelatedField(
            many=True,
            read_only=True)

    groups = \
        SlugRelatedField(
            many=True,
            read_only=True,
            slug_field='name')

    class Meta:
        model = EquipmentUniqueType

        fields = \
            'equipment_general_type', \
            'name', \
            'data_fields', \
            'groups', \
            'last_updated'


class EquipmentInstanceSerializer(ModelSerializer):
    equipment_general_type = \
        SlugRelatedField(
            read_only=True,
            slug_field='name')

    equipment_unique_type = \
        SlugRelatedField(
            read_only=True,
            slug_field='name')

    equipment_facility = \
        SlugRelatedField(
            read_only=True,
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


class EquipmentInstanceShortFormRelatedField(RelatedField):
    def to_internal_value(self, data):
        # TODO
        pass

    def to_representation(self, value):
        return dict(
            equipment_general_type=value.equipment_general_type.name,
            equipment_unique_type=value.equipment_unique_type.name,
            equipment_facility=value.equipment_facility.name,
            name=value.name)


class EquipmentFacilitySerializer(ModelSerializer):
    equipment_instances = \
        EquipmentInstanceShortFormRelatedField(
            many=True,
            read_only=True)

    class Meta:
        model = EquipmentFacility

        fields = \
            'name', \
            'equipment_instances', \
            'last_updated'


class EquipmentSystemSerializer(ModelSerializer):
    class Meta:
        model = EquipmentSystem

        fields = '__all__'


# serializer(obj)
# serializer(data=data)
# serializer(objs, many=True)
# serializer.data
# serializer.errors
# serializer.save()
