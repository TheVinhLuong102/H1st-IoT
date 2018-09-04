from dal import autocomplete

from .models import MonitoredEquipmentDataFieldConfig, EquipmentProblemPeriod, Alert


class MonitoredEquipmentDataFieldConfigForm(autocomplete.FutureModelForm):
    class Meta:
        model = MonitoredEquipmentDataFieldConfig

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


class EquipmentProblemPeriodForm(autocomplete.FutureModelForm):
    class Meta:
        model = EquipmentProblemPeriod

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

            equipment_problem_periods=
                autocomplete.ModelSelect2Multiple(
                    url='EquipmentProblemPeriod-AutoComplete',
                    attrs={# Only trigger autocompletion after characters have been typed
                           'data-minimum-input-length': 1}))
