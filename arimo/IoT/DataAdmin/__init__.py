from __future__ import print_function

import botocore
import boto3
import os
import six

from django.conf import settings
from django.core.management import call_command
from django.core.wsgi import get_wsgi_application

import arimo.IoT.DataAdmin._project.settings
from arimo.IoT.DataAdmin.util import clean_lower_str, _clean_upper_str


_STR_CLASSES = \
    (str, unicode) \
    if six.PY2 \
    else str


_PARQUET_EXT = '.parquet'


class Project(object):
    _CAT_DATA_TYPE_NAME = 'cat'
    _NUM_DATA_TYPE_NAME = 'num'

    _CONTROL_EQUIPMENT_DATA_FIELD_TYPE_NAME = 'control'
    _MEASURE_EQUIPMENT_DATA_FIELD_TYPE_NAME = 'measure'

    _EQUIPMENT_INSTANCE_ID_COL_NAME = 'equipment_instance_id'
    _DATE_TIME_COL_NAME = 'date_time'

    def __init__(
            self, db_args,
            s3_bucket, s3_equipment_data_dir_prefix,
            aws_access_key_id, aws_secret_access_key):
        from arimo.util import Namespace

        arimo.IoT.DataAdmin._project.settings.DATABASES['default'].update({k.upper(): v for k, v in db_args.items()})
        settings.configure(**arimo.IoT.DataAdmin._project.settings.__dict__)
        get_wsgi_application()

        self._migrate()

        from arimo.IoT.DataAdmin.base.models import \
            DataType, EquipmentDataFieldType, EquipmentDataField, \
            EquipmentGeneralType, EquipmentUniqueType, EquipmentInstance

        from arimo.IoT.DataAdmin.PredMaint.models import Blueprint

        self.data = \
            Namespace(
                DataTypes=DataType.objects,
                EquipmentDataFieldTypes=EquipmentDataFieldType.objects,
                EquipmentDataFields=EquipmentDataField.objects,
                EquipmentGeneralTypes=EquipmentGeneralType.objects,
                EquipmentUniqueTypes=EquipmentUniqueType.objects,
                EquipmentInstances=EquipmentInstance.objects,
                PredMaintBlueprints=Blueprint.objects)

        self.CAT_DATA_TYPE = \
            self.data.DataTypes.get_or_create(
                name=self._CAT_DATA_TYPE_NAME,
                defaults=None)[0]

        self.NUM_DATA_TYPE = \
            self.data.DataTypes.get_or_create(
                name=self._NUM_DATA_TYPE_NAME,
                defaults=None)[0]

        self.CONTROL_EQUIPMENT_DATA_FIELD_TYPE = \
            self.data.EquipmentDataFieldTypes.get_or_create(
                name=self._CONTROL_EQUIPMENT_DATA_FIELD_TYPE_NAME,
                defaults=None)[0]

        self.MEASURE_EQUIPMENT_DATA_FIELD_TYPE = \
            self.data.EquipmentDataFieldTypes.get_or_create(
                name=self._MEASURE_EQUIPMENT_DATA_FIELD_TYPE_NAME,
                defaults=None)[0]

        self.params = \
            Namespace(
                s3=Namespace(
                    bucket=s3_bucket,

                    access_key_id=aws_access_key_id,
                    secret_access_key=aws_secret_access_key,

                    equipment_data_dir_prefix=s3_equipment_data_dir_prefix,
                    equipment_data_dir_path='s3://{}/{}'.format(s3_bucket, s3_equipment_data_dir_prefix)))

        self.S3_CLIENT = \
            boto3.client(
                's3',
                aws_access_key_id=aws_access_key_id,
                aws_secret_access_key=aws_secret_access_key,
                config=botocore.client.Config(
                    connect_timeout=9,
                    read_timeout=9))

    def _collect_static(self):
        call_command('collectstatic')

    def _create_super_user(self):
        call_command('createsuperuser')

    def _make_migrations(self):
        call_command('makemigrations')

    def _migrate(self):
        call_command('migrate')

    def equipment_general_type(self, equipment_general_type_name):
        return self.data.EquipmentGeneralTypes.get_or_create(
            name=clean_lower_str(equipment_general_type_name),
            defaults=None)[0]

    def equipment_unique_type(self, equipment_general_type_name, equipment_unique_type_name):
        return self.data.EquipmentUniqueTypes.get_or_create(
            equipment_general_type=
                self.equipment_general_type(
                    equipment_general_type_name=equipment_general_type_name),
            name=clean_lower_str(equipment_unique_type_name),
            defaults=None)[0]

    def update_or_create_equipment_data_field(
            self, equipment_general_type_name, equipment_data_field_name, control=False, cat=False,
            equipment_unique_type_names_incl=set(), equipment_unique_type_names_excl=set(),
            **kwargs):
        kwargs['data_type'] = \
            self.CAT_DATA_TYPE \
            if cat \
            else self.NUM_DATA_TYPE

        try:
            equipment_data_field = \
                self.data.EquipmentDataFields.update_or_create(
                    equipment_general_type=
                        self.equipment_general_type(
                            equipment_general_type_name=equipment_general_type_name),
                    equipment_data_field_type=
                        self.CONTROL_EQUIPMENT_DATA_FIELD_TYPE
                        if control
                        else self.MEASURE_EQUIPMENT_DATA_FIELD_TYPE,
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
                    self.equipment_unique_type(
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
                self.equipment_unique_type(
                    equipment_general_type_name=equipment_general_type_name,
                    equipment_unique_type_name=equipment_unique_type_name)

        equipment_instance = \
            self.data.EquipmentInstances.update_or_create(
                equipment_general_type=
                    self.equipment_general_type(
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

                if equipment_data_field.equipment_data_field_type.name == self._CONTROL_EQUIPMENT_DATA_FIELD_TYPE_NAME:
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
                                    self.equipment_unique_type(
                                        equipment_general_type_name=equipment_general_type_name,
                                        equipment_unique_type_name=equipment_unique_type_name))

                                equipment_data_field.equipment_unique_types = equipment_unique_types

                                equipment_data_field.save()

                        equipment_data_fields.append(equipment_data_field)

                        control_equipment_data_field_names.append(equipment_data_field_name)

                elif equipment_data_field.equipment_data_field_type.name == self._MEASURE_EQUIPMENT_DATA_FIELD_TYPE_NAME:
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
                                    self.equipment_unique_type(
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

    def load_equipment_data(
            self, equipment_instance_id_or_data_set_name,
            _on_files=True, _spark=True,
            iCol=_EQUIPMENT_INSTANCE_ID_COL_NAME, tCol=_DATE_TIME_COL_NAME,
            verbose=True, **kwargs):
        from arimo.df.on_files import FileDF
        from arimo.df.spark import ADF
        from arimo.df.spark_on_files import FileADF
        from arimo.util.spark_sql_types import _DATE_TYPE, _STR_TYPE

        path = os.path.join(
            self.params.s3.equipment_data_dir_path,
            equipment_instance_id_or_data_set_name + _PARQUET_EXT)

        if _on_files:
            return FileADF(
                    path=path,
                    aws_access_key_id=self.params.s3.access_key_id,
                    aws_secret_access_key=self.params.s3.secret_access_key,
                    iCol=iCol, tCol=tCol,
                    verbose=verbose, **kwargs) \
                if _spark \
                else FileDF(
                    paths=path,
                    aws_access_key_id=self.params.s3.access_key_id,
                    aws_secret_access_key=self.params.s3.secret_access_key,
                    i_col=iCol, t_col=tCol,
                    verbose=verbose, **kwargs)

        else:
            _resave = False

            try:
                adf = ADF.load(
                    path=path,
                    format='parquet', mergeSchema=True,
                    aws_access_key_id=self.params.s3.access_key_id,
                    aws_secret_access_key=self.params.s3.secret_access_key,
                    iCol=iCol, tCol=tCol,
                    verbose=verbose, **kwargs)

            except:
                adf = ADF.load(
                    path=os.path.join(
                        self.params.s3.equipment_data_dir_path,
                        _clean_upper_str(equipment_instance_id_or_data_set_name) + _PARQUET_EXT),
                    format='parquet', mergeSchema=True,
                    aws_access_key_id=self.params.s3.access_key_id,
                    aws_secret_access_key=self.params.s3.secret_access_key,
                    iCol=iCol, tCol=tCol,
                    verbose=verbose)

                _resave = True

            _complex_col_names = []

            for col in adf.columns:
                _col_type = adf.type(col)
                if _col_type.startswith('array<') or _col_type.startswith('map<') \
                        or _col_type.startswith('struct<') or _col_type.startswith('vector'):
                    _complex_col_names.append(col)

            if _complex_col_names:
                _resave = True
                adf.rm(*_complex_col_names, inplace=True)

            if ADF._DEFAULT_I_COL in adf.columns:
                _resave = True

                if self._EQUIPMENT_INSTANCE_ID_COL_NAME in adf.columns:
                    adf('COALESCE({0}, {1}) AS {0}'.format(self._EQUIPMENT_INSTANCE_ID_COL_NAME, ADF._DEFAULT_I_COL),
                        *set(adf.columns).difference((self._EQUIPMENT_INSTANCE_ID_COL_NAME, ADF._DEFAULT_I_COL)),
                        inplace=True)

                else:
                    adf.rename(
                        iCol=self._EQUIPMENT_INSTANCE_ID_COL_NAME,
                        inplace=True,
                        **{self._EQUIPMENT_INSTANCE_ID_COL_NAME: ADF._DEFAULT_I_COL})

            else:
                assert self._EQUIPMENT_INSTANCE_ID_COL_NAME in adf.columns
                adf.iCol = self._EQUIPMENT_INSTANCE_ID_COL_NAME

            if ADF._DEFAULT_D_COL in adf.columns:
                _date_col_type = adf.type(ADF._DEFAULT_D_COL)

                if _date_col_type != _DATE_TYPE:
                    assert _date_col_type == _STR_TYPE
                    _resave = True
                    adf.rm(ADF._DEFAULT_D_COL, inplace=True)

            else:
                _resave = True

            assert self._DATE_TIME_COL_NAME in adf.columns
            adf.tCol = self._DATE_TIME_COL_NAME

            if _resave:
                adf.save(
                    path=path,
                    format='parquet',
                    aws_access_key_id=self.params.s3.access_key_id,
                    aws_secret_access_key=self.params.s3.secret_access_key,
                    switch=True,
                    verbose=verbose)

            return adf

    def save_equipment_data(self, df, equipment_id_or_data_set_name, mode='overwrite', verbose=True):
        import pandas
        import pyspark.sql
        from arimo.df.spark import ADF

        if isinstance(df, pandas.DataFrame):
            adf = ADF.create(data=df)

        elif isinstance(df, pyspark.sql.DataFrame):
            adf = ADF(sparkDF=df)

        else:
            assert isinstance(df, ADF)
            adf = df

        if ADF._DEFAULT_I_COL in adf.columns:
            assert self._EQUIPMENT_INSTANCE_ID_COL_NAME not in adf.columns

            adf.rename(
                inplace=True,
                **{self._EQUIPMENT_INSTANCE_ID_COL_NAME: ADF._DEFAULT_I_COL})

        else:
            assert self._EQUIPMENT_INSTANCE_ID_COL_NAME in adf.columns

        assert self._DATE_TIME_COL_NAME in adf.columns
        adf.tCol = self._DATE_TIME_COL_NAME

        adf.save(
            path=os.path.join(
                self.params.s3.equipment_data_dir_path,
                equipment_id_or_data_set_name + _PARQUET_EXT),
            format='parquet',
            mode=mode,
            aws_access_key_id=self.params.s3.access_key_id,
            aws_secret_access_key=self.params.s3.secret_access_key,
            verbose=verbose)

    def merge_equipment_data_for_equipment_unique_type(
            self,
            equipment_general_type_name, equipment_unique_type_name,
            _max_n_equipment_instances_at_same_time=100,
            _spark_conf={},
            verbose=True,
            _min_i=0):
        import arimo.backend
        from arimo.df.spark import ADF
        from arimo.util import fs

        equipment_unique_type = \
            self.equipment_unique_type(
                equipment_general_type_name=equipment_general_type_name,
                equipment_unique_type_name=equipment_unique_type_name)

        equipment_unique_type_equipment_data_fields = \
            set(equipment_unique_type.data_fields.all())

        equipment_instances_data_file_urls = []

        for equipment_instance in \
                self.data.EquipmentInstances\
                    .filter(
                        equipment_unique_type=equipment_unique_type,
                        data_file_url__startswith='s3://')\
                    .order_by('name'):
            equipment_id = clean_lower_str(equipment_instance.name)

            assert equipment_unique_type_equipment_data_fields.issuperset(equipment_instance.data_fields.all()), \
                "*** Equipment Instance #{}'s Data Fields NOT a Subset of Those of {} Unique Type {} ***".format(
                    equipment_id, equipment_general_type_name, equipment_unique_type_name)

            equipment_instances_data_file_urls.append(equipment_instance.data_file_url)

        n_equipment_instances = len(equipment_instances_data_file_urls)

        if n_equipment_instances <= _max_n_equipment_instances_at_same_time:
            if arimo.backend.spark is None:
                arimo.backend.init(sparkConf=_spark_conf)

            adf = ADF.load(
                path=equipment_instances_data_file_urls,
                format='parquet', mergeSchema=True,
                aws_access_key_id=self.params.s3.access_key_id,
                aws_secret_access_key=self.params.s3.secret_access_key,
                verbose=verbose)

            assert adf.type(ADF._DEFAULT_D_COL) == 'date'

            adf.save(
                path=os.path.join(
                    self.params.s3.equipment_data_dir_path,
                    '{}---{}'.format(
                        clean_lower_str(equipment_general_type_name).upper(),
                        clean_lower_str(equipment_unique_type_name)) + _PARQUET_EXT),
                format='parquet', partitionBy=ADF._DEFAULT_D_COL,
                aws_access_key_id=self.params.s3.access_key_id,
                aws_secret_access_key=self.params.s3.secret_access_key,
                verbose=verbose)

        else:
            _tmp_paths = []

            for i in range(0, n_equipment_instances, _max_n_equipment_instances_at_same_time):
                _source_paths = equipment_instances_data_file_urls[i:(i + _max_n_equipment_instances_at_same_time)]

                _tmp_path = \
                    '/tmp/PanaCC-Data---{}-{}---{}-from-{}-to-{}'.format(
                        equipment_general_type_name, equipment_unique_type_name, i,
                        _source_paths[0].rsplit('/', 1)[1],
                        _source_paths[-1].rsplit('/', 1)[1])

                _tmp_paths.append(_tmp_path)

                if i >= _min_i:
                    if i or (arimo.backend.spark is None):
                        arimo.backend.init(sparkApp=_tmp_path, sparkConf=_spark_conf)

                    try:
                        _adf = ADF.load(
                            path=_tmp_path,
                            format='parquet',
                            verbose=verbose)

                        print('\n*** {} ALREADY EXISTS ***\n'.format(_tmp_path))

                    except:
                        _adf = ADF.load(
                            path=_source_paths,
                            format='parquet', mergeSchema=True,
                            aws_access_key_id=self.params.s3.access_key_id,
                            aws_secret_access_key=self.params.s3.secret_access_key,
                            verbose=verbose)

                        assert _adf.type(ADF._DEFAULT_D_COL) == 'date'

                        _adf.save(
                            path=_tmp_path,
                            format='parquet', partitionBy=ADF._DEFAULT_D_COL,
                            verbose=verbose)

                    arimo.backend.spark.stop()

            arimo.backend.init(sparkConf=_spark_conf)

            adf = ADF.load(
                path=_tmp_paths,
                format='parquet', mergeSchema=True,
                verbose=verbose)

            assert adf.type(ADF._DEFAULT_D_COL) == 'date'

            adf.save(
                path=os.path.join(
                    self.params.s3.equipment_data_dir_path,
                    '{}---{}'.format(
                        clean_lower_str(equipment_general_type_name).upper(),
                        clean_lower_str(equipment_unique_type_name)) + _PARQUET_EXT),
                format='parquet', partitionBy=ADF._DEFAULT_D_COL,
                aws_access_key_id=self.params.s3.access_key_id,
                aws_secret_access_key=self.params.s3.secret_access_key,
                verbose=verbose)

            for _tmp_path in _tmp_paths:
                fs.rm(
                    path=_tmp_path,
                    hdfs=fs._ON_LINUX_CLUSTER_WITH_HDFS,
                    is_dir=True)

    def merge_equipment_data_for_multi_equipment_unique_types(
            self,
            equipment_general_type_name, *equipment_unique_type_names,
            **kwargs):
        from arimo.util.aws import s3

        verbose = kwargs.pop('verbose', True)

        equipment_general_type_name = \
            clean_lower_str(equipment_general_type_name).upper()

        equipment_unique_type_names = \
            sorted(clean_lower_str(equipment_unique_type_name)
                   for equipment_unique_type_name in equipment_unique_type_names)

        to_dir_path = \
            os.path.join(
                self.params.s3.equipment_data_dir_path,
                '{}---{}'.format(
                    equipment_general_type_name,
                    '---'.join(equipment_unique_type_names)) + _PARQUET_EXT)

        s3.rm(
            path=to_dir_path,
            dir=True,
            quiet=True,
            access_key_id=self.params.s3.access_key_id,
            secret_access_key=self.params.s3.secret_access_key,
            verbose=verbose)

        for equipment_unique_type_name in equipment_unique_type_names:
            s3.sync(
                from_dir_path=os.path.join(
                    self.params.s3.equipment_data_dir_path,
                    '{}---{}'.format(
                        equipment_general_type_name,
                        equipment_unique_type_name + _PARQUET_EXT)),
                to_dir_path=os.path.join(
                    to_dir_path,
                    '__equipment_unique_type__={}'.format(equipment_unique_type_name)),
                quiet=True, delete=False,
                access_key_id=self.params.s3.access_key_id,
                secret_access_key=self.params.s3.secret_access_key,
                verbose=verbose)
