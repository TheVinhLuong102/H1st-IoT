"""H1st IoT Data Management (Base) Autocompletes."""


# *** DON'T IMPORT SPECIFIC ITEMS INSIDE autocomplete
# AS THEY CHANGE BETWEEN VERSIONS ***
from dal import autocomplete

from h1st_iot.data_mgmt.base.models import (
    NumericMeasurementUnit,
    EquipmentGeneralType,
    EquipmentComponent,
    EquipmentDataField,
    EquipmentUniqueTypeGroup,
    EquipmentUniqueType,
    EquipmentFacility,
    EquipmentInstance,
)


class NumericMeasurementUnitAutoComplete(autocomplete.Select2QuerySetView):
    """NumericMeasurementUnitAutoComplete."""

    name = 'NumericMeasurementUnit-AutoComplete'

    def get_queryset(self):
        """Queryset."""
        if self.request.user.is_authenticated:
            query_set = NumericMeasurementUnit.objects.all()

            return (query_set.filter(name__icontains=self.q)
                    if self.q
                    else query_set)

        return NumericMeasurementUnit.objects.none()


class EquipmentGeneralTypeAutoComplete(autocomplete.Select2QuerySetView):
    """EquipmentGeneralTypeAutoComplete."""

    name = 'EquipmentGeneralType-AutoComplete'

    def get_queryset(self):
        """Queryset."""
        if self.request.user.is_authenticated:
            query_set = EquipmentGeneralType.objects.all()

            return (query_set.filter(name__icontains=self.q)
                    if self.q
                    else query_set)

        return EquipmentGeneralType.objects.none()


class EquipmentComponentAutoComplete(autocomplete.Select2QuerySetView):
    """EquipmentComponentAutoComplete."""

    name = 'EquipmentComponent-AutoComplete'

    def get_queryset(self):
        """Queryset."""
        if self.request.user.is_authenticated:
            query_set = EquipmentComponent.objects.all()

            return (query_set.filter(name__icontains=self.q)
                    if self.q
                    else query_set)

        return EquipmentComponent.objects.none()


class EquipmentDataFieldAutoComplete(autocomplete.Select2QuerySetView):
    """EquipmentDataFieldAutoComplete."""

    name = 'EquipmentDataField-AutoComplete'

    def get_queryset(self):
        """Queryset."""
        if self.request.user.is_authenticated:
            query_set = EquipmentDataField.objects.all()

            return (query_set.filter(name__icontains=self.q)
                    if self.q
                    else query_set)

        return EquipmentDataField.objects.none()


class EquipmentUniqueTypeGroupAutoComplete(autocomplete.Select2QuerySetView):
    """EquipmentUniqueTypeGroupAutoComplete."""

    name = 'EquipmentUniqueTypeGroup-AutoComplete'

    def get_queryset(self):
        """Queryset."""
        if self.request.user.is_authenticated:
            query_set = EquipmentUniqueTypeGroup.objects.all()

            return (query_set.filter(name__icontains=self.q)
                    if self.q
                    else query_set)

        return EquipmentUniqueTypeGroup.objects.none()


class EquipmentUniqueTypeAutoComplete(autocomplete.Select2QuerySetView):
    """EquipmentUniqueTypeAutoComplete."""

    name = 'EquipmentUniqueType-AutoComplete'

    def get_queryset(self):
        """Queryset."""
        if self.request.user.is_authenticated:
            query_set = EquipmentUniqueType.objects.all()

            return (query_set.filter(name__icontains=self.q)
                    if self.q
                    else query_set)

        return EquipmentUniqueType.objects.none()


class EquipmentFacilityAutoComplete(autocomplete.Select2QuerySetView):
    """EquipmentFacilityAutoComplete."""

    name = 'EquipmentFacility-AutoComplete'

    def get_queryset(self):
        """Queryset."""
        if self.request.user.is_authenticated:
            query_set = EquipmentFacility.objects.all()

            return (query_set.filter(name__icontains=self.q)
                    if self.q
                    else query_set)

        return EquipmentFacility.objects.none()


class EquipmentInstanceAutoComplete(autocomplete.Select2QuerySetView):
    """EquipmentInstanceAutoComplete."""

    name = 'EquipmentInstance-AutoComplete'

    def get_queryset(self):
        """Queryset."""
        if self.request.user.is_authenticated:
            query_set = EquipmentInstance.objects.all()

            return (query_set.filter(name__icontains=self.q)
                    if self.q
                    else query_set)

        return EquipmentInstance.objects.none()
