import os
from ruamel import yaml
import six
import warnings

from django.conf import settings
from django.core.management import call_command
from django.core.wsgi import get_wsgi_application

import arimo.IoT.DataAdmin._django_root.settings
from arimo.IoT.DataAdmin.util import _JSON_EXT, _PARQUET_EXT, _YAML_EXT


_STR_CLASSES = \
    (str, unicode) \
    if six.PY2 \
    else str


class Project(object):
    CONFIG_DIR_PATH = os.path.expanduser('~/.arimo/IoT')

    _CAT_DATA_TYPE_NAME = 'cat'
    _NUM_DATA_TYPE_NAME = 'num'

    _CONTROL_EQUIPMENT_DATA_FIELD_TYPE_NAME = 'control'
    _MEASURE_EQUIPMENT_DATA_FIELD_TYPE_NAME = 'measure'
    _CALC_EQUIPMENT_DATA_FIELD_TYPE_NAME = 'calc'
    _ALARM_EQUIPMENT_DATA_FIELD_TYPE_NAME = 'alarm'

    _AWS_PROFILE_NAME = 'arimo'

    _EQUIPMENT_INSTANCE_ID_COL_NAME = 'equipment_instance_id'
    _DATE_TIME_COL_NAME = 'date_time'

    _DEFAULT_PARAMS = \
        dict(
            s3=dict(
                BUCKET_NAME_GLOBAL_CONFIG_KEY='S3_BUCKET',
                ACCESS_KEY_ID_GLOBAL_CONFIG_KEY='AWS_ACCESS_KEY_ID',
                SECRET_ACCESS_KEY_GLOBAL_CONFIG_KEY='AWS_SECRET_ACCESS_KEY',

                equipment_data=dict(
                    dir_prefix='.arimo/IoT/EquipmentData',
                    raw_dir_prefix='.arimo/IoT/EquipmentData/raw',
                    daily_agg_dir_prefix='.arimo/IoT/EquipmentData/DailyAgg')))

    def __init__(self, params, **kwargs):
        from arimo.util import Namespace
        from arimo.util.aws import key_pair, s3

        self.params = Namespace(**self._DEFAULT_PARAMS)
        self.params.update(params, **kwargs)

        assert self.params.db.host \
           and self.params.db.db_name \
           and self.params.db.user \
           and self.params.db.password

        django_db_settings = arimo.IoT.DataAdmin._django_root.settings.DATABASES['default']
        django_db_settings['HOST'] = self.params.db.host
        django_db_settings['NAME'] = self.params.db.db_name
        django_db_settings['USER'] = self.params.db.user
        django_db_settings['PASSWORD'] = self.params.db.password
        settings.configure(**arimo.IoT.DataAdmin._django_root.settings.__dict__)
        get_wsgi_application()
        call_command('migrate')

        from arimo.IoT.DataAdmin.base.models import \
            GlobalConfig, \
            DataType, EquipmentDataFieldType, NumericMeasurementUnit, \
            EquipmentGeneralType, \
            EquipmentComponent, EquipmentDataField, \
            EquipmentUniqueTypeGroup, EquipmentUniqueType, \
            EquipmentInstance, EquipmentInstanceDailyMetadata, EquipmentInstanceDataFieldDailyAgg, \
            EquipmentFacility, EquipmentSystem, \
            Error

        self.data = \
            Namespace(
                GlobalConfigs=GlobalConfig.objects,

                NumericMeasurementUnits=NumericMeasurementUnit.objects,

                EquipmentGeneralTypes=EquipmentGeneralType.objects,

                EquipmentComponents=EquipmentComponent.objects,
                EquipmentDataFields=EquipmentDataField.objects,

                EquipmentUniqueTypeGroups=EquipmentUniqueTypeGroup.objects,
                EquipmentUniqueTypes=EquipmentUniqueType.objects,

                EquipmentInstances=EquipmentInstance.objects,
                EquipmentInstanceDailyMetadata=EquipmentInstanceDailyMetadata.objects,
                EquipmentInstanceDataFieldDailyAggs=EquipmentInstanceDataFieldDailyAgg.objects,

                EquipmentFacilities=EquipmentFacility.objects,
                EquipmentSystems=EquipmentSystem.objects,

                Errors=Error.objects)

        self.CAT_DATA_TYPE = \
            DataType.objects.get_or_create(
                name=self._CAT_DATA_TYPE_NAME,
                defaults=None)[0]

        self.NUM_DATA_TYPE = \
            DataType.objects.get_or_create(
                name=self._NUM_DATA_TYPE_NAME,
                defaults=None)[0]

        self.CONTROL_EQUIPMENT_DATA_FIELD_TYPE = \
            EquipmentDataFieldType.objects.get_or_create(
                name=self._CONTROL_EQUIPMENT_DATA_FIELD_TYPE_NAME,
                defaults=None)[0]

        self.MEASURE_EQUIPMENT_DATA_FIELD_TYPE = \
            EquipmentDataFieldType.objects.get_or_create(
                name=self._MEASURE_EQUIPMENT_DATA_FIELD_TYPE_NAME,
                defaults=None)[0]

        self.CALC_EQUIPMENT_DATA_FIELD_TYPE = \
            EquipmentDataFieldType.objects.get_or_create(
                name=self._CALC_EQUIPMENT_DATA_FIELD_TYPE_NAME,
                defaults=None)[0]

        self.ALARM_EQUIPMENT_DATA_FIELD_TYPE = \
            EquipmentDataFieldType.objects.get_or_create(
                name=self._ALARM_EQUIPMENT_DATA_FIELD_TYPE_NAME,
                defaults=None)[0]

        self.params.s3.bucket = \
            self.data.GlobalConfigs.get_or_create(
                key=self.params.s3.BUCKET_NAME_GLOBAL_CONFIG_KEY)[0].value

        if self.params.s3.bucket:
            assert isinstance(self.params.s3.bucket, _STR_CLASSES), \
                '*** S3 BUCKET = {} ***'.format(self.params.s3.bucket)

            if 'access_key_id' in self.params.s3:
                assert 'secret_access_key' in self.params.s3

            else:
                self.params.s3.access_key_id = \
                    self.data.GlobalConfigs.get_or_create(
                        key=self.params.s3.ACCESS_KEY_ID_GLOBAL_CONFIG_KEY)[0].value

                self.params.s3.secret_access_key = \
                    self.data.GlobalConfigs.get_or_create(
                        key=self.params.s3.SECRET_ACCESS_KEY_GLOBAL_CONFIG_KEY)[0].value

            if self.params.s3.access_key_id is None:
                warnings.warn(
                    '*** AWS ACCESS KEY ID = {} ***'.format(self.params.s3.access_key_id))
            else:
                assert isinstance(self.params.s3.access_key_id, _STR_CLASSES), \
                    '*** AWS ACCESS KEY ID = {} ***'.format(self.params.s3.access_key_id)

            if self.params.s3.secret_access_key is None:
                warnings.warn(
                    '*** AWS SECRET ACCESS KEY = {} ***'.format(self.params.s3.secret_access_key))
            else:
                assert isinstance(self.params.s3.secret_access_key, _STR_CLASSES), \
                    '*** AWS SECRET ACCESS KEY = {} ***'.format(self.params.s3.secret_access_key)

            self.s3_client = \
                s3.client(
                    access_key_id=self.params.s3.access_key_id,
                    secret_access_key=self.params.s3.secret_access_key)

            self.params.s3.equipment_data.dir_path = \
                's3://{}/{}'.format(
                    self.params.s3.bucket,
                    self.params.s3.equipment_data.dir_prefix)

            self.params.s3.equipment_data.raw_dir_path = \
                's3://{}/{}'.format(
                    self.params.s3.bucket,
                    self.params.s3.equipment_data.raw_dir_prefix)

            self.params.s3.equipment_data.daily_agg_dir_path = \
                os.path.join(
                    's3://{}'.format(self.params.s3.bucket),
                    self.params.s3.equipment_data.daily_agg_dir_prefix)

    @classmethod
    def __qual_name__(cls):
        return '{}.{}'.format(cls.__module__, cls.__name__)

    def get_or_create_equipment_general_type(self, equipment_general_type_name):
        return self.data.EquipmentGeneralTypes.get_or_create(name=equipment_general_type_name)[0]

    def equipment_general_type(self, equipment_general_type_name):
        return self.data.EquipmentGeneralTypes.get(name=equipment_general_type_name)

    def equipment_unique_type_group(self, equipment_general_type_name, equipment_unique_type_group_name):
        return self.data.EquipmentUniqueTypeGroups.get(
                equipment_general_type__name=equipment_general_type_name,
                name=equipment_unique_type_group_name)

    def equipment_unique_type(self, equipment_general_type_name, equipment_unique_type_name):
        return self.data.EquipmentUniqueTypes.get(
                equipment_general_type__name=equipment_general_type_name,
                name=equipment_unique_type_name)

    def equipment_data_field(self, equipment_general_type_name, equipment_data_field_name, control=False):
        kwargs = \
            dict(equipment_data_field_type=self.CONTROL_EQUIPMENT_DATA_FIELD_TYPE) \
            if control \
            else dict(equipment_data_field_type__in=
                        [self.MEASURE_EQUIPMENT_DATA_FIELD_TYPE,
                         self.CALC_EQUIPMENT_DATA_FIELD_TYPE,
                         self.ALARM_EQUIPMENT_DATA_FIELD_TYPE])

        return self.data.EquipmentDataFields.get(
                equipment_general_type__name=equipment_general_type_name,
                name=equipment_data_field_name,
                **kwargs)

    def equipment_instance(self, equipment_general_type_name, equipment_instance_name):
        return self.data.EquipmentInstances.get(
                equipment_general_type__name=equipment_general_type_name,
                name=equipment_instance_name)

    def load_equipment_data(
            self, equipment_instance_id_or_data_set_name,
            _from_files=True, _spark=False,
            set_i_col=True, set_t_col=True,
            verbose=True, **kwargs):
        from arimo.data.parquet import S3ParquetDataFeeder
        from arimo.data.distributed import DDF
        from arimo.data.distributed_parquet import S3ParquetDistributedDataFrame
        from arimo.util.date_time import DATE_COL

        path = os.path.join(
            self.params.s3.equipment_data.dir_path,
            equipment_instance_id_or_data_set_name + _PARQUET_EXT)

        df = (S3ParquetDistributedDataFrame(
                path=path, mergeSchema=True,
                aws_access_key_id=self.params.s3.access_key_id,
                aws_secret_access_key=self.params.s3.secret_access_key,
                iCol=self._EQUIPMENT_INSTANCE_ID_COL_NAME
                    if set_i_col
                    else None,
                tCol=self._DATE_TIME_COL_NAME
                    if set_t_col
                    else None,
                verbose=verbose, **kwargs)
               if _spark
               else S3ParquetDataFeeder(
                path=path,
                aws_access_key_id=self.params.s3.access_key_id,
                aws_secret_access_key=self.params.s3.secret_access_key,
                iCol=self._EQUIPMENT_INSTANCE_ID_COL_NAME
                    if set_i_col
                    else None,
                tCol=self._DATE_TIME_COL_NAME
                    if set_t_col
                    else None,
                verbose=verbose, **kwargs)) \
            if _from_files \
            else DDF.load(
                path=path,
                format='parquet', mergeSchema=True,
                aws_access_key_id=self.params.s3.access_key_id,
                aws_secret_access_key=self.params.s3.secret_access_key,
                iCol=self._EQUIPMENT_INSTANCE_ID_COL_NAME
                    if set_i_col
                    else None,
                tCol=self._DATE_TIME_COL_NAME
                    if set_t_col
                    else None,
                verbose=verbose, **kwargs)

        assert {self._EQUIPMENT_INSTANCE_ID_COL_NAME, DATE_COL, self._DATE_TIME_COL_NAME}.issubset(df.columns)

        return df


def project(name='TEST'):
    return Project(
            params=yaml.safe_load(
                    open(os.path.join(
                            Project.CONFIG_DIR_PATH,
                            name + _YAML_EXT))))
