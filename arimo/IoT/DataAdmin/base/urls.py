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


# API end-points
urlpatterns = format_suffix_patterns([
    url(r'$^', api_root),

    url(r'^data_types/$',
        DataTypeList.as_view(),
        name='data-type-list'),
    url(r'^data_types/(?P<pk>[0-9]+)/$',
        DataTypeDetail.as_view(),
        name='data-type-detail'),

    url(r'^numeric_measurement_units/$',
        NumericMeasurementUnitList.as_view(),
        name='numeric-measurement-unit-list'),
    url(r'^numeric_measurement_units/(?P<pk>[0-9]+)/$',
        NumericMeasurementUnitDetail.as_view(),
        name='numeric-measurement-unit-detail'),

    url(r'^equipment_data_field_types/$',
        EquipmentDataFieldTypeList.as_view(),
        name='equipment-data-field-type-list'),
    url(r'^equipment_data_field_types/(?P<pk>[0-9]+)/$',
        EquipmentDataFieldTypeDetail.as_view(),
        name='equipment-data-field-type-detail'),

    url(r'^equipment_general_types/$',
        EquipmentGeneralTypeList.as_view(),
        name='equipment-general-type-list'),
    url(r'^equipment_general_types/(?P<pk>[0-9]+)/$',
        EquipmentGeneralTypeDetail.as_view(),
        name='equipment-general-type-detail'),

    url(r'^equipment_data_fields/$',
        EquipmentDataFieldList.as_view(),
        name='equipment-data-field-list'),
    url(r'^equipment_data_fields/(?P<pk>[0-9]+)/$',
        EquipmentDataFieldDetail.as_view(),
        name='equipment-data-field-detail'),

    url(r'^equipment_unique_type_groups/$',
        EquipmentUniqueTypeGroupList.as_view(),
        name='equipment-unique-type-group-list'),
    url(r'^equipment_unique_type_groups/(?P<pk>[0-9]+)/$',
        EquipmentUniqueTypeGroupDetail.as_view(),
        name='equipment-unique-type-group-detail'),

    url(r'^equipment_unique_types/$',
        EquipmentUniqueTypeList.as_view(),
        name='equipment-unique-type-list'),
    url(r'^equipment_unique_types/(?P<pk>[0-9]+)/$',
        EquipmentUniqueTypeDetail.as_view(),
        name='equipment-unique-type-detail'),

    url(r'^equipment_facilities/$',
        EquipmentFacilityList.as_view(),
        name='equipment-facility-list'),
    url(r'^equipment_facilities/(?P<pk>[0-9]+)/$',
        EquipmentFacilityDetail.as_view(),
        name='equipment-facility-detail'),

    url(r'^equipment_instances/$',
        EquipmentInstanceList.as_view(),
        name='equipment-instance-list'),
    url(r'^equipment_instances/(?P<pk>[0-9]+)/$',
        EquipmentInstanceDetail.as_view(),
        name='equipment-instance-detail'),

    url(r'^equipment_systems/$',
        EquipmentSystemList.as_view(),
        name='equipment-system-list'),
    url(r'^equipment_systems/(?P<pk>[0-9]+)/$',
        EquipmentSystemDetail.as_view(),
        name='equipment-system-detail')
])
