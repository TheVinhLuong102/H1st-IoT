from dal import autocomplete

from .models import EquipmentDataField, EquipmentUniqueTypeGroup, EquipmentUniqueType, EquipmentFacility, EquipmentInstance


class EquipmentDataFieldAutoComplete(autocomplete.Select2QuerySetView):
    name = 'EquipmentDataField-AutoComplete'

    def get_queryset(self):
        if self.request.user.is_authenticated:
            query_set = \
                EquipmentDataField.objects \
                .select_related(
                    'equipment_general_type',
                    'equipment_data_field_type',
                    'data_type',
                    'numeric_measurement_unit')

            return query_set.filter(name__icontains=self.q) \
                if self.q \
              else query_set

        else:
            return EquipmentDataField.objects.none()


class EquipmentUniqueTypeGroupAutoComplete(autocomplete.Select2QuerySetView):
    name = 'EquipmentUniqueTypeGroup-AutoComplete'

    def get_queryset(self):
        if self.request.user.is_authenticated:
            query_set = \
                EquipmentUniqueTypeGroup.objects \
                .select_related(
                    'equipment_general_type')

            return query_set.filter(name__icontains=self.q) \
                if self.q \
              else query_set

        else:
            return EquipmentUniqueTypeGroup.objects.none()


class EquipmentUniqueTypeAutoComplete(autocomplete.Select2QuerySetView):
    name = 'EquipmentUniqueType-AutoComplete'

    def get_queryset(self):
        if self.request.user.is_authenticated:
            query_set = \
                EquipmentUniqueType.objects.objects \
                .select_related(
                    'equipment_general_type')

            return query_set.filter(name__icontains=self.q) \
                if self.q \
              else query_set

        else:
            return EquipmentUniqueType.objects.none()


class EquipmentFacilityAutoComplete(autocomplete.Select2QuerySetView):
    name = 'EquipmentFacility-AutoComplete'

    def get_queryset(self):
        if self.request.user.is_authenticated:
            query_set = EquipmentFacility.objects.all()

            return query_set.filter(name__icontains=self.q) \
                if self.q \
              else query_set

        else:
            return EquipmentFacility.objects.none()


class EquipmentInstanceAutoComplete(autocomplete.Select2QuerySetView):
    name = 'EquipmentInstance-AutoComplete'

    def get_queryset(self):
        if self.request.user.is_authenticated:
            query_set = \
                EquipmentInstance.objects \
                .select_related(
                    'equipment_general_type',
                    'equipment_unique_type',
                    'equipment_facility')

            return query_set.filter(name__icontains=self.q) \
                if self.q \
              else query_set

        else:
            return EquipmentInstance.objects.none()
