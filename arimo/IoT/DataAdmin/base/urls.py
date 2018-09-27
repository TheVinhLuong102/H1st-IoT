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


# API end-points
urlpatterns = format_suffix_patterns([
    url(r'^{}/$'.format(API_ROOT_URL), api_root),

    url(r'^{}/data-types/$'.format(API_ROOT_URL),
        DataTypeList.as_view(),
        name='data-type-list'),
    url(r'^data_types/(?P<pk>[0-9]+)/$',
        DataTypeDetail.as_view(),
        name='data-type-detail'),

    url(r'^{}/numeric-measurement-units/$'.format(API_ROOT_URL),
        NumericMeasurementUnitList.as_view(),
        name='numeric-measurement-unit-list'),
    url(r'^numeric_measurement_units/(?P<pk>[0-9]+)/$',
        NumericMeasurementUnitDetail.as_view(),
        name='numeric-measurement-unit-detail'),

    url(r'^{}/equipment-data-field-types/$'.format(API_ROOT_URL),
        EquipmentDataFieldTypeList.as_view(),
        name='equipment-data-field-type-list'),
    url(r'^equipment_data_field_types/(?P<pk>[0-9]+)/$',
        EquipmentDataFieldTypeDetail.as_view(),
        name='equipment-data-field-type-detail'),

    url(r'^{}/equipment-general-types/$'.format(API_ROOT_URL),
        EquipmentGeneralTypeList.as_view(),
        name='equipment-general-type-list'),
    url(r'^equipment_general_types/(?P<pk>[0-9]+)/$',
        EquipmentGeneralTypeDetail.as_view(),
        name='equipment-general-type-detail'),

    url(r'^{}/equipment-data-fields/$'.format(API_ROOT_URL),
        EquipmentDataFieldList.as_view(),
        name='equipment-data-field-list'),
    url(r'^equipment_data_fields/(?P<pk>[0-9]+)/$',
        EquipmentDataFieldDetail.as_view(),
        name='equipment-data-field-detail'),

    url(r'^{}/equipment-unique-type-groups/$'.format(API_ROOT_URL),
        EquipmentUniqueTypeGroupList.as_view(),
        name='equipment-unique-type-group-list'),
    url(r'^equipment_unique_type_groups/(?P<pk>[0-9]+)/$',
        EquipmentUniqueTypeGroupDetail.as_view(),
        name='equipment-unique-type-group-detail'),

    url(r'^{}/equipment-unique-types/$'.format(API_ROOT_URL),
        EquipmentUniqueTypeList.as_view(),
        name='equipment-unique-type-list'),
    url(r'^equipment_unique_types/(?P<pk>[0-9]+)/$',
        EquipmentUniqueTypeDetail.as_view(),
        name='equipment-unique-type-detail'),

    url(r'^{}/equipment_facilities/$'.format(API_ROOT_URL),
        EquipmentFacilityList.as_view(),
        name='equipment-facility-list'),
    url(r'^equipment_facilities/(?P<pk>[0-9]+)/$',
        EquipmentFacilityDetail.as_view(),
        name='equipment-facility-detail'),

    url(r'^{}/equipment_instances/$'.format(API_ROOT_URL),
        EquipmentInstanceList.as_view(),
        name='equipment-instance-list'),
    url(r'^equipment_instances/(?P<pk>[0-9]+)/$',
        EquipmentInstanceDetail.as_view(),
        name='equipment-instance-detail'),

    url(r'^{}/equipment_systems/$'.format(API_ROOT_URL),
        EquipmentSystemList.as_view(),
        name='equipment-system-list'),
    url(r'^equipment_systems/(?P<pk>[0-9]+)/$',
        EquipmentSystemDetail.as_view(),
        name='equipment-system-detail')
])
