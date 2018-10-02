from rest_framework.routers import DefaultRouter, SimpleRouter
from rest_framework.urlpatterns import format_suffix_patterns

from .views import \
    DataTypeViewSet, \
    NumericMeasurementUnitViewSet, \
    EquipmentDataFieldTypeViewSet, \
    EquipmentGeneralTypeViewSet, \
    EquipmentDataFieldViewSet, \
    EquipmentUniqueTypeGroupViewSet, \
    EquipmentUniqueTypeViewSet, \
    EquipmentFacilityViewSet, \
    EquipmentInstanceViewSet, \
    EquipmentSystemViewSet


ROUTER = DefaultRouter()
ROUTER.register('data-types', DataTypeViewSet)
ROUTER.register('numeric-measurement-units', NumericMeasurementUnitViewSet)
ROUTER.register('equipment-data-field-types', EquipmentDataFieldTypeViewSet)
ROUTER.register('equipment-general-types', EquipmentGeneralTypeViewSet)
ROUTER.register('equipment-data-fields', EquipmentDataFieldViewSet)
ROUTER.register('equipment-unique-type-groups', EquipmentUniqueTypeGroupViewSet)
ROUTER.register('equipment-unique-types', EquipmentUniqueTypeViewSet)
ROUTER.register('equipment-facilities', EquipmentFacilityViewSet)
ROUTER.register('equipment-instances', EquipmentInstanceViewSet)
ROUTER.register('equipment-systems', EquipmentSystemViewSet)


URL_PATTERNS = []
