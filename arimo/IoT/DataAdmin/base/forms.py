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

from .query_sets import \
    EQUIPMENT_GENERAL_TYPE_UNORDERED_QUERY_SET, \
    EQUIPMENT_COMPONENT_STR_QUERY_SET, \
    EQUIPMENT_DATA_FIELD_STR_QUERY_SET, \
    EQUIPMENT_UNIQUE_TYPE_GROUP_STR_QUERY_SET, \
    EQUIPMENT_UNIQUE_TYPE_STR_QUERY_SET, \
    EQUIPMENT_UNIQUE_TYPE_STR_UNORDERED_QUERY_SET, \
    EQUIPMENT_FACILITY_NAME_ONLY_UNORDERED_QUERY_SET, \
    EQUIPMENT_INSTANCE_STR_QUERY_SET


EQUIPMENT_COMPONENTS_MODEL_MULTIPLE_CHOICE_FIELD = \
    ModelMultipleChoiceField(
        queryset=EQUIPMENT_COMPONENT_STR_QUERY_SET,
        widget=autocomplete.ModelSelect2Multiple(
                url=EquipmentComponentAutoComplete.name),
        required=False)


EQUIPMENT_DATA_FIELDS_MODEL_MULTIPLE_CHOICE_FIELD = \
    ModelMultipleChoiceField(
        queryset=EQUIPMENT_DATA_FIELD_STR_QUERY_SET,
        widget=autocomplete.ModelSelect2Multiple(
                url=EquipmentDataFieldAutoComplete.name,
                attrs={'data-minimum-input-length': 1}),
        required=False)


EQUIPMENT_UNIQUE_TYPE_GROUPS_MODEL_MULTIPLE_CHOICE_FIELD = \
    ModelMultipleChoiceField(
        queryset=EQUIPMENT_UNIQUE_TYPE_GROUP_STR_QUERY_SET,
        widget=autocomplete.ModelSelect2Multiple(
                url=EquipmentUniqueTypeGroupAutoComplete.name,
                attrs={'data-minimum-input-length': 1}),
        required=False)


EQUIPMENT_UNIQUE_TYPES_MODEL_MULTIPLE_CHOICE_FIELD = \
    ModelMultipleChoiceField(
        queryset=EQUIPMENT_UNIQUE_TYPE_STR_QUERY_SET,
        widget=autocomplete.ModelSelect2Multiple(
                url=EquipmentUniqueTypeAutoComplete.name,
                attrs={'data-minimum-input-length': 1}),
        required=False)


class EquipmentComponentForm(autocomplete.FutureModelForm):
    directly_interacts_with_components = EQUIPMENT_COMPONENTS_MODEL_MULTIPLE_CHOICE_FIELD
    sub_components = EQUIPMENT_COMPONENTS_MODEL_MULTIPLE_CHOICE_FIELD
    equipment_data_fields = EQUIPMENT_DATA_FIELDS_MODEL_MULTIPLE_CHOICE_FIELD
    equipment_unique_types = EQUIPMENT_UNIQUE_TYPES_MODEL_MULTIPLE_CHOICE_FIELD

    class Meta:
        model = EquipmentComponent
        fields = '__all__'


class EquipmentDataFieldForm(autocomplete.FutureModelForm):
    equipment_components = EQUIPMENT_COMPONENTS_MODEL_MULTIPLE_CHOICE_FIELD
    equipment_unique_types = EQUIPMENT_UNIQUE_TYPES_MODEL_MULTIPLE_CHOICE_FIELD

    class Meta:
        model = EquipmentDataField
        fields = '__all__'


class EquipmentUniqueTypeGroupForm(autocomplete.FutureModelForm):
    equipment_unique_types = EQUIPMENT_UNIQUE_TYPES_MODEL_MULTIPLE_CHOICE_FIELD

    class Meta:
        model = EquipmentUniqueTypeGroup
        fields = '__all__'


class EquipmentUniqueTypeForm(autocomplete.FutureModelForm):
    equipment_components = EQUIPMENT_COMPONENTS_MODEL_MULTIPLE_CHOICE_FIELD
    equipment_data_fields = EQUIPMENT_DATA_FIELDS_MODEL_MULTIPLE_CHOICE_FIELD
    equipment_unique_type_groups = EQUIPMENT_UNIQUE_TYPE_GROUPS_MODEL_MULTIPLE_CHOICE_FIELD

    class Meta:
        model = EquipmentUniqueType
        fields = '__all__'


class EquipmentInstanceForm(autocomplete.FutureModelForm):
    equipment_general_type = \
        ModelChoiceField(
            queryset=EQUIPMENT_GENERAL_TYPE_UNORDERED_QUERY_SET,
            widget=autocomplete.ModelSelect2(
                    url=EquipmentGeneralTypeAutoComplete.name))

    equipment_unique_type = \
        ModelChoiceField(
            queryset=EQUIPMENT_UNIQUE_TYPE_STR_UNORDERED_QUERY_SET,
            widget=autocomplete.ModelSelect2(
                    url=EquipmentUniqueTypeAutoComplete.name,
                    attrs={'data-minimum-input-length': 1}),
            required=False)

    equipment_facility = \
        ModelChoiceField(
            queryset=EQUIPMENT_FACILITY_NAME_ONLY_UNORDERED_QUERY_SET,
            widget=autocomplete.ModelSelect2(
                    url=EquipmentFacilityAutoComplete.name,
                    attrs={'data-minimum-input-length': 1}))

    equipment_unique_type_groups = EQUIPMENT_UNIQUE_TYPE_GROUPS_MODEL_MULTIPLE_CHOICE_FIELD

    class Meta:
        model = EquipmentInstance
        fields = '__all__'


class EquipmentSystemForm(autocomplete.FutureModelForm):
    equipment_facility = \
        ModelChoiceField(
            queryset=EQUIPMENT_FACILITY_NAME_ONLY_UNORDERED_QUERY_SET,
            widget=autocomplete.ModelSelect2(
                    url=EquipmentFacilityAutoComplete.name,
                    attrs={'data-minimum-input-length': 1}))

    equipment_instances = \
        ModelMultipleChoiceField(
            queryset=EQUIPMENT_INSTANCE_STR_QUERY_SET,
            widget=autocomplete.ModelSelect2Multiple(
                    url=EquipmentInstanceAutoComplete.name,
                    attrs={'data-minimum-input-length': 1}),
            required=True)

    class Meta:
        model = EquipmentSystem
        fields = '__all__'
