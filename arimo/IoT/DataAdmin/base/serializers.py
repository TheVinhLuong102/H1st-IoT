from rest_framework.serializers import ModelSerializer, RelatedField, SlugRelatedField

from drf_writable_nested.serializers import WritableNestedModelSerializer

from .models import \
    GlobalConfig, \
    DataType, \
    NumericMeasurementUnit, \
    EquipmentDataFieldType, \
    EquipmentGeneralType, \
    EquipmentDataField, \
    EquipmentUniqueTypeGroup, \
    EquipmentUniqueType, \
    EquipmentFacility, \
    EquipmentInstance, \
    EquipmentInstanceDataFieldDailyAgg, \
    EquipmentSystem

from ..util import clean_lower_str


class GlobalConfigSerializer(ModelSerializer):
    class Meta:
        model = GlobalConfig

        fields = \
            'key', \
            'value', \
            'last_updated'


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
                id=value.id,
                equipment_general_type=value.equipment_general_type.name,
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
            queryset=EquipmentUniqueType.objects.all(), read_only=False,
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
            'numeric_measurement_unit', \
            'lower_numeric_null', \
            'upper_numeric_null', \
            'default_val', \
            'min_val', \
            'max_val', \
            'description', \
            'foreign_lang_description', \
            'equipment_unique_types', \
            'last_updated'


class EquipmentDataFieldShortFormRelatedField(RelatedField):
    def to_internal_value(self, data):
        return EquipmentDataField.objects.get_or_create(
                equipment_general_type=EquipmentGeneralType.objects.get_or_create(name=clean_lower_str(data['equipment_general_type']))[0],
                equipment_data_field_type=EquipmentDataFieldType.objects.get(name=clean_lower_str(data['equipment_data_field_type'])),
                name=clean_lower_str(data['name']))[0]

    def to_representation(self, value):
        return dict(
                id=value.id,
                equipment_general_type=value.equipment_general_type.name,
                equipment_data_field_type=value.equipment_data_field_type.name,
                name=value.name)


class EquipmentUniqueTypeGroupSerializer(WritableNestedModelSerializer):
    equipment_general_type = \
        SlugRelatedField(
            queryset=EquipmentGeneralType.objects.all(), read_only=False,
            slug_field='name',
            many=False,
            required=True)

    equipment_unique_types = \
        EquipmentUniqueTypeShortFormRelatedField(
            queryset=EquipmentUniqueType.objects.all(), read_only=False,
            many=True,
            required=False)

    equipment_data_fields = \
        EquipmentDataFieldShortFormRelatedField(
            queryset=EquipmentDataField.objects.all(), read_only=False,
            many=True,
            required=False)

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
            many=False,
            required=True)

    data_fields = \
        EquipmentDataFieldShortFormRelatedField(
            queryset=EquipmentDataField.objects.all(), read_only=False,
            many=True,
            required=False)

    groups = \
        SlugRelatedField(
            queryset=EquipmentUniqueTypeGroup.objects.all(), read_only=False,
            slug_field='name',
            many=True,
            required=False)

    class Meta:
        model = EquipmentUniqueType

        fields = \
            'id', \
            'equipment_general_type', \
            'name', \
            'data_fields', \
            'groups', \
            'last_updated'


class EquipmentFacilitySerializer(ModelSerializer):
    equipment_instances = \
        SlugRelatedField(
            queryset=EquipmentInstance.objects.all(), read_only=False,
            slug_field='name',
            many=True,
            required=False)

    class Meta:
        model = EquipmentFacility

        fields = \
            'name', \
            'equipment_instances', \
            'last_updated'


class EquipmentInstanceSerializer(WritableNestedModelSerializer):
    equipment_general_type = \
        SlugRelatedField(
            queryset=EquipmentGeneralType.objects.all(), read_only=False,
            slug_field='name',
            many=False,
            required=True)

    equipment_unique_type = \
        EquipmentUniqueTypeShortFormRelatedField(
            queryset=EquipmentUniqueType.objects.all(), read_only=False,
            many=False,
            required=False)

    equipment_facility = \
        SlugRelatedField(
            queryset=EquipmentFacility.objects.all(), read_only=False,
            slug_field='name',
            many=False,
            required=False)

    class Meta:
        model = EquipmentInstance

        fields = \
            'equipment_general_type', \
            'equipment_unique_type', \
            'equipment_facility', \
            'name', \
            'info', \
            'last_updated'


class EquipmentInstanceDataFieldDailyAggSerializer(ModelSerializer):
    equipment_instance = \
        SlugRelatedField(
            read_only=True,
            slug_field='name',
            many=False)

    equipment_data_field = \
        EquipmentDataFieldShortFormRelatedField(
            read_only=True,
            many=False)

    class Meta:
        model = EquipmentInstanceDataFieldDailyAgg

        fields = \
            'equipment_instance', \
            'equipment_data_field', \
            'date', \
            'daily_count', \
            'daily_distinct_value_counts', \
            'daily_min', \
            'daily_outlier_rst_min', \
            'daily_quartile', \
            'daily_median', \
            'daily_mean', \
            'daily_3rd_quartile', \
            'daily_outlier_rst_max', \
            'daily_max', \
            'last_updated'


class EquipmentSystemSerializer(ModelSerializer):
    equipment_facility = \
        SlugRelatedField(
            queryset=EquipmentFacility.objects.all(), read_only=False,
            slug_field='name',
            many=False,
            required=False)

    equipment_instances = \
        SlugRelatedField(
            queryset=EquipmentInstance.objects.all(), read_only=False,
            slug_field='name',
            many=False,
            required=False)

    class Meta:
        model = EquipmentSystem

        fields = \
            'id', \
            'equipment_facility', \
            'name', \
            'date', \
            'equipment_instances', \
            'last_updated'
