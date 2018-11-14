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
    EquipmentInstanceDataFieldDailyAgg, \
    EquipmentSystem


class DataTypeFilter(FilterSet):
    class Meta:
        model = DataType

        fields = dict(
            name=[
                'exact'   # , 'iexact',
                # 'gt', 'gte', 'lt', 'lte',
                # 'in',
                # 'contains', 'icontains',
                # 'startswith', 'istartswith', 'endswith', 'iendswith',
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
                'exact'   # , 'iexact',
                # 'gt', 'gte', 'lt', 'lte',
                # 'in',
                # 'contains', 'icontains',
                # 'startswith', 'istartswith', 'endswith', 'iendswith',
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

    equipment_unique_types = \
        RelatedFilter(
            queryset=EquipmentUniqueType.objects.all(),
            filterset='EquipmentUniqueTypeFilter')

    equipment_data_fields = \
        RelatedFilter(
            queryset=EquipmentDataField.objects.all(),
            filterset=EquipmentDataFieldFilter)

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

    data_fields = \
        RelatedFilter(
            queryset=EquipmentDataField.objects.all(),
            filterset=EquipmentDataFieldFilter)

    groups = \
        RelatedFilter(
            queryset=EquipmentUniqueTypeGroup.objects.all(),
            filterset=EquipmentUniqueTypeGroupFilter)

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
    equipment_instances = \
        RelatedFilter(
            queryset=EquipmentInstance.objects.all(),
            filterset='EquipmentInstanceFilter')

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
                # 'gt', 'gte', 'lt', 'lte',
                'in',
                'contains', 'icontains',
                'startswith', 'istartswith', 'endswith', 'iendswith',
                # 'range',
                # 'isnull',
                'regex', 'iregex'
            ])


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
                'exact',   # 'iexact',
                'gt', 'gte', 'lt', 'lte',
                'in',
                'contains',   # 'icontains'
                'startswith',   # 'istartswith'
                'endswith',   # 'iendswith',
                'range',
                'isnull',
                # 'regex', 'iregex',
                'year',   # 'year__iexact'
                'year__gt', 'year__gte', 'year__lt', 'year__lte',
                'year__in',
                # 'year__contains', 'year__icontains',
                # 'year__startswith', 'year__istartswith', 'year__endswith', year__iendswith',
                'year__range',
                # 'year__isnull',
                # 'year__regex', 'year__iregex',
                # 'year__contained_by',
                'month',   # 'month__iexact',
                'month__gt', 'month__gte', 'month__lt', 'month__lte',
                'month__in',
                # 'month__contains', 'month__icontains',
                # 'month__startswith', 'month__istartswith', 'month__endswith', 'month__iendswith'
                'month__range',
                # 'month__isnull',
                # 'month__regex', 'month__iregex',
                # 'month__contained_by',
                # 'day', 'day__iexact',
                # 'day__gt', 'day__gte', 'day__lt', 'day__lte',
                # 'day__in',
                # 'day__contains', 'day__icontains',
                # 'day__startswith', 'day__istartswith', 'day__endswith', 'day__iendswith',
                # 'day__range',
                # 'day__isnull'
                # 'day__regex', 'day__iregex'
                # 'day__contained_by'
                # 'week_day', 'week_day__iexact',
                # 'week_day__gt', 'week_day__gte', 'week_day__lt', 'week_day__lte',
                # 'week_day__in',
                # 'week_day__contains', 'week_day__icontains',
                # 'week_day__startswith', 'week_day__istartswith', 'week_day__endswith', 'week_day__iendswith',
                # 'week_day__range',
                # 'week_day__isnull',
                # 'week_day__regex', 'week_day__iregex'
                # 'week_day__contained_by',
                # 'week', 'week__iexact',
                # 'week__gt', 'week__gte', 'week__lt', 'week__lte',
                # 'week__in',
                # 'week__contains', 'week__icontains',
                # 'week__startswith', 'week__istartswith', 'week__endswith', 'week__iendswith',
                # 'week__range',
                # 'week__isnull',
                # 'week__regex', 'week__iregex',
                # 'week__contained_by',

                # django_filters.exceptions.FieldLookupError: Unsupported lookup 'quarter'
                # 'quarter',   # 'quarter__iexact',
                # 'quarter__gt', 'quarter__gte', 'quarter__lt', 'quarter__lte',
                # 'quarter__in',
                # 'quarter__contains', 'quarter__icontains',
                # 'quarter__startswith', 'quarter__istartswith', 'quarter__endswith', 'quarter__iendswith',
                # 'quarter__range'
                # 'quarter__isnull',
                # 'quarter__regex', 'quarter__iregex',
                # 'quarter__contained_by'

                # 'contained_by'
            ],

            daily_count=[
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

            daily_min=[
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

            daily_outlier_rst_min=[
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

            daily_quartile=[
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

            daily_median=[
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

            daily_mean=[
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

            daily_3rd_quartile=[
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

            daily_outlier_rst_max=[
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

            daily_max=[
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
                # 'gt', 'gte', 'lt', 'lte',
                'in',
                'contains', 'icontains',
                'startswith', 'istartswith', 'endswith', 'iendswith',
                # 'range',
                # 'isnull',
                # 'regex', 'iregex'
            ],

            date=[
                'exact',   # 'iexact',
                'gt', 'gte', 'lt', 'lte',
                'in',
                'contains',   # 'icontains'
                'startswith',   # 'istartswith'
                'endswith',   # 'iendswith',
                'range',
                'isnull',
                # 'regex', 'iregex',
                'year',   # 'year__iexact'
                'year__gt', 'year__gte', 'year__lt', 'year__lte',
                'year__in',
                # 'year__contains', 'year__icontains',
                # 'year__startswith', 'year__istartswith', 'year__endswith', year__iendswith',
                'year__range',
                # 'year__isnull',
                # 'year__regex', 'year__iregex',
                # 'year__contained_by',
                'month',   # 'month__iexact',
                'month__gt', 'month__gte', 'month__lt', 'month__lte',
                'month__in',
                # 'month__contains', 'month__icontains',
                # 'month__startswith', 'month__istartswith', 'month__endswith', 'month__iendswith'
                'month__range',
                # 'month__isnull',
                # 'month__regex', 'month__iregex',
                # 'month__contained_by',
                # 'day', 'day__iexact',
                # 'day__gt', 'day__gte', 'day__lt', 'day__lte',
                # 'day__in',
                # 'day__contains', 'day__icontains',
                # 'day__startswith', 'day__istartswith', 'day__endswith', 'day__iendswith',
                # 'day__range',
                # 'day__isnull'
                # 'day__regex', 'day__iregex'
                # 'day__contained_by'
                # 'week_day', 'week_day__iexact',
                # 'week_day__gt', 'week_day__gte', 'week_day__lt', 'week_day__lte',
                # 'week_day__in',
                # 'week_day__contains', 'week_day__icontains',
                # 'week_day__startswith', 'week_day__istartswith', 'week_day__endswith', 'week_day__iendswith',
                # 'week_day__range',
                # 'week_day__isnull',
                # 'week_day__regex', 'week_day__iregex'
                # 'week_day__contained_by',
                # 'week', 'week__iexact',
                # 'week__gt', 'week__gte', 'week__lt', 'week__lte',
                # 'week__in',
                # 'week__contains', 'week__icontains',
                # 'week__startswith', 'week__istartswith', 'week__endswith', 'week__iendswith',
                # 'week__range',
                # 'week__isnull',
                # 'week__regex', 'week__iregex',
                # 'week__contained_by',

                # django_filters.exceptions.FieldLookupError: Unsupported lookup 'quarter'
                # 'quarter',   # 'quarter__iexact',
                # 'quarter__gt', 'quarter__gte', 'quarter__lt', 'quarter__lte',
                # 'quarter__in',
                # 'quarter__contains', 'quarter__icontains',
                # 'quarter__startswith', 'quarter__istartswith', 'quarter__endswith', 'quarter__iendswith',
                # 'quarter__range'
                # 'quarter__isnull',
                # 'quarter__regex', 'quarter__iregex',
                # 'quarter__contained_by'

                # 'contained_by'
            ])
