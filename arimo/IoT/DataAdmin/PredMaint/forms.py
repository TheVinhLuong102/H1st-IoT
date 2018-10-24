from django.forms import ModelChoiceField, ModelMultipleChoiceField

from dal.autocomplete import FutureModelForm, ModelSelect2, ModelSelect2Multiple

from .autocompletes import \
    EquipmentProblemTypeAutoComplete, \
    EquipmentProblemDiagnosisAutoComplete
from .models import \
    EquipmentUniqueTypeGroupServiceConfig, EquipmentUniqueTypeGroupMonitoredDataFieldConfig, \
    EquipmentProblemDiagnosis, Alert

from ..base.autocompletes import \
    EquipmentDataFieldAutoComplete, \
    EquipmentInstanceAutoComplete
from ..base.models import \
    EquipmentDataField, \
    EquipmentInstance


class EquipmentUniqueTypeGroupServiceConfigForm(FutureModelForm):
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
                ModelSelect2Multiple(
                    url=EquipmentDataFieldAutoComplete.name,
                    attrs={# Only trigger autocompletion after characters have been typed
                           'data-minimum-input-length': 1}))

    class Meta:
        model = EquipmentUniqueTypeGroupServiceConfig

        fields = '__all__'


class EquipmentUniqueTypeGroupMonitoredDataFieldConfigForm(FutureModelForm):
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
                ModelSelect2(
                    url=EquipmentDataFieldAutoComplete.name,
                    attrs={# Only trigger autocompletion after characters have been typed
                           'data-minimum-input-length': 1}))

    excluded_equipment_data_fields = \
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
        model = EquipmentUniqueTypeGroupMonitoredDataFieldConfig

        fields = '__all__'


class EquipmentProblemDiagnosisForm(FutureModelForm):
    equipment_instance = \
        ModelChoiceField(
            queryset=
                EquipmentInstance.objects
                .select_related(
                    'equipment_general_type',
                    'equipment_unique_type', 'equipment_unique_type__equipment_general_type',
                    'equipment_facility'),

            widget=
                ModelSelect2(
                    url=EquipmentInstanceAutoComplete.name,
                    attrs={# Only trigger autocompletion after characters have been typed
                           'data-minimum-input-length': 1}))

    alerts = \
        ModelMultipleChoiceField(
            queryset=
                Alert.objects
                .select_related(
                    'equipment_unique_type_group', 'equipment_unique_type_group__equipment_general_type',
                    'equipment_instance', 'equipment_instance__equipment_general_type',
                    'equipment_instance__equipment_unique_type', 'equipment_instance__equipment_unique_type__equipment_general_type',
                    'diagnosis_status'))

    class Meta:
        model = EquipmentProblemDiagnosis

        fields = '__all__'

        widgets = dict(
            equipment_problem_types=
                ModelSelect2Multiple(
                    url=EquipmentProblemTypeAutoComplete.name,
                    attrs={# Only trigger autocompletion after characters have been typed
                           'data-minimum-input-length': 1}))


class AlertForm(FutureModelForm):
    equipment_instance = \
        ModelChoiceField(
            queryset=
                EquipmentInstance.objects
                .select_related(
                    'equipment_general_type',
                    'equipment_unique_type', 'equipment_unique_type__equipment_general_type',
                    'equipment_facility'),

            widget=
                ModelSelect2(
                    url=EquipmentInstanceAutoComplete.name,
                    attrs={# Only trigger autocompletion after characters have been typed
                           'data-minimum-input-length': 1}))

    equipment_problem_diagnoses = \
        ModelMultipleChoiceField(
            queryset=
                EquipmentProblemDiagnosis.objects
                .select_related(
                    'equipment_instance', 'equipment_instance__equipment_general_type',
                    'equipment_instance__equipment_unique_type', 'equipment_instance__equipment_unique_type__equipment_general_type')
                .prefetch_related(
                    'equipment_problem_types'),

            widget=
                ModelSelect2Multiple(
                    url=EquipmentProblemDiagnosisAutoComplete.name,
                    attrs={# Only trigger autocompletion after characters have been typed
                           'data-minimum-input-length': 1}))

    class Meta:
        model = Alert

        fields = '__all__'
