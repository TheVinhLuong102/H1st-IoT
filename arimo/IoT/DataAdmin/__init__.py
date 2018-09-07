from collections import Counter
import datetime
import os
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

    _EQUIPMENT_INSTANCE_ID_COL_NAME = 'equipment_instance_id'
    _EQUIPMENT_INSTANCE_ALIAS_COL_NAME = 'equipment_instance_alias'
    _DATE_TIME_COL_NAME = 'date_time'

    _DEFAULT_PARAMS = \
        dict(
            db=dict(
                admin=dict(
                    host=None, db_name=None,
                    user=None, password=None)),

            s3=dict(
                bucket=None,

                access_key_id=None,
                secret_access_key=None,

                equipment_data=dict(
                    dir_prefix='.arimo/PredMaint/EquipmentData')))

    def __init__(self, params, **kwargs):
        from arimo.util import Namespace
        from arimo.util.aws import s3

        self.params = Namespace(**self._DEFAULT_PARAMS)
        self.params.update(params, **kwargs)

        assert self.params.db.admin.host \
           and self.params.db.admin.db_name \
           and self.params.db.admin.user \
           and self.params.db.admin.password

        django_db_settings = arimo.IoT.DataAdmin._project.settings.DATABASES['default']
        django_db_settings['HOST'] = self.params.db.admin.host
        django_db_settings['NAME'] = self.params.db.admin.db_name
        django_db_settings['USER'] = self.params.db.admin.user
        django_db_settings['PASSWORD'] = self.params.db.admin.password
        settings.configure(**arimo.IoT.DataAdmin._project.settings.__dict__)
        get_wsgi_application()

        self._migrate()

        from arimo.IoT.DataAdmin.base.models import \
            DataType, EquipmentDataFieldType, EquipmentDataField, NumericMeasurementUnit, \
            EquipmentGeneralType, EquipmentUniqueTypeGroup, EquipmentUniqueType, \
            EquipmentFacility, EquipmentInstance, EquipmentSystem

        from arimo.IoT.DataAdmin.PredMaint.models import \
            EquipmentUniqueTypeGroupDataFieldProfile, \
            EquipmentUniqueTypeGroupServiceConfig, \
            Blueprint, \
            EquipmentUniqueTypeGroupDataFieldBlueprintBenchmarkMetricProfile, \
            EquipmentProblemPeriod, EquipmentProblemType, \
            AlertDiagnosisStatus, Alert

        self.data = \
            Namespace(
                DataTypes=DataType.objects,
                EquipmentDataFieldTypes=EquipmentDataFieldType.objects,
                EquipmentDataFields=EquipmentDataField.objects,
                NumericMeasurementUnits=NumericMeasurementUnit.objects,
                EquipmentGeneralTypes=EquipmentGeneralType.objects,
                EquipmentUniqueTypeGroups=EquipmentUniqueTypeGroup.objects,
                EquipmentUniqueTypes=EquipmentUniqueType.objects,
                EquipmentFacilities=EquipmentFacility.objects,
                EquipmentInstances=EquipmentInstance.objects,
                EquipmentSystems=EquipmentSystem.objects,

                EquipmentUniqueTypeGroupDataFieldProfiles=
                    EquipmentUniqueTypeGroupDataFieldProfile.objects,
                EquipmentUniqueTypeGroupPredMaintServiceConfigs=
                    EquipmentUniqueTypeGroupServiceConfig.objects,

                PredMaintBlueprints=Blueprint.objects,
                EquipmentUniqueTypeGroupDataFieldPredMaintBlueprintBenchmarkMetricProfiles=
                    EquipmentUniqueTypeGroupDataFieldBlueprintBenchmarkMetricProfile.objects,

                EquipmentProblemTypes=EquipmentProblemType.objects,
                EquipmentProblemPeriods=EquipmentProblemPeriod.objects,

                PredMaintAlerts=Alert.objects,
                PredMaintAlertDiagnosisStatuses=AlertDiagnosisStatus.objects)

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

        if 's3' in self.params:
            self.params.s3.equipment_data.dir_path = \
                's3://{}/{}'.format(
                    self.params.s3.bucket,
                    self.params.s3.equipment_data.dir_prefix)

            self.s3_client = \
                s3.client(
                    access_key_id=self.params.s3.access_key_id,
                    secret_access_key=self.params.s3.secret_access_key)

    @classmethod
    def __qual_name__(cls):
        return '{}.{}'.format(cls.__module__, cls.__name__)

    def _collect_static(self):
        call_command('collectstatic')

    def _create_super_user(self):
        call_command('createsuperuser')

    def _make_migrations(self):
        call_command('makemigrations')

    def _migrate(self):
        call_command('migrate')

    def create_equipment_general_type(self, equipment_general_type_name):
        return self.data.EquipmentGeneralTypes.get_or_create(
                name=clean_lower_str(equipment_general_type_name),
                defaults=None)[0]

    def equipment_general_type(self, equipment_general_type_name):
        equipment_general_types = \
            self.data.EquipmentGeneralTypes.filter(
                name=clean_lower_str(equipment_general_type_name))

        assert len(equipment_general_types) == 1, \
            '*** {}: {} ***'.format(equipment_general_type_name, equipment_general_types)

        return equipment_general_types[0]

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
        equipment_general_type_groups = \
            self.data.EquipmentUniqueTypeGroups.filter(
                equipment_general_type__name=clean_lower_str(equipment_general_type_name),
                name=clean_lower_str(equipment_unique_type_group_name))

        assert len(equipment_general_type_groups) == 1, \
            '*** {} {}: {} ***'.format(
                equipment_general_type_name,
                equipment_unique_type_group_name,
                equipment_general_type_groups)

        return equipment_general_type_groups[0]

    def update_or_create_equipment_unique_type(
            self, equipment_general_type_name, equipment_unique_type_name,
            equipment_unique_type_group_names_incl=set(), equipment_unique_type_group_names_excl=set()):
        equipment_unique_type = \
            self.data.EquipmentUniqueTypes.get_or_create(
                equipment_general_type=
                    self.equipment_general_type(
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
        equipment_unique_types = \
            self.data.EquipmentUniqueTypes.filter(
                equipment_general_type__name=clean_lower_str(equipment_general_type_name),
                name=clean_lower_str(equipment_unique_type_name))

        assert len(equipment_unique_types) == 1, \
            '*** {} {}: {} ***'.format(
                equipment_general_type_name,
                equipment_unique_type_name,
                equipment_unique_types)

        return equipment_unique_types[0]

    def update_or_create_equipment_data_field(
            self, equipment_general_type_name, equipment_data_field_name, control=False, cat=None,
            equipment_unique_type_names_incl=set(), equipment_unique_type_names_excl=set(),
            **kwargs):
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
                    self.CONTROL_EQUIPMENT_DATA_FIELD_TYPE
                    if control
                    else self.MEASURE_EQUIPMENT_DATA_FIELD_TYPE,
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
        equipment_data_fields = \
            self.data.EquipmentDataFields.filter(
                equipment_general_type__name=clean_lower_str(equipment_general_type_name),
                equipment_data_field_type=
                    self.CONTROL_EQUIPMENT_DATA_FIELD_TYPE
                    if control
                    else self.MEASURE_EQUIPMENT_DATA_FIELD_TYPE,
                name=clean_lower_str(equipment_data_field_name))

        assert len(equipment_data_fields) == 1, \
            '*** {} ***'.format(equipment_data_fields)

        return equipment_data_fields[0]

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

    def equipment_instance(self, equipment_general_type_name, equipment_instance_name):
        equipment_instances = \
            self.data.EquipmentInstances.filter(
                equipment_general_type__name=clean_lower_str(equipment_general_type_name),
                name=clean_lower_str(equipment_instance_name))

        assert len(equipment_instances) == 1, \
            '*** MULTIPLE {} ***'.format(equipment_instances) \
            if bool(equipment_instances) \
            else '*** {} #{} DOES NOT EXIST ***'.format(equipment_general_type_name, equipment_instance_name)

        return equipment_instances[0]

    def save_equipment_data(
            self, df, equipment_instance_id_or_data_set_name,
            mode='overwrite', _spark=False, verbose=True):
        import pandas
        import pyspark.sql
        from arimo.df.spark import SparkADF
        from arimo.util.date_time import DATE_COL

        if isinstance(df, _STR_CLASSES):
            adf = SparkADF.load(
                path=df,
                aws_access_key_id=self.params.s3.access_key_id,
                aws_secret_access_key=self.params.s3.secret_access_key,
                verbose=verbose)

        elif isinstance(df, pandas.DataFrame):
            adf = SparkADF.create(data=df)

        elif isinstance(df, pyspark.sql.DataFrame):
            adf = SparkADF(sparkDF=df)

        else:
            assert isinstance(df, SparkADF)
            adf = df

        if SparkADF._DEFAULT_I_COL in adf.columns:
            assert self._EQUIPMENT_INSTANCE_ID_COL_NAME not in adf.columns

            adf.rename(
                inplace=True,
                iCol=self._EQUIPMENT_INSTANCE_ID_COL_NAME,
                **{self._EQUIPMENT_INSTANCE_ID_COL_NAME: SparkADF._DEFAULT_I_COL})

        else:
            assert self._EQUIPMENT_INSTANCE_ID_COL_NAME in adf.columns
            adf.tCol = self._EQUIPMENT_INSTANCE_ID_COL_NAME

        assert self._DATE_TIME_COL_NAME in adf.columns
        adf.tCol = self._DATE_TIME_COL_NAME

        adf.save(
            path=os.path.join(
                self.params.s3.equipment_data.dir_path,
                equipment_instance_id_or_data_set_name + _PARQUET_EXT),
            format='parquet',
            mode=mode,
            partitionBy=DATE_COL,
            aws_access_key_id=self.params.s3.access_key_id,
            aws_secret_access_key=self.params.s3.secret_access_key,
            verbose=verbose)

    def load_equipment_data(
            self, equipment_instance_id_or_data_set_name,
            _from_files=True, _spark=False,
            set_i_col=True, set_t_col=True,
            verbose=True, **kwargs):
        from arimo.df.from_files import ArrowADF
        from arimo.df.spark import SparkADF
        from arimo.df.spark_from_files import ArrowSparkADF
        from arimo.util.date_time import DATE_COL

        path = os.path.join(
            self.params.s3.equipment_data.dir_path,
            equipment_instance_id_or_data_set_name + _PARQUET_EXT)

        adf = (ArrowSparkADF(
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
               else ArrowADF(
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
            else SparkADF.load(
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

    def check_equipment_data_integrity(self, equipment_instance_id_or_data_set_name):
        from arimo.df.spark_from_files import ArrowSparkADF
        from arimo.util.date_time import DATE_COL
        from arimo.util.types.spark_sql import _DATE_TYPE

        file_adf = \
            ArrowSparkADF(
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

    def equipment_unique_type_group_data_fields(self, equipment_general_type_name, equipment_unique_type_group_name):
        equipment_unique_types = \
            self.equipment_unique_type_group(
                equipment_general_type_name=equipment_general_type_name,
                equipment_unique_type_group_name=equipment_unique_type_group_name) \
            .equipment_unique_types.all()

        return equipment_unique_types[0].data_fields.all().union(
                *(equipment_unique_type.data_fields.all()
                  for equipment_unique_type in equipment_unique_types[1:]),
                all=False)

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

    def _equipment_data_fields_n_equipment_unique_types(only0=True):
        df = pandas.DataFrame.from_records(
            data=IoT_DATA_ADMIN_PROJECT.models.base.EquipmentDataField.objects
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

    def equipment_unique_types_n_equipment_data_fields(only0=True):
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

    def equipment_data_field_names_n_counts(only_multi=True):
        d = {(i['equipment_general_type__name'], i['name']): i['n']
             for i in IoT_DATA_ADMIN_PROJECT.models.base.EquipmentDataField.objects
                 .values('equipment_general_type__name', 'name')
                 .annotate(n=Count('name'))
                 .order_by('equipment_general_type__name', 'name')}

        return {k: v for k, v in d.items() if v > 1} \
            if only_multi \
            else d

    def equipment_instances_w_cap_urls():
        _PREFIX = 's3://arimo-panasonic-ap/data/CombinedConfigMeasure/'
        _PREFIX_LEN = len(_PREFIX)

        ls = []

        for equipment_instance in \
                IoT_DATA_ADMIN_PROJECT.models.base.EquipmentInstance.objects.filter(data_file_url__startswith=_PREFIX):
            data_file_url = equipment_instance.data_file_url[_PREFIX_LEN:]
            if data_file_url != data_file_url.lower():
                ls.append(data_file_url)

        return ls

    def equipment_instances_n_equipment_unique_types(only_multi=False):
        s = pandas.DataFrame.from_records(
            data=IoT_DATA_ADMIN_PROJECT.models.base.EquipmentInstance.objects
                .values('name')
                .annotate(n_equipment_unique_types=Count('equipment_unique_type'))
                .order_by('name'),
            index=None,
            exclude=None,
            columns=['name', 'n_equipment_unique_types'],
            coerce_float=False,
            nrows=None) \
            .set_index(
            keys='name',
            drop=True,
            append=False,
            inplace=False,
            verify_integrity=True)['n_equipment_unique_types']

        return s.loc[s > 1] \
            if only_multi \
            else s

    def equipment_unique_types_n_equipment_instances_w_data(equipment_general_type_name='refrig'):
        return pandas.DataFrame.from_records(
            data=IoT_DATA_ADMIN_PROJECT.models.base.EquipmentInstance.objects
                .filter(
                equipment_general_type__name=equipment_general_type_name,
                data_file_url__startswith='s3://')
                .values('equipment_unique_type__name')
                .annotate(n=Count('data_file_url'))
                .order_by('equipment_unique_type__name'),
            index=None,
            exclude=None,
            columns=['equipment_unique_type__name', 'n'],
            coerce_float=False,
            nrows=None) \
            .set_index(
            keys='equipment_unique_type__name',
            drop=True,
            append=False,
            inplace=False,
            verify_integrity=True)['n']


def project(name='TEST'):
    from arimo.util.aws import key_pair

    params = yaml.safe_load(open(os.path.join(Project.CONFIG_DIR_PATH, name + _YAML_EXT), 'r'))

    if 's3' in params:
        params['s3']['access_key_id'], params['s3']['secret_access_key'] = key_pair(profile=name)

    return Project(params=params)
