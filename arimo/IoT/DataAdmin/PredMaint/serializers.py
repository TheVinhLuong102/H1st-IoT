from rest_framework.serializers import ModelSerializer, RelatedField, SlugRelatedField

from drf_writable_nested.serializers import WritableNestedModelSerializer

from .models import \
    GlobalConfig, \
    EquipmentUniqueTypeGroupDataFieldProfile, \
    EquipmentUniqueTypeGroupServiceConfig, \
    Blueprint, \
    EquipmentUniqueTypeGroupDataFieldBlueprintBenchmarkMetricProfile, \
    EquipmentInstanceDailyRiskScore, \
    EquipmentProblemType, \
    EquipmentInstanceAlarmPeriod, \
    EquipmentInstanceProblemDiagnosis, \
    AlertDiagnosisStatus, \
    EquipmentInstanceAlertPeriod

from ..base.models import \
    EquipmentInstance

from ..base.serializers import \
    EquipmentDataFieldRelatedField


class GlobalConfigSerializer(ModelSerializer):
    class Meta:
        model = GlobalConfig

        fields = \
            'key', \
            'value'


class EquipmentUniqueTypeGroupDataFieldProfileSerializer(ModelSerializer):
    equipment_unique_type_group = \
        SlugRelatedField(
            read_only=True,
            slug_field='name',
            many=False)

    equipment_data_field = \
        EquipmentDataFieldRelatedField(
            read_only=True,
            many=False)

    class Meta:
        model = EquipmentUniqueTypeGroupDataFieldProfile

        fields = \
            'id', \
            'equipment_unique_type_group', \
            'equipment_data_field', \
            'to_date', \
            'valid_proportion', \
            'n_distinct_values', \
            'distinct_values', \
            'sample_min', \
            'outlier_rst_min', \
            'sample_quartile', \
            'sample_median', \
            'sample_3rd_quartile', \
            'outlier_rst_max', \
            'sample_max'


class EquipmentUniqueTypeGroupMonitoredDataFieldConfigRelatedField(RelatedField):
    def to_representation(self, value):
        return dict(
                monitored_equipment_data_field=value.monitored_equipment_data_field.name,
                manually_included_equipment_data_fields=[i.name for i in value.manually_included_equipment_data_fields.all()],
                manually_excluded_equipment_data_fields=[i.name for i in value.manually_excluded_equipment_data_fields.all()],
                active=value.active,
                comments=value.comments)


class EquipmentUniqueTypeGroupServiceConfigSerializer(ModelSerializer):
    equipment_unique_type_group = \
        SlugRelatedField(
            read_only=True,
            slug_field='name',
            many=False)

    equipment_unique_type_group_monitored_data_field_configs = \
        EquipmentUniqueTypeGroupMonitoredDataFieldConfigRelatedField(
            read_only=True,
            many=True)

    global_excluded_equipment_data_fields = \
        EquipmentDataFieldRelatedField(
            read_only=True,
            many=True)

    class Meta:
        model = EquipmentUniqueTypeGroupServiceConfig

        fields = \
            'id', \
            'equipment_unique_type_group', \
            'equipment_unique_type_group_monitored_data_field_configs', \
            'include_categorical_equipment_data_fields', \
            'global_excluded_equipment_data_fields', \
            'active', \
            'from_date', \
            'to_date', \
            'configs', \
            'comments'


class BlueprintSerializer(ModelSerializer):
    equipment_unique_type_group = \
        SlugRelatedField(
            read_only=True,
            slug_field='name',
            many=False)

    class Meta:
        model = Blueprint

        fields = \
            'equipment_unique_type_group', \
            'trained_to_date', \
            'uuid', \
            'timestamp', \
            'active'


class EquipmentUniqueTypeGroupDataFieldBlueprintBenchmarkMetricProfileSerializer(ModelSerializer):
    equipment_unique_type_group = \
        SlugRelatedField(
            read_only=True,
            slug_field='name',
            many=False)

    equipment_data_field = \
        SlugRelatedField(
            read_only=True,
            slug_field='name',
            many=False)

    class Meta:
        model = EquipmentUniqueTypeGroupDataFieldBlueprintBenchmarkMetricProfile

        fields = \
            'id', \
            'equipment_unique_type_group', \
            'equipment_data_field', \
            'trained_to_date', \
            'n', \
            'mae', \
            'medae', \
            'rmse', \
            'r2'


class EquipmentInstanceDailyRiskScoreSerializer(ModelSerializer):
    equipment_unique_type_group = \
        SlugRelatedField(
            read_only=True,
            slug_field='name',
            many=False)

    equipment_instance = \
        SlugRelatedField(
            read_only=True,
            slug_field='name',
            many=False)

    class Meta:
        model = EquipmentInstanceDailyRiskScore

        fields = \
            'equipment_unique_type_group', \
            'equipment_instance', \
            'risk_score_name', \
            'date', \
            'risk_score_value'


class EquipmentProblemTypeSerializer(ModelSerializer):
    class Meta:
        model = EquipmentProblemType
        fields = 'name',


class EquipmentInstanceAlarmPeriodShortFormRelatedField(RelatedField):
    def to_representation(self, value):
        return dict(
                equipment_instance=value.equipment_instance.name,
                alarm_type=value.alarm_type.name,
                from_utc_date_time=str(value.from_utc_date_time),
                to_utc_date_time=str(value.to_utc_date_time),
                duration_in_days=value.duration_in_days,
                has_associated_equipment_instance_alert_periods=value.has_associated_equipment_instance_alert_periods,
                has_associated_equipment_instance_problem_diagnoses=value.has_associated_equipment_instance_problem_diagnoses)


class EquipmentInstanceProblemDiagnosisShortFormRelatedField(RelatedField):
    def to_representation(self, value):
        return dict(
                equipment_instance=value.equipment_instance.name,
                from_date=str(value.from_date),
                to_date=str(value.to_date),
                duration=value.duration,
                ongoing=value.ongoing,
                has_equipment_problems=value.has_equipment_problems,
                equipment_problem_types=[i.name for i in value.equipment_problem_types.all()],
                dismissed=value.dismissed,
                comments=value.comments,
                has_associated_equipment_instance_alarm_periods=value.has_associated_equipment_instance_alarm_periods,
                has_associated_equipment_instance_alert_periods=value.has_associated_equipment_instance_alert_periods)


class EquipmentInstanceAlertPeriodShortFormRelatedField(RelatedField):
    def to_representation(self, value):
        return dict(
                equipment_unique_type_group=value.equipment_unique_type_group.name,
                equipment_instance=value.equipment_instance.name,
                risk_score_name=value.risk_score_name,
                threshold=value.threshold,
                from_date=str(value.from_date),
                to_date=str(value.to_date),
                duration=value.duration,
                cumulative_excess_risk_score=value.cumulative_excess_risk_score,
                approx_average_risk_score=value.approx_average_risk_score,
                last_risk_score=value.last_risk_score,
                ongoing=value.ongoing,
                diagnosis_status=value.diagnosis_status.name,
                has_associated_equipment_instance_alarm_periods=value.has_associated_equipment_instance_alarm_periods,
                has_associated_equipment_instance_problem_diagnoses=value.has_associated_equipment_instance_problem_diagnoses)


class EquipmentInstanceAlarmPeriodSerializer(WritableNestedModelSerializer):
    equipment_instance = \
        SlugRelatedField(
            queryset=EquipmentInstance.objects.all(), read_only=False,
            slug_field='name',
            many=False,
            required=True)

    alarm_type = \
        SlugRelatedField(
            queryset=EquipmentProblemType.objects.all(), read_only=False,
            slug_field='name',
            many=False,
            required=True)

    equipment_instance_alert_periods = \
        EquipmentInstanceAlertPeriodShortFormRelatedField(
            read_only=True,
            many=True)

    equipment_instance_problem_diagnoses = \
        EquipmentInstanceProblemDiagnosisShortFormRelatedField(
            read_only=True,
            many=True)

    class Meta:
        model = EquipmentInstanceAlarmPeriod

        fields = \
            'id', \
            'equipment_instance', \
            'alarm_type', \
            'from_utc_date_time', \
            'to_utc_date_time', \
            'duration_in_days', \
            'has_associated_equipment_instance_alert_periods', \
            'equipment_instance_alert_periods', \
            'has_associated_equipment_instance_problem_diagnoses', \
            'equipment_instance_problem_diagnoses'


class EquipmentInstanceProblemDiagnosisSerializer(WritableNestedModelSerializer):
    equipment_instance = \
        SlugRelatedField(
            queryset=EquipmentInstance.objects.all(), read_only=False,
            slug_field='name',
            many=False,
            required=True)

    equipment_problem_types = \
        SlugRelatedField(
            queryset=EquipmentProblemType.objects.all(), read_only=False,
            slug_field='name',
            many=True,
            required=True)

    equipment_instance_alarm_periods = \
        EquipmentInstanceAlarmPeriodShortFormRelatedField(
            read_only=True,
            many=True)

    equipment_instance_alert_periods = \
        EquipmentInstanceAlertPeriodShortFormRelatedField(
            read_only=True,
            many=True)

    class Meta:
        model = EquipmentInstanceProblemDiagnosis

        fields = \
            'id', \
            'equipment_instance', \
            'from_date', \
            'to_date', \
            'duration', \
            'ongoing', \
            'equipment_problem_types', \
            'has_equipment_problems', \
            'dismissed', \
            'comments', \
            'has_associated_equipment_instance_alarm_periods', \
            'equipment_instance_alarm_periods', \
            'has_associated_equipment_instance_alert_periods', \
            'equipment_instance_alert_periods'


class AlertDiagnosisStatusSerializer(ModelSerializer):
    class Meta:
        model = AlertDiagnosisStatus
        fields = 'name',


class EquipmentInstanceAlertPeriodSerializer(ModelSerializer):
    equipment_unique_type_group = \
        SlugRelatedField(
            read_only=True,
            slug_field='name',
            many=False)

    equipment_instance = \
        SlugRelatedField(
            read_only=True,
            slug_field='name',
            many=False)

    diagnosis_status = \
        SlugRelatedField(
            queryset=AlertDiagnosisStatus.objects.all(), read_only=False,
            slug_field='name',
            many=False,
            required=False)

    equipment_instance_alarm_periods = \
        EquipmentInstanceAlarmPeriodShortFormRelatedField(
            read_only=True,
            many=True)

    equipment_instance_problem_diagnoses = \
        EquipmentInstanceProblemDiagnosisShortFormRelatedField(
            read_only=True,
            many=True)

    class Meta:
        model = EquipmentInstanceAlertPeriod

        fields = \
            'id', \
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
            'info', \
            'diagnosis_status', \
            'has_associated_equipment_instance_alarm_periods', \
            'equipment_instance_alarm_periods', \
            'has_associated_equipment_instance_problem_diagnoses', \
            'equipment_instance_problem_diagnoses'
