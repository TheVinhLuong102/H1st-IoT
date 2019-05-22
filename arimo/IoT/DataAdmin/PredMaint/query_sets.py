from .models import \
    GlobalConfig, \
    EquipmentUniqueTypeGroupDataFieldProfile


GLOBAL_CONFIG_QUERY_SET = \
    GlobalConfig.objects.all()


EQUIPMENT_UNIQUE_TYPE_GROUP_DATA_FIELD_PROFILE_REST_API_QUERY_SET = \
    EquipmentUniqueTypeGroupDataFieldProfile.objects \
    .select_related(
        'equipment_unique_type_group',
        'equipment_data_field',
        'equipment_data_field__equipment_general_type', 'equipment_data_field__equipment_data_field_type',
        'equipment_data_field__data_type', 'equipment_data_field__numeric_measurement_unit') \
    .defer(
        'equipment_unique_type_group__equipment_general_type',
        'equipment_unique_type_group__description',
        'equipment_unique_type_group__last_updated',
        'equipment_data_field__last_updated',
        'equipment_data_field__numeric_measurement_unit__description')
