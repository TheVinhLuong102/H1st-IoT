from django.db.models import \
    Model, \
    DateField, DateTimeField, \
    ForeignKey, \
    PROTECT

from ..base.models import EquipmentUniqueTypeGroup


class EquipmentUniqueTypeGroupRiskScoringTask(Model):
    RELATED_NAME = 'equipment_unique_type_group_risk_scoring_task'
    RELATED_QUERY_NAME = 'equipment_unique_type_group_risk_scoring_tasks'

    equipment_unique_type_group = \
        ForeignKey(
            to=EquipmentUniqueTypeGroup,
            related_name=RELATED_NAME,
            related_query_name=RELATED_QUERY_NAME,
            blank=False,
            null=False,
            on_delete=PROTECT)

    date = \
        DateField(
            blank=False,
            null=False,
            default=None,
            auto_now=False,
            auto_now_add=False)

    finished = \
        DateTimeField(
            blank=True,
            null=True,
            default=None,
            auto_now=False,
            auto_now_add=False)

    class Meta:
        unique_together = \
            'equipment_unique_type_group', \
            'date'

        ordering = \
            'equipment_unique_type_group', \
            '-date'


class EquipmentUniqueTypeGroupDataAggTask(Model):
    RELATED_NAME = 'equipment_unique_type_group_data_agg_task'
    RELATED_QUERY_NAME = 'equipment_unique_type_group_data_agg_tasks'

    equipment_unique_type_group = \
        ForeignKey(
            to=EquipmentUniqueTypeGroup,
            related_name=RELATED_NAME,
            related_query_name=RELATED_QUERY_NAME,
            blank=False,
            null=False,
            on_delete=PROTECT)

    date = \
        DateField(
            blank=False,
            null=False,
            default=None,
            auto_now=False,
            auto_now_add=False)

    finished = \
        DateTimeField(
            blank=True,
            null=True,
            default=None,
            auto_now=False,
            auto_now_add=False)

    class Meta:
        unique_together = \
            'equipment_unique_type_group', \
            'date'

        ordering = \
            'equipment_unique_type_group', \
            '-date'
