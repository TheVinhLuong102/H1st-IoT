from rest_framework.serializers import ModelSerializer, RelatedField, SlugRelatedField

from drf_writable_nested.serializers import WritableNestedModelSerializer

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
    EquipmentSystem

from ..util import clean_lower_str


class GlobalConfigSerializer(ModelSerializer):
    class Meta:
        model = GlobalConfig

        fields = \
            'key', \
            'value'


class DataTypeSerializer(ModelSerializer):
    class Meta:
        model = DataType
        fields = 'name',


class NumericMeasurementUnitSerializer(ModelSerializer):
    class Meta:
        model = NumericMeasurementUnit

        fields = \
            'name', \
            'description'


class EquipmentDataFieldTypeSerializer(ModelSerializer):
    class Meta:
        model = EquipmentDataFieldType
        fields = 'name',


class EquipmentGeneralTypeSerializer(ModelSerializer):
    class Meta:
        model = EquipmentGeneralType
        fields = 'name',


class EquipmentComponentRelatedField(RelatedField):
    def to_internal_value(self, data):
        return EquipmentComponent.objects.update_or_create(
                equipment_general_type=EquipmentGeneralType.objects.get_or_create(name=clean_lower_str(data['equipment_general_type']))[0],
                name=clean_lower_str(data['name']),
                defaults=dict(
                    description=data['description']))[0]

    def to_representation(self, value):
        return dict(
                id=value.id,
                equipment_general_type=value.equipment_general_type.name,
                name=value.name,
                description=value.description)


class EquipmentDataFieldRelatedField(RelatedField):
    def to_internal_value(self, data):
        return EquipmentDataField.objects.update_or_create(
                equipment_general_type=EquipmentGeneralType.objects.get_or_create(name=clean_lower_str(data['equipment_general_type']))[0],
                name=clean_lower_str(data['name']),
                defaults=dict(
                    equipment_data_field_type=EquipmentDataFieldType.objects.get(name=clean_lower_str(data['equipment_data_field_type'])),
                    data_type=DataType.objects.get(name=clean_lower_str(data['data_type'])),
                    numeric_measurement_unit=NumericMeasurementUnit.objects.get_or_create(name=data['numeric_measurement_unit'].strip())[0],
                    lower_numeric_null=data['lower_numeric_null'],
                    upper_numeric_null=data['upper_numeric_null'],
                    default_val=data['default_val'],
                    min_val=data['min_val'],
                    max_val=data['max_val']))[0]

    def to_representation(self, value):
        return dict(
                id=value.id,
                equipment_general_type=value.equipment_general_type.name,
                name=value.name,
                description=value.description,
                equipment_data_field_type=value.equipment_data_field_type.name,
                data_type=value.data_type.name
                    if value.data_type
                    else None,
                numeric_measurement_unit=value.numeric_measurement_unit.name
                    if value.numeric_measurement_unit
                    else None,
                lower_numeric_null=value.lower_numeric_null,
                upper_numeric_null=value.upper_numeric_null,
                default_val=value.default_val,
                min_val=value.min_val,
                max_val=value.max_val)


class EquipmentUniqueTypeRelatedField(RelatedField):
    def to_internal_value(self, data):
        return EquipmentUniqueType.objects.update_or_create(
                equipment_general_type=EquipmentGeneralType.objects.get_or_create(name=clean_lower_str(data['equipment_general_type']))[0],
                name=clean_lower_str(data['name']),
                defaults=dict(
                    description=data['description']))[0]

    def to_representation(self, value):
        return dict(
                equipment_general_type=value.equipment_general_type.name,
                name=value.name,
                description=value.description)


class EquipmentUniqueTypeGroupRelatedField(RelatedField):
    def to_internal_value(self, data):
        return EquipmentUniqueTypeGroup.objects.update_or_create(
                equipment_general_type=EquipmentGeneralType.objects.get_or_create(name=clean_lower_str(data['equipment_general_type']))[0],
                name=clean_lower_str(data['name']),
                defaults=dict(
                    description=data['description']))[0]

    def to_representation(self, value):
        return dict(
                equipment_general_type=value.equipment_general_type.name,
                name=value.name,
                description=value.description)


class EquipmentComponentSerializer(WritableNestedModelSerializer):
    equipment_general_type = \
        SlugRelatedField(
            queryset=EquipmentGeneralType.objects.all(), read_only=False,
            slug_field='name',
            many=False,
            required=True)

    equipment_data_fields = \
        EquipmentDataFieldRelatedField(
            queryset=EquipmentDataField.objects.all(), read_only=False,
            many=True,
            required=False)

    equipment_unique_types = \
        EquipmentUniqueTypeRelatedField(
            queryset=EquipmentUniqueType.objects.all(), read_only=False,
            many=True,
            required=False)

    class Meta:
        model = EquipmentComponent

        fields = \
            'id', \
            'equipment_general_type', \
            'name', \
            'description', \
            'equipment_data_fields', \
            'equipment_unique_types'


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

    equipment_components = \
        EquipmentComponentRelatedField(
            queryset=EquipmentComponent.objects.all(), read_only=False,
            many=True,
            required=False)

    equipment_unique_types = \
        EquipmentUniqueTypeRelatedField(
            queryset=EquipmentUniqueType.objects.all(), read_only=False,
            many=True,
            required=False)

    class Meta:
        model = EquipmentDataField

        fields = \
            'id', \
            'equipment_general_type', \
            'name', \
            'description', \
            'equipment_data_field_type', \
            'data_type', \
            'numeric_measurement_unit', \
            'lower_numeric_null', \
            'upper_numeric_null', \
            'default_val', \
            'min_val', \
            'max_val', \
            'equipment_components', \
            'equipment_unique_types'


class EquipmentUniqueTypeGroupSerializer(WritableNestedModelSerializer):
    equipment_general_type = \
        SlugRelatedField(
            queryset=EquipmentGeneralType.objects.all(), read_only=False,
            slug_field='name',
            many=False,
            required=True)

    equipment_unique_types = \
        EquipmentUniqueTypeRelatedField(
            queryset=EquipmentUniqueType.objects.all(), read_only=False,
            many=True,
            required=False)

    equipment_components = \
        EquipmentComponentRelatedField(
            queryset=EquipmentComponent.objects.all(), read_only=False,
            many=True,
            required=False)

    equipment_data_fields = \
        EquipmentDataFieldRelatedField(
            queryset=EquipmentDataField.objects.all(), read_only=False,
            many=True,
            required=False)

    class Meta:
        model = EquipmentUniqueTypeGroup

        fields = \
            'equipment_general_type', \
            'name', \
            'description', \
            'equipment_unique_types', \
            'equipment_components', \
            'equipment_data_fields'


class EquipmentUniqueTypeSerializer(WritableNestedModelSerializer):
    equipment_general_type = \
        SlugRelatedField(
            queryset=EquipmentGeneralType.objects.all(), read_only=False,
            slug_field='name',
            many=False,
            required=True)

    equipment_components = \
        EquipmentComponentRelatedField(
            queryset=EquipmentComponent.objects.all(), read_only=False,
            many=True,
            required=False)

    equipment_data_fields = \
        EquipmentDataFieldRelatedField(
            queryset=EquipmentDataField.objects.all(), read_only=False,
            many=True,
            required=False)

    equipment_unique_type_groups = \
        EquipmentUniqueTypeGroupRelatedField(
            queryset=EquipmentUniqueTypeGroup.objects.all(), read_only=False,
            many=True,
            required=False)

    class Meta:
        model = EquipmentUniqueType

        fields = \
            'equipment_general_type', \
            'name', \
            'description', \
            'equipment_components', \
            'equipment_data_fields', \
            'equipment_unique_type_groups'


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
            'info', \
            'equipment_instances'


class EquipmentInstanceSerializer(WritableNestedModelSerializer):
    equipment_general_type = \
        SlugRelatedField(
            queryset=EquipmentGeneralType.objects.all(), read_only=False,
            slug_field='name',
            many=False,
            required=True)

    equipment_unique_type = \
        EquipmentUniqueTypeRelatedField(
            queryset=EquipmentUniqueType.objects.all(), read_only=False,
            many=False,
            required=False)

    equipment_facility = \
        SlugRelatedField(
            queryset=EquipmentFacility.objects.all(), read_only=False,
            slug_field='name',
            many=False,
            required=False)

    equipment_unique_type_groups = \
        EquipmentUniqueTypeGroupRelatedField(
            queryset=EquipmentUniqueTypeGroup.objects.all(), read_only=False,
            many=True,
            required=False)

    class Meta:
        model = EquipmentInstance

        fields = \
            'equipment_general_type', \
            'equipment_unique_type', \
            'equipment_facility', \
            'name', \
            'info', \
            'equipment_unique_type_groups'


class EquipmentInstanceDataFieldDailyAggSerializer(ModelSerializer):
    equipment_instance = \
        SlugRelatedField(
            read_only=True,
            slug_field='name',
            many=False)

    equipment_data_field = \
        EquipmentDataFieldRelatedField(
            read_only=True,
            many=False)

    class Meta:
        model = EquipmentInstanceDataFieldDailyAgg

        fields = \
            'id', \
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
            'daily_max'


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
            many=True,
            required=False)

    class Meta:
        model = EquipmentSystem

        fields = \
            'id', \
            'equipment_facility', \
            'name', \
            'date', \
            'equipment_instances'
