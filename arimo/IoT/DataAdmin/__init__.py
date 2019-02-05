from collections import Counter
import datetime
import os
import pandas
from ruamel import yaml
import six

from django.conf import settings
from django.core.management import call_command
from django.core.wsgi import get_wsgi_application
from django.db.models import Count

import arimo.IoT.DataAdmin._project.settings
from arimo.IoT.DataAdmin.util import clean_lower_str, _JSON_EXT, _PARQUET_EXT, _YAML_EXT


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

        django_db_settings = arimo.IoT.DataAdmin._project.settings.DATABASES['default']
        django_db_settings['HOST'] = self.params.db.host
        django_db_settings['NAME'] = self.params.db.db_name
        django_db_settings['USER'] = self.params.db.user
        django_db_settings['PASSWORD'] = self.params.db.password
        settings.configure(**arimo.IoT.DataAdmin._project.settings.__dict__)
        get_wsgi_application()
        call_command('migrate')

        from arimo.IoT.DataAdmin.base.models import \
            GlobalConfig, \
            DataType, EquipmentDataFieldType, NumericMeasurementUnit, \
            EquipmentGeneralType, EquipmentUniqueTypeGroup, EquipmentUniqueType, EquipmentDataField, \
            EquipmentInstance, EquipmentInstanceDataFieldDailyAgg, \
            EquipmentFacility, EquipmentSystem

        self.data = \
            Namespace(
                GlobalConfigs=GlobalConfig.objects,

                NumericMeasurementUnits=NumericMeasurementUnit.objects,

                EquipmentGeneralTypes=EquipmentGeneralType.objects,
                EquipmentUniqueTypeGroups=EquipmentUniqueTypeGroup.objects,
                EquipmentUniqueTypes=EquipmentUniqueType.objects,
                EquipmentDataFields=EquipmentDataField.objects,

                EquipmentInstances=EquipmentInstance.objects,
                EquipmentInstanceDataFieldDailyAggs=EquipmentInstanceDataFieldDailyAgg.objects,

                EquipmentFacilities=EquipmentFacility.objects,
                EquipmentSystems=EquipmentSystem.objects)

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
                '*** {} ***'.format(self.params.s3.bucket)

            if 'access_key_id' in self.params.s3:
                assert self.params.s3.access_key_id and self.params.s3.secret_access_key

            else:
                self.params.s3.access_key_id, self.params.s3.secret_access_key = \
                    key_pair(profile=self._AWS_PROFILE_NAME)

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
        return self.data.EquipmentGeneralTypes.get_or_create(
                name=clean_lower_str(equipment_general_type_name),
                defaults=None)[0]

    def equipment_general_type(self, equipment_general_type_name):
        return self.data.EquipmentGeneralTypes.get(
                name=clean_lower_str(equipment_general_type_name))

    def update_or_create_equipment_unique_type_group(
            self, equipment_general_type_name, equipment_unique_type_group_name,
            equipment_unique_type_names_incl=set(), equipment_unique_type_names_excl=set()):
        equipment_unique_type_group = \
            self.data.EquipmentUniqueTypeGroups.get_or_create(
                equipment_general_type=
                    self.equipment_general_type(
                        equipment_general_type_name=equipment_general_type_name),
                name=clean_lower_str(equipment_unique_type_group_name),
                defaults=None)[0]

        if equipment_unique_type_names_excl or equipment_unique_type_names_incl:
            equipment_unique_type_names_excl = \
                {clean_lower_str(equipment_unique_type_names_excl)} \
                if isinstance(equipment_unique_type_names_excl, _STR_CLASSES) \
                else {clean_lower_str(equipment_unique_type_name)
                      for equipment_unique_type_name in equipment_unique_type_names_excl}

            equipment_unique_types = []
            equipment_unique_type_names = []

            for equipment_unique_type in \
                    equipment_unique_type_group.equipment_unique_types.filter(
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
                    self.update_or_create_equipment_unique_type(
                        equipment_general_type_name=equipment_general_type_name,
                        equipment_unique_type_name=equipment_unique_type_name))

            equipment_unique_type_group.equipment_unique_types = equipment_unique_types

            equipment_unique_type_group.save()

        return equipment_unique_type_group

    def equipment_unique_type_group(self, equipment_general_type_name, equipment_unique_type_group_name):
        return self.data.EquipmentUniqueTypeGroups.get(
                equipment_general_type__name=clean_lower_str(equipment_general_type_name),
                name=clean_lower_str(equipment_unique_type_group_name))

    def update_or_create_equipment_unique_type(
            self, equipment_general_type_name, equipment_unique_type_name,
            equipment_unique_type_group_names_incl=set(), equipment_unique_type_group_names_excl=set()):
        equipment_unique_type = \
            self.data.EquipmentUniqueTypes.get_or_create(
                equipment_general_type=
                    self.get_or_create_equipment_general_type(
                        equipment_general_type_name=equipment_general_type_name),
                name=clean_lower_str(equipment_unique_type_name),
                defaults=None)[0]

        if equipment_unique_type_group_names_excl or equipment_unique_type_group_names_incl:
            equipment_unique_type_group_names_excl = \
                {clean_lower_str(equipment_unique_type_group_names_excl)} \
                if isinstance(equipment_unique_type_group_names_excl, _STR_CLASSES) \
                else {clean_lower_str(equipment_unique_type_group_name)
                      for equipment_unique_type_group_name in equipment_unique_type_group_names_excl}

            equipment_unique_type_groups = []
            equipment_unique_type_group_names = []

            for equipment_unique_type_group in \
                    equipment_unique_type.groups.filter(
                        equipment_general_type__name=clean_lower_str(equipment_general_type_name)):
                equipment_unique_type_group_name = equipment_unique_type_group.name
                if equipment_unique_type_group_name not in equipment_unique_type_group_names_excl:
                    equipment_unique_type_groups.append(equipment_unique_type_group)
                    equipment_unique_type_group_names.append(equipment_unique_type_group_name)

            for equipment_unique_type_group_name in \
                    ({clean_lower_str(equipment_unique_type_group_names_incl)}
                     if isinstance(equipment_unique_type_group_names_incl, _STR_CLASSES)
                     else {clean_lower_str(equipment_unique_type_group_name)
                           for equipment_unique_type_group_name in equipment_unique_type_group_names_incl}) \
                    .difference(equipment_unique_type_group_names_excl, equipment_unique_type_group_names):
                equipment_unique_type_groups.append(
                    self.update_or_create_equipment_unique_type_group(
                        equipment_general_type_name=equipment_general_type_name,
                        equipment_unique_type_group_name=equipment_unique_type_group_name))

            equipment_unique_type.groups = equipment_unique_type_groups

            equipment_unique_type.save()

        return equipment_unique_type

    def equipment_unique_type(self, equipment_general_type_name, equipment_unique_type_name):
        return self.data.EquipmentUniqueTypes.get(
                equipment_general_type__name=clean_lower_str(equipment_general_type_name),
                name=clean_lower_str(equipment_unique_type_name))

    def update_or_create_equipment_data_field(
            self, equipment_general_type_name, equipment_data_field_name, equipment_data_field_type='measure', cat=None,
            equipment_unique_type_names_incl=set(), equipment_unique_type_names_excl=set(),
            **kwargs):
        equipment_data_field_types = \
            dict(control=self.CONTROL_EQUIPMENT_DATA_FIELD_TYPE,
                 measure=self.MEASURE_EQUIPMENT_DATA_FIELD_TYPE,
                 calc=self.CALC_EQUIPMENT_DATA_FIELD_TYPE,
                 alarm=self.ALARM_EQUIPMENT_DATA_FIELD_TYPE)

        if cat is not None:
            kwargs['data_type'] = \
                self.CAT_DATA_TYPE \
                if cat \
                else self.NUM_DATA_TYPE

        equipment_data_field = \
            self.data.EquipmentDataFields.update_or_create(
                equipment_general_type=
                    self.equipment_general_type(
                        equipment_general_type_name=equipment_general_type_name),
                equipment_data_field_type=
                    equipment_data_field_types[equipment_data_field_type],
                name=clean_lower_str(equipment_data_field_name),
                defaults=kwargs)[0]

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
                    self.equipment_unique_type(
                        equipment_general_type_name=equipment_general_type_name,
                        equipment_unique_type_name=equipment_unique_type_name))

            equipment_data_field.equipment_unique_types = equipment_unique_types

            equipment_data_field.save()

        return equipment_data_field

    def equipment_data_field(self, equipment_general_type_name, equipment_data_field_name, control=False):
        kwargs = \
            dict(equipment_data_field_type=self.CONTROL_EQUIPMENT_DATA_FIELD_TYPE) \
            if control \
            else dict(equipment_data_field_type__in=
                        [self.MEASURE_EQUIPMENT_DATA_FIELD_TYPE,
                         self.CALC_EQUIPMENT_DATA_FIELD_TYPE,
                         self.ALARM_EQUIPMENT_DATA_FIELD_TYPE])

        return self.data.EquipmentDataFields.get(
                equipment_general_type__name=clean_lower_str(equipment_general_type_name),
                name=clean_lower_str(equipment_data_field_name),
                **kwargs)

    def update_or_create_equipment_instance(
            self, equipment_general_type_name, name, equipment_unique_type_name=None,
            **kwargs):
        if equipment_unique_type_name:
            kwargs['equipment_unique_type'] = \
                self.update_or_create_equipment_unique_type(
                    equipment_general_type_name=equipment_general_type_name,
                    equipment_unique_type_name=equipment_unique_type_name)

        try:
            equipment_instance = \
                self.data.EquipmentInstances.update_or_create(
                    equipment_general_type=
                        self.equipment_general_type(
                            equipment_general_type_name=equipment_general_type_name),
                    name=clean_lower_str(name),
                    defaults=kwargs)[0]
            
        except Exception as err:
            print('*** {} #{} ***'.format(equipment_general_type_name, name))
            raise err

        return equipment_instance

    def equipment_instance(self, equipment_general_type_name, equipment_instance_name):
        return self.data.EquipmentInstances.get(
                equipment_general_type__name=clean_lower_str(equipment_general_type_name),
                name=clean_lower_str(equipment_instance_name))

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

        adf = (S3ParquetDistributedDataFrame(
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

        assert {self._EQUIPMENT_INSTANCE_ID_COL_NAME, DATE_COL, self._DATE_TIME_COL_NAME}.issubset(adf.columns)

        return adf

    # *** BELOW METHODS ARE EXPERIMENTAL >>>

    def check_equipment_data_integrity(self, equipment_instance_id_or_data_set_name):
        from arimo.data.distributed_parquet import S3ParquetDistributedDataFrame
        from arimo.util.date_time import DATE_COL
        from arimo.util.types.spark_sql import _DATE_TYPE

        file_adf = \
            S3ParquetDistributedDataFrame(
                path=os.path.join(
                    self.params.s3.equipment_data.dir_path,
                    equipment_instance_id_or_data_set_name + _PARQUET_EXT),
                aws_access_key_id=self.params.s3.access_key_id,
                aws_secret_access_key=self.params.s3.secret_access_key,
                iCol=None, tCol=None,
                verbose=True)

        assert file_adf.type(DATE_COL) == _DATE_TYPE, \
            '*** Date Col not of Date Type (likely because of NULL Date-Times) ***'

        equipment_instance_ids = \
            file_adf('SELECT DISTINCT {} FROM this'
                .format(self._EQUIPMENT_INSTANCE_ID_COL_NAME)) \
            .toPandas().iloc[:, 0]

        non_compliant_equipment_instance_ids = \
            {equipment_instance_id
             for equipment_instance_id in equipment_instance_ids
             if clean_lower_str(equipment_instance_id) != equipment_instance_id}

        if non_compliant_equipment_instance_ids:
            print('*** NON-COMPLIANT EQUIPMENT INSTANCE IDs: {} ***'.format(non_compliant_equipment_instance_ids))

        equipment_instance_ids_w_dups = \
            {equipment_instance_id
             for equipment_instance_id, count in
                Counter([clean_lower_str(equipment_instance_id)
                         for equipment_instance_id in equipment_instance_ids]).items()
             if count > 1}

        if equipment_instance_ids_w_dups:
            print('*** DUPLICATED EQUIPMENT INSTANCE IDs: {} ***'.format(equipment_instance_ids_w_dups))

    def equipment_unique_type_names(self, equipment_general_type_name):
        return sorted(
            equipment_unique_type.name
            for equipment_unique_type in
                self.data.EquipmentUniqueTypes.filter(
                    equipment_general_type__name=clean_lower_str(equipment_general_type_name)))

    def equipment_unique_type_names_and_equipment_data_field_names(self, equipment_general_type_name):
        return {equipment_unique_type.name:
                    {equipment_data_field.name
                     for equipment_data_field in equipment_unique_type.data_fields.all()}
                for equipment_unique_type in
                    self.data.EquipmentUniqueTypes.filter(
                        equipment_general_type__name=clean_lower_str(equipment_general_type_name))}

    def associated_equipment_instances(self, equipment_instance_name, from_date=None, to_date=None):
        kwargs = {}

        if from_date:
            kwargs['date__gte'] = datetime.datetime.strptime(from_date, "%Y-%m-%d").date()

        if to_date:
            kwargs['date__lte'] = datetime.datetime.strptime(to_date, "%Y-%m-%d").date()

        equipment_systems = \
            self.data.EquipmentSystems.filter(
                equipment_instances__name=clean_lower_str(equipment_instance_name))

        if equipment_systems:
            return equipment_systems[0].equipment_instances.all().union(
                    *(equipment_system.equipment_instances.all()
                      for equipment_system in equipment_systems[1:]),
                    all=False)

        else:
            return self.data.EquipmentInstances.filter(
                    name=clean_lower_str(equipment_instance_name))

    def test_equipment_data_date_vs_date_time(self, equipment_instance_id_or_data_set_name):
        from pyspark.sql.functions import to_date
        from arimo.util.date_time import DATE_COL

        equipment_data_adf = \
            self.load_equipment_data(
                equipment_instance_id_or_data_set_name=equipment_instance_id_or_data_set_name,
                _from_files=True, _spark=True,
                set_i_col=False, set_t_col=False,
                verbose=True) \
            [[self._EQUIPMENT_INSTANCE_ID_COL_NAME,
              DATE_COL,
              self._DATE_TIME_COL_NAME]]

        equipment_data_adf_w_diff_date_vs_date_time = \
            equipment_data_adf.filter(
                to_date(equipment_data_adf[self._DATE_TIME_COL_NAME])
                != equipment_data_adf[DATE_COL])

        equipment_data_adf_w_diff_date_vs_date_time.cache()

        if equipment_data_adf_w_diff_date_vs_date_time.nRows:
            path = 's3://{}/tmp/{}---DATE-vs-DATE-TIME{}'.format(
                        self.params.s3.bucket,
                        equipment_instance_id_or_data_set_name,
                        _JSON_EXT)

            equipment_data_adf_w_diff_date_vs_date_time.repartition(1).save(
                path=path,
                format='json',
                aws_access_key_id=self.params.s3.access_key_id,
                aws_secret_access_key=self.params.s3.secret_access_key)

            raise ValueError('*** ERRONEOUS ROWS SAVED TO "{}" ***'.format(path))

    def _equipment_general_types_n_equipment_data_fields(self, only0=True):
        df = pandas.DataFrame.from_records(
            data=self.data.EquipmentGeneralTypes
                .values('name')
                .annotate(n_equipment_data_fields=Count('equipment_data_field'))
                .order_by('name'),
            index=None,
            exclude=None,
            columns=['name', 'n_equipment_data_fields'],
            coerce_float=False,
            nrows=None)

        return df.loc[df.n_equipment_data_fields == 0] \
            if only0 \
          else df

    def _equipment_general_types_n_equipment_unique_type_groups(self, only0=True):
        df = pandas.DataFrame.from_records(
            data=self.data.EquipmentGeneralTypes
                .values('name')
                .annotate(n_equipment_unique_type_groups=Count('equipment_unique_type_group'))
                .order_by('name'),
            index=None,
            exclude=None,
            columns=['name', 'n_equipment_unique_type_groups'],
            coerce_float=False,
            nrows=None)

        return df.loc[df.n_equipment_unique_type_groups == 0] \
            if only0 \
          else df

    def _equipment_general_types_n_equipment_unique_types(self, only0=True):
        df = pandas.DataFrame.from_records(
            data=self.data.EquipmentGeneralTypes
                .values('name')
                .annotate(n_equipment_unique_types=Count('equipment_unique_type'))
                .order_by('name'),
            index=None,
            exclude=None,
            columns=['name', 'n_equipment_unique_types'],
            coerce_float=False,
            nrows=None)

        return df.loc[df.n_equipment_unique_types == 0] \
            if only0 \
          else df

    def _equipment_general_types_n_equipment_instances(self, only0=True):
        df = pandas.DataFrame.from_records(
            data=self.data.EquipmentGeneralTypes
                .values('name')
                .annotate(n_equipment_instances=Count('equipment_instance'))
                .order_by('name'),
            index=None,
            exclude=None,
            columns=['name', 'n_equipment_instances'],
            coerce_float=False,
            nrows=None)

        return df.loc[df.n_equipment_instances == 0] \
            if only0 \
          else df

    def _equipment_data_fields_n_equipment_unique_types(self, only0=True):
        df = pandas.DataFrame.from_records(
            data=self.data.EquipmentDataFields
                .values('equipment_general_type__name', 'equipment_data_field_type__name', 'name')
                .annotate(n_equipment_unique_types=Count('equipment_unique_types'))
                .order_by('equipment_general_type__name', 'equipment_data_field_type__name', 'name'),
            index=None,
            exclude=None,
            columns=['equipment_general_type__name', 'equipment_data_field_type__name', 'name', 'n_equipment_unique_types'],
            coerce_float=False,
            nrows=None)

        return df.loc[df.n_equipment_unique_types == 0] \
            if only0 \
          else df

    def _equipment_data_fields_n_equipment_instances(self, only0=True):
        df = pandas.DataFrame.from_records(
            data=self.data.EquipmentDataFields
                .values('equipment_general_type__name', 'equipment_data_field_type__name', 'name')
                .annotate(n_equipment_instances=Count('equipment_instance'))
                .order_by('equipment_general_type__name', 'equipment_data_field_type__name', 'name'),
            index=None,
            exclude=None,
            columns=['equipment_general_type__name', 'equipment_data_field_type__name', 'name', 'n_equipment_instances'],
            coerce_float=False,
            nrows=None)

        return df.loc[df.n_equipment_instances == 0] \
            if only0 \
          else df

    def _equipment_unique_type_groups_n_equipment_unique_types(self, only0=True):
        df = pandas.DataFrame.from_records(
            data=self.data.EquipmentUniqueTypeGroups
                .values('equipment_general_type__name', 'name')
                .annotate(n_equipment_unique_types=Count('equipment_unique_types'))
                .order_by('equipment_general_type__name', 'name'),
            index=None,
            exclude=None,
            columns=['equipment_general_type__name', 'name', 'n_equipment_unique_types'],
            coerce_float=False,
            nrows=None)

        return df.loc[df.n_equipment_unique_types == 0] \
            if only0 \
          else df

    def _equipment_unique_types_n_equipment_unique_type_groups(self, only0=True):
        df = pandas.DataFrame.from_records(
            data=self.data.EquipmentUniqueTypes
                .values('equipment_general_type__name', 'name')
                .annotate(n_equipment_unique_type_groups=Count('groups'))
                .order_by('equipment_general_type__name', 'name'),
            index=None,
            exclude=None,
            columns=['equipment_general_type__name', 'name', 'n_equipment_unique_type_groups'],
            coerce_float=False,
            nrows=None)

        return df.loc[df.n_equipment_unique_type_groups == 0] \
            if only0 \
          else df

    def _equipment_unique_types_n_equipment_data_fields(self, only0=True):
        df = pandas.DataFrame.from_records(
            data=self.data.EquipmentUniqueTypes
                .values('equipment_general_type__name', 'name')
                .annotate(n_equipment_data_fields=Count('data_fields'))
                .order_by('equipment_general_type__name', 'name'),
            index=None,
            exclude=None,
            columns=['equipment_general_type__name', 'name', 'n_equipment_data_fields'],
            coerce_float=False,
            nrows=None)

        return df.loc[df.n_equipment_data_fields == 0] \
            if only0 \
          else df

    def _equipment_data_field_names_n_counts(self, only_multi=True):
        d = {(i['equipment_general_type__name'], i['name']): i['n']
             for i in self.data.EquipmentDataFields
                 .values('equipment_general_type__name', 'name')
                 .annotate(n=Count('name'))
                 .order_by('equipment_general_type__name', 'name')}

        return {k: v
                for k, v in d.items()
                if v > 1} \
            if only_multi \
          else d

    def _equipment_facilities_n_equipment_instances(self, only0=True):
        df = pandas.DataFrame.from_records(
            data=self.data.EquipmentFacilities
                .values('name')
                .annotate(n_equipment_instances=Count('equipment_instance'))
                .order_by('name'),
            index=None,
            exclude=None,
            columns=['name', 'n_equipment_instances'],
            coerce_float=False,
            nrows=None)

        return df.loc[df.n_equipment_instances == 0] \
            if only0 \
          else df

    def _equipment_facilities_n_equipment_systems(self, only0=True):
        df = pandas.DataFrame.from_records(
            data=self.data.EquipmentFacilities
                .values('name')
                .annotate(n_equipment_systems=Count('equipment_system'))
                .order_by('name'),
            index=None,
            exclude=None,
            columns=['name', 'n_equipment_systems'],
            coerce_float=False,
            nrows=None)

        return df.loc[df.n_equipment_systems == 0] \
            if only0 \
            else df

    def _equipment_systems_n_equipment_instances(self, only0=True):
        df = pandas.DataFrame.from_records(
            data=self.data.EquipmentSystems
                .values('name')
                .annotate(n_equipment_instances=Count('equipment_instances'))
                .order_by('name'),
            index=None,
            exclude=None,
            columns=['name', 'n_equipment_instances'],
            coerce_float=False,
            nrows=None)

        return df.loc[df.n_equipment_instances == 0] \
            if only0 \
            else df


def project(name='TEST'):
    return Project(
        params=yaml.safe_load(
                open(os.path.join(
                        Project.CONFIG_DIR_PATH,
                        name + _YAML_EXT))))
