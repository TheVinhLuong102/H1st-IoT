from django.forms import ModelChoiceField, ModelMultipleChoiceField

from dal import autocomplete   # *** DON'T IMPORT SPECIFIC ITEMS INSIDE autocomplete AS THEY CHANGE BETWEEN VERSIONS ***

from .autocompletes import \
    EquipmentGeneralTypeAutoComplete, \
    EquipmentDataFieldAutoComplete, \
    EquipmentUniqueTypeGroupAutoComplete, \
    EquipmentUniqueTypeAutoComplete, \
    EquipmentFacilityAutoComplete, \
    EquipmentInstanceAutoComplete
from .models import \
    EquipmentDataField, \
    EquipmentUniqueTypeGroup, \
    EquipmentUniqueType, \
    EquipmentInstance, \
    EquipmentSystem


class EquipmentUniqueTypeGroupForm(autocomplete.FutureModelForm):
    equipment_unique_types = \
        ModelMultipleChoiceField(
            queryset=
                EquipmentUniqueType.objects
                .select_related(
                    'equipment_general_type'),
            widget=
                autocomplete.ModelSelect2Multiple(
                    url=EquipmentUniqueTypeAutoComplete.name,
                    attrs={# Only trigger autocompletion after characters have been typed
                           'data-minimum-input-length': 1}),
            required=False)

    class Meta:
        model = EquipmentUniqueTypeGroup

        fields = '__all__'


class EquipmentUniqueTypeForm(autocomplete.FutureModelForm):
    data_fields = \
        ModelMultipleChoiceField(
            queryset=
                EquipmentDataField.objects
                .select_related(
                    'equipment_general_type',
                    'equipment_data_field_type',
                    'data_type',
                    'numeric_measurement_unit'),
            widget=
                autocomplete.ModelSelect2Multiple(
                    url=EquipmentDataFieldAutoComplete.name,
                    attrs={# Only trigger autocompletion after characters have been typed
                           'data-minimum-input-length': 1}),
            required=False)

    class Meta:
        model = EquipmentUniqueType

        fields = '__all__'


class EquipmentInstanceForm(autocomplete.FutureModelForm):
    equipment_unique_type = \
        ModelChoiceField(
            queryset=
                EquipmentUniqueType.objects
                .select_related(
                    'equipment_general_type'),
            widget=
                autocomplete.ModelSelect2(
                    url=EquipmentUniqueTypeAutoComplete.name,
                    attrs={# Only trigger autocompletion after characters have been typed
                           'data-minimum-input-length': 1}),
            required=False)

    class Meta:
        model = EquipmentInstance

        fields = '__all__'

        widgets = dict(
            equipment_general_type=
                autocomplete.ModelSelect2(
                    url=EquipmentGeneralTypeAutoComplete.name),

            equipment_facility=
                autocomplete.ModelSelect2(
                    url=EquipmentFacilityAutoComplete.name,
                    attrs={# Only trigger autocompletion after characters have been typed
                           'data-minimum-input-length': 1}))


class EquipmentSystemForm(autocomplete.FutureModelForm):
    equipment_instances = \
        ModelMultipleChoiceField(
            queryset=
                EquipmentInstance.objects
                .select_related(
                    'equipment_general_type',
                    'equipment_unique_type', 'equipment_unique_type__equipment_general_type',
                    'equipment_facility'),
            widget=
                autocomplete.ModelSelect2Multiple(
                    url=EquipmentInstanceAutoComplete.name,
                    attrs={# Only trigger autocompletion after characters have been typed
                           'data-minimum-input-length': 1}),
            required=True)

    class Meta:
        model = EquipmentSystem

        fields = '__all__'

        widgets = dict(
            equipment_facility=
                autocomplete.ModelSelect2(
                    url=EquipmentFacilityAutoComplete.name,
                    attrs={# Only trigger autocompletion after characters have been typed
                           'data-minimum-input-length': 1}))
