from rest_framework.serializers import \
    Serializer, \
    ModelSerializer, RelatedField, ManyRelatedField, PrimaryKeyRelatedField, SlugRelatedField, StringRelatedField, \
    HyperlinkedModelSerializer, HyperlinkedIdentityField, HyperlinkedRelatedField


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

        fields = '__all__'


class EquipmentProblemPeriodSerializer(ModelSerializer):
    class Meta:
        model = EquipmentProblemPeriod

        fields = '__all__'


class AlertDiagnosisStatusSerializer(ModelSerializer):
    class Meta:
        model = AlertDiagnosisStatus

        fields = '__all__'


class AlertSerializer(ModelSerializer):
    class Meta:
        model = Alert

        fields = '__all__'
