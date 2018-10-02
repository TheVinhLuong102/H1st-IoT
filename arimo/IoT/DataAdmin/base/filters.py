from rest_framework_filters import FilterSet, RelatedFilter, AllLookupsFilter

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


class DataTypeFilter(FilterSet):
    class Meta:
        model = DataType

        fields = dict(
            name=[
                'exact', 'iexact',
                # 'gt', 'gte', 'lt', 'lte',
                'in',
                'contains', 'icontains',
                'startswith', 'istartswith', 'endswith', 'iendswith',
                # 'range',
                # 'isnull',
                # 'regex', 'iregex'
            ]
        )


class NumericMeasurementUnitFilter(FilterSet):
    class Meta:
        model = NumericMeasurementUnit

        fields = dict(
            name=[
                'exact', 'iexact',
                # 'gt', 'gte', 'lt', 'lte',
                'in',
                'contains', 'icontains',
                'startswith', 'istartswith', 'endswith', 'iendswith',
                # 'range',
                # 'isnull',
                # 'regex', 'iregex'
            ]
        )


class EquipmentDataFieldTypeFilter(FilterSet):
    class Meta:
        model = EquipmentDataFieldType

        fields = dict(
            name=[
                'exact', 'iexact',
                # 'gt', 'gte', 'lt', 'lte',
                'in',
                'contains', 'icontains',
                'startswith', 'istartswith', 'endswith', 'iendswith',
                # 'range',
                # 'isnull',
                # 'regex', 'iregex'
            ]
        )


class EquipmentGeneralTypeFilter(FilterSet):
    class Meta:
        model = EquipmentGeneralType

        fields = dict(
            name=[
                'exact', 'iexact',
                # 'gt', 'gte', 'lt', 'lte',
                'in',
                'contains', 'icontains',
                'startswith', 'istartswith', 'endswith', 'iendswith',
                # 'range',
                # 'isnull',
                # 'regex', 'iregex'
            ]
        )


class EquipmentDataFieldFilter(FilterSet):
    equipment_general_type = \
        RelatedFilter(
            filterset=EquipmentGeneralTypeFilter,
            queryset=EquipmentUniqueType.objects.all())

    equipment_data_field_type = \
        RelatedFilter(
            filterset=EquipmentDataFieldTypeFilter,
            queryset=EquipmentDataFieldType.objects.all())

    data_type = \
        RelatedFilter(
            filterset=DataTypeFilter,
            queryset=DataType.objects.all())

    numeric_measurement_unit = \
        RelatedFilter(
            filterset=NumericMeasurementUnitFilter,
            queryset=NumericMeasurementUnit.objects.all())

    equipment_unique_types = \
        RelatedFilter(
            filterset='EquipmentUniqueTypeFilter',
            queryset=EquipmentUniqueType.objects.all())

    class Meta:
        model = EquipmentDataField

        fields = dict(
            equipment_general_type='__all__',

            equipment_data_field_type='__all__',

            name=[
                'exact', 'iexact',
                # 'gt', 'gte', 'lt', 'lte',
                'in',
                'contains', 'icontains',
                'startswith', 'istartswith', 'endswith', 'iendswith',
                # 'range',
                # 'isnull',
                # 'regex', 'iregex'
            ],

            data_type='__all__',

            nullable='__all__',

            numeric_measurement_unit='__all__',

            lower_numeric_null='__all__',

            upper_numeric_null='__all__',

            default_val='__all__',

            min_val='__all__',

            max_val='__all__',

            equipment_unique_types='__all__'
        )


class EquipmentUniqueTypeGroupFilter(FilterSet):
    class Meta:
        model = EquipmentUniqueTypeGroup

        fields = '__all__'


class EquipmentUniqueTypeFilter(FilterSet):
    class Meta:
        model = EquipmentUniqueType

        fields = '__all__'


class EquipmentFacilityFilter(FilterSet):
    class Meta:
        model = EquipmentFacility

        fields = '__all__'


class EquipmentInstanceFilter(FilterSet):
    class Meta:
        model = EquipmentInstance

        fields = '__all__'


class EquipmentSystemFilter(FilterSet):
    class Meta:
        model = EquipmentSystem

        fields = '__all__'
