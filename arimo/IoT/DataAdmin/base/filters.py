from rest_framework_filters import FilterSet, \
    CharFilter, DateFilter

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

        fields = 'name',


class NumericMeasurementUnitFilter(FilterSet):
    class Meta:
        model = NumericMeasurementUnit

        fields = 'name',


class EquipmentDataFieldTypeFilter(FilterSet):
    class Meta:
        model = EquipmentDataFieldType

        fields = 'name',


class EquipmentGeneralTypeFilter(FilterSet):
    class Meta:
        model = EquipmentGeneralType

        fields = '__all__'


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
