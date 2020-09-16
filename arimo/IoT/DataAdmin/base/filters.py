from django.contrib.postgres.fields import JSONField

from rest_framework_filters import CharFilter, FilterSet, RelatedFilter

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


class GlobalConfigFilter(FilterSet):
    class Meta:
        model = GlobalConfig

        fields = dict(
            key=[
                'exact', 'iexact',
                'in',
                'contains', 'icontains',
                'startswith', 'istartswith', 'endswith', 'iendswith',
                'regex', 'iregex'
            ]
        )


class DataTypeFilter(FilterSet):
    class Meta:
        model = DataType

        fields = dict(
            name=['exact']
        )


class NumericMeasurementUnitFilter(FilterSet):
    class Meta:
        model = NumericMeasurementUnit

        fields = dict(
            name=[
                'exact', 'iexact',
                'in',
                'contains', 'icontains',
                'startswith', 'istartswith', 'endswith', 'iendswith',
                'regex', 'iregex'
            ]
        )


class EquipmentDataFieldTypeFilter(FilterSet):
    class Meta:
        model = EquipmentDataFieldType

        fields = dict(
            name=['exact']
        )


class EquipmentGeneralTypeFilter(FilterSet):
    class Meta:
        model = EquipmentGeneralType

        fields = dict(
            name=[
                'exact', 'iexact',
                'in',
                'contains', 'icontains',
                'startswith', 'istartswith', 'endswith', 'iendswith',
                'regex', 'iregex'
            ]
        )


class EquipmentComponentFilter(FilterSet):
    equipment_general_type = \
        RelatedFilter(
            queryset=EquipmentGeneralType.objects.all(),
            filterset=EquipmentGeneralTypeFilter)

    equipment_data_fields = \
        RelatedFilter(
            queryset=EquipmentDataField.objects.all(),
            filterset='EquipmentDataFieldFilter')

    equipment_unique_types = \
        RelatedFilter(
            queryset=EquipmentUniqueType.objects.all(),
            filterset='EquipmentUniqueTypeFilter')

    class Meta:
        model = EquipmentComponent

        fields = dict(
            name=[
                'exact', 'iexact',
                'in',
                'contains', 'icontains',
                'startswith', 'istartswith', 'endswith', 'iendswith',
                'regex', 'iregex'
            ],

            description='__all__')

        filter_overrides = {
            JSONField: dict(
                filter_class=CharFilter
                # 'extra': lambda f: {'lookup_expr': 'icontains'}
            )
        }


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

    equipment_components = \
        RelatedFilter(
            queryset=EquipmentComponent.objects.all(),
            filterset=EquipmentComponentFilter)

    equipment_unique_types = \
        RelatedFilter(
            queryset=EquipmentUniqueType.objects.all(),
            filterset='EquipmentUniqueTypeFilter')

    class Meta:
        model = EquipmentDataField

        fields = dict(
            name=[
                'exact', 'iexact',
                'in',
                'contains', 'icontains',
                'startswith', 'istartswith', 'endswith', 'iendswith',
                'regex', 'iregex'
            ],

            lower_numeric_null=[
                'exact',
                'gt', 'gte', 'lt', 'lte',
                'in',
                'contains',
                'startswith',
                'endswith',
                'range'
            ],

            upper_numeric_null=[
                'exact',
                'gt', 'gte', 'lt', 'lte',
                'in',
                'contains',
                'startswith',
                'endswith',
                'range'
            ],

            default_val=[
                'exact',
                'gt', 'gte', 'lt', 'lte',
                'in',
                'contains',
                'startswith',
                'endswith',
                'range',
                'isnull'
            ],

            min_val=[
                'exact',
                'gt', 'gte', 'lt', 'lte',
                'in',
                'contains',
                'startswith',
                'endswith',
                'range',
                'isnull'
            ],

            max_val=[
                'exact',
                'gt', 'gte', 'lt', 'lte',
                'in',
                'contains',
                'startswith',
                'endswith',
                'range',
                'isnull'
            ],

            description='__all__')

        filter_overrides = {
            JSONField: dict(
                filter_class=CharFilter
                # 'extra': lambda f: {'lookup_expr': 'icontains'}
            )
        }


class EquipmentUniqueTypeGroupFilter(FilterSet):
    equipment_general_type = \
        RelatedFilter(
            queryset=EquipmentGeneralType.objects.all(),
            filterset=EquipmentGeneralTypeFilter)

    equipment_unique_types = \
        RelatedFilter(
            queryset=EquipmentUniqueType.objects.all(),
            filterset='EquipmentUniqueTypeFilter')

    equipment_components = \
        RelatedFilter(
            queryset=EquipmentComponent.objects.all(),
            filterset=EquipmentComponentFilter)

    equipment_data_fields = \
        RelatedFilter(
            queryset=EquipmentDataField.objects.all(),
            filterset=EquipmentDataFieldFilter)

    class Meta:
        model = EquipmentUniqueTypeGroup

        fields = dict(
            name=[
                'exact', 'iexact',
                'in',
                'contains', 'icontains',
                'startswith', 'istartswith', 'endswith', 'iendswith',
                'regex', 'iregex'
            ],

            description='__all__')

        filter_overrides = {
            JSONField: dict(
                filter_class=CharFilter
                # 'extra': lambda f: {'lookup_expr': 'icontains'}
            )
        }


class EquipmentUniqueTypeFilter(FilterSet):
    equipment_general_type = \
        RelatedFilter(
            queryset=EquipmentGeneralType.objects.all(),
            filterset=EquipmentGeneralTypeFilter)

    equipment_components = \
        RelatedFilter(
            queryset=EquipmentComponent.objects.all(),
            filterset=EquipmentComponentFilter)

    equipment_data_fields = \
        RelatedFilter(
            queryset=EquipmentDataField.objects.all(),
            filterset=EquipmentDataFieldFilter)

    equipment_unique_type_groups = \
        RelatedFilter(
            queryset=EquipmentUniqueTypeGroup.objects.all(),
            filterset=EquipmentUniqueTypeGroupFilter)

    class Meta:
        model = EquipmentUniqueType

        fields = dict(
            name=[
                'exact', 'iexact',
                'in',
                'contains', 'icontains',
                'startswith', 'istartswith', 'endswith', 'iendswith',
                'regex', 'iregex'
            ],

            description='__all__')

        filter_overrides = {
            JSONField: dict(
                filter_class=CharFilter
                # 'extra': lambda f: {'lookup_expr': 'icontains'}
            )
        }


class EquipmentFacilityFilter(FilterSet):
    class Meta:
        model = EquipmentFacility

        fields = dict(
            name=[
                'exact', 'iexact',
                'in',
                'contains', 'icontains',
                'startswith', 'istartswith', 'endswith', 'iendswith',
                'regex', 'iregex'
            ],

            info='__all__')

        filter_overrides = {
            JSONField: dict(
                filter_class=CharFilter
                # 'extra': lambda f: {'lookup_expr': 'icontains'}
            )
        }


class EquipmentInstanceFilter(FilterSet):
    equipment_general_type = \
        RelatedFilter(
            queryset=EquipmentGeneralType.objects.all(),
            filterset=EquipmentGeneralTypeFilter)

    equipment_unique_type = \
        RelatedFilter(
            queryset=EquipmentUniqueType.objects.all(),
            filterset=EquipmentUniqueTypeFilter)

    equipment_facility = \
        RelatedFilter(
            queryset=EquipmentFacility.objects.all(),
            filterset=EquipmentFacilityFilter)

    class Meta:
        model = EquipmentInstance

        fields = dict(
            name=[
                'exact', 'iexact',
                'in',
                'contains', 'icontains',
                'startswith', 'istartswith', 'endswith', 'iendswith',
                'regex', 'iregex'
            ],

            info='__all__')

        filter_overrides = {
            JSONField: dict(
                filter_class=CharFilter
                # 'extra': lambda f: {'lookup_expr': 'icontains'}
            )
        }


class EquipmentInstanceDataFieldDailyAggFilter(FilterSet):
    equipment_instance = \
        RelatedFilter(
            queryset=EquipmentInstance.objects.all(),
            filterset=EquipmentInstanceFilter)

    equipment_data_field = \
        RelatedFilter(
            queryset=EquipmentDataField.objects.all(),
            filterset=EquipmentDataFieldFilter)

    class Meta:
        model = EquipmentInstanceDataFieldDailyAgg

        fields = dict(
            date=[
                'exact',
                'gt', 'gte', 'lt', 'lte',
                'in',
                'contains',
                'startswith',
                'endswith',
                'range',
                'isnull',
                'year',
                'year__gt', 'year__gte', 'year__lt', 'year__lte',
                'year__in',
                'year__range',
                'month',
                'month__gt', 'month__gte', 'month__lt', 'month__lte',
                'month__in',
                'month__range'
            ],

            daily_count=[
                'exact',
                'gt', 'gte', 'lt', 'lte',
                'in',
                'contains',
                'startswith',
                'endswith',
                'range',
                'isnull'
            ],

            daily_min=[
                'exact',
                'gt', 'gte', 'lt', 'lte',
                'in',
                'contains',
                'startswith',
                'endswith',
                'range',
                'isnull'
            ],

            daily_outlier_rst_min=[
                'exact',
                'gt', 'gte', 'lt', 'lte',
                'in',
                'contains',
                'startswith',
                'endswith',
                'range',
                'isnull'
            ],

            daily_quartile=[
                'exact',
                'gt', 'gte', 'lt', 'lte',
                'in',
                'contains',
                'startswith',
                'endswith',
                'range',
                'isnull'
            ],

            daily_median=[
                'exact',
                'gt', 'gte', 'lt', 'lte',
                'in',
                'contains',
                'startswith',
                'endswith',
                'range',
                'isnull'
            ],

            daily_mean=[
                'exact',
                'gt', 'gte', 'lt', 'lte',
                'in',
                'contains',
                'startswith',
                'endswith',
                'range',
                'isnull'
            ],

            daily_3rd_quartile=[
                'exact',
                'gt', 'gte', 'lt', 'lte',
                'in',
                'contains',
                'startswith',
                'endswith',
                'range',
                'isnull'
            ],

            daily_outlier_rst_max=[
                'exact',
                'gt', 'gte', 'lt', 'lte',
                'in',
                'contains',
                'startswith',
                'endswith',
                'range',
                'isnull'
            ],

            daily_max=[
                'exact',
                'gt', 'gte', 'lt', 'lte',
                'in',
                'contains',
                'startswith',
                'endswith',
                'range',
                'isnull'
            ])


class EquipmentSystemFilter(FilterSet):
    equipment_facility = \
        RelatedFilter(
            queryset=EquipmentFacility.objects.all(),
            filterset=EquipmentFacilityFilter)

    equipment_instances = \
        RelatedFilter(
            queryset=EquipmentInstance.objects.all(),
            filterset=EquipmentInstanceFilter)

    class Meta:
        model = EquipmentSystem

        fields = dict(
            name=[
                'exact', 'iexact',
                'in',
                'contains', 'icontains',
                'startswith', 'istartswith', 'endswith', 'iendswith',
                'regex', 'iregex'
            ],

            date=[
                'exact',
                'gt', 'gte', 'lt', 'lte',
                'in',
                'contains',
                'startswith',
                'endswith',
                'range',
                'isnull',
                'year',
                'year__gt', 'year__gte', 'year__lt', 'year__lte',
                'year__in',
                'year__range',
                'month',
                'month__gt', 'month__gte', 'month__lt', 'month__lte',
                'month__in',
                'month__range'
            ])
