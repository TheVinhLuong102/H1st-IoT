from django.forms import ModelChoiceField, ModelMultipleChoiceField

from dal import autocomplete   # *** DON'T IMPORT SPECIFIC ITEMS INSIDE autocomplete AS THEY CHANGE BETWEEN VERSIONS ***

from .autocompletes import \
    EquipmentProblemTypeAutoComplete, \
    EquipmentInstanceProblemDiagnosisAutoComplete
from .models import \
    EquipmentUniqueTypeGroupServiceConfig, EquipmentUniqueTypeGroupMonitoredDataFieldConfig, \
    EquipmentInstanceProblemDiagnosis, Alert

from ..base.autocompletes import \
    EquipmentDataFieldAutoComplete, \
    EquipmentInstanceAutoComplete
from ..base.models import \
    EquipmentDataField, \
    EquipmentInstance


class EquipmentUniqueTypeGroupServiceConfigForm(autocomplete.FutureModelForm):
    global_excluded_equipment_data_fields = \
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
        model = EquipmentUniqueTypeGroupServiceConfig

        fields = '__all__'


class EquipmentUniqueTypeGroupMonitoredDataFieldConfigForm(autocomplete.FutureModelForm):
    monitored_equipment_data_field = \
        ModelChoiceField(
            queryset=
                EquipmentDataField.objects
                .select_related(
                    'equipment_general_type',
                    'equipment_data_field_type',
                    'data_type',
                    'numeric_measurement_unit'),
            widget=
                autocomplete.ModelSelect2(
                    url=EquipmentDataFieldAutoComplete.name,
                    attrs={# Only trigger autocompletion after characters have been typed
                           'data-minimum-input-length': 1}),
            required=True)

    manually_included_equipment_data_fields = \
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

    manually_excluded_equipment_data_fields = \
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
        model = EquipmentUniqueTypeGroupMonitoredDataFieldConfig

        fields = '__all__'


class EquipmentInstanceProblemDiagnosisForm(autocomplete.FutureModelForm):
    equipment_instance = \
        ModelChoiceField(
            queryset=
                EquipmentInstance.objects
                .select_related(
                    'equipment_general_type',
                    'equipment_unique_type', 'equipment_unique_type__equipment_general_type',
                    'equipment_facility'),
            widget=
                autocomplete.ModelSelect2(
                    url=EquipmentInstanceAutoComplete.name,
                    attrs={'data-minimum-input-length': 1}),
            required=True)

    class Meta:
        model = EquipmentInstanceProblemDiagnosis

        fields = '__all__'

        widgets = dict(
            equipment_problem_types=
                autocomplete.ModelSelect2Multiple(
                    url=EquipmentProblemTypeAutoComplete.name))


class AlertForm(autocomplete.FutureModelForm):
    equipment_problem_diagnoses = \
        ModelMultipleChoiceField(
            queryset=
                EquipmentInstanceProblemDiagnosis.objects
                .select_related(
                    'equipment_instance', 'equipment_instance__equipment_general_type',
                    'equipment_instance__equipment_unique_type', 'equipment_instance__equipment_unique_type__equipment_general_type')
                .prefetch_related(
                    'equipment_problem_types'),
            widget=
                autocomplete.ModelSelect2Multiple(
                    url=EquipmentInstanceProblemDiagnosisAutoComplete.name,
                    attrs={# Only trigger autocompletion after characters have been typed
                           'data-minimum-input-length': 1}),
            required=False)

    class Meta:
        model = Alert

        fields = '__all__'
