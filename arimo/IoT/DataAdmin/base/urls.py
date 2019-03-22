from django.conf.urls import include, url

from rest_framework.routers import DefaultRouter

from .autocompletes import \
    NumericMeasurementUnitAutoComplete, \
    EquipmentGeneralTypeAutoComplete, \
    EquipmentDataFieldAutoComplete, \
    EquipmentUniqueTypeGroupAutoComplete, \
    EquipmentUniqueTypeAutoComplete, \
    EquipmentFacilityAutoComplete, \
    EquipmentInstanceAutoComplete

from .views import \
    GlobalConfigViewSet, \
    DataTypeViewSet, \
    NumericMeasurementUnitViewSet, \
    EquipmentDataFieldTypeViewSet, \
    EquipmentGeneralTypeViewSet, \
    EquipmentDataFieldViewSet, \
    EquipmentUniqueTypeGroupViewSet, \
    EquipmentUniqueTypeViewSet, \
    EquipmentFacilityViewSet, \
    EquipmentInstanceViewSet, \
    EquipmentInstanceDataFieldDailyAggViewSet, \
    EquipmentSystemViewSet, \
    ErrorViewSet


ROUTER = DefaultRouter()
ROUTER.register('global-configs', GlobalConfigViewSet)
ROUTER.register('data-types', DataTypeViewSet)
ROUTER.register('numeric-measurement-units', NumericMeasurementUnitViewSet)
ROUTER.register('equipment-data-field-types', EquipmentDataFieldTypeViewSet)
ROUTER.register('equipment-general-types', EquipmentGeneralTypeViewSet)
ROUTER.register('equipment-data-fields', EquipmentDataFieldViewSet)
ROUTER.register('equipment-unique-type-groups', EquipmentUniqueTypeGroupViewSet)
ROUTER.register('equipment-unique-types', EquipmentUniqueTypeViewSet)
ROUTER.register('equipment-facilities', EquipmentFacilityViewSet)
ROUTER.register('equipment-instances', EquipmentInstanceViewSet)
ROUTER.register('equipment-instance-data-field-daily-aggs', EquipmentInstanceDataFieldDailyAggViewSet)
ROUTER.register('equipment-systems', EquipmentSystemViewSet)
ROUTER.register('errors', ErrorViewSet)


URL_PATTERNS = [
    # API URLs
    url(r'^api/base/', include(ROUTER.urls)),

    # Auto-Complete URLs
    url(r'^{}/$'.format(NumericMeasurementUnitAutoComplete.name),
        NumericMeasurementUnitAutoComplete.as_view(),
        name=NumericMeasurementUnitAutoComplete.name),

    url(r'^{}/$'.format(EquipmentGeneralTypeAutoComplete.name),
        EquipmentGeneralTypeAutoComplete.as_view(),
        name=EquipmentGeneralTypeAutoComplete.name),

    url(r'^{}/$'.format(EquipmentDataFieldAutoComplete.name),
        EquipmentDataFieldAutoComplete.as_view(),
        name=EquipmentDataFieldAutoComplete.name),

    url(r'^{}/$'.format(EquipmentUniqueTypeGroupAutoComplete.name),
        EquipmentUniqueTypeGroupAutoComplete.as_view(),
        name=EquipmentUniqueTypeGroupAutoComplete.name),

    url(r'^{}/$'.format(EquipmentUniqueTypeAutoComplete.name),
        EquipmentUniqueTypeAutoComplete.as_view(),
        name=EquipmentUniqueTypeAutoComplete.name),

    url(r'^{}/$'.format(EquipmentFacilityAutoComplete.name),
        EquipmentFacilityAutoComplete.as_view(),
        name=EquipmentFacilityAutoComplete.name),

    url(r'^{}/$'.format(EquipmentInstanceAutoComplete.name),
        EquipmentInstanceAutoComplete.as_view(),
        name=EquipmentInstanceAutoComplete.name)
]
