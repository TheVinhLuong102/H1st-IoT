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
    EquipmentFacility, \
    EquipmentInstance, \
    EquipmentSystem


EQUIPMENT_COMPONENTS_MODEL_MULTIPLE_CHOICE_FIELD = \
    ModelMultipleChoiceField(
        queryset=
            EquipmentComponent.objects
            .defer('description', 'last_updated')
            .select_related(
                'equipment_general_type'),
        widget=
            autocomplete.ModelSelect2Multiple(
                url=EquipmentComponentAutoComplete.name),
        required=False)


EQUIPMENT_DATA_FIELDS_MODEL_MULTIPLE_CHOICE_FIELD = \
    ModelMultipleChoiceField(
        queryset=
            EquipmentDataField.objects
            .defer('description', 'last_updated')
            .select_related(
                'equipment_general_type',
                'equipment_data_field_type',
                'data_type',
                'numeric_measurement_unit')
            .defer(
                'numeric_measurement_unit__description'),
        widget=
            autocomplete.ModelSelect2Multiple(
                url=EquipmentDataFieldAutoComplete.name,
                attrs={'data-minimum-input-length': 1}),
        required=False)


EQUIPMENT_UNIQUE_TYPES_MODEL_MULTIPLE_CHOICE_FIELD = \
    ModelMultipleChoiceField(
        queryset=
            EquipmentUniqueType.objects
            .defer('description', 'last_updated')
            .select_related(
                'equipment_general_type'),
        widget=
            autocomplete.ModelSelect2Multiple(
                url=EquipmentUniqueTypeAutoComplete.name,
                attrs={'data-minimum-input-length': 1}),
        required=False)


class EquipmentComponentForm(autocomplete.FutureModelForm):
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

    equipment_unique_type_groups = \
        ModelMultipleChoiceField(
            queryset=
                EquipmentUniqueTypeGroup.objects
                .defer('description', 'last_updated')
                .select_related(
                    'equipment_general_type'),
            widget=
                autocomplete.ModelSelect2Multiple(
                    url=EquipmentUniqueTypeGroupAutoComplete.name),
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
                    'equipment_general_type')
                .order_by(),
            widget=
                autocomplete.ModelSelect2(
                    url=EquipmentUniqueTypeAutoComplete.name,
                    attrs={'data-minimum-input-length': 1}),
            required=False)

    equipment_facility = \
        ModelChoiceField(
            queryset=EquipmentFacility.objects.only('name').order_by(),
            widget=
                autocomplete.ModelSelect2(
                    url=EquipmentFacilityAutoComplete.name,
                    attrs={'data-minimum-input-length': 1}))

    class Meta:
        model = EquipmentInstance

        fields = '__all__'

        widgets = dict(
            equipment_general_type=
                autocomplete.ModelSelect2(
                    url=EquipmentGeneralTypeAutoComplete.name))


class EquipmentSystemForm(autocomplete.FutureModelForm):
    equipment_instances = \
        ModelMultipleChoiceField(
            queryset=
                EquipmentInstance.objects
                .select_related(
                    'equipment_general_type',
                    'equipment_unique_type',
                    'equipment_facility'),
            widget=
                autocomplete.ModelSelect2Multiple(
                    url=EquipmentInstanceAutoComplete.name,
                    attrs={'data-minimum-input-length': 1}),
            required=True)

    class Meta:
        model = EquipmentSystem

        fields = '__all__'

        widgets = dict(
            equipment_facility=
                autocomplete.ModelSelect2(
                    url=EquipmentFacilityAutoComplete.name,
                    attrs={'data-minimum-input-length': 1}))
