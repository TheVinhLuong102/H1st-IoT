from dal import autocomplete

from .models import EquipmentDataField, EquipmentUniqueTypeGroup, EquipmentUniqueType


class EquipmentDataFieldAutoComplete(autocomplete.Select2QuerySetView):
    name = 'EquipmentDataField-AutoComplete'

    def get_queryset(self):
        if self.request.user.is_authenticated():
            query_set = EquipmentDataField.objects.all()

        else:
            return EquipmentDataField.objects.none()

        if self.q:
            query_set = query_set.filter(name__icontains=self.q)

        return query_set


class EquipmentUniqueTypeGroupAutoComplete(autocomplete.Select2QuerySetView):
    name = 'EquipmentUniqueTypeGroup-AutoComplete'

    def get_queryset(self):
        if self.request.user.is_authenticated():
            query_set = EquipmentUniqueTypeGroup.objects.all()

        else:
            return EquipmentUniqueTypeGroup.objects.none()

        if self.q:
            query_set = query_set.filter(name__icontains=self.q)

        return query_set


class EquipmentUniqueTypeAutoComplete(autocomplete.Select2QuerySetView):
    name = 'EquipmentUniqueType-AutoComplete'

    def get_queryset(self):
        if self.request.user.is_authenticated():
            query_set = EquipmentUniqueType.objects.all()

        else:
            return EquipmentUniqueType.objects.none()

        if self.q:
            query_set = query_set.filter(name__icontains=self.q)

        return query_set
