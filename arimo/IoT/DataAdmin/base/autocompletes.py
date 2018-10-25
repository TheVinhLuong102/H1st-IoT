from dal.autocomplete import Select2QuerySetView

from .models import \
    EquipmentGeneralType, \
    EquipmentDataField, \
    EquipmentUniqueTypeGroup, \
    EquipmentUniqueType, \
    EquipmentFacility, \
    EquipmentInstance


class EquipmentGeneralTypeAutoComplete(Select2QuerySetView):
    name = 'EquipmentGeneralType-AutoComplete'

    def get_queryset(self):
        if self.request.user.is_authenticated:
            query_set = EquipmentGeneralType.objects.all()

            return query_set.filter(name__icontains=self.q) \
                if self.q \
                else query_set

        else:
            return EquipmentGeneralType.objects.none()


class EquipmentDataFieldAutoComplete(Select2QuerySetView):
    name = 'EquipmentDataField-AutoComplete'

    def get_queryset(self):
        if self.request.user.is_authenticated:
            query_set = EquipmentDataField.objects.all()

            return query_set.filter(name__icontains=self.q) \
                if self.q \
              else query_set

        else:
            return EquipmentDataField.objects.none()


class EquipmentUniqueTypeGroupAutoComplete(Select2QuerySetView):
    name = 'EquipmentUniqueTypeGroup-AutoComplete'

    def get_queryset(self):
        if self.request.user.is_authenticated:
            query_set = EquipmentUniqueTypeGroup.objects.all()

            return query_set.filter(name__icontains=self.q) \
                if self.q \
              else query_set

        else:
            return EquipmentUniqueTypeGroup.objects.none()


class EquipmentUniqueTypeAutoComplete(Select2QuerySetView):
    name = 'EquipmentUniqueType-AutoComplete'

    def get_queryset(self):
        if self.request.user.is_authenticated:
            query_set = EquipmentUniqueType.objects.all()

            return query_set.filter(name__icontains=self.q) \
                if self.q \
              else query_set

        else:
            return EquipmentUniqueType.objects.none()


class EquipmentFacilityAutoComplete(Select2QuerySetView):
    name = 'EquipmentFacility-AutoComplete'

    def get_queryset(self):
        if self.request.user.is_authenticated:
            query_set = EquipmentFacility.objects.all()

            return query_set.filter(name__icontains=self.q) \
                if self.q \
              else query_set

        else:
            return EquipmentFacility.objects.none()


class EquipmentInstanceAutoComplete(Select2QuerySetView):
    name = 'EquipmentInstance-AutoComplete'

    def get_queryset(self):
        if self.request.user.is_authenticated:
            query_set = EquipmentInstance.objects.all()

            return query_set.filter(name__icontains=self.q) \
                if self.q \
              else query_set

        else:
            return EquipmentInstance.objects.none()
