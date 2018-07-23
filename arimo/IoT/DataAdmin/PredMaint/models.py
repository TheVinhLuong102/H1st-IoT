from django.db.models import \
    Model, \
    BooleanField, CharField, DateField, DateTimeField, FloatField, ForeignKey, PositiveSmallIntegerField, \
    ManyToManyField, TextField, URLField, \
    CASCADE, PROTECT, SET_NULL
from django.contrib.postgres.fields import JSONField
from django.utils.encoding import python_2_unicode_compatible

from ..base.models import EquipmentGeneralType, EquipmentUniqueTypeGroup, EquipmentInstance
from ..util import MAX_CHAR_LEN, clean_lower_str


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

    timestamp = \
        DateTimeField(
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

    benchmark_metrics = \
        JSONField(
            default=dict,
            encoder=None)

    active = \
        BooleanField(
            blank=False,
            null=False,
            default=False)

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


@python_2_unicode_compatible
class EquipmentProblemType(Model):
    name = \
        CharField(
            max_length=MAX_CHAR_LEN,
            blank=False,
            null=False,
            unique=True)

    class Meta:
        ordering = 'name',

    def __str__(self):
        return 'EqProbTp {}'.format(self.name.upper())

    def save(self, *args, **kwargs):
        self.name = clean_lower_str(self.name)
        return super(EquipmentProblemType, self).save(*args, **kwargs)


@python_2_unicode_compatible
class EquipmentProblemPeriod(Model):
    RELATED_NAME = 'equipment_problem_instances'
    RELATED_QUERY_NAME = 'equipment_problem_instance'

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

    equipment_problem_types = \
        ManyToManyField(
            to=EquipmentProblemType,
            related_name=RELATED_NAME,
            related_query_name=RELATED_QUERY_NAME,
            blank=True)

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
            related_name=RELATED_NAME,
            related_query_name=RELATED_QUERY_NAME,
            blank=True)

    class Meta:
        ordering = '-from_date', '-to_date', 'equipment_instance', 'dismissed'

    def __str__(self):
        return 'EqInst #{} from {} to {}: {}{}'.format(
            self.equipment_instance.name,
            self.from_date,
            self.to_date,
            ', '.join(equipment_problem_type.name.upper()
                      for equipment_problem_type in self.equipment_problem_types.all()),
            ' (DISMISSED)'
                if self.dismissed
                else '')


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

    quantified_risk_degree = \
        FloatField(
            blank=False,
            null=False,
            default=0)

    diagnosis_status = \
        ForeignKey(
            to=AlertDiagnosisStatus,
            blank=True,
            null=True)

    equipment_problem_periods = \
        ManyToManyField(
            to=EquipmentProblemPeriod,
            through=EquipmentProblemPeriod.alerts.through,
            # related_name=RELATED_NAME,
            # related_query_name=RELATED_QUERY_NAME,
                # Arimo_IoT_DataAdmin_PredMaint.Alert.equipment_problem_periods: (fields.E302) Reverse accessor for 'Alert.equipment_problem_periods' clashes with field name 'EquipmentProblemPeriod.alerts'.
                # HINT: Rename field 'EquipmentProblemPeriod.alerts', or add/change a related_name argument to the definition for field 'Alert.equipment_problem_periods'.
            blank=True)

    class Meta:
        ordering = \
            'diagnosis_status', \
            'risk_score_name', \
            '-threshold', \
            '-quantified_risk_degree'

    def __str__(self):
        if self.diagnosis_status is None:
            self.save()
            
        return '{}: Alert on {} {} #{} from {} to {} with Quantified Risk Degree {:,.1f} based on {} > {}'.format(
            self.diagnosis_status.name.upper(),
            self.equipment_general_type.name.upper(),
            self.equipment_unique_type_group.name,
            self.equipment_instance.name,
            self.from_date,
            self.to_date,
            self.quantified_risk_degree,
            self.risk_score_name,
            self.threshold)

    def save(self, *args, **kwargs):
        if self.diagnosis_status is None:
            self.diagnosis_status = AlertDiagnosisStatus.objects.get_or_create(index=0)[0]
        return super(Alert, self).save(*args, **kwargs)
