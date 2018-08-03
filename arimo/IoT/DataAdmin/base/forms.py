from dal import autocomplete

from .models import \
    EquipmentDataField, \
    EquipmentUniqueTypeGroup, \
    EquipmentUniqueType, \
    EquipmentInstance, \
    EquipmentSystem


class EquipmentDataFieldForm(autocomplete.FutureModelForm):
    class Meta:
        model = EquipmentDataField

        fields = '__all__'

        widgets = dict(
            equipment_unique_types=
                autocomplete.ModelSelect2Multiple(
                    url='EquipmentUniqueType-AutoComplete',
                    attrs={# Only trigger autocompletion after characters have been typed
                           'data-minimum-input-length': 1}))


class EquipmentUniqueTypeGroupForm(autocomplete.FutureModelForm):
    class Meta:
        model = EquipmentUniqueTypeGroup

        fields = '__all__'

        widgets = dict(
            equipment_unique_types=
                autocomplete.ModelSelect2Multiple(
                    url='EquipmentUniqueType-AutoComplete',
                    attrs={# Only trigger autocompletion after characters have been typed
                           'data-minimum-input-length': 1}))


class EquipmentUniqueTypeForm(autocomplete.FutureModelForm):
    class Meta:
        model = EquipmentUniqueType

        fields = '__all__'

        widgets = dict(
            data_fields=
                autocomplete.ModelSelect2Multiple(
                    url='EquipmentDataField-AutoComplete',
                    attrs={# Only trigger autocompletion after characters have been typed
                           'data-minimum-input-length': 1}),

            groups=
                autocomplete.ModelSelect2Multiple(
                    url='EquipmentUniqueTypeGroup-AutoComplete',
                    attrs={# Only trigger autocompletion after characters have been typed
                           'data-minimum-input-length': 1}))


class EquipmentInstanceForm(autocomplete.FutureModelForm):
    class Meta:
        model = EquipmentInstance

        fields = '__all__'

        widgets = dict(
            equipment_unique_type=
                autocomplete.ModelSelect2(
                    url='EquipmentUniqueType-AutoComplete',
                    attrs={# Only trigger autocompletion after characters have been typed
                           'data-minimum-input-length': 1}),

            equipment_facility=
                autocomplete.ModelSelect2(
                    url='EquipmentFacility-AutoComplete',
                    attrs={# Only trigger autocompletion after characters have been typed
                        'data-minimum-input-length': 1}),

            data_fields=
                autocomplete.ModelSelect2Multiple(
                    url='EquipmentDataField-AutoComplete',
                    attrs={# Only trigger autocompletion after characters have been typed
                           'data-minimum-input-length': 1}))


class EquipmentSystemForm(autocomplete.FutureModelForm):
    class Meta:
        model = EquipmentSystem

        fields = '__all__'

        widgets = dict(
            equipment_facility=
                autocomplete.ModelSelect2(
                    url='EquipmentFacility-AutoComplete',
                    attrs={# Only trigger autocompletion after characters have been typed
                        'data-minimum-input-length': 1}),

            equipment_instances=
                autocomplete.ModelSelect2Multiple(
                    url='EquipmentInstance-AutoComplete',
                    attrs={# Only trigger autocompletion after characters have been typed
                           'data-minimum-input-length': 1}))
