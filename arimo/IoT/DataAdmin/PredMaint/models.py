from __future__ import division

from django.db.models import \
    Model, \
    BigAutoField, BigIntegerField, BooleanField, CharField, DateField, DateTimeField, FloatField, PositiveSmallIntegerField, IntegerField, TextField, \
    ForeignKey, ManyToManyField, \
    PROTECT
from django.db.models.signals import post_save
from django.contrib.postgres.fields import DateRangeField, JSONField
from django.utils.encoding import python_2_unicode_compatible

from psycopg2.extras import DateRange

from ..base.models import \
    EquipmentGeneralType, \
    EquipmentDataField, \
    EquipmentUniqueTypeGroup, \
    EquipmentInstance
from ..util import MAX_CHAR_LEN, clean_lower_str


class EquipmentUniqueTypeGroupDataFieldProfile(Model):
    RELATED_NAME = 'equipment_unique_type_group_data_field_profiles'
    RELATED_QUERY_NAME = 'equipment_unique_type_group_data_field_profile'

    equipment_general_type = \
        ForeignKey(
            to=EquipmentGeneralType,
            related_name=RELATED_NAME,
            related_query_name=RELATED_QUERY_NAME,
            blank=False,
            null=False,
            on_delete=PROTECT)

    equipment_unique_type_group = \
        ForeignKey(
            to=EquipmentUniqueTypeGroup,
            related_name=RELATED_NAME,
            related_query_name=RELATED_QUERY_NAME,
            blank=False,
            null=False,
            on_delete=PROTECT)

    equipment_data_field = \
        ForeignKey(
            to=EquipmentDataField,
            related_name=RELATED_NAME,
            related_query_name=RELATED_QUERY_NAME,
            blank=False,
            null=False,
            on_delete=PROTECT)

    to_date = \
        DateField(
            blank=True,
            null=True)

    valid_proportion = \
        FloatField(
            blank=False,
            null=False,
            default=0)

    distinct_values = \
        JSONField(
            default=dict,
            encoder=None)

    n_distinct_values = \
        IntegerField(
            blank=False,
            null=False,
            default=0)

    sample_min = \
        FloatField(
            blank=True,
            null=True)

    outlier_rst_min = \
        FloatField(
            blank=True,
            null=True)

    sample_quartile = \
        FloatField(
            blank=True,
            null=True)

    sample_median = \
        FloatField(
            blank=True,
            null=True)

    sample_3rd_quartile = \
        FloatField(
            blank=True,
            null=True)

    outlier_rst_max = \
        FloatField(
            blank=True,
            null=True)

    sample_max = \
        FloatField(
            blank=True,
            null=True)

    last_updated = \
        DateTimeField(
            auto_now=True)

    class Meta:
        ordering = \
            'equipment_general_type', \
            'equipment_unique_type_group', \
            'equipment_data_field', \
            '-to_date'


@python_2_unicode_compatible
class EquipmentUniqueTypeGroupServiceConfig(Model):
    RELATED_NAME = 'equipment_unique_type_group_service_configs'
    RELATED_QUERY_NAME = 'equipment_unique_type_group_service_config'

    equipment_general_type = \
        ForeignKey(
            to=EquipmentGeneralType,
            related_name=RELATED_NAME,
            related_query_name=RELATED_QUERY_NAME,
            blank=False,
            null=False,
            on_delete=PROTECT)

    equipment_unique_type_group = \
        ForeignKey(
            to=EquipmentUniqueTypeGroup,
            related_name=RELATED_NAME,
            related_query_name=RELATED_QUERY_NAME,
            blank=False,
            null=False,
            on_delete=PROTECT)

    global_excluded_equipment_data_fields = \
        ManyToManyField(
            to=EquipmentDataField,
            related_name=RELATED_NAME,
            related_query_name=RELATED_QUERY_NAME,
            blank=True)

    active = \
        BooleanField(
            blank=False,
            null=False,
            default=True)

    comments = \
        TextField(
            blank=True,
            null=True)

    last_updated = \
        DateTimeField(
            auto_now=True)

    class Meta:
        ordering = \
            '-active', \
            'equipment_general_type', \
            'equipment_unique_type_group'

    def __str__(self):
        return '{}Pred Maint Svc Config: {} {}'.format(
            '' if self.active
               else '(INACTIVE) ',
            self.equipment_general_type.name.upper(), self.equipment_unique_type_group.name)


class EquipmentUniqueTypeGroupMonitoredDataFieldConfig(Model):
    RELATED_NAME = 'equipment_unique_type_group_monitored_data_field_configs'
    RELATED_QUERY_NAME = 'equipment_unique_type_group_monitored_data_field_config'

    equipment_unique_type_group_service_config = \
        ForeignKey(
            to=EquipmentUniqueTypeGroupServiceConfig,
            related_name=RELATED_NAME,
            related_query_name=RELATED_QUERY_NAME,
            blank=True,
            null=True,
            on_delete=PROTECT)

    monitored_equipment_data_field = \
        ForeignKey(
            to=EquipmentDataField,
            related_name=RELATED_NAME,
            related_query_name=RELATED_QUERY_NAME,
            blank=False,
            null=False,
            on_delete=PROTECT)

    excluded_equipment_data_fields = \
        ManyToManyField(
            to=EquipmentDataField,
            related_name='equipment_unique_type_group_monitored_data_field_configs_excl',
            related_query_name='equipment_unique_type_group_monitored_data_field_config_excl',
            blank=True)

    active = \
        BooleanField(
            blank=False,
            null=False,
            default=True)

    comments = \
        TextField(
            blank=True,
            null=True)

    class Meta:
        ordering = \
            '-active', \
            'equipment_unique_type_group_service_config', \
            'monitored_equipment_data_field'


@python_2_unicode_compatible
class Blueprint(Model):
    RELATED_NAME = 'blueprints'
    RELATED_QUERY_NAME = 'blueprint'

    equipment_general_type = \
        ForeignKey(
            to=EquipmentGeneralType,
            related_name=RELATED_NAME,
            related_query_name=RELATED_QUERY_NAME,
            blank=False,
            null=False,
            on_delete=PROTECT)

    equipment_unique_type_group = \
        ForeignKey(
            to=EquipmentUniqueTypeGroup,
            related_name=RELATED_NAME,
            related_query_name=RELATED_QUERY_NAME,
            blank=False,
            null=False,
            on_delete=PROTECT)

    trained_to_date = \
        DateField(
            blank=False,
            null=False,
            auto_now=False,
            auto_created=False,
            default=None)

    uuid = \
        CharField(
            max_length=MAX_CHAR_LEN,
            blank=False,
            null=False,
            unique=True)

    timestamp = \
        DateTimeField(
            auto_now_add=True)

    benchmark_metrics = \
        JSONField(
            default=dict,
            encoder=None)

    active = \
        BooleanField(
            blank=False,
            null=False,
            default=False)

    last_updated = \
        DateTimeField(
            auto_now=True)

    class Meta:
        ordering = \
            'equipment_general_type', \
            'equipment_unique_type_group', \
            '-trained_to_date', \
            '-timestamp'

    def __str__(self):
        return 'Blueprint "{}" ({}){}'.format(
            self.uuid,
            self.timestamp,
            '' if self.active
               else ' (INACTIVE)')


class EquipmentUniqueTypeGroupDataFieldBlueprintBenchmarkMetricProfile(Model):
    RELATED_NAME = 'equipment_unique_type_group_data_field_measurement_data_field_benchmark_metric_profiles'
    RELATED_QUERY_NAME = 'equipment_unique_type_group_data_field_measurement_data_field_benchmark_metric_profile'

    equipment_general_type = \
        ForeignKey(
            to=EquipmentGeneralType,
            related_name=RELATED_NAME,
            related_query_name=RELATED_QUERY_NAME,
            blank=False,
            null=False,
            on_delete=PROTECT)

    equipment_unique_type_group = \
        ForeignKey(
            to=EquipmentUniqueTypeGroup,
            related_name=RELATED_NAME,
            related_query_name=RELATED_QUERY_NAME,
            blank=False,
            null=False,
            on_delete=PROTECT)

    equipment_data_field = \
        ForeignKey(
            to=EquipmentDataField,
            related_name=RELATED_NAME,
            related_query_name=RELATED_QUERY_NAME,
            blank=False,
            null=False,
            on_delete=PROTECT)

    trained_to_date = \
        DateField(
            auto_now=False,
            auto_now_add=False,
            default=None)

    n = BigIntegerField(
            blank=False,
            null=False,
            default=0)

    mae = \
        FloatField(
            blank=True,
            null=True)

    medae = \
        FloatField(
            blank=True,
            null=True)

    rmse = \
        FloatField(
            blank=True,
            null=True)

    r2 = \
        FloatField(
            blank=True,
            null=True)

    last_updated = \
        DateTimeField(
            auto_now=True)

    class Meta:
        ordering = \
            'equipment_general_type', \
            'equipment_unique_type_group', \
            'equipment_data_field', \
            '-trained_to_date'


@python_2_unicode_compatible
class EquipmentInstanceDailyRiskScore(Model):
    RELATED_NAME = 'equipment_instance_daily_risk_scores'
    RELATED_QUERY_NAME = 'equipment_instance_daily_risk_score'

    id = BigAutoField(
        primary_key=True)

    equipment_general_type = \
        ForeignKey(
            to=EquipmentGeneralType,
            related_name=RELATED_NAME,
            related_query_name=RELATED_QUERY_NAME,
            blank=False,
            null=False,
            on_delete=PROTECT)

    equipment_unique_type_group = \
        ForeignKey(
            to=EquipmentUniqueTypeGroup,
            related_name=RELATED_NAME,
            related_query_name=RELATED_QUERY_NAME,
            blank=False,
            null=False,
            on_delete=PROTECT)

    equipment_instance = \
        ForeignKey(
            to=EquipmentInstance,
            related_name=RELATED_NAME,
            related_query_name=RELATED_QUERY_NAME,
            blank=False,
            null=False,
            on_delete=PROTECT)

    risk_score_name = \
        CharField(
            max_length=MAX_CHAR_LEN,
            blank=False,
            null=False)

    date = \
        DateField(
            blank=False,
            null=False,
            auto_now=False,
            auto_created=False,
            default=None)

    risk_score_value = \
        FloatField(
            blank=False,
            null=False,
            default=0)

    last_updated = \
        DateTimeField(
            auto_now=True)

    class Meta:
        ordering = \
            'equipment_general_type', \
            'equipment_unique_type_group', \
            'equipment_instance', \
            'risk_score_name', \
            '-date'

    def __str__(self):
        return '{} {} #{} on {}: {} = {:.3g}'.format(
            self.equipment_general_type.name,
            self.equipment_unique_type_group.name,
            self.equipment_instance.name,
            self.date,
            self.risk_score_name,
            self.risk_score_value)


@python_2_unicode_compatible
class EquipmentProblemType(Model):
    name = \
        CharField(
            max_length=MAX_CHAR_LEN,
            blank=False,
            null=False,
            unique=True)

    last_updated = \
        DateTimeField(
            auto_now=True)

    class Meta:
        ordering = 'name',

    def __str__(self):
        return 'EqProbTp {}'.format(self.name.upper())

    def save(self, *args, **kwargs):
        self.name = clean_lower_str(self.name)
        return super(EquipmentProblemType, self).save(*args, **kwargs)


@python_2_unicode_compatible
class EquipmentProblemPeriod(Model):
    RELATED_NAME = 'equipment_problem_diagnoses'
    RELATED_QUERY_NAME = 'equipment_problem_diagnosis'

    equipment_instance = \
        ForeignKey(
            to=EquipmentInstance,
            related_name=RELATED_NAME,
            related_query_name=RELATED_QUERY_NAME,
            blank=False,
            null=False,
            on_delete=PROTECT)

    from_date = \
        DateField(
            blank=False,
            null=False,
            auto_now=False,
            auto_created=False,
            default=None)

    to_date = \
        DateField(
            blank=False,
            null=False,
            auto_now=False,
            auto_created=False,
            default=None)

    date_range = \
        DateRangeField(
            blank=True,
            null=True)

    duration = \
        IntegerField(
            blank=False,
            null=False,
            default=0)

    ongoing = \
        BooleanField(
            blank=False,
            null=False,
            default=False)

    equipment_problem_types = \
        ManyToManyField(
            to=EquipmentProblemType,
            related_name=RELATED_NAME,
            related_query_name=RELATED_QUERY_NAME,
            blank=True)

    has_equipment_problems = \
        BooleanField(
            blank=False,
            null=False,
            default=False)

    dismissed = \
        BooleanField(
            blank=False,
            null=False,
            default=False)

    comments = \
        TextField(
            blank=True,
            null=True)

    alerts = \
        ManyToManyField(
            to='Alert',
            # related_name=RELATED_NAME,
            # related_query_name=RELATED_QUERY_NAME,
            blank=True)
    
    has_associated_alerts = \
        BooleanField(
            blank=False,
            null=False,
            default=False)

    last_updated = \
        DateTimeField(
            auto_now=True)

    class Meta:
        ordering = \
            '-ongoing', \
            '-from_date', \
            '-to_date', \
            'equipment_instance', \
            'dismissed'

    def __str__(self):
        return 'EqInst #{} from {} to {}{}: {}{}'.format(
            self.equipment_instance.name,
            self.from_date,
            self.to_date,
            ' ONGOING'
                if self.ongoing
                else '',
            ', '.join(equipment_problem_type.name.upper()
                      for equipment_problem_type in self.equipment_problem_types.all()),
            ' (DISMISSED)'
                if self.dismissed
                else '')

    def save(self, *args, **kwargs):
        self.date_range = \
            DateRange(
                lower=self.from_date,
                upper=self.to_date,
                bounds='[]',
                empty=False)

        self.duration = \
            (self.to_date - self.from_date).days + 1

        return super(EquipmentProblemPeriod, self).save(*args, **kwargs)


# rename more correctly
EquipmentProblemDiagnosis = EquipmentProblemPeriod


def equipment_problem_diagnosis_post_save(sender, instance, *args, **kwargs):
    alerts = \
        Alert.objects.filter(
            equipment_instance=instance.equipment_instance,
            date_range__overlap=instance.date_range)

    instance.alerts.set(
        alerts,
        # bulk=True,   # For many-to-many relationships, the bulk keyword argument doesn't exist
        clear=False)

    EquipmentProblemDiagnosis.objects.filter(pk=instance.pk).update(
        has_equipment_problems=bool(instance.equipment_problem_types.count()),
        has_associated_alerts=bool(alerts.count()))


post_save.connect(
    receiver=equipment_problem_diagnosis_post_save,
    sender=EquipmentProblemDiagnosis,
    weak=True,
    dispatch_uid=None)


@python_2_unicode_compatible
class AlertDiagnosisStatus(Model):
    RELATED_NAME = 'alert_diagnosis_statuses'
    RELATED_QUERY_NAME = 'alert_diagnosis_status'

    index = \
        PositiveSmallIntegerField(
            blank=False,
            null=False,
            unique=True,
            default=0)

    name = \
        CharField(
            max_length=MAX_CHAR_LEN,
            blank=False,
            null=False,
            unique=True,
            default='to_diagnose')

    last_updated = \
        DateTimeField(
            auto_now=True)

    class Meta:
        ordering = 'index',

    def __str__(self):
        return '{}. {}'.format(self.index, self.name)

    def save(self, *args, **kwargs):
        self.name = clean_lower_str(self.name)
        return super(AlertDiagnosisStatus, self).save(*args, **kwargs)


@python_2_unicode_compatible
class Alert(Model):
    RELATED_NAME = 'alerts'
    RELATED_QUERY_NAME = 'alert'

    equipment_general_type = \
        ForeignKey(
            to=EquipmentGeneralType,
            related_name=RELATED_NAME,
            related_query_name=RELATED_QUERY_NAME,
            blank=False,
            null=False,
            on_delete=PROTECT)

    equipment_unique_type_group = \
        ForeignKey(
            to=EquipmentUniqueTypeGroup,
            related_name=RELATED_NAME,
            related_query_name=RELATED_QUERY_NAME,
            blank=False,
            null=False,
            on_delete=PROTECT)

    equipment_instance = \
        ForeignKey(
            to=EquipmentInstance,
            related_name=RELATED_NAME,
            related_query_name=RELATED_QUERY_NAME,
            blank=False,
            null=False,
            on_delete=PROTECT)

    risk_score_name = \
        CharField(
            max_length=MAX_CHAR_LEN,
            blank=False,
            null=False,
            unique=False)

    threshold = \
        FloatField(
            blank=False,
            null=False,
            default=0)

    from_date = \
        DateField(
            blank=False,
            null=False,
            auto_now=False,
            auto_created=False,
            default=None)

    to_date = \
        DateField(
            blank=False,
            null=False,
            auto_now=False,
            auto_created=False,
            default=None)

    date_range = \
        DateRangeField(
            blank=True,
            null=True)

    duration = \
        IntegerField(
            blank=False,
            null=False,
            default=0)

    cumulative_excess_risk_score = \
        FloatField(
            blank=False,
            null=False,
            default=0)

    approx_average_risk_score = \
        FloatField(
            blank=False,
            null=False,
            default=0)

    last_risk_score = \
        FloatField(
            blank=False,
            null=False,
            default=0)

    ongoing = \
        BooleanField(
            blank=False,
            null=False,
            default=False)

    diagnosis_status = \
        ForeignKey(
            to=AlertDiagnosisStatus,
            blank=True,
            null=True,
            on_delete=PROTECT)

    equipment_problem_diagnoses = \
        ManyToManyField(
            to=EquipmentProblemDiagnosis,
            through=EquipmentProblemDiagnosis.alerts.through,
            # related_name=RELATED_NAME,
            # related_query_name=RELATED_QUERY_NAME,
                # Arimo_IoT_DataAdmin_PredMaint.Alert.equipment_problem_diagnoses: (fields.E302) Reverse accessor for 'Alert.equipment_problem_diagnoses' clashes with field name 'EquipmentProblemPeriod.alerts'.
                # HINT: Rename field 'EquipmentProblemPeriod.alerts', or add/change a related_name argument to the definition for field 'Alert.equipment_problem_diagnoses'.
            blank=True)
    
    has_associated_equipment_problem_diagnoses = \
        BooleanField(
            blank=False,
            null=False,
            default=False)

    last_updated = \
        DateTimeField(
            auto_now=True)

    class Meta:
        ordering = \
            'diagnosis_status', \
            '-ongoing', \
            'risk_score_name', \
            '-threshold', \
            '-cumulative_excess_risk_score'

    def __str__(self):
        if self.diagnosis_status is None:
            self.save()
            
        return '{}: {}Alert on {} {} #{} from {} to {} w Approx Avg Risk Score {:,.1f} (Last: {:,.1f}) (based on {} > {}) for {:,} Days'.format(
            self.diagnosis_status.name.upper(),
            'ONGOING '
                if self.ongoing
                else '',
            self.equipment_general_type.name.upper(),
            self.equipment_unique_type_group.name,
            self.equipment_instance.name,
            self.from_date,
            self.to_date,
            self.approx_average_risk_score,
            self.last_risk_score,
            self.risk_score_name,
            self.threshold,
            self.duration)

    def save(self, *args, **kwargs):
        self.date_range = \
            DateRange(
                lower=self.from_date,
                upper=self.to_date,
                bounds='[]',
                empty=False)

        self.duration = duration = \
            (self.to_date - self.from_date).days + 1

        self.approx_average_risk_score = \
            self.threshold + \
            (self.cumulative_excess_risk_score / duration)

        if self.diagnosis_status is None:
            self.diagnosis_status = AlertDiagnosisStatus.objects.get_or_create(index=0)[0]

        return super(Alert, self).save(*args, **kwargs)


def alert_post_save(sender, instance, *args, **kwargs):
    equipment_problem_diagnoses = \
        EquipmentProblemDiagnosis.objects.filter(
            equipment_instance=instance.equipment_instance,
            date_range__overlap=instance.date_range)
    
    instance.equipment_problem_diagnoses.set(
        equipment_problem_diagnoses,
        # bulk=True,   # For many-to-many relationships, the bulk keyword argument doesn't exist
        clear=False)

    Alert.objects.filter(pk=instance.pk).update(
        has_associated_equipment_problem_diagnoses=bool(equipment_problem_diagnoses.count()))


post_save.connect(
    receiver=alert_post_save,
    sender=Alert,
    weak=True,
    dispatch_uid=None)
