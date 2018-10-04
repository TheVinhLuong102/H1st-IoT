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
    EquipmentProblemPeriod, \
    AlertDiagnosisStatus, \
    Alert
from ..base.models import \
    EquipmentGeneralType, \
    EquipmentUniqueTypeGroup, \
    EquipmentInstance


class EquipmentUniqueTypeGroupDataFieldProfileSerializer(ModelSerializer):
    class Meta:
        model = EquipmentUniqueTypeGroupDataFieldProfile

        fields = '__all__'


class EquipmentUniqueTypeGroupServiceConfigSerializer(ModelSerializer):
    class Meta:
        model = EquipmentUniqueTypeGroupServiceConfig

        fields = '__all__'


class EquipmentUniqueTypeGroupMonitoredDataFieldConfigSerializer(ModelSerializer):
    class Meta:
        model = EquipmentUniqueTypeGroupMonitoredDataFieldConfig

        fields = '__all__'


class BlueprintSerializer(ModelSerializer):
    class Meta:
        model = Blueprint

        fields = '__all__'


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


class EquipmentProblemPeriodSerializer(WritableNestedModelSerializer):
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


class AlertDiagnosisStatusSerializer(ModelSerializer):
    class Meta:
        model = AlertDiagnosisStatus

        fields = '__all__'


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
