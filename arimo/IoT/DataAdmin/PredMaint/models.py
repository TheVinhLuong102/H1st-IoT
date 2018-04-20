from django.db.models import \
    Model, \
    BooleanField, CharField, DateField, DateTimeField, FloatField, ForeignKey, ManyToManyField, URLField, \
    CASCADE, PROTECT, SET_NULL

from django.contrib.postgres.fields import JSONField

from ..base.models import EquipmentGeneralType, EquipmentUniqueTypeGroup, EquipmentInstance
from ..util import MAX_CHAR_LEN


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

    url = \
        URLField(
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

    def __unicode__(self):
        return 'Blueprint "{}" ({}){}'.format(
            self.uuid,
            self.timestamp,
            '' if self.active
               else ' (INACTIVE)')


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

    active = \
        BooleanField(
            blank=False,
            null=False,
            default=True)

    class Meta:
        ordering = \
            'risk_score_name', \
            '-threshold', \
            '-quantified_risk_degree'

    def __unicode__(self):
        return '{}Alert on {} {} Instance {} from {} to {} with Quantfd Risk Deg {:,.1f} based on {} > {}'.format(
            '' if self.active
               else '(INACTIVE) ',
            self.equipment_general_type.name.upper(),
            self.equipment_unique_type_group.name,
            self.equipment_instance.name,
            self.from_date,
            self.to_date,
            self.quantified_risk_degree,
            self.risk_score_name,
            self.threshold)
