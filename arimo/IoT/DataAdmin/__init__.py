from django.conf import settings
from django.core.management import call_command
from django.core.wsgi import get_wsgi_application

import arimo.IoT.DataAdmin._project.settings
from arimo.util import Namespace


class Project(object):
    def __init__(self, db_args):
        arimo.IoT.DataAdmin._project.settings.DATABASES['default'].update(db_args)
        settings.configure(**arimo.IoT.DataAdmin._project.settings.__dict__)
        get_wsgi_application()

        self._migrate()

        from arimo.IoT.DataAdmin.base.models import \
            DataType, EquipmentDataFieldType, EquipmentDataField, \
            EquipmentGeneralType, EquipmentUniqueType

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
