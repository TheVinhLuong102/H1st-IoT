"""H1st IoT Data Management: Maintenance Operations: Filters."""


from rest_framework_filters import FilterSet, RelatedFilter

from .models import (
    GlobalConfig,
    EquipmentInstanceDailyRiskScore,
    EquipmentProblemType,
    EquipmentInstanceAlarmPeriod,
    EquipmentInstanceProblemDiagnosis,
    AlertDiagnosisStatus,
    EquipmentInstanceAlertPeriod,
)

from h1st_iot.data_mgmt.filters import (
    EquipmentUniqueTypeGroupFilter,
    EquipmentDataFieldFilter,
    EquipmentInstanceFilter,
)

from h1st_iot.data_mgmt.models import \
    EquipmentUniqueTypeGroup, \
    EquipmentDataField, \
    EquipmentInstance


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


class EquipmentInstanceDailyRiskScoreFilter(FilterSet):
    equipment_unique_type_group = \
        RelatedFilter(
            queryset=EquipmentUniqueTypeGroup.objects.all(),
            filterset=EquipmentUniqueTypeGroupFilter)

    equipment_instance = \
        RelatedFilter(
            queryset=EquipmentInstance.objects.all(),
            filterset=EquipmentInstanceFilter)

    class Meta:
        model = EquipmentInstanceDailyRiskScore

        fields = dict(
            risk_score_name=[
                'exact', 'iexact',
                'in',
                'contains', 'icontains',
                'startswith', 'istartswith', 'endswith', 'iendswith'
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
            ],

            risk_score_value=[
                'gt', 'gte', 'lt', 'lte',
                'startswith', 'istartswith',
                'range'
            ])


class EquipmentProblemTypeFilter(FilterSet):
    class Meta:
        model = EquipmentProblemType

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


class EquipmentInstanceAlarmPeriodFilter(FilterSet):
    equipment_instance = \
        RelatedFilter(
            queryset=EquipmentInstance.objects.all(),
            filterset=EquipmentInstanceFilter)

    alarm_type = \
        RelatedFilter(
            queryset=EquipmentProblemType.objects.all(),
            filterset=EquipmentProblemTypeFilter)

    class Meta:
        model = EquipmentInstanceAlarmPeriod

        fields = dict(
            from_utc_date_time=[
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

                # 'to_date__contained_by'
            ],

            to_utc_date_time=[
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

                # 'to_date__contained_by'
            ],

            duration_in_days=[
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

            has_associated_equipment_instance_alert_periods=['exact'],

            has_associated_equipment_instance_problem_diagnoses=['exact'])


class EquipmentInstanceProblemDiagnosisFilter(FilterSet):
    equipment_instance = \
        RelatedFilter(
            queryset=EquipmentInstance.objects.all(),
            filterset=EquipmentInstanceFilter)

    equipment_problem_types = \
        RelatedFilter(
            queryset=EquipmentProblemType.objects.all(),
            filterset=EquipmentProblemTypeFilter)

    class Meta:
         model = EquipmentInstanceProblemDiagnosis

         fields = dict(
             from_date=[
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

                 # 'to_date__contained_by'
             ],

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

                 # 'to_date__contained_by'
             ],

             duration=[
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

             has_equipment_problems=['exact'],

             dismissed=['exact'],

             has_associated_equipment_instance_alarm_periods=['exact'],

             has_associated_equipment_instance_alert_periods=['exact'])


class AlertDiagnosisStatusFilter(FilterSet):
    class Meta:
        model = AlertDiagnosisStatus

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


class EquipmentInstanceAlertPeriodFilter(FilterSet):
    equipment_unique_type_group = \
        RelatedFilter(
            queryset=EquipmentUniqueTypeGroup.objects.all(),
            filterset=EquipmentUniqueTypeGroupFilter)

    equipment_instance = \
        RelatedFilter(
            queryset=EquipmentInstance.objects.all(),
            filterset=EquipmentInstanceFilter)

    diagnosis_status = \
        RelatedFilter(
            queryset=AlertDiagnosisStatus.objects.all(),
            filterset=AlertDiagnosisStatusFilter)

    class Meta:
        model = EquipmentInstanceAlertPeriod

        fields = dict(
            risk_score_name=[
                'exact', 'iexact',
                # 'gt', 'gte', 'lt', 'lte',
                'in',
                'contains', 'icontains',
                'startswith', 'istartswith', 'endswith', 'iendswith',
                # 'range',
                # 'isnull',
                # 'regex', 'iregex'
            ],

            threshold=[
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

            from_date=[
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

                # 'to_date__contained_by'
            ],

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

                # 'to_date__contained_by'
            ],

            duration=[
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

            cumulative_excess_risk_score=[
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

            approx_average_risk_score=[
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

            last_risk_score=[
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

            ongoing=['exact'],

            has_associated_equipment_instance_alarm_periods=['exact'],

            has_associated_equipment_instance_problem_diagnoses=['exact'])
