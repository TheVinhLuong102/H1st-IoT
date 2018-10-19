from rest_framework.serializers import \
    Serializer, CharField, ListField, \
    ModelSerializer, RelatedField, ManyRelatedField, PrimaryKeyRelatedField, SlugRelatedField, StringRelatedField, \
    HyperlinkedModelSerializer, HyperlinkedIdentityField, HyperlinkedRelatedField

from drf_writable_nested.serializers import WritableNestedModelSerializer

from .models import \
    EquipmentUniqueTypeGroupDataFieldProfile, \
    EquipmentUniqueTypeGroupServiceConfig, \
    EquipmentUniqueTypeGroupMonitoredDataFieldConfig, \
    Blueprint, \
    EquipmentUniqueTypeGroupDataFieldBlueprintBenchmarkMetricProfile, \
    EquipmentInstanceDailyRiskScore, \
    EquipmentProblemType, \
    EquipmentProblemPeriod as EquipmentDiagnosis, \
    AlertDiagnosisStatus, \
    Alert
from ..base.models import \
    EquipmentGeneralType, \
    EquipmentUniqueTypeGroup, \
    EquipmentInstance
from ..base.serializers import EquipmentDataFieldShortFormRelatedField


class EquipmentUniqueTypeGroupDataFieldProfileSerializer(ModelSerializer):
    equipment_general_type = \
        SlugRelatedField(
            read_only=True,
            slug_field='name',
            many=False)

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
            'equipment_general_type', \
            'equipment_unique_type_group', \
            'equipment_data_field', \
            'to_date', \
            'valid_proportion', \
            'distinct_values', \
            'n_distinct_values', \
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
                excluded_equipment_data_fields=[i.name for i in value.excluded_equipment_data_fields.all()],
                active=value.active,
                comments=value.comments)


class EquipmentUniqueTypeGroupServiceConfigSerializer(ModelSerializer):
    equipment_general_type = \
        SlugRelatedField(
            read_only=True,
            slug_field='name',
            many=False)

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
            'equipment_general_type', \
            'equipment_unique_type_group', \
            'equipment_unique_type_group_monitored_data_field_configs', \
            'global_excluded_equipment_data_fields', \
            'active', \
            'comments', \
            'last_updated'


class BlueprintSerializer(ModelSerializer):
    equipment_general_type = \
        SlugRelatedField(
            read_only=True,
            slug_field='name',
            many=False)

    equipment_unique_type_group = \
        SlugRelatedField(
            read_only=True,
            slug_field='name',
            many=False)

    class Meta:
        model = Blueprint

        fields = \
            'equipment_general_type', \
            'equipment_unique_type_group', \
            'trained_to_date', \
            'timestamp', \
            'uuid', \
            'benchmark_metrics', \
            'active', \
            'last_updated'


class EquipmentUniqueTypeGroupDataFieldBlueprintBenchmarkMetricProfileSerializer(ModelSerializer):
    class Meta:
        model = EquipmentUniqueTypeGroupDataFieldBlueprintBenchmarkMetricProfile

        fields = '__all__'


class EquipmentInstanceDailyRiskScoreSerializer(ModelSerializer):
    class Meta:
        model = EquipmentInstanceDailyRiskScore
        fields = '__all__'


class EquipmentProblemTypeSerializer(ModelSerializer):
    class Meta:
        model = EquipmentProblemType
        fields = 'name',


class EquipmentDiagnosisSerializer(WritableNestedModelSerializer):
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

    class Meta:
        model = EquipmentDiagnosis

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


class AlertDiagnosisStatusSerializer(ModelSerializer):
    class Meta:
        model = AlertDiagnosisStatus
        fields = 'name',


class AlertSerializer(ModelSerializer):
    equipment_general_type = \
        SlugRelatedField(
            read_only=True,
            slug_field='name',
            many=False)

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
            read_only=True,
            slug_field='name',
            many=False)

    class Meta:
        model = Alert

        fields = \
            'id', \
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
