from dal import autocomplete

from .models import EquipmentProblemPeriod


class EquipmentProblemPeriodForm(autocomplete.FutureModelForm):
    class Meta:
        model = EquipmentProblemPeriod
        fields = '__all__'
        widgets = {
            'equipment_problem_types':
                autocomplete.ModelSelect2Multiple(
                    url='EquipmentProblemType-AutoComplete',
                    attrs={
                        # Only trigger autocompletion after characters have been typed
                        'data-minimum-input-length': 1
                    }
                )
        }
