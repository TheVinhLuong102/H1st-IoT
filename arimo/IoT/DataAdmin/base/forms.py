from django.forms import ModelChoiceField, ModelMultipleChoiceField

from dal.autocomplete import FutureModelForm, ModelSelect2, ModelSelect2Multiple

from .autocompletes import \
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


class EquipmentDataFieldForm(FutureModelForm):
    equipment_unique_types = \
        ModelMultipleChoiceField(
            queryset=
                EquipmentUniqueType.objects
                .select_related(
                    'equipment_general_type'),

            widget=
                ModelSelect2Multiple(
                    url=EquipmentUniqueTypeAutoComplete.name,
                    attrs={# Only trigger autocompletion after characters have been typed
                           'data-minimum-input-length': 1}))

    class Meta:
        model = EquipmentDataField

        fields = '__all__'


class EquipmentUniqueTypeGroupForm(FutureModelForm):
    equipment_unique_types = \
        ModelMultipleChoiceField(
            queryset=
                EquipmentUniqueType.objects
                .select_related(
                    'equipment_general_type'),

            widget=
                ModelSelect2Multiple(
                    url=EquipmentUniqueTypeAutoComplete.name,
                    attrs={# Only trigger autocompletion after characters have been typed
                           'data-minimum-input-length': 1}))

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
                ModelSelect2Multiple(
                    url=EquipmentDataFieldAutoComplete.name,
                    attrs={# Only trigger autocompletion after characters have been typed
                           'data-minimum-input-length': 1}))

    class Meta:
        model = EquipmentUniqueTypeGroup

        fields = '__all__'


class EquipmentUniqueTypeForm(FutureModelForm):
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
                ModelSelect2Multiple(
                    url=EquipmentDataFieldAutoComplete.name,
                    attrs={# Only trigger autocompletion after characters have been typed
                           'data-minimum-input-length': 1}))

    groups = \
        ModelMultipleChoiceField(
            queryset=
                EquipmentUniqueTypeGroup.objects
                .select_related(
                    'equipment_general_type'),

            widget=
                ModelSelect2Multiple(
                    url=EquipmentUniqueTypeGroupAutoComplete.name,
                    attrs={# Only trigger autocompletion after characters have been typed
                           'data-minimum-input-length': 1}))

    class Meta:
        model = EquipmentUniqueType

        fields = '__all__'


class EquipmentInstanceForm(FutureModelForm):
    equipment_unique_type = \
        ModelChoiceField(
            queryset=
                EquipmentUniqueType.objects
                .select_related(
                    'equipment_general_type'),

            widget=
                ModelSelect2(
                    url=EquipmentUniqueTypeAutoComplete.name,
                    attrs={# Only trigger autocompletion after characters have been typed
                           'data-minimum-input-length': 1}))

    class Meta:
        model = EquipmentInstance

        fields = '__all__'

        widgets = dict(
            equipment_facility=
                ModelSelect2(
                    url=EquipmentFacilityAutoComplete.name,
                    attrs={# Only trigger autocompletion after characters have been typed
                           'data-minimum-input-length': 1}))


class EquipmentSystemForm(FutureModelForm):
    equipment_instances = \
        ModelMultipleChoiceField(
            queryset=
                EquipmentInstance.objects
                .select_related(
                    'equipment_general_type',
                    'equipment_unique_type', 'equipment_unique_type__equipment_general_type',
                    'equipment_facility'),

            widget=
                ModelSelect2Multiple(
                    url=EquipmentInstanceAutoComplete.name,
                    attrs={# Only trigger autocompletion after characters have been typed
                           'data-minimum-input-length': 1}))

    class Meta:
        model = EquipmentSystem

        fields = '__all__'

        widgets = dict(
            equipment_facility=
                ModelSelect2(
                    url=EquipmentFacilityAutoComplete.name,
                    attrs={# Only trigger autocompletion after characters have been typed
                           'data-minimum-input-length': 1}))
