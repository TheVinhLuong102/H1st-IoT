from django.forms import ModelChoiceField, ModelMultipleChoiceField

from dal import autocomplete   # *** DON'T IMPORT SPECIFIC ITEMS INSIDE autocomplete AS THEY CHANGE BETWEEN VERSIONS ***

from .autocompletes import \
    EquipmentGeneralTypeAutoComplete, \
    EquipmentComponentAutoComplete, \
    EquipmentDataFieldAutoComplete, \
    EquipmentUniqueTypeGroupAutoComplete, \
    EquipmentUniqueTypeAutoComplete, \
    EquipmentFacilityAutoComplete, \
    EquipmentInstanceAutoComplete
from .models import \
    EquipmentComponent, \
    EquipmentDataField, \
    EquipmentUniqueTypeGroup, \
    EquipmentUniqueType, \
    EquipmentInstance, \
    EquipmentSystem


class EquipmentComponentForm(autocomplete.FutureModelForm):
    equipment_data_fields = \
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
                    attrs={'data-minimum-input-length': 1}))

    equipment_unique_types = \
        ModelMultipleChoiceField(
            queryset=
                EquipmentUniqueType.objects
                .select_related(
                    'equipment_general_type'),
            widget=
                autocomplete.ModelSelect2Multiple(
                    url=EquipmentUniqueTypeAutoComplete.name,
                    attrs={'data-minimum-input-length': 1}))

    class Meta:
        model = EquipmentComponent

        fields = '__all__'


class EquipmentDataFieldForm(autocomplete.FutureModelForm):
    equipment_components = \
        ModelMultipleChoiceField(
            queryset=
                EquipmentComponent.objects
                .select_related(
                    'equipment_general_type'),
            widget=
                autocomplete.ModelSelect2Multiple(
                    url=EquipmentComponentAutoComplete.name))

    equipment_unique_types = \
        ModelMultipleChoiceField(
            queryset=
                EquipmentUniqueType.objects
                .select_related(
                    'equipment_general_type'),
            widget=
                autocomplete.ModelSelect2Multiple(
                    url=EquipmentUniqueTypeAutoComplete.name,
                    attrs={'data-minimum-input-length': 1}))

    class Meta:
        model = EquipmentDataField

        fields = '__all__'


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
                    attrs={'data-minimum-input-length': 1}))

    equipment_components = \
        ModelMultipleChoiceField(
            queryset=
                EquipmentComponent.objects
                .select_related(
                    'equipment_general_type'))

    equipment_data_fields = \
        ModelMultipleChoiceField(
            queryset=
                EquipmentDataField.objects
                .select_related(
                    'equipment_general_type',
                    'equipment_data_field_type',
                    'data_type',
                    'numeric_measurement_unit'))

    class Meta:
        model = EquipmentUniqueTypeGroup

        fields = '__all__'


class EquipmentUniqueTypeForm(autocomplete.FutureModelForm):
    equipment_components = \
        ModelMultipleChoiceField(
            queryset=
                EquipmentComponent.objects
                .select_related(
                    'equipment_general_type'),
            widget=
                autocomplete.ModelSelect2Multiple(
                    url=EquipmentComponentAutoComplete.name))

    equipment_data_fields = \
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
                    attrs={'data-minimum-input-length': 1}))

    equipment_unique_type_groups = \
        ModelMultipleChoiceField(
            queryset=
                EquipmentUniqueTypeGroup.objects
                .select_related(
                    'equipment_general_type'),
            widget=
                autocomplete.ModelSelect2Multiple(
                    url=EquipmentUniqueTypeGroupAutoComplete.name))

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
                    attrs={'data-minimum-input-length': 1}))

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
