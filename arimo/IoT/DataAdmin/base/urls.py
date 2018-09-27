import os

from django.conf.urls import url

from rest_framework.urlpatterns import format_suffix_patterns

from .views import api_root, \
    DataTypeList, DataTypeDetail, \
    NumericMeasurementUnitList, NumericMeasurementUnitDetail, \
    EquipmentDataFieldTypeList, EquipmentDataFieldTypeDetail, \
    EquipmentGeneralTypeList, EquipmentGeneralTypeDetail, \
    EquipmentDataFieldList, EquipmentDataFieldDetail, \
    EquipmentUniqueTypeGroupList, EquipmentUniqueTypeGroupDetail, \
    EquipmentUniqueTypeList, EquipmentUniqueTypeDetail, \
    EquipmentFacilityList, EquipmentFacilityDetail, \
    EquipmentInstanceList, EquipmentInstanceDetail, \
    EquipmentSystemList, EquipmentSystemDetail


API_ROOT_URL = 'api/base'
DATA_TYPES_API_URL = os.path.join(API_ROOT_URL, 'data-types')
NUMERIC_MEASUREMENT_UNITS_API_URL = os.path.join(API_ROOT_URL, 'numeric-measurement-units')
EQUIPMENT_DATA_FIELD_TYPES_API_URL = os.path.join(API_ROOT_URL, 'equipment-data-field-types')
EQUIPMENT_GENERAL_TYPES_API_URL = os.path.join(API_ROOT_URL, 'equipment-general-types')
EQUIPMENT_DATA_FIELDS_API_URL = os.path.join(API_ROOT_URL, 'equipment-data-fields')
EQUIPMENT_UNIQUE_TYPE_GROUPS_API_URL = os.path.join(API_ROOT_URL, 'equipment-unique-type-groups')
EQUIPMENT_UNIQUE_TYPES_API_URL = os.path.join(API_ROOT_URL, 'equipment-unique-types')
EQUIPMENT_FACILITIES_API_URL = os.path.join(API_ROOT_URL, 'equipment-facilities')
EQUIPMENT_INSTANCES_API_URL = os.path.join(API_ROOT_URL, 'equipment-instances')
EQUIPMENT_SYSTEMS_API_URL = os.path.join(API_ROOT_URL, 'equipment-systems')


# API end-points
urlpatterns = format_suffix_patterns([
    url(r'^{}/$'.format(API_ROOT_URL), api_root),

    url(r'^/$'.format(DATA_TYPES_API_URL),
        DataTypeList.as_view(),
        name='data-type-list'),
    url(r'^/(?P<pk>[0-9]+)/$'.format(DATA_TYPES_API_URL),
        DataTypeDetail.as_view(),
        name='data-type-detail'),

    url(r'^{}/$'.format(NUMERIC_MEASUREMENT_UNITS_API_URL),
        NumericMeasurementUnitList.as_view(),
        name='numeric-measurement-unit-list'),
    url(r'^{}/(?P<pk>[0-9]+)/$'.format(NUMERIC_MEASUREMENT_UNITS_API_URL),
        NumericMeasurementUnitDetail.as_view(),
        name='numeric-measurement-unit-detail'),

    url(r'^{}/$'.format(EQUIPMENT_DATA_FIELD_TYPES_API_URL),
        EquipmentDataFieldTypeList.as_view(),
        name='equipment-data-field-type-list'),
    url(r'^{}/(?P<pk>[0-9]+)/$'.format(EQUIPMENT_DATA_FIELD_TYPES_API_URL),
        EquipmentDataFieldTypeDetail.as_view(),
        name='equipment-data-field-type-detail'),

    url(r'^{}/$'.format(EQUIPMENT_GENERAL_TYPES_API_URL),
        EquipmentGeneralTypeList.as_view(),
        name='equipment-general-type-list'),
    url(r'^{}/(?P<pk>[0-9]+)/$'.format(EQUIPMENT_GENERAL_TYPES_API_URL),
        EquipmentGeneralTypeDetail.as_view(),
        name='equipment-general-type-detail'),

    url(r'^{}/$'.format(EQUIPMENT_DATA_FIELDS_API_URL),
        EquipmentDataFieldList.as_view(),
        name='equipment-data-field-list'),
    url(r'^{}/(?P<pk>[0-9]+)/$'.format(EQUIPMENT_DATA_FIELDS_API_URL),
        EquipmentDataFieldDetail.as_view(),
        name='equipment-data-field-detail'),

    url(r'^{}/$'.format(EQUIPMENT_UNIQUE_TYPE_GROUPS_API_URL),
        EquipmentUniqueTypeGroupList.as_view(),
        name='equipment-unique-type-group-list'),
    url(r'^{}/(?P<pk>[0-9]+)/$'.format(EQUIPMENT_UNIQUE_TYPE_GROUPS_API_URL),
        EquipmentUniqueTypeGroupDetail.as_view(),
        name='equipment-unique-type-group-detail'),

    url(r'^{}/$'.format(EQUIPMENT_UNIQUE_TYPES_API_URL),
        EquipmentUniqueTypeList.as_view(),
        name='equipment-unique-type-list'),
    url(r'^{}/(?P<pk>[0-9]+)/$'.format(EQUIPMENT_UNIQUE_TYPES_API_URL),
        EquipmentUniqueTypeDetail.as_view(),
        name='equipment-unique-type-detail'),

    url(r'^{}/$'.format(EQUIPMENT_FACILITIES_API_URL),
        EquipmentFacilityList.as_view(),
        name='equipment-facility-list'),
    url(r'^{}/(?P<pk>[0-9]+)/$'.format(EQUIPMENT_FACILITIES_API_URL),
        EquipmentFacilityDetail.as_view(),
        name='equipment-facility-detail'),

    url(r'^{}/$'.format(EQUIPMENT_INSTANCES_API_URL),
        EquipmentInstanceList.as_view(),
        name='equipment-instance-list'),
    url(r'^{}/(?P<pk>[0-9]+)/$'.format(EQUIPMENT_INSTANCES_API_URL),
        EquipmentInstanceDetail.as_view(),
        name='equipment-instance-detail'),

    url(r'^{}/$'.format(EQUIPMENT_SYSTEMS_API_URL),
        EquipmentSystemList.as_view(),
        name='equipment-system-list'),
    url(r'^{}(?P<pk>[0-9]+)/$'.format(EQUIPMENT_SYSTEMS_API_URL),
        EquipmentSystemDetail.as_view(),
        name='equipment-system-detail')
])
