from rest_framework.serializers import HyperlinkedModelSerializer, ModelSerializer, Serializer


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

        fields = '__all__'


class NumericMeasurementUnitSerializer(ModelSerializer):
    class Meta:
        model = NumericMeasurementUnit

        fields = '__all__'


class EquipmentDataFieldTypeSerializer(ModelSerializer):
    class Meta:
        model = EquipmentDataFieldType

        fields = '__all__'


class EquipmentGeneralTypeSerializer(ModelSerializer):
    class Meta:
        model = EquipmentGeneralType

        fields = '__all__'


class EquipmentDataFieldSerializer(ModelSerializer):
    class Meta:
        model = EquipmentDataField

        fields = '__all__'


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
