from dal import autocomplete

from .models import EquipmentProblemPeriod, Alert


class EquipmentProblemPeriodForm(autocomplete.FutureModelForm):
    class Meta:
        model = EquipmentProblemPeriod
        fields = '__all__'
        widgets = {
            'equipment_instance':
                autocomplete.ModelSelect2(
                    url='EquipmentInstance-AutoComplete',
                    attrs={
                        # Only trigger autocompletion after characters have been typed
                        'data-minimum-input-length': 1
                    }
                ),

            'equipment_problem_types':
                autocomplete.ModelSelect2Multiple(
                    url='EquipmentProblemType-AutoComplete',
                    attrs={
                        # Only trigger autocompletion after characters have been typed
                        'data-minimum-input-length': 1
                    }
                )
        }


class AlertForm(autocomplete.FutureModelForm):
    class Meta:
        model = Alert
        fields = '__all__'
        widgets = {
            'equipment_instance':
                autocomplete.ModelSelect2(
                    url='EquipmentInstance-AutoComplete',
                    attrs={
                        # Only trigger autocompletion after characters have been typed
                        'data-minimum-input-length': 1
                    }
                )
        }
