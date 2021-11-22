from django.forms import ModelChoiceField, ModelMultipleChoiceField

from dal import autocomplete   # *** DON'T IMPORT SPECIFIC ITEMS INSIDE autocomplete AS THEY CHANGE BETWEEN VERSIONS ***

from .autocompletes import \
    EquipmentProblemTypeAutoComplete, \
    EquipmentInstanceProblemDiagnosisAutoComplete

from .models import \
    EquipmentUniqueTypeGroupServiceConfig, EquipmentUniqueTypeGroupMonitoredDataFieldConfig, \
    EquipmentInstanceProblemDiagnosis, EquipmentInstanceAlertPeriod

from ..base.autocompletes import \
    EquipmentDataFieldAutoComplete, \
    EquipmentUniqueTypeGroupAutoComplete, \
    EquipmentInstanceAutoComplete

from ..base.models import \
    EquipmentInstance

from ..base.query_sets import \
    EQUIPMENT_DATA_FIELD_STR_QUERY_SET, \
    EQUIPMENT_DATA_FIELD_STR_UNORDERED_QUERY_SET, \
    EQUIPMENT_UNIQUE_TYPE_GROUP_STR_UNORDERED_QUERY_SET


class EquipmentUniqueTypeGroupServiceConfigForm(autocomplete.FutureModelForm):
    equipment_unique_type_group = \
        ModelChoiceField(
            queryset=EQUIPMENT_UNIQUE_TYPE_GROUP_STR_UNORDERED_QUERY_SET,
            widget=autocomplete.ModelSelect2(
                    url=EquipmentUniqueTypeGroupAutoComplete.name),
            required=True)

    global_excluded_equipment_data_fields = \
        ModelMultipleChoiceField(
            queryset=EQUIPMENT_DATA_FIELD_STR_QUERY_SET,
            widget=autocomplete.ModelSelect2Multiple(
                    url=EquipmentDataFieldAutoComplete.name,
                    attrs={'data-minimum-input-length': 1}),
            required=False)

    class Meta:
        model = EquipmentUniqueTypeGroupServiceConfig
        fields = '__all__'


class EquipmentUniqueTypeGroupMonitoredDataFieldConfigForm(autocomplete.FutureModelForm):
    monitored_equipment_data_field = \
        ModelChoiceField(
            queryset=EQUIPMENT_DATA_FIELD_STR_UNORDERED_QUERY_SET,
            widget=autocomplete.ModelSelect2(
                    url=EquipmentDataFieldAutoComplete.name,
                    attrs={'data-minimum-input-length': 1}),
            required=True)

    manually_included_equipment_data_fields = \
        ModelMultipleChoiceField(
            queryset=EQUIPMENT_DATA_FIELD_STR_QUERY_SET,
            widget=autocomplete.ModelSelect2Multiple(
                    url=EquipmentDataFieldAutoComplete.name,
                    attrs={'data-minimum-input-length': 1}),
            required=False)

    manually_excluded_equipment_data_fields = \
        ModelMultipleChoiceField(
            queryset=EQUIPMENT_DATA_FIELD_STR_QUERY_SET,
            widget=autocomplete.ModelSelect2Multiple(
                    url=EquipmentDataFieldAutoComplete.name,
                    attrs={'data-minimum-input-length': 1}),
            required=False)

    class Meta:
        model = EquipmentUniqueTypeGroupMonitoredDataFieldConfig
        fields = '__all__'


class EquipmentInstanceProblemDiagnosisForm(autocomplete.FutureModelForm):
    equipment_instance = \
        ModelChoiceField(
            queryset=
                EquipmentInstance.objects
                .defer(
                    'equipment_facility',
                    'info')
                .select_related(
                    'equipment_general_type',
                    'equipment_unique_type')
                .order_by(),
            widget=autocomplete.ModelSelect2(
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


class EquipmentInstanceAlertPeriodForm(autocomplete.FutureModelForm):
    equipment_instance_problem_diagnoses = \
        ModelMultipleChoiceField(
            queryset=
                EquipmentInstanceProblemDiagnosis.objects
                .defer(
                    'date_range',
                    'duration',
                    'has_equipment_problems',
                    'comments',
                    'has_associated_equipment_instance_alarm_periods',
                    'has_associated_equipment_instance_alert_periods')
                .select_related(
                    'equipment_instance',
                    'equipment_instance__equipment_general_type', 'equipment_instance__equipment_unique_type')
                .defer(
                    'equipment_instance__equipment_facility', 'equipment_instance__info')
                .prefetch_related(
                    'equipment_problem_types'),
            widget=
                autocomplete.ModelSelect2Multiple(
                    url=EquipmentInstanceProblemDiagnosisAutoComplete.name,
                    attrs={'data-minimum-input-length': 1}),
            required=False)

    class Meta:
        model = EquipmentInstanceAlertPeriod
        fields = '__all__'
