from argparse import Namespace

from django.conf import settings
from django.core.management import call_command
from django.core.wsgi import get_wsgi_application

import arimo.IoT.DataAdmin._project.settings


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
            EquipmentGeneralType, EquipmentUniqueType

        self.cat_data_type_obj = \
            DataType.objects.get_or_create(
                name=_CAT_DATA_TYPE_NAME,
                defaults=None)

        self.num_data_type_obj = \
            DataType.objects.get_or_create(
                name=_NUM_DATA_TYPE_NAME,
                defaults=None)

        self.control_equipment_data_field_type_obj = \
            EquipmentDataFieldType.objects.get_or_create(
                name=_CONTROL_EQUIPMENT_DATA_FIELD_TYPE_NAME,
                defaults=None)

        self.measure_equipment_data_field_type_obj = \
            EquipmentDataFieldType.objects.get_or_create(
                name=_MEASURE_EQUIPMENT_DATA_FIELD_TYPE_NAME,
                defaults=None)

        # from arimo.IoT.DataAdmin.PredMaint.models import

        self.models = \
            Namespace(
                base=Namespace(
                    DataType=DataType,
                    EquipmentDataFieldType=EquipmentDataFieldType,
                    EquipmentDataField=EquipmentDataField,
                    EquipmentGeneralType=EquipmentGeneralType,
                    EquipmentUniqueType=EquipmentUniqueType,
                    EquipmentInstance=None),

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
            name=equipment_general_type_name.lower(),
            defaults=None)[0]

    def get_or_create_equipment_unique_type(self, equipment_general_type_name, equipment_unique_type_name):
        return self.models.base.EquipmentUniqueType.objects.get_or_create(
            equipment_general_type=
                self.get_or_create_equipment_general_type(
                    equipment_general_type_name=equipment_general_type_name),
            name=equipment_unique_type_name.lower(),
            defaults=None)[0]

    def update_or_create_equipment_data_field(
            self, equipment_general_type_name, equipment_data_field_name, control=False, cat=False,
            equipment_unique_type_names_incl=set(), equipment_unique_type_names_excl=set(),
            **kwargs):
        kwargs['equipment_data_field_type'] = \
            self.control_equipment_data_field_type_obj \
            if control \
            else self.measure_equipment_data_field_type_obj

        kwargs['data_type'] = \
            self.cat_data_type_obj \
            if cat \
            else self.num_data_type_obj

        equipment_data_field, created = \
            self.models.base.EquipmentDataField.objects.update_or_create(
                equipment_general_type=
                    self.get_or_create_equipment_general_type(
                        equipment_general_type_name=equipment_general_type_name),
                name=equipment_data_field_name.lower(),
                defaults=kwargs)[0]

        return equipment_data_field.equipment_unique_types
