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
            queryset=EquipmentGeneralType.objects.all(),
            filterset=EquipmentGeneralTypeFilter)

    equipment_data_field_type = \
        RelatedFilter(
            queryset=EquipmentDataFieldType.objects.all(),
            filterset=EquipmentDataFieldTypeFilter)

    data_type = \
        RelatedFilter(
            queryset=DataType.objects.all(),
            filterset=DataTypeFilter)

    numeric_measurement_unit = \
        RelatedFilter(
            queryset=NumericMeasurementUnit.objects.all(),
            filterset=NumericMeasurementUnitFilter)

    equipment_unique_types = \
        RelatedFilter(
            queryset=EquipmentUniqueType.objects.all(),
            filterset='EquipmentUniqueTypeFilter')

    class Meta:
        model = EquipmentDataField

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
            ],

            lower_numeric_null=[
                'exact',   # 'iexact',
                'gt', 'gte', 'lt', 'lte',
                'in',
                'contains',   # 'icontains',
                'startswith',   # 'istartswith',
                'endswith',   # 'iendswith',
                'range'
                # 'isnull',
                # 'regex', 'iregex',
                # 'contained_by'
            ],

            upper_numeric_null=[
                'exact',   # 'iexact',
                'gt', 'gte', 'lt', 'lte',
                'in',
                'contains',   # 'icontains',
                'startswith',   # 'istartswith',
                'endswith',   # 'iendswith',
                'range'
                # 'isnull',
                # 'regex', 'iregex',
                # 'contained_by'
            ],

            default_val=[
                'exact',   # 'iexact',
                'gt', 'gte', 'lt', 'lte',
                'in',
                'contains',   # 'icontains',
                'startswith',   # 'istartswith',
                'endswith',   # 'iendswith',
                'range',
                'isnull'
                # 'regex', 'iregex',
                # 'contained_by'
            ],

            min_val=[
                'exact',   # 'iexact',
                'gt', 'gte', 'lt', 'lte',
                'in',
                'contains',   # 'icontains',
                'startswith',   # 'istartswith',
                'endswith',   # 'iendswith',
                'range',
                'isnull'
                # 'regex', 'iregex',
                # 'contained_by'
            ],

            max_val=[
                'exact',   # 'iexact',
                'gt', 'gte', 'lt', 'lte',
                'in',
                'contains',   # 'icontains',
                'startswith',   # 'istartswith',
                'endswith',   # 'iendswith',
                'range',
                'isnull'
                # 'regex', 'iregex',
                # 'contained_by'
            ])


class EquipmentUniqueTypeGroupFilter(FilterSet):
    equipment_general_type = \
        RelatedFilter(
            queryset=EquipmentGeneralType.objects.all(),
            filterset=EquipmentGeneralTypeFilter)

    class Meta:
        model = EquipmentUniqueTypeGroup

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
            ])


class EquipmentUniqueTypeFilter(FilterSet):
    equipment_general_type = \
        RelatedFilter(
            queryset=EquipmentGeneralType.objects.all(),
            filterset=EquipmentGeneralTypeFilter)

    class Meta:
        model = EquipmentUniqueType

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
            ])


class EquipmentFacilityFilter(FilterSet):
    class Meta:
        model = EquipmentFacility

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
            ])


class EquipmentInstanceFilter(FilterSet):
    equipment_general_type = \
        RelatedFilter(
            queryset=EquipmentGeneralType.objects.all(),
            filterset=EquipmentGeneralTypeFilter)

    class Meta:
        model = EquipmentInstance

        fields = dict(
            name=[
                'exact', 'iexact',
                # 'gt', 'gte', 'lt', 'lte',
                'in',
                'contains', 'icontains',
                'startswith', 'istartswith', 'endswith', 'iendswith',
                # 'range',
                # 'isnull',
                'regex', 'iregex'
            ])


class EquipmentSystemFilter(FilterSet):
    class Meta:
        model = EquipmentSystem

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
            ])
