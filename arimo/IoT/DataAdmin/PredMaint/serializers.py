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
    EquipmentProblemDiagnosis, \
    AlertDiagnosisStatus, \
    Alert

from ..base.models import \
    EquipmentInstance

from ..base.serializers import \
    EquipmentDataFieldShortFormRelatedField


class GlobalConfigSerializer(ModelSerializer):
    class Meta:
        model = GlobalConfig

        fields = \
            'key', \
            'value', \
            'last_updated'


class EquipmentUniqueTypeGroupDataFieldProfileSerializer(ModelSerializer):
    equipment_unique_type_group = \
        SlugRelatedField(
            read_only=True,
            slug_field='name',
            many=False)

    equipment_data_field = \
        EquipmentDataFieldShortFormRelatedField(
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
            'sample_max', \
            'last_updated'


class EquipmentUniqueTypeGroupMonitoredDataFieldConfigRelatedField(RelatedField):
    def to_representation(self, value):
        return dict(
                monitored_equipment_data_field=value.monitored_equipment_data_field.name,
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
        EquipmentDataFieldShortFormRelatedField(
            read_only=True,
            many=True)

    class Meta:
        model = EquipmentUniqueTypeGroupServiceConfig

        fields = \
            'id', \
            'equipment_unique_type_group', \
            'equipment_unique_type_group_monitored_data_field_configs', \
            'global_excluded_equipment_data_fields', \
            'active', \
            'from_date', \
            'to_date', \
            'configs', \
            'comments', \
            'last_updated'


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
            'active', \
            'last_updated'


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
            'r2', \
            'last_updated'


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


class AlertShortFormRelatedField(RelatedField):
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
                has_associated_equipment_problem_diagnoses=value.has_associated_equipment_problem_diagnoses)


class EquipmentProblemDiagnosisSerializer(WritableNestedModelSerializer):
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

    alerts = \
        AlertShortFormRelatedField(
            read_only=True,
            many=True)

    class Meta:
        model = EquipmentProblemDiagnosis

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
            'has_associated_alerts', \
            'alerts', \
            'last_updated'


class AlertDiagnosisStatusSerializer(ModelSerializer):
    class Meta:
        model = AlertDiagnosisStatus
        fields = 'name',


class EquipmentProblemDiagnosisShortFormRelatedField(RelatedField):
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
            has_associated_alerts=value.has_associated_alerts)


class AlertSerializer(ModelSerializer):
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

    equipment_problem_diagnoses = \
        EquipmentProblemDiagnosisShortFormRelatedField(
            read_only=True,
            many=True)

    class Meta:
        model = Alert

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
            'has_associated_equipment_problem_diagnoses', \
            'equipment_problem_diagnoses', \
            'last_updated'
