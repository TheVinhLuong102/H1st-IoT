from django.db.models import \
    Model, \
    BooleanField, CharField, DateField, DateTimeField, ForeignKey, ManyToManyField, URLField, \
    CASCADE, PROTECT, SET_NULL

from django.contrib.postgres.fields import JSONField

from ..base.models import EquipmentGeneralType, EquipmentUniqueType
from ..util import MAX_CHAR_LEN


class Blueprint(Model):
    RELATED_NAME = 'blueprints'
    RELATED_QUERY_NAME = 'blueprint'

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

    equipment_general_type = \
        ForeignKey(
            to=EquipmentGeneralType,
            related_name=RELATED_NAME,
            related_query_name=RELATED_QUERY_NAME,
            blank=False,
            null=False,
            on_delete=PROTECT)

    equipment_unique_type = \
        ForeignKey(
            to=EquipmentUniqueType,
            related_name=RELATED_NAME,
            related_query_name=RELATED_QUERY_NAME,
            blank=True,
            null=True,
            on_delete=PROTECT)

    trained_to_date = \
        DateField(
            blank=True,
            null=True,
            auto_now=False,
            auto_created=False,
            default=None)

    timestamp = \
        DateTimeField(
            blank=True,
            null=True,
            auto_now=False,
            auto_created=False,
            default=None)

    active = \
        BooleanField(
            blank=False,
            null=False,
            default=True)

    benchmark_metrics = \
        JSONField(
            default=dict,
            encoder=None)

    class Meta:
        ordering = 'equipment_general_type', 'equipment_unique_type', 'trained_to_date', 'timestamp'

    def __unicode__(self):
        return 'Blueprint "{}"'.format(self.uuid)
