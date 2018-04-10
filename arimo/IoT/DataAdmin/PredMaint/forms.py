from dal import autocomplete

from .models import Blueprint


class BlueprintForm(autocomplete.FutureModelForm):
    class Meta:
        model = Blueprint
        fields = '__all__'
        widgets = {
            'equipment_unique_types':
                autocomplete.ModelSelect2Multiple(
                    url='EquipmentUniqueType-AutoComplete',
                    attrs={
                        # Only trigger autocompletion after characters have been typed
                        'data-minimum-input-length': 1
                    }
                )
        }
