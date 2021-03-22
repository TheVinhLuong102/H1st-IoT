from __future__ import division

from datetime import timedelta

from django.db.models import \
    Model, \
    BigAutoField, BigIntegerField, BooleanField, CharField, DateField, DateTimeField, FloatField, PositiveSmallIntegerField, IntegerField, TextField, \
    JSONField, \
    ForeignKey, ManyToManyField, OneToOneField, \
    CASCADE, PROTECT
from django.db.models.signals import post_save
from django.contrib.postgres.fields import DateRangeField

from psycopg2.extras import DateRange

from ..base.models import \
    EquipmentDataField, \
    EquipmentUniqueTypeGroup, \
    EquipmentInstance
from ..util import MAX_CHAR_LEN, clean_lower_str, clean_upper_str


_ONE_DAY_TIME_DELTA = timedelta(days=1)
_ONE_DAY_TIME_DELTA_TOTAL_SECONDS = _ONE_DAY_TIME_DELTA.total_seconds()


class GlobalConfig(Model):
    key = \
        CharField(
            blank=False,
            null=False,
            unique=True,
            max_length=MAX_CHAR_LEN)

    value = \
        JSONField(
            blank=True,
            null=True)

    class Meta:
        ordering = 'key',

    def __str__(self):
        return '{} = {}'.format(self.key, self.value)

    def save(self, *args, **kwargs):
        self.key = clean_upper_str(self.key)
        super(type(self), self).save( *args, **kwargs)


class EquipmentUniqueTypeGroupDataFieldProfile(Model):
    RELATED_NAME = 'equipment_unique_type_group_data_field_profiles'
    RELATED_QUERY_NAME = 'equipment_unique_type_group_data_field_profile'

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
            null=True,
            db_index=True)

    valid_proportion = \
        FloatField(
            blank=False,
            null=False)

    n_distinct_values = \
        IntegerField(
            blank=False,
            null=False)

    distinct_values = \
        JSONField(
            blank=True,
            null=True)

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
        unique_together = \
            'equipment_unique_type_group', \
            'equipment_data_field', \
            'to_date'

        ordering = \
            'equipment_unique_type_group', \
            'equipment_data_field', \
            '-to_date'


class EquipmentUniqueTypeGroupDataFieldPairwiseCorrelation(Model):
    RELATED_NAME = 'equipment_unique_type_group_data_field_pairwise_correlations'
    RELATED_QUERY_NAME = 'equipment_unique_type_group_data_field_pairwise_correlation'

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

    equipment_data_field_2 = \
        ForeignKey(
            to=EquipmentDataField,
            blank=False,
            null=False,
            on_delete=PROTECT)

    sample_correlation = \
        FloatField(
            blank=False,
            null=False)

    last_updated = \
        DateTimeField(
            auto_now=True)

    class Meta:
        unique_together = \
            'equipment_unique_type_group', \
            'equipment_data_field', \
            'equipment_data_field_2'

        ordering = \
            'equipment_unique_type_group', \
            'equipment_data_field', \
            'equipment_data_field_2'


class EquipmentUniqueTypeGroupServiceConfig(Model):
    RELATED_NAME = 'equipment_unique_type_group_service_configs'
    RELATED_QUERY_NAME = 'equipment_unique_type_group_service_config'

    equipment_unique_type_group = \
        OneToOneField(
            to=EquipmentUniqueTypeGroup,
            related_name=RELATED_NAME,
            related_query_name=RELATED_QUERY_NAME,
            blank=False,
            null=False,
            on_delete=PROTECT)

    include_categorical_equipment_data_fields = \
        BooleanField(
            blank=False,
            null=False,
            default=True)

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
            default=True,
            db_index=True)

    from_date = \
        DateField(
            blank=True,
            null=True)

    to_date = \
        DateField(
            blank=True,
            null=True)

    configs = \
        JSONField(
            blank=True,
            null=True)

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
            'equipment_unique_type_group'

    def __str__(self):
        return '{}Pred Maint Svc Config: {}'.format(
                '' if self.active
                   else '(INACTIVE) ',
                self.equipment_unique_type_group.name)


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
            on_delete=CASCADE)

    monitored_equipment_data_field = \
        ForeignKey(
            to=EquipmentDataField,
            related_name=RELATED_NAME,
            related_query_name=RELATED_QUERY_NAME,
            blank=False,
            null=False,
            on_delete=PROTECT)

    highly_correlated_numeric_equipment_data_fields = \
        JSONField(
            blank=True,
            null=True,
            default=list)

    auto_included_numeric_equipment_data_fields = \
        JSONField(
            blank=True,
            null=True,
            default=list)

    lowly_correlated_numeric_equipment_data_fields = \
        JSONField(
            blank=True,
            null=True,
            default=list)

    manually_included_equipment_data_fields = \
        ManyToManyField(
            to=EquipmentDataField,
            related_name='equipment_unique_type_group_monitored_data_field_configs_extra_manual_incl',
            related_query_name='equipment_unique_type_group_monitored_data_field_config_extra_manual_incl',
            blank=True)

    manually_excluded_equipment_data_fields = \
        ManyToManyField(
            to=EquipmentDataField,
            related_name='equipment_unique_type_group_monitored_data_field_configs_manual_excl',
            related_query_name='equipment_unique_type_group_monitored_data_field_config_manual_excl',
            blank=True)

    active = \
        BooleanField(
            blank=False,
            null=False,
            default=True,
            db_index=True)

    comments = \
        TextField(
            blank=True,
            null=True)

    class Meta:
        unique_together = \
            'equipment_unique_type_group_service_config', \
            'monitored_equipment_data_field'

        ordering = \
            '-active', \
            'monitored_equipment_data_field__name'


class Blueprint(Model):
    RELATED_NAME = 'blueprints'
    RELATED_QUERY_NAME = 'blueprint'

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
            default=None,
            db_index=True)

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
            blank=True,
            null=True)

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
            blank=False,
            null=False,
            db_index=True)

    n = BigIntegerField(
            blank=False,
            null=False)

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
        unique_together = \
            'equipment_unique_type_group', \
            'equipment_data_field', \
            'trained_to_date'

        ordering = \
            'equipment_unique_type_group', \
            'equipment_data_field', \
            '-trained_to_date'


class EquipmentInstanceDailyRiskScore(Model):
    RELATED_NAME = 'equipment_instance_daily_risk_scores'
    RELATED_QUERY_NAME = 'equipment_instance_daily_risk_score'

    id = BigAutoField(
            primary_key=True)

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
            blank=False,
            null=False,
            db_index=True,
            max_length=MAX_CHAR_LEN)

    date = \
        DateField(
            blank=False,
            null=False,
            db_index=True)

    risk_score_value = \
        FloatField(
            blank=False,
            null=False)

    last_updated = \
        DateTimeField(
            auto_now=True)

    class Meta:
        unique_together = \
            'equipment_unique_type_group', \
            'equipment_instance', \
            'risk_score_name', \
            'date'

    def __str__(self):
        return '{} {} #{} on {}: {} = {:.3g}'.format(
                self.equipment_unique_type_group.equipment_general_type.name,
                self.equipment_unique_type_group.name,
                self.equipment_instance.name,
                self.date,
                self.risk_score_name,
                self.risk_score_value)


class EquipmentProblemType(Model):
    name = \
        CharField(
            verbose_name='Equipment Problem Type',
            max_length=MAX_CHAR_LEN,
            blank=False,
            null=False,
            unique=True,
            db_index=True)

    class Meta:
        ordering = 'name',

    def __str__(self):
        return f'EqProbTp "{self.name}""'

    def save(self, *args, **kwargs):
        self.name = self.name.strip()
        super(type(self), self).save(*args, **kwargs)


class EquipmentInstanceAlarmPeriod(Model):
    RELATED_NAME = 'equipment_instance_alarm_periods'
    RELATED_QUERY_NAME = 'equipment_instance_alarm_period'

    equipment_instance = \
        ForeignKey(
            to=EquipmentInstance,
            related_name=RELATED_NAME,
            related_query_name=RELATED_QUERY_NAME,
            blank=False,
            null=False,
            on_delete=PROTECT)

    alarm_type = \
        ForeignKey(
            to=EquipmentProblemType,
            related_name=RELATED_NAME,
            related_query_name=RELATED_QUERY_NAME,
            blank=False,
            null=False,
            on_delete=PROTECT)

    from_utc_date_time = \
        DateTimeField(
            blank=False,
            null=False,
            db_index=True)

    to_utc_date_time = \
        DateTimeField(
            blank=True,
            null=True,
            db_index=True)

    duration_in_days = \
        FloatField(
            blank=True,
            null=True,
            db_index=True)

    date_range = \
        DateRangeField(
            blank=True,
            null=True)

    equipment_instance_alert_periods = \
        ManyToManyField(
            to='Alert',   # EquipmentInstanceAlertPeriods
            related_name=RELATED_NAME + '_reverse',
            related_query_name=RELATED_QUERY_NAME,
            blank=True)

    has_associated_equipment_instance_alert_periods = \
        BooleanField(
            blank=False,
            null=False,
            default=False,
            db_index=True)

    equipment_instance_problem_diagnoses = \
        ManyToManyField(
            to='EquipmentProblemPeriod',   # EquipmentInstanceProblemDiagnosis
            related_name=RELATED_NAME + '_reverse',
            related_query_name=RELATED_QUERY_NAME,
            blank=True)

    has_associated_equipment_instance_problem_diagnoses = \
        BooleanField(
            blank=False,
            null=False,
            default=False,
            db_index=True)

    last_updated = \
        DateTimeField(
            auto_now=True)

    class Meta:
        unique_together = \
            'equipment_instance', \
            'alarm_type', \
            'from_utc_date_time'

        ordering = \
            'equipment_instance', \
            '-from_utc_date_time'

    def __str__(self):
        return '{}: {} from {}{}'.format(
                self.equipment_instance,
                self.alarm_type.name.upper(),
                self.from_utc_date_time,
                ' to {} ({:.3f} Days)'.format(self.to_utc_date_time, self.duration_in_days)
                    if self.to_utc_date_time
                    else ' (ONGOING)')

    def save(self, *args, **kwargs):
        if self.to_utc_date_time:
            self.duration_in_days = \
                (self.to_utc_date_time - self.from_utc_date_time).total_seconds() \
                / _ONE_DAY_TIME_DELTA_TOTAL_SECONDS

            _to_date = (self.to_utc_date_time + _ONE_DAY_TIME_DELTA).date()

        else:
            self.duration_in_days = _to_date = None

        self.date_range = \
            DateRange(
                lower=(self.from_utc_date_time - _ONE_DAY_TIME_DELTA).date(),
                upper=_to_date,
                bounds='[]',
                empty=False)

        super(type(self), self).save(*args, **kwargs)


class EquipmentProblemPeriod(Model):
    RELATED_NAME = 'equipment_instance_problem_diagnoses'
    RELATED_QUERY_NAME = 'equipment_instance_problem_diagnosis'

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
            db_index=True)

    to_date = \
        DateField(
            blank=True,
            null=True,
            db_index=True)

    date_range = \
        DateRangeField(
            blank=True,
            null=True)

    duration = \
        IntegerField(
            blank=True,
            null=True)

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
            default=False,
            db_index=True)

    dismissed = \
        BooleanField(
            blank=False,
            null=False,
            default=False,
            db_index=True)

    comments = \
        TextField(
            blank=True,
            null=True)

    equipment_instance_alarm_periods = \
        ManyToManyField(
            to=EquipmentInstanceAlarmPeriod,
            through=EquipmentInstanceAlarmPeriod.equipment_instance_problem_diagnoses.through,
            related_name=RELATED_NAME + '_reverse',
            related_query_name=RELATED_QUERY_NAME,
            blank=True)

    has_associated_equipment_instance_alarm_periods = \
        BooleanField(
            blank=False,
            null=False,
            default=False,
            db_index=True)

    equipment_instance_alert_periods = \
        ManyToManyField(
            to='Alert',   # EquipmentInstanceAlertPeriod
            related_name=RELATED_NAME + '_reverse',
            related_query_name=RELATED_QUERY_NAME,
            blank=True)
    
    has_associated_equipment_instance_alert_periods = \
        BooleanField(
            blank=False,
            null=False,
            default=False,
            db_index=True)

    last_updated = \
        DateTimeField(
            auto_now=True)

    class Meta:
        unique_together = \
            'equipment_instance', \
            'from_date'

        ordering = \
            'dismissed', \
            '-to_date', \
            'from_date'

    def __str__(self):
        return '{} from {} {}{}{}'.format(
                self.equipment_instance,
                self.from_date,
                'to {}'.format(self.to_date)
                    if self.to_date
                    else '(ONGOING)',
                ': {}'.format(
                    ', '.join(equipment_problem_type.name.upper()
                              for equipment_problem_type in self.equipment_problem_types.all()))
                    if self.equipment_problem_types.count()
                    else '',
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
            (self.to_date - self.from_date).days + 1 \
            if self.to_date \
            else None

        super(type(self), self).save(*args, **kwargs)


# rename more correctly
EquipmentInstanceProblemDiagnosis = EquipmentProblemPeriod


class AlertDiagnosisStatus(Model):
    RELATED_NAME = 'alert_diagnosis_statuses'
    RELATED_QUERY_NAME = 'alert_diagnosis_status'

    index = \
        PositiveSmallIntegerField(
            blank=False,
            null=False,
            unique=True,
            default=0,
            db_index=True)

    name = \
        CharField(
            verbose_name='Alert Diagnosis Status Name',
            max_length=MAX_CHAR_LEN,
            blank=False,
            null=False,
            unique=True,
            default='to_diagnose')

    class Meta:
        verbose_name_plural = 'Alert Diagnosis Statuses'

        ordering = 'index',

    def __str__(self):
        return '{}. {}'.format(self.index, self.name)

    def save(self, *args, **kwargs):
        self.name = clean_lower_str(self.name)
        super(type(self), self).save(*args, **kwargs)


class Alert(Model):
    RELATED_NAME = 'equipment_instance_alert_periods'
    RELATED_QUERY_NAME = 'equipment_instance_alert_period'

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
            unique=False,
            db_index=True)

    threshold = \
        FloatField(
            blank=False,
            null=False,
            default=0,
            db_index=True)

    from_date = \
        DateField(
            blank=False,
            null=False,
            auto_now=False,
            auto_created=False,
            default=None,
            db_index=True)

    to_date = \
        DateField(
            blank=False,
            null=False,
            auto_now=False,
            auto_created=False,
            default=None,
            db_index=True)

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
            default=False,
            db_index=True)

    info = \
        JSONField(
            blank=True,
            null=True,
            default=dict)

    diagnosis_status = \
        ForeignKey(
            to=AlertDiagnosisStatus,
            blank=True,
            null=True,
            on_delete=PROTECT)

    equipment_instance_alarm_periods = \
        ManyToManyField(
            to=EquipmentInstanceAlarmPeriod,
            through=EquipmentInstanceAlarmPeriod.equipment_instance_alert_periods.through,
            related_name=RELATED_NAME + '_reverse',
            related_query_name=RELATED_QUERY_NAME,
            blank=True)

    has_associated_equipment_instance_alarm_periods = \
        BooleanField(
            blank=False,
            null=False,
            default=False,
            db_index=True)

    equipment_instance_problem_diagnoses = \
        ManyToManyField(
            to=EquipmentInstanceProblemDiagnosis,
            through=EquipmentInstanceProblemDiagnosis.equipment_instance_alert_periods.through,
            related_name=RELATED_NAME + '_reverse',
            related_query_name=RELATED_QUERY_NAME,
            blank=True)
    
    has_associated_equipment_instance_problem_diagnoses = \
        BooleanField(
            blank=False,
            null=False,
            default=False,
            db_index=True)

    last_updated = \
        DateTimeField(
            auto_now=True)

    class Meta:
        unique_together = \
            ('equipment_unique_type_group',
             'equipment_instance',
             'risk_score_name',
             'threshold',
             'from_date'), \
            ('equipment_unique_type_group',
             'equipment_instance',
             'risk_score_name',
             'threshold',
             'to_date')

        ordering = \
            'diagnosis_status', \
            '-ongoing', \
            'risk_score_name', \
            '-threshold', \
            '-cumulative_excess_risk_score'

    def __str__(self):
        if self.diagnosis_status is None:
            self.save()
            
        return '{}: {}Alert on {} {} #{} from {} to {} w Approx Avg Risk Score {:,.1f} (Last: {:,.1f}) (based on {} > {}) for {:,} Day(s)'.format(
                self.diagnosis_status.name.upper(),
                'ONGOING '
                    if self.ongoing
                    else '',
                self.equipment_unique_type_group.equipment_general_type.name.upper(),
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

        super(type(self), self).save(*args, **kwargs)


# rename more correctly
EquipmentInstanceAlertPeriod = Alert


def equipment_instance_alarm_period_post_save(sender, instance, *args, **kwargs):
    equipment_instance_alert_periods = \
        EquipmentInstanceAlertPeriod.objects.filter(
            equipment_instance=instance.equipment_instance,
            date_range__overlap=instance.date_range)

    instance.equipment_instance_alert_periods.set(
        equipment_instance_alert_periods,
        clear=False)

    equipment_instance_alert_periods.update(
        has_associated_equipment_instance_alarm_periods=True)

    equipment_instance_problem_diagnoses = \
        EquipmentInstanceProblemDiagnosis.objects.filter(
            equipment_instance=instance.equipment_instance,
            date_range__overlap=instance.date_range)

    instance.equipment_instance_problem_diagnoses.set(
        equipment_instance_problem_diagnoses,
        clear=False)

    equipment_instance_problem_diagnoses.update(
        has_associated_equipment_instance_alarm_periods=True)

    EquipmentInstanceAlarmPeriod.objects.filter(pk=instance.pk).update(
        has_associated_equipment_instance_alert_periods=bool(equipment_instance_alert_periods.count()),
        has_associated_equipment_instance_problem_diagnoses=bool(equipment_instance_problem_diagnoses.count()))


post_save.connect(
    receiver=equipment_instance_alarm_period_post_save,
    sender=EquipmentInstanceAlarmPeriod,
    weak=True,
    dispatch_uid=None,
    apps=None)


def equipment_instance_alert_period(sender, instance, *args, **kwargs):
    equipment_instance_alarm_periods = \
        EquipmentInstanceAlarmPeriod.objects.filter(
            equipment_instance=instance.equipment_instance,
            date_range__overlap=instance.date_range)

    instance.equipment_instance_alarm_periods.set(
        equipment_instance_alarm_periods,
        clear=False)

    equipment_instance_alarm_periods.update(
        has_associated_equipment_instance_alert_periods=True)

    equipment_instance_problem_diagnoses = \
        EquipmentInstanceProblemDiagnosis.objects.filter(
            equipment_instance=instance.equipment_instance,
            date_range__overlap=instance.date_range)
    
    instance.equipment_instance_problem_diagnoses.set(
        equipment_instance_problem_diagnoses,
        clear=False)

    equipment_instance_problem_diagnoses.update(
        has_associated_equipment_instance_alert_periods=True)

    Alert.objects.filter(pk=instance.pk).update(
        has_associated_equipment_instance_problem_diagnoses=bool(equipment_instance_problem_diagnoses.count()))


post_save.connect(
    receiver=equipment_instance_alert_period,
    sender=EquipmentInstanceAlertPeriod,
    weak=True,
    dispatch_uid=None,
    apps=None)


def equipment_instance_problem_diagnosis_post_save(sender, instance, *args, **kwargs):
    equipment_instance_alarm_periods = \
        EquipmentInstanceAlarmPeriod.objects.filter(
            equipment_instance=instance.equipment_instance,
            date_range__overlap=instance.date_range)

    instance.equipment_instance_alarm_periods.set(
        equipment_instance_alarm_periods,
        clear=False)

    equipment_instance_alarm_periods.update(
        has_associated_equipment_instance_problem_diagnoses=True)

    equipment_instance_alert_periods = \
        EquipmentInstanceAlertPeriod.objects.filter(
            equipment_instance=instance.equipment_instance,
            date_range__overlap=instance.date_range)

    instance.equipment_instance_alert_periods.set(
        equipment_instance_alert_periods,
        clear=False)

    equipment_instance_alert_periods.update(
        has_associated_equipment_instance_problem_diagnoses=True)

    EquipmentInstanceProblemDiagnosis.objects.filter(pk=instance.pk).update(
        has_equipment_problems=bool(instance.equipment_problem_types.count()),
        has_associated_equipment_instance_alarm_periods=bool(equipment_instance_alarm_periods.count()),
        has_associated_equipment_instance_alert_periods=bool(equipment_instance_alert_periods.count()))


post_save.connect(
    receiver=equipment_instance_problem_diagnosis_post_save,
    sender=EquipmentInstanceProblemDiagnosis,
    weak=True,
    dispatch_uid=None,
    apps=None)
