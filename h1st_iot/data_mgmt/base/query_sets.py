from django.db.models import Prefetch

from .models import (
    GlobalConfig,
    DataType,
    NumericMeasurementUnit,
    EquipmentDataFieldType,
    EquipmentGeneralType,
    EquipmentDataField,
    EquipmentUniqueTypeGroup,
    EquipmentUniqueType,
    EquipmentFacility,
    EquipmentInstance,
    EquipmentInstanceDataFieldDailyAgg,
    EquipmentSystem,
    EquipmentUniqueTypeGroupDataFieldProfile,
)


GLOBAL_CONFIG_QUERY_SET = \
    GlobalConfig.objects.all()


DATA_TYPE_QUERY_SET = \
    DataType.objects.all()


NUMERIC_MEASUREMENT_UNIT_NAME_ONLY_UNORDERED_QUERY_SET = \
    NumericMeasurementUnit.objects \
    .only('name') \
    .order_by()


NUMERIC_MEASUREMENT_UNIT_QUERY_SET = \
    NumericMeasurementUnit.objects.all()


EQUIPMENT_DATA_FIELD_TYPE_QUERY_SET = \
    EquipmentDataFieldType.objects.all()


EQUIPMENT_GENERAL_TYPE_UNORDERED_QUERY_SET = \
    EquipmentGeneralType.objects \
    .order_by()


EQUIPMENT_GENERAL_TYPE_QUERY_SET = \
    EquipmentGeneralType.objects.all()


EQUIPMENT_DATA_FIELD_ID_ONLY_UNORDERED_QUERY_SET = \
    EquipmentDataField.objects \
    .only('id') \
    .order_by()


EQUIPMENT_DATA_FIELD_NAME_ONLY_QUERY_SET = \
    EquipmentDataField.objects \
    .only('name') \
    .order_by('name')


EQUIPMENT_DATA_FIELD_INCL_DESCRIPTION_QUERY_SET = \
    EquipmentDataField.objects \
    .select_related(
        'equipment_general_type',
        'equipment_data_field_type',
        'data_type',
        'numeric_measurement_unit')


EQUIPMENT_DATA_FIELD_STR_QUERY_SET = \
    EQUIPMENT_DATA_FIELD_INCL_DESCRIPTION_QUERY_SET \
    .defer('description')


EQUIPMENT_DATA_FIELD_STR_UNORDERED_QUERY_SET = \
    EQUIPMENT_DATA_FIELD_STR_QUERY_SET \
    .order_by()


EQUIPMENT_UNIQUE_TYPE_GROUP_ID_ONLY_UNORDERED_QUERY_SET = \
    EquipmentUniqueTypeGroup.objects \
    .only('id') \
    .order_by()


EQUIPMENT_UNIQUE_TYPE_GROUP_NAME_ONLY_QUERY_SET = \
    EquipmentUniqueTypeGroup.objects \
    .only('name') \
    .order_by('name')


EQUIPMENT_UNIQUE_TYPE_GROUP_INCL_DESCRIPTION_QUERY_SET = \
    EquipmentUniqueTypeGroup.objects \
    .select_related(
        'equipment_general_type')


EQUIPMENT_UNIQUE_TYPE_GROUP_STR_QUERY_SET = \
    EQUIPMENT_UNIQUE_TYPE_GROUP_INCL_DESCRIPTION_QUERY_SET \
    .defer('description')


EQUIPMENT_UNIQUE_TYPE_GROUP_STR_UNORDERED_QUERY_SET = \
    EQUIPMENT_UNIQUE_TYPE_GROUP_STR_QUERY_SET \
    .order_by()


EQUIPMENT_UNIQUE_TYPE_ID_ONLY_UNORDERED_QUERY_SET = \
    EquipmentUniqueType.objects \
    .only('id') \
    .order_by()


EQUIPMENT_UNIQUE_TYPE_NAME_ONLY_QUERY_SET = \
    EquipmentUniqueType.objects \
    .defer(
        'equipment_general_type') \
    .order_by(
        'name')


EQUIPMENT_UNIQUE_TYPE_INCL_DESCRIPTION_QUERY_SET = \
    EquipmentUniqueType.objects \
    .select_related(
        'equipment_general_type')


EQUIPMENT_UNIQUE_TYPE_STR_QUERY_SET = \
    EQUIPMENT_UNIQUE_TYPE_INCL_DESCRIPTION_QUERY_SET  \
    .defer('description')


EQUIPMENT_UNIQUE_TYPE_STR_UNORDERED_QUERY_SET = \
    EQUIPMENT_UNIQUE_TYPE_STR_QUERY_SET \
    .order_by()


EQUIPMENT_DATA_FIELD_REST_API_QUERY_SET = \
    EQUIPMENT_DATA_FIELD_INCL_DESCRIPTION_QUERY_SET \
    .prefetch_related(
        Prefetch(
            lookup='equipment_unique_types',
            queryset=EQUIPMENT_UNIQUE_TYPE_INCL_DESCRIPTION_QUERY_SET))


EQUIPMENT_UNIQUE_TYPE_GROUP_REST_API_QUERY_SET = \
    EQUIPMENT_UNIQUE_TYPE_GROUP_INCL_DESCRIPTION_QUERY_SET \
    .prefetch_related(
        Prefetch(
            lookup='equipment_unique_types',
            queryset=EQUIPMENT_UNIQUE_TYPE_INCL_DESCRIPTION_QUERY_SET),
        Prefetch(
            lookup='equipment_data_fields',
            queryset=EQUIPMENT_DATA_FIELD_INCL_DESCRIPTION_QUERY_SET))


EQUIPMENT_UNIQUE_TYPE_REST_API_QUERY_SET = \
    EQUIPMENT_UNIQUE_TYPE_INCL_DESCRIPTION_QUERY_SET \
    .prefetch_related(
        Prefetch(
            lookup='equipment_data_fields',
            queryset=EQUIPMENT_DATA_FIELD_INCL_DESCRIPTION_QUERY_SET),
        Prefetch(
            lookup='equipment_unique_type_groups',
            queryset=EQUIPMENT_UNIQUE_TYPE_GROUP_INCL_DESCRIPTION_QUERY_SET))


EQUIPMENT_INSTANCE_ID_ONLY_UNORDERED_QUERY_SET = \
    EquipmentInstance.objects \
    .only('id') \
    .order_by()


EQUIPMENT_INSTANCE_RELATED_TO_EQUIPMENT_UNIQUE_TYPE_ID_ONLY_UNORDERED_QUERY_SET = \
    EquipmentInstance.objects \
    .only(
        'id',
        'equipment_unique_type') \
    .order_by()


EQUIPMENT_INSTANCE_RELATED_TO_EQUIPMENT_FACILITY_ID_ONLY_UNORDERED_QUERY_SET = \
    EquipmentInstance.objects \
    .only(
        'id',
        'equipment_facility') \
    .order_by()


EQUIPMENT_INSTANCE_RELATED_TO_EQUIPMENT_FACILITY_STR_QUERY_SET = \
    EquipmentInstance.objects \
    .only(
        'name',
        'equipment_facility') \
    .order_by(
        'name')


EQUIPMENT_INSTANCE_NAME_ONLY_QUERY_SET = \
    EquipmentInstance.objects \
    .only(
        'name') \
    .order_by(
        'name')


EQUIPMENT_INSTANCE_STR_QUERY_SET = \
    EquipmentInstance.objects \
    .defer(
        'equipment_facility',
        'info') \
    .select_related(
        'equipment_general_type',
        'equipment_unique_type') \
    .defer(
        'equipment_unique_type__equipment_general_type')


EQUIPMENT_INSTANCE_REST_API_QUERY_SET = \
    EquipmentInstance.objects \
    .select_related(
        'equipment_general_type',
        'equipment_unique_type', 'equipment_unique_type__equipment_general_type',
        'equipment_facility') \
    .defer(
        'equipment_facility__info') \
    .prefetch_related(
        Prefetch(
            lookup='equipment_unique_type_groups',
            queryset=EQUIPMENT_UNIQUE_TYPE_GROUP_INCL_DESCRIPTION_QUERY_SET))


EQUIPMENT_FACILITY_NAME_ONLY_UNORDERED_QUERY_SET = \
    EquipmentFacility.objects \
    .only('name') \
    .order_by()


EQUIPMENT_FACILITY_STR_QUERY_SET = \
    EquipmentFacility.objects


EQUIPMENT_FACILITY_REST_API_QUERY_SET = \
    EQUIPMENT_FACILITY_STR_QUERY_SET \
    .prefetch_related(
        Prefetch(
            lookup='equipment_instances',
            queryset=EQUIPMENT_INSTANCE_RELATED_TO_EQUIPMENT_FACILITY_STR_QUERY_SET))


EQUIPMENT_INSTANCE_DATA_FIELD_DAILY_AGG_REST_API_QUERY_SET = \
    EquipmentInstanceDataFieldDailyAgg.objects \
    .select_related(
        'equipment_instance',
        'equipment_data_field',
        'equipment_data_field__equipment_general_type', 'equipment_data_field__equipment_data_field_type',
        'equipment_data_field__data_type', 'equipment_data_field__numeric_measurement_unit') \
    .defer(
        'equipment_instance__equipment_general_type',
        'equipment_instance__equipment_unique_type',
        'equipment_instance__equipment_facility',
        'equipment_instance__info')


EQUIPMENT_SYSTEM_REST_API_QUERY_SET = \
    EquipmentSystem.objects \
    .select_related(
        'equipment_facility') \
    .defer(
        'equipment_facility__info') \
    .prefetch_related(
        Prefetch(
            lookup='equipment_instances',
            queryset=EQUIPMENT_INSTANCE_NAME_ONLY_QUERY_SET))


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
