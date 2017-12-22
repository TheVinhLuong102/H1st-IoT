from django.conf import settings
from django.core.wsgi import get_wsgi_application

import arimo.IoT.DataAdmin._project.settings
from arimo.util import Namespace


class Project(object):
    def __init__(self, **db_args):
        d = arimo.IoT.DataAdmin._project.settings.__dict__.copy()
        d['DATABASES']['default'].update(db_args)

        settings.configure(**d)
        self.wsgi_application = get_wsgi_application()

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
