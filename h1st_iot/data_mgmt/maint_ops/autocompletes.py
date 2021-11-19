"""H1st IoT Data Management: Maintenance Operations: Autocompletes."""


# *** DON'T IMPORT SPECIFIC ITEMS INSIDE autocomplete
# AS THEY CHANGE BETWEEN VERSIONS ***
from dal import autocomplete

from h1st_iot.data_mgmt.maint_ops.models import (
    EquipmentProblemType,
    EquipmentInstanceProblemDiagnosis,
)


class EquipmentProblemTypeAutoComplete(autocomplete.Select2QuerySetView):
    """EquipmentProblemTypeAutoComplete."""

    name = 'EquipmentProblemType-AutoComplete'

    def get_queryset(self):
        """Queryset."""
        if self.request.user.is_authenticated:
            query_set = EquipmentProblemType.objects.all()

            return (query_set.filter(name__icontains=self.q)
                    if self.q
                    else query_set)

        return EquipmentProblemType.objects.none()


class EquipmentInstanceProblemDiagnosisAutoComplete(
        autocomplete.Select2QuerySetView):
    """EquipmentInstanceProblemDiagnosisAutoComplete."""

    name = 'EquipmentInstanceProblemDiagnosis-AutoComplete'

    def get_queryset(self):
        """Queryset."""
        if self.request.user.is_authenticated:
            query_set = EquipmentInstanceProblemDiagnosis.objects.all()

            return (query_set.filter(
                        equipment_instance__name__icontains=self.q)
                    if self.q
                    else query_set)

        return EquipmentInstanceProblemDiagnosis.objects.none()
