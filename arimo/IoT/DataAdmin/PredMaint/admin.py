from django.contrib.admin import ModelAdmin, site

from .forms import EquipmentProblemPeriodForm
from .models import Blueprint, EquipmentProblemType, EquipmentProblemPeriod, Alert


class BlueprintAdmin(ModelAdmin):
    list_display = \
        'equipment_general_type', \
        'equipment_unique_type_group', \
        'trained_to_date', \
        'timestamp', \
        'uuid', \
        'active'

    list_filter = \
        'equipment_general_type', \
        'equipment_unique_type_group', \
        'trained_to_date', \
        'timestamp', \
        'active'

    list_select_related = \
        'equipment_general_type', \
        'equipment_unique_type_group'

    show_full_result_count = False

    search_fields = \
        'equipment_general_type', \
        'equipment_unique_type_group', \
        'uuid'


site.register(
    Blueprint,
    admin_class=BlueprintAdmin)


class EquipmentProblemTypeAdmin(ModelAdmin):
    list_display = 'name',

    list_filter = 'name',

    show_full_result_count = False

    search_fields = 'name',


site.register(
    EquipmentProblemType,
    admin_class=EquipmentProblemTypeAdmin)


class EquipmentProblemPeriodAdmin(ModelAdmin):
    list_display = 'equipment_instance', 'from_date', 'to_date'

    list_filter = 'equipment_instance', 'from_date', 'to_date'

    show_full_result_count = False

    search_fields = 'equipment_instance',

    form = EquipmentProblemPeriodForm


site.register(
    EquipmentProblemPeriod,
    admin_class=EquipmentProblemPeriodAdmin)


class AlertAdmin(ModelAdmin):
    list_display = \
        'equipment_general_type', \
        'equipment_unique_type_group', \
        'equipment_instance', \
        'risk_score_name', \
        'threshold', \
        'from_date', \
        'to_date', \
        'quantified_risk_degree', \
        'active'

    list_select_related = \
        'equipment_general_type', \
        'equipment_unique_type_group', \
        'equipment_instance'

    list_filter = \
        'equipment_general_type', \
        'equipment_unique_type_group', \
        'risk_score_name', \
        'threshold', \
        'from_date', \
        'to_date', \
        'active', \
        'equipment_instance'

    show_full_result_count = False

    search_fields = \
        'equipment_general_type', \
        'equipment_unique_type_group', \
        'equipment_instance', \
        'risk_score_name'


site.register(
    Alert,
    admin_class=AlertAdmin)
