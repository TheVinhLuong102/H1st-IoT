from dal import autocomplete

from .models import EquipmentDataField, EquipmentUniqueTypeGroup, EquipmentUniqueType, EquipmentFacility, EquipmentInstance


class EquipmentDataFieldAutoComplete(autocomplete.Select2QuerySetView):
    name = 'EquipmentDataField-AutoComplete'

    def get_queryset(self):
        if self.request.user.is_authenticated:
            query_set = EquipmentDataField.objects.all()

        else:
            return EquipmentDataField.objects.none()

        if self.q:
            query_set = query_set.filter(name__icontains=self.q)

        return query_set


class EquipmentUniqueTypeGroupAutoComplete(autocomplete.Select2QuerySetView):
    name = 'EquipmentUniqueTypeGroup-AutoComplete'

    def get_queryset(self):
        if self.request.user.is_authenticated:
            query_set = EquipmentUniqueTypeGroup.objects.all()

        else:
            return EquipmentUniqueTypeGroup.objects.none()

        if self.q:
            query_set = query_set.filter(name__icontains=self.q)

        return query_set


class EquipmentUniqueTypeAutoComplete(autocomplete.Select2QuerySetView):
    name = 'EquipmentUniqueType-AutoComplete'

    def get_queryset(self):
        if self.request.user.is_authenticated:
            query_set = EquipmentUniqueType.objects.all()

        else:
            return EquipmentUniqueType.objects.none()

        if self.q:
            query_set = query_set.filter(name__icontains=self.q)

        return query_set


class EquipmentFacilityAutoComplete(autocomplete.Select2QuerySetView):
    name = 'EquipmentFacility-AutoComplete'

    def get_queryset(self):
        if self.request.user.is_authenticated:
            query_set = EquipmentFacility.objects.all()

        else:
            return EquipmentFacility.objects.none()

        if self.q:
            query_set = query_set.filter(name__icontains=self.q)

        return query_set


class EquipmentInstanceAutoComplete(autocomplete.Select2QuerySetView):
    name = 'EquipmentInstance-AutoComplete'

    def get_queryset(self):
        if self.request.user.is_authenticated:
            query_set = EquipmentInstance.objects.all()

        else:
            return EquipmentInstance.objects.none()

        if self.q:
            query_set = query_set.filter(name__icontains=self.q)

        return query_set
