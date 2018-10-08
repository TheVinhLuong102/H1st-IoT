from rest_framework_filters import FilterSet, RelatedFilter

from .models import \
    EquipmentUniqueTypeGroupDataFieldProfile, \
    EquipmentUniqueTypeGroupServiceConfig, \
    EquipmentUniqueTypeGroupMonitoredDataFieldConfig, \
    Blueprint, \
    EquipmentUniqueTypeGroupDataFieldBlueprintBenchmarkMetricProfile, \
    EquipmentInstanceDailyRiskScore, \
    EquipmentProblemType, \
    EquipmentProblemPeriod, \
    AlertDiagnosisStatus, \
    Alert
from ..base.filters import \
    EquipmentGeneralTypeFilter, \
    EquipmentUniqueTypeGroupFilter, \
    EquipmentDataFieldFilter, \
    EquipmentInstanceFilter
from ..base.models import \
    EquipmentGeneralType, \
    EquipmentUniqueTypeGroup, \
    EquipmentDataField, \
    EquipmentInstance


class EquipmentUniqueTypeGroupDataFieldProfileFilter(FilterSet):
    equipment_general_type = \
        RelatedFilter(
            queryset=EquipmentGeneralType.objects.all(),
            filterset=EquipmentGeneralTypeFilter)

    equipment_unique_type_group = \
        RelatedFilter(
            queryset=EquipmentUniqueTypeGroup.objects.all(),
            filterset=EquipmentUniqueTypeGroupFilter)

    equipment_data_field = \
        RelatedFilter(
            queryset=EquipmentDataField.objects.all(),
            filterset=EquipmentDataFieldFilter)

    class Meta:
        model = EquipmentUniqueTypeGroupDataFieldProfile

        fields = dict(
             to_date=[
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
                 'month__gt', 'month__gte', 'month__lt', 'month__lte'
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
                 'quarter',   # 'quarter__iexact',
                 'quarter__gt', 'quarter__gte', 'quarter__lt', 'quarter__lte',
                 'quarter__in',
                 # 'quarter__contains', 'quarter__icontains',
                 # 'quarter__startswith', 'quarter__istartswith', 'quarter__endswith', 'quarter__iendswith',
                 'quarter__range'
                 # 'quarter__isnull',
                 # 'quarter__regex', 'quarter__iregex',
                 # 'quarter__contained_by'
                 # 'to_date__contained_by'
             ],

            valid_proportion=[
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

            n_distinct_values=[
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
            ])


class EquipmentUniqueTypeGroupServiceConfigFilter(FilterSet):
    class Meta:
        model = EquipmentUniqueTypeGroupServiceConfig

        fields = \
            'equipment_general_type', \
            'equipment_unique_type_group', \
            'global_excluded_equipment_data_fields', \
            'active', \
            'comments', \
            'last_updated'
            # 'equipment_unique_type_group_monitored_data_field_configs'


class BlueprintFilter(FilterSet):
     class Meta:
         model = Blueprint

         fields = \
             'equipment_general_type', \
             'equipment_unique_type_group', \
             'trained_to_date', \
             'timestamp', \
             'uuid', \
             'active', \
             'last_updated'


class EquipmentUniqueTypeGroupDataFieldBlueprintBenchmarkMetricProfileFilter(FilterSet):
    class Meta:
        model = EquipmentUniqueTypeGroupDataFieldBlueprintBenchmarkMetricProfile

        fields = '__all__'


class EquipmentInstanceDailyRiskScoreFilter(FilterSet):
    class Meta:
        model = EquipmentInstanceDailyRiskScore

        fields = '__all__'


class EquipmentProblemTypeFilter(FilterSet):
    class Meta:
        model = EquipmentProblemType

        fields = '__all__'


class EquipmentProblemPeriodFilter(FilterSet):
     class Meta:
         model = EquipmentProblemPeriod

         fields = \
             'equipment_instance', \
             'from_date', \
             'to_date', \
             'dismissed', \
             'duration', \
             'ongoing', \
             'equipment_problem_types', \
             'comments', \
             'last_updated'


class AlertDiagnosisStatusFilter(FilterSet):
    class Meta:
        model = AlertDiagnosisStatus

        fields = '__all__'


class AlertFilter(FilterSet):
    class Meta:
        model = Alert
        fields = \
            'equipment_general_type', \
            'equipment_unique_type_group', \
            'equipment_instance', \
            'risk_score_name', \
            'threshold', \
            'from_date', \
            'to_date', \
            'duration', \
            'cumulative_excess_risk_score', \
            'approx_average_risk_score', \
            'last_risk_score', \
            'ongoing', \
            'diagnosis_status', \
            'last_updated'
