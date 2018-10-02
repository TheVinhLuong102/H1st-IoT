from rest_framework_filters import FilterSet, \
    CharFilter, DateFilter, \
    RelatedFilter, AllLookupsFilter

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
    class Meta:
        model = EquipmentDataField

        fields = '__all__'


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
