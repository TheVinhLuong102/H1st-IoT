from django.contrib.admin import ModelAdmin, site

from silk.profiling.profiler import silk_profile

from .models import \
    EquipmentUniqueTypeGroupRiskScoringTask, EquipmentUniqueTypeGroupCopyRiskScoresToDBTask


class EquipmentUniqueTypeGroupRiskScoringTaskAdmin(ModelAdmin):
    list_display = \
        'equipment_unique_type_group', \
        'date', \
        'finished'

    list_filter = \
        'equipment_unique_type_group__equipment_general_type__name', \
        'equipment_unique_type_group__name', \
        'date'

    search_fields = \
        'equipment_unique_type_group__equipment_general_type__name', \
        'equipment_unique_type_group__name'

    list_select_related = \
        'equipment_unique_type_group', 'equipment_unique_type_group__equipment_general_type'

    show_full_result_count = False   # too many

    readonly_fields = \
        'equipment_unique_type_group', \
        'date', \
        'finished'

    @silk_profile(name='ADMIN: Equipment Unique Type Group Risk Scoring Tasks')
    def changelist_view(self, request, extra_context=None):
        return super(EquipmentUniqueTypeGroupRiskScoringTaskAdmin, self).changelist_view(
                request=request,
                extra_context=extra_context)

    @silk_profile(name='ADMIN: Equipment Unique Type Group Risk Scoring Task')
    def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
        return super(EquipmentUniqueTypeGroupRiskScoringTaskAdmin, self).changeform_view(
                request=request,
                object_id=object_id,
                form_url=form_url,
                extra_context=extra_context)


site.register(
    EquipmentUniqueTypeGroupRiskScoringTask,
    admin_class=EquipmentUniqueTypeGroupRiskScoringTaskAdmin)


class EquipmentUniqueTypeGroupCopyRiskScoresToDBTaskAdmin(ModelAdmin):
    list_display = \
        'equipment_unique_type_group', \
        'date', \
        'finished'

    list_filter = \
        'equipment_unique_type_group__equipment_general_type__name', \
        'equipment_unique_type_group__name', \
        'date'

    search_fields = \
        'equipment_unique_type_group__equipment_general_type__name', \
        'equipment_unique_type_group__name'

    list_select_related = \
        'equipment_unique_type_group', 'equipment_unique_type_group__equipment_general_type'

    show_full_result_count = False   # too many

    readonly_fields = \
        'equipment_unique_type_group', \
        'date', \
        'finished'

    @silk_profile(name='ADMIN: Equipment Unique Type Group Copy Risk Scores to DB Tasks')
    def changelist_view(self, request, extra_context=None):
        return super(EquipmentUniqueTypeGroupCopyRiskScoresToDBTaskAdmin, self).changelist_view(
                request=request,
                extra_context=extra_context)

    @silk_profile(name='ADMIN: Equipment Unique Type Group Copy Risk Scores to DB  Task')
    def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
        return super(EquipmentUniqueTypeGroupCopyRiskScoresToDBTaskAdmin, self).changeform_view(
                request=request,
                object_id=object_id,
                form_url=form_url,
                extra_context=extra_context)


site.register(
    EquipmentUniqueTypeGroupCopyRiskScoresToDBTask,
    admin_class=EquipmentUniqueTypeGroupCopyRiskScoresToDBTaskAdmin)
