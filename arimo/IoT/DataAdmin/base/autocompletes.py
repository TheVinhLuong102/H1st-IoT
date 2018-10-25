from dal import autocomplete   # *** DON'T IMPORT SPECIFIC ITEMS INSIDE autocomplete AS THEY CHANGE BETWEEN VERSIONS ***

from .models import \
    EquipmentGeneralType, \
    EquipmentDataField, \
    EquipmentUniqueTypeGroup, \
    EquipmentUniqueType, \
    EquipmentFacility, \
    EquipmentInstance


class EquipmentGeneralTypeAutoComplete(autocomplete.Select2QuerySetView):
    name = 'EquipmentGeneralType-AutoComplete'

    def get_queryset(self):
        if self.request.user.is_authenticated:
            query_set = EquipmentGeneralType.objects.all()

            return query_set.filter(name__icontains=self.q) \
                if self.q \
                else query_set

        else:
            return EquipmentGeneralType.objects.none()


class EquipmentDataFieldAutoComplete(autocomplete.Select2QuerySetView):
    name = 'EquipmentDataField-AutoComplete'

    def get_queryset(self):
        if self.request.user.is_authenticated:
            query_set = EquipmentDataField.objects.all()

            return query_set.filter(name__icontains=self.q) \
                if self.q \
              else query_set

        else:
            return EquipmentDataField.objects.none()


class EquipmentUniqueTypeGroupAutoComplete(autocomplete.Select2QuerySetView):
    name = 'EquipmentUniqueTypeGroup-AutoComplete'

    def get_queryset(self):
        if self.request.user.is_authenticated:
            query_set = EquipmentUniqueTypeGroup.objects.all()

            return query_set.filter(name__icontains=self.q) \
                if self.q \
              else query_set

        else:
            return EquipmentUniqueTypeGroup.objects.none()


class EquipmentUniqueTypeAutoComplete(autocomplete.Select2QuerySetView):
    name = 'EquipmentUniqueType-AutoComplete'

    def get_queryset(self):
        if self.request.user.is_authenticated:
            query_set = EquipmentUniqueType.objects.all()

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
            query_set = EquipmentInstance.objects.all()

            return query_set.filter(name__icontains=self.q) \
                if self.q \
              else query_set

        else:
            return EquipmentInstance.objects.none()
