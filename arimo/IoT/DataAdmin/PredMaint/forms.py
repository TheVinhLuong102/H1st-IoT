from dal import autocomplete

from .models import \
    EquipmentUniqueTypeGroupServiceConfig, EquipmentUniqueTypeGroupMonitoredDataFieldConfig, \
    EquipmentProblemPeriod as EquipmentProblemDiagnosis, Alert


class EquipmentUniqueTypeGroupServiceConfigForm(autocomplete.FutureModelForm):
    class Meta:
        model = EquipmentUniqueTypeGroupServiceConfig

        fields = '__all__'

        widgets = dict(
            global_excluded_equipment_data_fields=
                autocomplete.ModelSelect2Multiple(
                    url='EquipmentDataField-AutoComplete',
                    attrs={# Only trigger autocompletion after characters have been typed
                           'data-minimum-input-length': 1}))


class EquipmentUniqueTypeGroupMonitoredDataFieldConfigForm(autocomplete.FutureModelForm):
    class Meta:
        model = EquipmentUniqueTypeGroupMonitoredDataFieldConfig

        fields = '__all__'

        widgets = dict(
            monitored_equipment_data_field=
                autocomplete.ModelSelect2(
                    url='EquipmentDataField-AutoComplete',
                    attrs={# Only trigger autocompletion after characters have been typed
                           'data-minimum-input-length': 1}),

            excluded_equipment_data_fields=
                autocomplete.ModelSelect2Multiple(
                    url='EquipmentDataField-AutoComplete',
                    attrs={# Only trigger autocompletion after characters have been typed
                           'data-minimum-input-length': 1}))


class EquipmentProblemDiagnosisForm(autocomplete.FutureModelForm):
    class Meta:
        model = EquipmentProblemDiagnosis

        fields = '__all__'

        widgets = dict(
            equipment_instance=
                autocomplete.ModelSelect2(
                    url='EquipmentInstance-AutoComplete',
                    attrs={# Only trigger autocompletion after characters have been typed
                           'data-minimum-input-length': 1}),

            equipment_problem_types=
                autocomplete.ModelSelect2Multiple(
                    url='EquipmentProblemType-AutoComplete',
                    attrs={# Only trigger autocompletion after characters have been typed
                           'data-minimum-input-length': 1}))


class AlertForm(autocomplete.FutureModelForm):
    class Meta:
        model = Alert

        fields = '__all__'

        widgets = dict(
            equipment_instance=
                autocomplete.ModelSelect2(
                    url='EquipmentInstance-AutoComplete',
                    attrs={# Only trigger autocompletion after characters have been typed
                           'data-minimum-input-length': 1}),

            equipment_diagnoses=
                 autocomplete.ModelSelect2Multiple(
                     url='EquipmentProblemDiagnosis-AutoComplete',
                     attrs={# Only trigger autocompletion after characters have been typed
                           'data-minimum-input-length': 1}))
