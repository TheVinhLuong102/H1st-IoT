from django.db.models import Prefetch

from .models import \
    GlobalConfig, \
    DataType, \
    NumericMeasurementUnit, \
    EquipmentDataFieldType, \
    EquipmentGeneralType, \
    EquipmentComponent, \
    EquipmentDataField, \
    EquipmentUniqueTypeGroup, \
    EquipmentUniqueType, \
    EquipmentFacility, \
    EquipmentInstance


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


EQUIPMENT_COMPONENT_ID_ONLY_UNORDERED_QUERY_SET = \
    EquipmentComponent.objects \
    .only('id') \
    .order_by()


EQUIPMENT_COMPONENT_NAME_ONLY_QUERY_SET = \
    EquipmentComponent.objects \
    .only('name') \
    .order_by('name')


EQUIPMENT_COMPONENT_INCL_DESCRIPTION_QUERY_SET = \
    EquipmentComponent.objects \
    .defer(
        'last_updated') \
    .select_related(
        'equipment_general_type')


EQUIPMENT_COMPONENT_STR_QUERY_SET = \
    EQUIPMENT_COMPONENT_INCL_DESCRIPTION_QUERY_SET \
    .defer('description')


EQUIPMENT_DATA_FIELD_ID_ONLY_UNORDERED_QUERY_SET = \
    EquipmentDataField.objects \
    .only('id') \
    .order_by()


EQUIPMENT_DATA_FIELD_INCL_DESCRIPTION_QUERY_SET = \
    EquipmentDataField.objects \
    .defer(
        'last_updated') \
    .select_related(
        'equipment_general_type',
        'equipment_data_field_type',
        'data_type',
        'numeric_measurement_unit') \
    .defer(
        'numeric_measurement_unit__description')


EQUIPMENT_DATA_FIELD_STR_QUERY_SET = \
    EQUIPMENT_DATA_FIELD_INCL_DESCRIPTION_QUERY_SET \
    .defer('description')


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
    .defer(
        'last_updated') \
    .select_related(
        'equipment_general_type')


EQUIPMENT_UNIQUE_TYPE_GROUP_STR_QUERY_SET = \
    EQUIPMENT_UNIQUE_TYPE_GROUP_INCL_DESCRIPTION_QUERY_SET \
    .defer('description')


EQUIPMENT_UNIQUE_TYPE_ID_ONLY_UNORDERED_QUERY_SET = \
    EquipmentUniqueType.objects \
    .only('id') \
    .order_by()


EQUIPMENT_UNIQUE_TYPE_NAME_ONLY_QUERY_SET = \
    EquipmentUniqueType.objects \
    .defer(
        'equipment_general_type',
        'description',
        'last_updated') \
    .order_by(
        'name')


EQUIPMENT_UNIQUE_TYPE_INCL_DESCRIPTION_QUERY_SET = \
    EquipmentUniqueType.objects \
    .defer(
        'last_updated') \
    .select_related(
        'equipment_general_type')


EQUIPMENT_UNIQUE_TYPE_STR_QUERY_SET = \
    EQUIPMENT_UNIQUE_TYPE_INCL_DESCRIPTION_QUERY_SET  \
    .defer('description')


EQUIPMENT_UNIQUE_TYPE_STR_UNORDERED_QUERY_SET = \
    EQUIPMENT_UNIQUE_TYPE_STR_QUERY_SET \
    .order_by()


EQUIPMENT_COMPONENT_REST_API_QUERY_SET = \
    EQUIPMENT_COMPONENT_INCL_DESCRIPTION_QUERY_SET \
    .prefetch_related(
        Prefetch(
            lookup='equipment_data_fields',
            queryset=EQUIPMENT_DATA_FIELD_INCL_DESCRIPTION_QUERY_SET),
        Prefetch(
            lookup='equipment_unique_types',
            queryset=EQUIPMENT_UNIQUE_TYPE_INCL_DESCRIPTION_QUERY_SET))


EQUIPMENT_DATA_FIELD_REST_API_QUERY_SET = \
    EQUIPMENT_DATA_FIELD_INCL_DESCRIPTION_QUERY_SET \
    .prefetch_related(
        Prefetch(
            lookup='equipment_components',
            queryset=EQUIPMENT_COMPONENT_INCL_DESCRIPTION_QUERY_SET),
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
            lookup='equipment_components',
            queryset=EQUIPMENT_COMPONENT_INCL_DESCRIPTION_QUERY_SET),
        Prefetch(
            lookup='equipment_data_fields',
            queryset=EQUIPMENT_DATA_FIELD_INCL_DESCRIPTION_QUERY_SET))


EQUIPMENT_UNIQUE_TYPE_REST_API_QUERY_SET = \
    EQUIPMENT_UNIQUE_TYPE_INCL_DESCRIPTION_QUERY_SET \
    .prefetch_related(
        Prefetch(
            lookup='equipment_components',
            queryset=EQUIPMENT_COMPONENT_INCL_DESCRIPTION_QUERY_SET),
        Prefetch(
            lookup='equipment_data_fields',
            queryset=EQUIPMENT_DATA_FIELD_INCL_DESCRIPTION_QUERY_SET),
        Prefetch(
            lookup='equipment_unique_type_groups',
            queryset=EQUIPMENT_UNIQUE_TYPE_GROUP_INCL_DESCRIPTION_QUERY_SET))


EQUIPMENT_FACILITY_STR_UNORDERED_QUERY_SET = \
    EquipmentFacility.objects \
    .only('name') \
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


EQUIPMENT_INSTANCE_STR_QUERY_SET = \
    EquipmentInstance.objects \
    .defer(
        'equipment_facility',
        'info',
        'last_updated') \
    .select_related(
        'equipment_general_type',
        'equipment_unique_type') \
    .defer(
        'equipment_unique_type__description', 'equipment_unique_type__last_updated')
