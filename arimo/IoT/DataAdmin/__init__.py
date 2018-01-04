from __future__ import print_function

from argparse import Namespace
import six

from django.conf import settings
from django.core.management import call_command
from django.core.wsgi import get_wsgi_application

import arimo.IoT.DataAdmin._project.settings
from arimo.IoT.DataAdmin.util import clean_lower_str


_STR_CLASSES = \
    (str, unicode) \
    if six.PY2 \
    else str


_CAT_DATA_TYPE_NAME = 'cat'
_NUM_DATA_TYPE_NAME = 'num'

_CONTROL_EQUIPMENT_DATA_FIELD_TYPE_NAME = 'control'
_MEASURE_EQUIPMENT_DATA_FIELD_TYPE_NAME = 'measure'


class Project(object):
    def __init__(self, db_args):
        arimo.IoT.DataAdmin._project.settings.DATABASES['default'].update({k.upper(): v for k, v in db_args.items()})
        settings.configure(**arimo.IoT.DataAdmin._project.settings.__dict__)
        get_wsgi_application()

        self._migrate()

        from arimo.IoT.DataAdmin.base.models import \
            DataType, EquipmentDataFieldType, EquipmentDataField, \
            EquipmentGeneralType, EquipmentUniqueType, EquipmentInstance

        self.cat_data_type_obj = \
            DataType.objects.get_or_create(
                name=_CAT_DATA_TYPE_NAME,
                defaults=None)[0]

        self.num_data_type_obj = \
            DataType.objects.get_or_create(
                name=_NUM_DATA_TYPE_NAME,
                defaults=None)[0]

        self.control_equipment_data_field_type_obj = \
            EquipmentDataFieldType.objects.get_or_create(
                name=_CONTROL_EQUIPMENT_DATA_FIELD_TYPE_NAME,
                defaults=None)[0]

        self.measure_equipment_data_field_type_obj = \
            EquipmentDataFieldType.objects.get_or_create(
                name=_MEASURE_EQUIPMENT_DATA_FIELD_TYPE_NAME,
                defaults=None)[0]

        # from arimo.IoT.DataAdmin.PredMaint.models import

        self.models = \
            Namespace(
                base=Namespace(
                    DataType=DataType,
                    EquipmentDataFieldType=EquipmentDataFieldType,
                    EquipmentDataField=EquipmentDataField,
                    EquipmentGeneralType=EquipmentGeneralType,
                    EquipmentUniqueType=EquipmentUniqueType,
                    EquipmentInstance=EquipmentInstance),

                PredMaint=Namespace(

                ))

    def _collect_static(self):
        call_command('collectstatic')

    def _create_super_user(self):
        call_command('createsuperuser')

    def _make_migrations(self):
        call_command('makemigrations')

    def _migrate(self):
        call_command('migrate')

    def get_or_create_equipment_general_type(self, equipment_general_type_name):
        return self.models.base.EquipmentGeneralType.objects.get_or_create(
            name=clean_lower_str(equipment_general_type_name),
            defaults=None)[0]

    def get_or_create_equipment_unique_type(self, equipment_general_type_name, equipment_unique_type_name):
        return self.models.base.EquipmentUniqueType.objects.get_or_create(
            equipment_general_type=
                self.get_or_create_equipment_general_type(
                    equipment_general_type_name=equipment_general_type_name),
            name=clean_lower_str(equipment_unique_type_name),
            defaults=None)[0]

    def update_or_create_equipment_data_field(
            self, equipment_general_type_name, equipment_data_field_name, control=False, cat=False,
            equipment_unique_type_names_incl=set(), equipment_unique_type_names_excl=set(),
            **kwargs):
        kwargs['data_type'] = \
            self.cat_data_type_obj \
            if cat \
            else self.num_data_type_obj

        try:
            equipment_data_field = \
                self.models.base.EquipmentDataField.objects.update_or_create(
                    equipment_general_type=
                        self.get_or_create_equipment_general_type(
                            equipment_general_type_name=equipment_general_type_name),
                    equipment_data_field_type=
                        self.control_equipment_data_field_type_obj
                        if control
                        else self.measure_equipment_data_field_type_obj,
                    name=clean_lower_str(equipment_data_field_name),
                    defaults=kwargs)[0]

        except Exception as err:
            print(equipment_general_type_name, equipment_data_field_name)
            raise err

        if equipment_unique_type_names_excl or equipment_unique_type_names_incl:
            equipment_unique_type_names_excl = \
                {clean_lower_str(equipment_unique_type_names_excl)} \
                if isinstance(equipment_unique_type_names_excl, _STR_CLASSES) \
                else {clean_lower_str(equipment_unique_type_name)
                      for equipment_unique_type_name in equipment_unique_type_names_excl}

            equipment_unique_types = []
            equipment_unique_type_names = []

            for equipment_unique_type in \
                    equipment_data_field.equipment_unique_types.filter(
                        equipment_general_type__name=clean_lower_str(equipment_general_type_name)):
                equipment_unique_type_name = equipment_unique_type.name
                if equipment_unique_type_name not in equipment_unique_type_names_excl:
                    equipment_unique_types.append(equipment_unique_type)
                    equipment_unique_type_names.append(equipment_unique_type_name)

            for equipment_unique_type_name in \
                    ({clean_lower_str(equipment_unique_type_names_incl)}
                     if isinstance(equipment_unique_type_names_incl, _STR_CLASSES)
                     else {clean_lower_str(equipment_unique_type_name)
                           for equipment_unique_type_name in equipment_unique_type_names_incl}) \
                    .difference(equipment_unique_type_names_excl, equipment_unique_type_names):
                equipment_unique_types.append(
                    self.get_or_create_equipment_unique_type(
                        equipment_general_type_name=equipment_general_type_name,
                        equipment_unique_type_name=equipment_unique_type_name))

            equipment_data_field.equipment_unique_types = equipment_unique_types

            equipment_data_field.save()

        return equipment_data_field

    def update_or_create_equipment_instance(
            self, equipment_general_type_name, name, equipment_unique_type_name=None,
            control_data_field_names_incl=set(), control_data_field_names_excl=set(),
            measure_data_field_names_incl=set(), measure_data_field_names_excl=set(),
            **kwargs):
        if equipment_unique_type_name:
            kwargs['equipment_unique_type'] = \
                self.get_or_create_equipment_unique_type(
                    equipment_general_type_name=equipment_general_type_name,
                    equipment_unique_type_name=equipment_unique_type_name)

        equipment_instance = \
            self.models.base.EquipmentInstance.objects.update_or_create(
                equipment_general_type=
                    self.get_or_create_equipment_general_type(
                        equipment_general_type_name=equipment_general_type_name),
                name=clean_lower_str(name),
                defaults=kwargs)[0]

        if equipment_unique_type_name or \
                control_data_field_names_incl or control_data_field_names_excl or \
                measure_data_field_names_incl or measure_data_field_names_excl:
            _clean_lower_equipment_general_type_name = \
                clean_lower_str(equipment_general_type_name)

            _clean_lower_equipment_unique_type_name = \
                clean_lower_str(equipment_unique_type_name) \
                if equipment_unique_type_name \
                else None

            control_data_field_names_excl = \
                {clean_lower_str(control_data_field_names_excl)} \
                if isinstance(control_data_field_names_excl, _STR_CLASSES) \
                else {clean_lower_str(control_equipment_data_field_name)
                      for control_equipment_data_field_name in control_data_field_names_excl}

            measure_data_field_names_excl = \
                {clean_lower_str(measure_data_field_names_excl)} \
                if isinstance(measure_data_field_names_excl, _STR_CLASSES) \
                else {clean_lower_str(measure_equipment_data_field_name)
                      for measure_equipment_data_field_name in measure_data_field_names_excl}

            equipment_data_fields = []
            control_equipment_data_field_names = []
            measure_equipment_data_field_names = []

            for equipment_data_field in \
                    equipment_instance.data_fields.filter(
                        equipment_general_type__name=_clean_lower_equipment_general_type_name):
                equipment_data_field_name = equipment_data_field.name

                if equipment_data_field.equipment_data_field_type.name == _CONTROL_EQUIPMENT_DATA_FIELD_TYPE_NAME:
                    if equipment_data_field_name not in control_data_field_names_excl:
                        if equipment_unique_type_name:
                            insert_equipment_type = True
                            equipment_unique_types = []

                            for equipment_unique_type in \
                                    equipment_data_field.equipment_unique_types.filter(
                                        equipment_general_type__name=_clean_lower_equipment_general_type_name):
                                if equipment_unique_type.name == _clean_lower_equipment_unique_type_name:
                                    insert_equipment_type = False
                                    break

                                else:
                                    equipment_unique_types.append(equipment_unique_type)

                            if insert_equipment_type:
                                equipment_unique_types.append(
                                    self.get_or_create_equipment_unique_type(
                                        equipment_general_type_name=equipment_general_type_name,
                                        equipment_unique_type_name=equipment_unique_type_name))

                                equipment_data_field.equipment_unique_types = equipment_unique_types

                                equipment_data_field.save()

                        equipment_data_fields.append(equipment_data_field)

                        control_equipment_data_field_names.append(equipment_data_field_name)

                elif equipment_data_field.equipment_data_field_type.name == _MEASURE_EQUIPMENT_DATA_FIELD_TYPE_NAME:
                    if equipment_data_field_name not in measure_data_field_names_excl:
                        if equipment_unique_type_name:
                            insert_equipment_type = True
                            equipment_unique_types = []

                            for equipment_unique_type in \
                                    equipment_data_field.equipment_unique_types.filter(
                                        equipment_general_type__name=_clean_lower_equipment_general_type_name):
                                if equipment_unique_type.name == _clean_lower_equipment_unique_type_name:
                                    insert_equipment_type = False
                                    break

                                else:
                                    equipment_unique_types.append(equipment_unique_type)

                            if insert_equipment_type:
                                equipment_unique_types.append(
                                    self.get_or_create_equipment_unique_type(
                                        equipment_general_type_name=equipment_general_type_name,
                                        equipment_unique_type_name=equipment_unique_type_name))

                                equipment_data_field.equipment_unique_types = equipment_unique_types

                                equipment_data_field.save()

                        equipment_data_fields.append(equipment_data_field)
                        
                        measure_equipment_data_field_names.append(equipment_data_field_name)

            for control_equipment_data_field_name in \
                    ({clean_lower_str(control_data_field_names_incl)}
                     if isinstance(control_data_field_names_incl, _STR_CLASSES)
                     else {clean_lower_str(control_equipment_data_field_name)
                           for control_equipment_data_field_name in control_data_field_names_incl}) \
                    .difference(control_data_field_names_excl, control_equipment_data_field_names):
                equipment_data_fields.append(
                    self.update_or_create_equipment_data_field(
                        equipment_general_type_name=equipment_general_type_name,
                        equipment_data_field_name=control_equipment_data_field_name,
                        control=True,
                        equipment_unique_type_names_incl=
                            {equipment_unique_type_name}
                            if equipment_unique_type_name
                            else set()))

            for measure_equipment_data_field_name in \
                    ({clean_lower_str(measure_data_field_names_incl)}
                     if isinstance(measure_data_field_names_incl, _STR_CLASSES)
                     else {clean_lower_str(measure_equipment_data_field_name)
                           for measure_equipment_data_field_name in measure_data_field_names_incl}) \
                    .difference(measure_data_field_names_excl, measure_equipment_data_field_names):
                equipment_data_fields.append(
                    self.update_or_create_equipment_data_field(
                        equipment_general_type_name=equipment_general_type_name,
                        equipment_data_field_name=measure_equipment_data_field_name,
                        control=False,
                        equipment_unique_type_names_incl=
                            {equipment_unique_type_name}
                            if equipment_unique_type_name
                            else set()))

            equipment_instance.data_fields = equipment_data_fields

            equipment_instance.save()

        return equipment_instance
