from dal import autocomplete

from .models import EquipmentDataField, EquipmentUniqueType


class EquipmentDataFieldForm(autocomplete.FutureModelForm):
    class Meta:
        model = EquipmentDataField
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


class EquipmentUniqueTypeForm(autocomplete.FutureModelForm):
    class Meta:
        model = EquipmentUniqueType
        fields = '__all__'
        widgets = {
            'equipment_data_fields':
                autocomplete.ModelSelect2Multiple(
                    url='EquipmentDataField-AutoComplete',
                    attrs={
                        # Only trigger autocompletion after characters have been typed
                        'data-minimum-input-length': 1
                    }
                )
        }
