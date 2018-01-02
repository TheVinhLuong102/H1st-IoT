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

        _cat_data_type_objs = DataType.objects.filter(name=_CAT_DATA_TYPE_NAME)

        if _cat_data_type_objs:
            assert len(_cat_data_type_objs) == 1
            self.cat_data_type_obj = _cat_data_type_objs[0]

        else:
            self.cat_data_type_obj = DataType(name=_CAT_DATA_TYPE_NAME)
            self.cat_data_type_obj.save()

        _num_data_type_objs = DataType.objects.filter(name=_NUM_DATA_TYPE_NAME)

        if _num_data_type_objs:
            assert len(_num_data_type_objs) == 1
            self.num_data_type_obj = _num_data_type_objs[0]

        else:
            self.num_data_type_obj = DataType(name=_NUM_DATA_TYPE_NAME)
            self.num_data_type_obj.save()

        _control_equipment_data_field_type_objs = EquipmentDataFieldType.objects.filter(name=_CONTROL_EQUIPMENT_DATA_FIELD_TYPE_NAME)

        if _control_equipment_data_field_type_objs:
            assert len(_control_equipment_data_field_type_objs) == 1
            self.control_equipment_data_field_type_obj = _control_equipment_data_field_type_objs[0]

        else:
            self.control_equipment_data_field_type_obj = EquipmentDataFieldType(name=_CONTROL_EQUIPMENT_DATA_FIELD_TYPE_NAME)
            self.control_equipment_data_field_type_obj.save()

        _measure_equipment_data_field_type_objs = EquipmentDataFieldType.objects.filter(name=_MEASURE_EQUIPMENT_DATA_FIELD_TYPE_NAME)

        if _measure_equipment_data_field_type_objs:
            assert len(_measure_equipment_data_field_type_objs) == 1
            self.measure_equipment_data_field_type_obj = _measure_equipment_data_field_type_objs[0]

        else:
            self.measure_equipment_data_field_type_obj = EquipmentDataFieldType(name=_MEASURE_EQUIPMENT_DATA_FIELD_TYPE_NAME)
            self.measure_equipment_data_field_type_obj.save()

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
        return self.models.base.EquipmentGeneralType.get_or_create(
            name=equipment_general_type_name.lower(),
            defaults=None)[0]

    def get_or_create_equipment_unique_type(self, equipment_general_type_name, equipment_unique_type_name):
        return self.models.base.EquipmentUniqueType.get_or_create(
            equipment_general_type=
                self.get_or_create_equipment_general_type(
                    equipment_general_type_name=equipment_general_type_name),
            name=equipment_unique_type_name.lower())[0]

