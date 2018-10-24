from dal import autocomplete

from .models import EquipmentProblemType, EquipmentProblemDiagnosis


class EquipmentProblemTypeAutoComplete(autocomplete.Select2QuerySetView):
    name = 'EquipmentProblemType-AutoComplete'

    def get_queryset(self):
        if self.request.user.is_authenticated:
            query_set = EquipmentProblemType.objects.all()

            return query_set.filter(name__icontains=self.q) \
                if self.q \
              else query_set

        else:
            return EquipmentProblemType.objects.none()


class EquipmentProblemDiagnosisAutoComplete(autocomplete.Select2QuerySetView):
    name = 'EquipmentProblemDiagnosis-AutoComplete'

    def get_queryset(self):
        if self.request.user.is_authenticated:
            query_set = EquipmentProblemDiagnosis.objects.all()

            return query_set.filter(equipment_instance__name__icontains=self.q) \
                if self.q \
              else query_set

        else:
            return EquipmentProblemDiagnosis.objects.none()
