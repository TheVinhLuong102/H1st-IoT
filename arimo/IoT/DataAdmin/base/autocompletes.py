from dal import autocomplete

from .models import EquipmentDataField, EquipmentUniqueType


class EquipmentDataFieldAutoComplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if self.request.user.is_authenticated():
            query_set = EquipmentDataField.objects.all()

        else:
            return EquipmentDataField.objects.none()

        if self.q:
            query_set = query_set.filter(name__icontains=self.q)

        return query_set


class EquipmentUniqueTypeAutoComplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if self.request.user.is_authenticated():
            query_set = EquipmentUniqueType.objects.all()

        else:
            return EquipmentUniqueType.objects.none()

        if self.q:
            query_set = query_set.filter(name__icontains=self.q)

        return query_set
