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
        CharField(
            source='equipment_general_type.name')

    equipment_data_field_type = \
        CharField(
            source='equipment_data_field_type.name')

    data_type = \
        CharField(
            allow_null=True,
            source='data_type.name')

    numeric_measurement_unit = \
        CharField(
            allow_null=True,
            source='numeric_measurement_unit.name')

    equipment_unique_types = \
        ListField(
            # many=True,
            source='equipment_unique_types.name'
        )

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

        depth = 1


class EquipmentUniqueTypeGroupSerializer(ModelSerializer):
    class Meta:
        model = EquipmentUniqueTypeGroup

        fields = '__all__'


class EquipmentUniqueTypeSerializer(ModelSerializer):
    class Meta:
        model = EquipmentUniqueType

        fields = '__all__'


class EquipmentFacilitySerializer(ModelSerializer):
    class Meta:
        model = EquipmentFacility

        fields = '__all__'


class EquipmentInstanceSerializer(ModelSerializer):
    class Meta:
        model = EquipmentInstance

        fields = '__all__'


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
