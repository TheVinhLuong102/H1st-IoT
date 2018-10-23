from dal import autocomplete

from .models import EquipmentProblemType, EquipmentProblemDiagnosis


class EquipmentProblemTypeAutoComplete(autocomplete.Select2QuerySetView):
    name = 'EquipmentProblemType-AutoComplete'

    def get_queryset(self):
        if self.request.user.is_authenticated:
            query_set = EquipmentProblemType.objects.all()

        else:
            return EquipmentProblemType.objects.none()

        if self.q:
            query_set = query_set.filter(name__icontains=self.q)

        return query_set


class EquipmentProblemDiagnosisAutoComplete(autocomplete.Select2QuerySetView):
    name = 'EquipmentProblemDiagnosis-AutoComplete'

    def get_queryset(self):
        if self.request.user.is_authenticated:
            query_set = EquipmentProblemDiagnosis.objects.all()

        else:
            return EquipmentProblemDiagnosis.objects.none()

        if self.q:
            query_set = query_set.filter(equipment_instance__name__icontains=self.q)

        return query_set
