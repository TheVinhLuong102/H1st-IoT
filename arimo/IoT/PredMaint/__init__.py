from __future__ import absolute_import, division, print_function

from collections import Counter
import datetime
from dateutil.relativedelta import relativedelta
import math
import numpy
import os
import pandas
from psycopg2.extras import DateRange
from pyspark.sql import functions
from ruamel import yaml
from scipy.stats import pearsonr
import tempfile
import time
import tqdm
import uuid

import arimo.backend
from arimo.blueprints import AbstractPPPBlueprint, load as load_blueprint
from arimo.blueprints.cs import anom as cs_anom, regr as cs_regr
from arimo.data.parquet import S3ParquetDataFeeder
from arimo.data.distributed import DDF
from arimo.data.distributed_parquet import S3ParquetDistributedDataFrame
from arimo.util import fs, Namespace
from arimo.util.aws import key_pair, s3
from arimo.util.date_time import \
    DATE_COL, MONTH_COL, \
    _PRED_VARS_INCL_T_AUX_COLS, _T_WoM_COL, _T_DoW_COL, _T_DELTA_COL, _T_PoM_COL, _T_PoW_COL, _T_PoD_COL, \
    month_end, month_str
from arimo.util.types.spark_sql import _BOOL_TYPE

from django.conf import settings
from django.core.management import call_command
from django.core.wsgi import get_wsgi_application

import arimo.IoT.DataAdmin._django_root.settings
from arimo.IoT.DataAdmin.util import _PARQUET_EXT, _YAML_EXT, clean_lower_str


class Project(object):
    CONFIG_LOCAL_DIR_PATH = os.path.expanduser('~/.arimo/pm')
    CONFIG_S3_BUCKET = 'arimo-iot-pm'
    AWS_PROFILE_NAME = 'arimo'

    _CAT_DATA_TYPE_NAME = 'cat'
    _NUM_DATA_TYPE_NAME = 'num'

    _CONTROL_EQUIPMENT_DATA_FIELD_TYPE_NAME = 'control'
    _MEASURE_EQUIPMENT_DATA_FIELD_TYPE_NAME = 'measure'
    _CALC_EQUIPMENT_DATA_FIELD_TYPE_NAME = 'calc'
    _ALARM_EQUIPMENT_DATA_FIELD_TYPE_NAME = 'alarm'

    _EQUIPMENT_INSTANCE_ID_COL_NAME = 'equipment_instance_id'
    _DATE_TIME_COL_NAME = 'date_time'

    REF_N_MONTHS = 18

    BENCHMARK_REF_DATA_PROPORTION = .32

    _LOADED_BLUEPRINTS = {}

    MIN_PROPORTION_OF_GOOD_COMPONENT_BLUEPRINTS = .32

    MAX_INDIV_REF_BENCHMARK_METRIC_OVER_GLOBAL_REF_BENCHMARK_METRIC_RATIO = 1.68

    _BLUEPRINT_UUID_COL = 'blueprint_uuid'

    _OVERALL_PPP_ANOM_SCORE_NAME_PREFIX = 'rowHigh__'
    _OVERALL_PPP_ANOM_SCORE_NAME_PREFIX_LEN = len(_OVERALL_PPP_ANOM_SCORE_NAME_PREFIX)

    DEFAULT_EWMA_ALPHA = .168

    _DEFAULT_EWMA_ALPHA_PREFIX = 'ewma' + '{:.3f}'.format(DEFAULT_EWMA_ALPHA)[-3:] + '__'
    _DEFAULT_EWMA_ALPHA_PREFIX_LEN = len(_DEFAULT_EWMA_ALPHA_PREFIX)

    _DEFAULT_PARAMS = \
        Namespace(
            s3=Namespace(
                equipment_data=Namespace(
                    dir_prefix='.arimo/PredMaint/EquipmentData',
                    raw_dir_prefix='.arimo/PredMaint/EquipmentData/raw',
                    daily_agg_dir_prefix='.arimo/PredMaint/EquipmentData/DailyAgg',
                    train_val_benchmark_dir_prefix='.arimo/PredMaint/EquipmentData/TrainValBenchmark'),

                ppp=Namespace(
                    blueprints_dir_prefix='.arimo/PredMaint/PPP/Blueprints',
                    err_mults_dir_prefix='.arimo/PredMaint/PPP/ErrMults',
                    daily_err_mults_dir_prefix='.arimo/PredMaint/PPP/DailyErrMults'),

                anom_scores=Namespace(
                    dir_prefix='.arimo/PredMaint/AnomScores')),

            equipment_monitoring=Namespace(
                anom_score_names_and_thresholds=dict(
                    rowHigh__dailyMean__abs__MAE_Mult=(2, 2.5, 3, 3.5, 4, 4.5, 5))))

    _ALERT_DIAGNOSIS_STATUS_TO_DIAGNOSE_STR = 'to_diagnose'
    _ALERT_DIAGNOSIS_STATUS_MONITORING_STR = 'monitoring'
    _ALERT_DIAGNOSIS_STATUS_CONCLUDED_TRUE_EQUIPMENT_PROBLEMS_STR = 'concluded_true_equipment_problems'
    _ALERT_DIAGNOSIS_STATUS_CONCLUDED_NO_EQUIPMENT_PROBLEMS_STR = 'concluded_no_equipment_problems'

    _MAX_N_DISTINCT_VALUES_TO_PROFILE = 30
    _MAX_N_ROWS_TO_COPY_TO_DB_AT_ONE_TIME = 10 ** 3

    def __init__(self, params, **kwargs):
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
            EquipmentComponent, \
            EquipmentDataField, \
            EquipmentUniqueTypeGroup, EquipmentUniqueType, \
            EquipmentInstance, EquipmentInstanceDailyMetadata, EquipmentInstanceDataFieldDailyAgg, \
            EquipmentFacility, EquipmentSystem, \
            Error

        from arimo.IoT.DataAdmin.PredMaint.models import \
            EquipmentUniqueTypeGroupDataFieldProfile, \
            EquipmentUniqueTypeGroupDataFieldPairwiseCorrelation, \
            EquipmentUniqueTypeGroupServiceConfig, \
            Blueprint, \
            EquipmentUniqueTypeGroupDataFieldBlueprintBenchmarkMetricProfile, \
            EquipmentInstanceDailyRiskScore, \
            EquipmentProblemType, EquipmentInstanceAlarmPeriod, EquipmentInstanceProblemDiagnosis, \
            AlertDiagnosisStatus, Alert

        from arimo.IoT.DataAdmin.tasks.models import \
            EquipmentUniqueTypeGroupRiskScoringTask

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

                Errors=Error.objects,

                EquipmentUniqueTypeGroupDataFieldProfiles=
                    EquipmentUniqueTypeGroupDataFieldProfile.objects,
                EquipmentUniqueTypeGroupDataFieldPairwiseCorrelations=
                    EquipmentUniqueTypeGroupDataFieldPairwiseCorrelation.objects,

                EquipmentUniqueTypeGroupPredMaintServiceConfigs=
                    EquipmentUniqueTypeGroupServiceConfig.objects,

                PredMaintBlueprints=Blueprint.objects,
                EquipmentUniqueTypeGroupDataFieldPredMaintBlueprintBenchmarkMetricProfiles=
                    EquipmentUniqueTypeGroupDataFieldBlueprintBenchmarkMetricProfile.objects,

                EquipmentInstanceDailyRiskScores=EquipmentInstanceDailyRiskScore.objects,

                EquipmentProblemTypes=EquipmentProblemType.objects,
                EquipmentInstanceAlarmPeriods=EquipmentInstanceAlarmPeriod.objects,
                EquipmentInstanceProblemDiagnoses=EquipmentInstanceProblemDiagnosis.objects,

                PredMaintAlertDiagnosisStatuses=AlertDiagnosisStatus.objects,
                PredMaintAlerts=Alert.objects,

                EquipmentUniqueTypeGroupRiskScoringTasks=EquipmentUniqueTypeGroupRiskScoringTask.objects)

        self.CAT_DATA_TYPE = DataType.objects.get_or_create(name=self._CAT_DATA_TYPE_NAME)[0]

        self.NUM_DATA_TYPE = DataType.objects.get_or_create(name=self._NUM_DATA_TYPE_NAME)[0]

        self.CONTROL_EQUIPMENT_DATA_FIELD_TYPE = \
            EquipmentDataFieldType.objects.get_or_create(name=self._CONTROL_EQUIPMENT_DATA_FIELD_TYPE_NAME)[0]

        self.MEASURE_EQUIPMENT_DATA_FIELD_TYPE = \
            EquipmentDataFieldType.objects.get_or_create(name=self._MEASURE_EQUIPMENT_DATA_FIELD_TYPE_NAME)[0]

        self.CALC_EQUIPMENT_DATA_FIELD_TYPE = \
            EquipmentDataFieldType.objects.get_or_create(name=self._CALC_EQUIPMENT_DATA_FIELD_TYPE_NAME)[0]

        self.ALARM_EQUIPMENT_DATA_FIELD_TYPE = \
            EquipmentDataFieldType.objects.get_or_create(name=self._ALARM_EQUIPMENT_DATA_FIELD_TYPE_NAME)[0]

        self.params.s3.bucket = GlobalConfig.objects.get_or_create(key='S3_BUCKET')[0].value

        if self.params.s3.bucket:
            if 'access_key_id' in self.params.s3:
                assert 'secret_access_key' in self.params.s3

            else:
                self.params.s3.access_key_id = \
                    GlobalConfig.objects.get_or_create(
                        key='AWS_ACCESS_KEY_ID')[0].value

                self.params.s3.secret_access_key = \
                    GlobalConfig.objects.get_or_create(
                        key='AWS_SECRET_ACCESS_KEY')[0].value

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
                's3://{}/{}'.format(
                    self.params.s3.bucket,
                    self.params.s3.equipment_data.daily_agg_dir_prefix)

            self.params.s3.equipment_data.train_val_benchmark_dir_path = \
                's3://{}/{}'.format(
                    self.params.s3.bucket,
                    self.params.s3.equipment_data.train_val_benchmark_dir_prefix)
    
            self.params.s3.ppp.blueprints_dir_path = \
                's3://{}/{}'.format(
                    self.params.s3.bucket,
                    self.params.s3.ppp.blueprints_dir_prefix)

        self.ALERT_DIAGNOSIS_STATUS_TO_DIAGNOSE = \
            AlertDiagnosisStatus.objects.get_or_create(
                name=self._ALERT_DIAGNOSIS_STATUS_TO_DIAGNOSE_STR,
                defaults=dict(index=0))[0]

        self.ALERT_DIAGNOSIS_STATUS_MONITORING = \
            AlertDiagnosisStatus.objects.get_or_create(
                name=self._ALERT_DIAGNOSIS_STATUS_MONITORING_STR,
                defaults=dict(index=1))[0]

        self.ALERT_DIAGNOSIS_STATUS_CONCLUDED_TRUE_EQUIPMENT_PROBLEMS = \
            AlertDiagnosisStatus.objects.get_or_create(
                name=self._ALERT_DIAGNOSIS_STATUS_CONCLUDED_TRUE_EQUIPMENT_PROBLEMS_STR,
                defaults=dict(index=9))[0]

        self.ALERT_DIAGNOSIS_STATUS_CONCLUDED_NO_EQUIPMENT_PROBLEMS = \
            AlertDiagnosisStatus.objects.get_or_create(
                name=self._ALERT_DIAGNOSIS_STATUS_CONCLUDED_NO_EQUIPMENT_PROBLEMS_STR,
                defaults=dict(index=10))[0]

        self.params.equipment_monitoring.equipment_unique_type_groups_monitored_and_included_excluded_data_fields = Namespace()

        for equipment_unique_type_group_service_config in EquipmentUniqueTypeGroupServiceConfig.objects.filter(active=True):
            equipment_general_type_name = equipment_unique_type_group_service_config.equipment_unique_type_group.equipment_general_type.name

            if equipment_general_type_name not in self.params.equipment_monitoring.equipment_unique_type_groups_monitored_and_included_excluded_data_fields:
                self.params.equipment_monitoring.equipment_unique_type_groups_monitored_and_included_excluded_data_fields[equipment_general_type_name] = Namespace()

            equipment_unique_type_group_name = equipment_unique_type_group_service_config.equipment_unique_type_group.name

            if equipment_unique_type_group_name not in self.params.equipment_monitoring.equipment_unique_type_groups_monitored_and_included_excluded_data_fields[equipment_general_type_name]:
                self.params.equipment_monitoring.equipment_unique_type_groups_monitored_and_included_excluded_data_fields[equipment_general_type_name][equipment_unique_type_group_name] = Namespace()

            included_categorical_equipment_data_field_names = \
                {categorical_equipment_data_field.name
                 for categorical_equipment_data_field in
                    equipment_unique_type_group_service_config.equipment_unique_type_group.equipment_data_fields
                    .exclude(data_type=self.NUM_DATA_TYPE)} \
                if equipment_unique_type_group_service_config.include_categorical_equipment_data_fields \
                else set()

            for equipment_unique_type_group_monitored_data_field_config in \
                    equipment_unique_type_group_service_config.equipment_unique_type_group_monitored_data_field_configs.filter(active=True):
                excluded_equipment_data_field_names = \
                    sorted(
                        excluded_equipment_data_field.name
                        for excluded_equipment_data_field in
                            equipment_unique_type_group_service_config.global_excluded_equipment_data_fields.all().union(
                                equipment_unique_type_group_monitored_data_field_config.manually_excluded_equipment_data_fields.all(),
                                all=False))

                self.params.equipment_monitoring.equipment_unique_type_groups_monitored_and_included_excluded_data_fields[equipment_general_type_name][equipment_unique_type_group_name][equipment_unique_type_group_monitored_data_field_config.monitored_equipment_data_field.name] = \
                    Namespace(
                        included=
                            sorted(
                                included_categorical_equipment_data_field_names.union(
                                    included_equipment_data_field.name
                                    for included_equipment_data_field in
                                        equipment_unique_type_group_service_config.equipment_unique_type_group.equipment_data_fields.filter(
                                            name__in={i[0] for i in equipment_unique_type_group_monitored_data_field_config.auto_included_numeric_equipment_data_fields})
                                        .union(
                                            equipment_unique_type_group_monitored_data_field_config.manually_included_equipment_data_fields.all(),
                                            all=False))
                                .difference(excluded_equipment_data_field_names)),
                        excluded=excluded_equipment_data_field_names)

    def load_equipment_data(
            self, equipment_data_set_name,
            spark=False, set_i_col=True, set_t_col=True,
            verbose=True, **kwargs):
        path = os.path.join(
                self.params.s3.equipment_data.dir_path,
                equipment_data_set_name + _PARQUET_EXT)

        df = S3ParquetDistributedDataFrame(
                path=path, mergeSchema=True,
                aws_access_key_id=self.params.s3.access_key_id,
                aws_secret_access_key=self.params.s3.secret_access_key,
                iCol=self._EQUIPMENT_INSTANCE_ID_COL_NAME
                    if set_i_col
                    else None,
                tCol=self._DATE_TIME_COL_NAME
                    if set_t_col
                    else None,
                verbose=verbose, **kwargs) \
            if spark \
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
                    verbose=verbose, **kwargs)

        assert {self._EQUIPMENT_INSTANCE_ID_COL_NAME, DATE_COL, self._DATE_TIME_COL_NAME}.issubset(df.columns)

        return df

    def profile_equipment_data_fields(self, equipment_general_type_name=None, equipment_unique_type_group_name=None, to_month=None):
        results = \
            Namespace(**{
                equipment_general_type_name:
                    Namespace(**{
                        equipment_unique_type_group_name: None
                    })
                    if equipment_unique_type_group_name
                    else Namespace(**{
                        equipment_unique_type_group_name: None
                        for equipment_unique_type_group_name in
                            self.params.equipment_monitoring.equipment_unique_type_groups_monitored_and_included_excluded_data_fields[equipment_general_type_name]
                    })
            }) \
            if equipment_general_type_name \
            else Namespace(**{
                equipment_general_type_name:
                    Namespace(**{
                        equipment_unique_type_group_name: None
                        for equipment_unique_type_group_name in
                            self.params.equipment_monitoring.equipment_unique_type_groups_monitored_and_included_excluded_data_fields[equipment_general_type_name]
                    })
                for equipment_general_type_name in self.params.equipment_monitoring.equipment_unique_type_groups_monitored_and_included_excluded_data_fields
            })

        for equipment_general_type_name, equipment_unique_type_group_names in tqdm.tqdm(results.items()):
            for equipment_unique_type_group_name in tqdm.tqdm(equipment_unique_type_group_names):
                equipment_unique_type_group_data_set_name = \
                    '{}---{}'.format(
                        equipment_general_type_name.upper(),
                        equipment_unique_type_group_name)

                s3_parquet_df = \
                    self.load_equipment_data(
                        equipment_unique_type_group_data_set_name,
                        spark=False, set_i_col=True, set_t_col=True,
                        verbose=True)

                if to_month:
                    to_date = month_end(to_month)

                    s3_parquet_df = \
                        s3_parquet_df.filterByPartitionKeys(
                            (DATE_COL,
                             str((datetime.datetime.strptime('{}-01'.format(to_month), '%Y-%m-%d') -
                                  relativedelta(months=self.REF_N_MONTHS - 1)).date()),
                             str(to_date)))

                else:
                    to_date = None

                equipment_unique_type_group = \
                    self.data.EquipmentUniqueTypeGroups.get(
                        equipment_general_type__name=equipment_general_type_name,
                        name=equipment_unique_type_group_name)

                self.data.EquipmentUniqueTypeGroupDataFieldProfiles.filter(
                    equipment_unique_type_group=equipment_unique_type_group,
                    to_date=to_date) \
                .delete()

                for equipment_data_field in tqdm.tqdm(equipment_unique_type_group.equipment_data_fields.all()):
                    equipment_data_field_name = equipment_data_field.name

                    if equipment_data_field_name in s3_parquet_df.contentCols:
                        if s3_parquet_df.typeIsNum(equipment_data_field_name):
                            s3_parquet_df._nulls[equipment_data_field_name] = \
                                equipment_data_field.lower_numeric_null, \
                                equipment_data_field.upper_numeric_null

                        _distinct_values_proportions = s3_parquet_df.distinct(equipment_data_field_name, count=True).to_dict()
                        _n_distinct_values = len(_distinct_values_proportions)

                        equipment_unique_type_group_data_field_profile = \
                            self.data.EquipmentUniqueTypeGroupDataFieldProfiles.create(
                                equipment_unique_type_group=equipment_unique_type_group,
                                equipment_data_field=equipment_data_field,
                                to_date=to_date,
                                valid_proportion=s3_parquet_df.nonNullProportion(equipment_data_field_name),
                                n_distinct_values=_n_distinct_values)

                        if _n_distinct_values <= self._MAX_N_DISTINCT_VALUES_TO_PROFILE:
                            equipment_unique_type_group_data_field_profile.distinct_values = _distinct_values_proportions

                        if s3_parquet_df.typeIsNum(equipment_data_field_name):
                            quartiles = \
                                s3_parquet_df.reprSample[equipment_data_field_name] \
                                .describe(
                                    percentiles=(.25, .5, .75)) \
                                .drop(
                                    index='count',
                                    level=None,
                                    inplace=False,
                                    errors='raise') \
                                .to_dict()

                            equipment_unique_type_group_data_field_profile.sample_min = \
                                quartiles['min']

                            equipment_unique_type_group_data_field_profile.outlier_rst_min = \
                                s3_parquet_df.outlierRstMin(equipment_data_field_name)

                            equipment_unique_type_group_data_field_profile.sample_quartile = \
                                quartiles['25%']

                            equipment_unique_type_group_data_field_profile.sample_median = \
                                quartiles['50%']

                            equipment_unique_type_group_data_field_profile.sample_3rd_quartile = \
                                quartiles['75%']

                            equipment_unique_type_group_data_field_profile.outlier_rst_max = \
                                s3_parquet_df.outlierRstMax(equipment_data_field_name)

                            equipment_unique_type_group_data_field_profile.sample_max = \
                                quartiles['max']

                        equipment_unique_type_group_data_field_profile.save()

    def profile_equipment_data_field_pairwise_correlations(self, equipment_general_type_name=None, equipment_unique_type_group_name=None):
        results = \
            Namespace(**{
                equipment_general_type_name:
                    Namespace(**{
                        equipment_unique_type_group_name: None
                    })
                    if equipment_unique_type_group_name
                    else Namespace(**{
                        equipment_unique_type_group_name: None
                        for equipment_unique_type_group_name in
                            self.params.equipment_monitoring.equipment_unique_type_groups_monitored_and_included_excluded_data_fields[equipment_general_type_name]
                    })
            }) \
            if equipment_general_type_name \
            else Namespace(**{
                equipment_general_type_name:
                    Namespace(**{
                        equipment_unique_type_group_name: None
                        for equipment_unique_type_group_name in
                            self.params.equipment_monitoring.equipment_unique_type_groups_monitored_and_included_excluded_data_fields[equipment_general_type_name]
                    })
                for equipment_general_type_name in self.params.equipment_monitoring.equipment_unique_type_groups_monitored_and_included_excluded_data_fields
            })

        for equipment_general_type_name, equipment_unique_type_group_names in tqdm.tqdm(results.items()):
            for equipment_unique_type_group_name in tqdm.tqdm(equipment_unique_type_group_names):
                equipment_unique_type_group_data_set_name = \
                    '{}---{}'.format(
                        equipment_general_type_name.upper(),
                        equipment_unique_type_group_name)

                s3_parquet_df = \
                    self.load_equipment_data(
                        equipment_unique_type_group_data_set_name,
                        spark=False, set_i_col=True, set_t_col=True,
                        verbose=True)

                equipment_unique_type_group = \
                    self.data.EquipmentUniqueTypeGroups.get(
                        equipment_general_type__name=equipment_general_type_name,
                        name=equipment_unique_type_group_name)

                self.data.EquipmentUniqueTypeGroupDataFieldPairwiseCorrelations.filter(
                    equipment_unique_type_group=equipment_unique_type_group) \
                .delete()

                equipment_data_fields = equipment_unique_type_group.equipment_data_fields.filter(data_type=self.NUM_DATA_TYPE)

                n_equipment_data_fields = equipment_data_fields.count()

                from arimo.IoT.DataAdmin.PredMaint.models import EquipmentUniqueTypeGroupDataFieldPairwiseCorrelation

                for i in tqdm.tqdm(range(n_equipment_data_fields - 1)):
                    equipment_data_field = equipment_data_fields[i]
                    equipment_data_field_name = equipment_data_field.name

                    if equipment_data_field_name in s3_parquet_df.possibleNumContentCols:
                        s3_parquet_df._nulls[equipment_data_field_name] = \
                            equipment_data_field.lower_numeric_null, \
                            equipment_data_field.upper_numeric_null

                        outlier_rst_min = s3_parquet_df.outlierRstMin(equipment_data_field_name)
                        outlier_rst_max = s3_parquet_df.outlierRstMax(equipment_data_field_name)

                        if outlier_rst_min < outlier_rst_max:
                            for i_2 in tqdm.tqdm(range(i + 1, n_equipment_data_fields)):
                                equipment_data_field_2 = equipment_data_fields[i_2]
                                equipment_data_field_name_2 = equipment_data_field_2.name

                                if (equipment_data_field_name_2 != equipment_data_field_name) and \
                                        (equipment_data_field_name_2 in s3_parquet_df.possibleNumContentCols):
                                    s3_parquet_df._nulls[equipment_data_field_name_2] = \
                                        equipment_data_field_2.lower_numeric_null, \
                                        equipment_data_field_2.upper_numeric_null

                                    outlier_rst_min_2 = s3_parquet_df.outlierRstMin(equipment_data_field_name_2)
                                    outlier_rst_max_2 = s3_parquet_df.outlierRstMax(equipment_data_field_name_2)

                                    if outlier_rst_min_2 < outlier_rst_max_2:
                                        sample_df = \
                                            s3_parquet_df.reprSample.loc[
                                                s3_parquet_df.reprSample[equipment_data_field_name].between(
                                                    outlier_rst_min,
                                                    outlier_rst_max,
                                                    inclusive=True) &
                                                s3_parquet_df.reprSample[equipment_data_field_name_2].between(
                                                    outlier_rst_min_2,
                                                    outlier_rst_max_2,
                                                    inclusive=True),
                                                [equipment_data_field_name, equipment_data_field_name_2]]

                                        if len(sample_df) > 1:
                                            outlier_rst_min = float(sample_df[equipment_data_field_name].min())
                                            outlier_rst_max = float(sample_df[equipment_data_field_name].max())

                                            if outlier_rst_min < outlier_rst_max:
                                                outlier_rst_min_2 = float(sample_df[equipment_data_field_name_2].min())
                                                outlier_rst_max_2 = float(sample_df[equipment_data_field_name_2].max())

                                                if outlier_rst_min_2 < outlier_rst_max_2:
                                                    sample_correlation = \
                                                        pearsonr(
                                                            x=sample_df[equipment_data_field_name],
                                                            y=sample_df[equipment_data_field_name_2])[0]

                                                    if pandas.notnull(sample_correlation):
                                                        self.data.EquipmentUniqueTypeGroupDataFieldPairwiseCorrelations.bulk_create(
                                                            [EquipmentUniqueTypeGroupDataFieldPairwiseCorrelation(
                                                                equipment_unique_type_group=equipment_unique_type_group,
                                                                equipment_data_field=equipment_data_field,
                                                                equipment_data_field_2=equipment_data_field_2,
                                                                sample_correlation=sample_correlation),
                                                             EquipmentUniqueTypeGroupDataFieldPairwiseCorrelation(
                                                                equipment_unique_type_group=equipment_unique_type_group,
                                                                equipment_data_field=equipment_data_field_2,
                                                                equipment_data_field_2=equipment_data_field,
                                                                sample_correlation=sample_correlation)])

    def recommend_auto_included_ppp_input_equipment_data_fields(
            self,
            equipment_general_type_name,
            equipment_unique_type_group_name,
            absolute_correlation_lower_threshold=.2,
            absolute_correlation_upper_threshold=.9):
        equipment_unique_type_group = \
            self.data.EquipmentUniqueTypeGroups.get(
                equipment_general_type__name=equipment_general_type_name,
                name=equipment_unique_type_group_name)

        equipment_unique_type_group_service_config = \
            self.data.EquipmentUniqueTypeGroupPredMaintServiceConfigs.get(
                equipment_unique_type_group=equipment_unique_type_group)

        equipment_unique_type_group_data_field_pairwise_correlations = \
            self.data.EquipmentUniqueTypeGroupDataFieldPairwiseCorrelations.filter(
                equipment_unique_type_group=equipment_unique_type_group)

        for equipment_unique_type_group_monitored_data_field_config in \
                tqdm.tqdm(equipment_unique_type_group_service_config.equipment_unique_type_group_monitored_data_field_configs.all()):
            _equipment_unique_type_group_data_field_pairwise_correlations = \
                equipment_unique_type_group_data_field_pairwise_correlations.filter(
                    equipment_data_field=equipment_unique_type_group_monitored_data_field_config.monitored_equipment_data_field)

            equipment_unique_type_group_monitored_data_field_config.highly_correlated_numeric_equipment_data_fields = \
                [(i['equipment_data_field_2__name'], i['sample_correlation'])
                 for i in
                    sorted(
                        _equipment_unique_type_group_data_field_pairwise_correlations
                            .exclude(sample_correlation__range=(-absolute_correlation_upper_threshold, absolute_correlation_upper_threshold))
                            .values('equipment_data_field_2__name', 'sample_correlation'),
                        key=lambda i: abs(i['sample_correlation']),
                        reverse=True)]

            equipment_unique_type_group_monitored_data_field_config.auto_included_numeric_equipment_data_fields = \
                [(i['equipment_data_field_2__name'], i['sample_correlation'])
                 for i in
                    sorted(
                        _equipment_unique_type_group_data_field_pairwise_correlations
                            .filter(sample_correlation__gte=-absolute_correlation_upper_threshold)
                            .filter(sample_correlation__lte=absolute_correlation_upper_threshold)
                            .exclude(sample_correlation__range=(-absolute_correlation_lower_threshold, absolute_correlation_lower_threshold))
                            .values('equipment_data_field_2__name', 'sample_correlation'),
                        key=lambda i: abs(i['sample_correlation']),
                        reverse=True)]

            equipment_unique_type_group_monitored_data_field_config.lowly_correlated_numeric_equipment_data_fields = \
                [(i['equipment_data_field_2__name'], i['sample_correlation'])
                 for i in
                    sorted(
                        _equipment_unique_type_group_data_field_pairwise_correlations
                            .filter(sample_correlation__range=(-absolute_correlation_lower_threshold, absolute_correlation_lower_threshold))
                            .values('equipment_data_field_2__name', 'sample_correlation'),
                        key=lambda i: abs(i['sample_correlation']),
                        reverse=True)]

            equipment_unique_type_group_monitored_data_field_config.save()

    def _train_val_s3_parquet_df(
            self,
            equipment_general_type_name,
            equipment_unique_type_group_name,
            to_month,
            verbose=True):
        equipment_unique_type_group_data_set_name = \
            '{}---{}'.format(
                equipment_general_type_name.upper(),
                equipment_unique_type_group_name)

        from_date = \
            str((datetime.datetime.strptime('{}-01'.format(to_month), '%Y-%m-%d') -
                 relativedelta(months=self.REF_N_MONTHS - 1)).date())

        from_month = from_date[:7]

        equipment_unique_type_group_train_val_data_set_name = \
            '{}---from-{}---to-{}---TrainVal'.format(
                equipment_unique_type_group_data_set_name,
                from_month, to_month)

        try:
            train_val_s3_parquet_df = \
                S3ParquetDataFeeder(
                    path=os.path.join(
                            self.params.s3.equipment_data.train_val_benchmark_dir_path,
                            equipment_unique_type_group_train_val_data_set_name + _PARQUET_EXT),
                    aws_access_key_id=self.params.s3.access_key_id,
                    aws_secret_access_key=self.params.s3.secret_access_key,
                    iCol=None,
                    tCol=self._DATE_TIME_COL_NAME,
                    verbose=verbose)

        except:
            train_val_s3_parquet_df, benchmark_s3_parquet_df = \
                S3ParquetDataFeeder(
                    path=os.path.join(
                            self.params.s3.equipment_data.dir_path,
                            equipment_unique_type_group_data_set_name + _PARQUET_EXT),
                    aws_access_key_id=self.params.s3.access_key_id,
                    aws_secret_access_key=self.params.s3.secret_access_key,
                    iCol=None,
                    tCol=self._DATE_TIME_COL_NAME,
                    verbose=verbose) \
                .filterByPartitionKeys(
                    (DATE_COL,
                     from_date,
                     '{}-31'.format(to_month))) \
                .split(
                    1 - self.BENCHMARK_REF_DATA_PROPORTION,
                    self.BENCHMARK_REF_DATA_PROPORTION)

            train_val_s3_parquet_df.copyToPath(
                path=os.path.join(
                        self.params.s3.equipment_data.train_val_benchmark_dir_path,
                        equipment_unique_type_group_train_val_data_set_name + _PARQUET_EXT))

            benchmark_s3_parquet_df.copyToPath(
                path=os.path.join(
                        self.params.s3.equipment_data.train_val_benchmark_dir_path,
                        '{}---from-{}---to-{}---Benchmark{}'.format(
                            equipment_unique_type_group_data_set_name,
                            from_month, to_month, _PARQUET_EXT)))

        equipment_unique_type_group = \
            self.data.EquipmentUniqueTypeGroups.get(
                equipment_general_type__name=equipment_general_type_name,
                name=equipment_unique_type_group_name)

        for col in train_val_s3_parquet_df.possibleNumContentCols:
            equipment_data_field = \
                equipment_unique_type_group.equipment_data_fields.filter(
                    name=clean_lower_str(col)) \
                .first()

            if equipment_data_field:
                train_val_s3_parquet_df._nulls[col] = \
                    equipment_data_field.lower_numeric_null, \
                    equipment_data_field.upper_numeric_null

        return train_val_s3_parquet_df

    def _benchmark_s3_parquet_ddf(
            self,
            equipment_general_type_name,
            equipment_unique_type_group_name,
            to_month,
            verbose=True):
        return S3ParquetDistributedDataFrame(
                path=os.path.join(
                        self.params.s3.equipment_data.train_val_benchmark_dir_path,
                        '{}---{}---from-{}---to-{}---Benchmark{}'.format(
                            equipment_general_type_name.upper(),
                            equipment_unique_type_group_name,
                            month_str(to_month, n_months_offset=-self.REF_N_MONTHS + 1),
                            to_month,
                            _PARQUET_EXT)),
                aws_access_key_id=self.params.s3.access_key_id,
                aws_secret_access_key=self.params.s3.secret_access_key,
                iCol=None,
                tCol=self._DATE_TIME_COL_NAME,
                verbose=verbose)

    def _ppp_blueprint(
            self, uuid=None, set_uuid=None,
            equipment_general_type_name=None, equipment_unique_type_group_name=None,
            incl_time_features=True, excl_mth_time_features=False,
            __model_params__=
                {'train.n_samples': 248 * 10 ** 6,
                 'train.n_train_samples_per_epoch': 10 ** 6,
                 'train.min_n_val_samples_per_epoch': 10 ** 5,
                 'train.batch_size': 500,
                 'train.val_batch_size': 10 ** 4},
            params={}, **kwargs):
        if uuid:
            if uuid not in self._LOADED_BLUEPRINTS:
                self._LOADED_BLUEPRINTS[uuid] = \
                    load_blueprint(
                        dir_path=os.path.join(self.params.s3.ppp.blueprints_dir_path, uuid),
                        s3_bucket=self.params.s3.bucket,
                        s3_dir_prefix=os.path.join(self.params.s3.ppp.blueprints_dir_prefix, uuid),
                        aws_access_key_id=self.params.s3.access_key_id,
                        aws_secret_access_key=self.params.s3.secret_access_key,
                        s3_client=self.s3_client,
                        verbose=False)

            return self._LOADED_BLUEPRINTS[uuid]

        else:
            equipment_unique_type_group = \
                self.data.EquipmentUniqueTypeGroups.get(
                    equipment_general_type__name=equipment_general_type_name,
                    name=equipment_unique_type_group_name)

            cat_equipment_data_field_names = []
            num_equipment_data_field_names = []

            for equipment_data_field in equipment_unique_type_group.equipment_data_fields.all():
                if equipment_data_field.data_type == self.CAT_DATA_TYPE:
                    cat_equipment_data_field_names.append(equipment_data_field.name)

                elif equipment_data_field.data_type == self.NUM_DATA_TYPE:
                    num_equipment_data_field_names.append(equipment_data_field.name)

            _pred_vars_incl = \
                ([_T_WoM_COL, _T_DoW_COL,
                  _T_DELTA_COL,
                  _T_PoM_COL, _T_PoW_COL, _T_PoD_COL]
                 if excl_mth_time_features
                 else list(_PRED_VARS_INCL_T_AUX_COLS)) \
                if incl_time_features \
                else []

            _pred_vars_excl = \
                list(set(DDF._T_COMPONENT_AUX_COLS)
                     .difference(_pred_vars_incl))

            component_blueprints = {}

            for monitored_measure_numeric_equipment_data_field_name, included_excluded_equipment_data_field_names in \
                    self.params.equipment_monitoring.equipment_unique_type_groups_monitored_and_included_excluded_data_fields[equipment_general_type_name][equipment_unique_type_group_name].items():
                # verify there's a unique Numeric Measurement Equipment Data Field
                _monitored_measure_equipment_data_field = \
                    equipment_unique_type_group.equipment_data_fields.get(
                        equipment_data_field_type__in=
                            (self.MEASURE_EQUIPMENT_DATA_FIELD_TYPE,
                             self.CALC_EQUIPMENT_DATA_FIELD_TYPE),
                        name=monitored_measure_numeric_equipment_data_field_name,
                        data_type=self.NUM_DATA_TYPE)

                component_blueprints[monitored_measure_numeric_equipment_data_field_name] = \
                    cs_regr.DLBlueprint(
                        params=Namespace(
                                data=Namespace(
                                        label=Namespace(
                                            var=monitored_measure_numeric_equipment_data_field_name),
                                        pred_vars=
                                            _pred_vars_incl +
                                            included_excluded_equipment_data_field_names.included,
                                        pred_vars_excl=
                                            _pred_vars_excl +
                                            [monitored_measure_numeric_equipment_data_field_name] +
                                            included_excluded_equipment_data_field_names.excluded,
                                        force_cat=cat_equipment_data_field_names,
                                        force_num=num_equipment_data_field_names)),
                        verbose=False)

            blueprint_params = \
                Namespace(
                    data=Namespace(
                            id_col=self._EQUIPMENT_INSTANCE_ID_COL_NAME,
                            time_col=self._DATE_TIME_COL_NAME,
                            force_cat=cat_equipment_data_field_names,
                            force_num=num_equipment_data_field_names,
                            nulls={equipment_data_field.name: (equipment_data_field.lower_numeric_null, equipment_data_field.upper_numeric_null)
                                   for equipment_data_field in equipment_unique_type_group.equipment_data_fields.all()}),
                    model=Namespace(
                            component_blueprints=component_blueprints),
                    persist=Namespace(
                            s3=Namespace(
                                bucket=self.params.s3.bucket,
                                dir_prefix=self.params.s3.ppp.blueprints_dir_prefix)))

            blueprint_params.update(params)

            return cs_anom.DLPPPBlueprint(
                    uuid=set_uuid,
                    params=blueprint_params, __model_params__=__model_params__,
                    aws_access_key_id=self.params.s3.access_key_id,
                    aws_secret_access_key=self.params.s3.secret_access_key,
                    verbose=False,
                    **kwargs)

    def train_ppp_blueprint(
            self,
            equipment_general_type_name, equipment_unique_type_group_name,
            to_month,
            incl_time_features=True,
            __model_params__=
                {'train.n_samples': 248 * 10 ** 6,
                 'train.n_train_samples_per_epoch': 10 ** 6,
                 'train.min_n_val_samples_per_epoch': 10 ** 5,
                 'train.batch_size': 500,
                 'train.val_batch_size': 10 ** 4},
            params={},
            verbose=True,
            **kwargs):
        self.profile_equipment_data_fields(
            equipment_general_type_name=equipment_general_type_name,
            equipment_unique_type_group_name=equipment_unique_type_group_name,
            to_month=to_month)

        ppp_blueprint_uuid = \
            '{}---{}---to-{}---{}'.format(
                equipment_general_type_name.upper(),
                equipment_unique_type_group_name,
                to_month,
                uuid.uuid4())

        ppp_blueprint = \
            self._ppp_blueprint(
                set_uuid=ppp_blueprint_uuid,
                equipment_general_type_name=equipment_general_type_name,
                equipment_unique_type_group_name=equipment_unique_type_group_name,
                incl_time_features=incl_time_features, excl_mth_time_features=False,
                __model_params__=__model_params__, params=params)

        ppp_blueprint.train(
            df=self._train_val_s3_parquet_df(
                equipment_general_type_name=equipment_general_type_name,
                equipment_unique_type_group_name=equipment_unique_type_group_name,
                to_month=to_month,
                set_i_col=False,
                verbose=verbose),
            verbose=verbose,
            **kwargs)

        if any(component_blueprint_params.model.ver
               for component_blueprint_params in ppp_blueprint.params.model.component_blueprints.values()):
            self.data.PredMaintBlueprints.create(
                uuid=ppp_blueprint_uuid,

                equipment_unique_type_group=
                    self.data.EquipmentUniqueTypeGroups.get(
                        equipment_general_type__name=equipment_general_type_name,
                        name=equipment_unique_type_group_name),

                trained_to_date=month_end(to_month))

        return ppp_blueprint

    def _good_ppp_label_var_names(self, bp_obj, benchmark_metrics=None):
        if not benchmark_metrics:
            benchmark_metrics = bp_obj.benchmark_metrics

        label_var_names = []

        for label_var_name in self.params.equipment_monitoring.equipment_unique_type_groups_monitored_and_included_excluded_data_fields[bp_obj.equipment_unique_type_group.equipment_general_type.name][bp_obj.equipment_unique_type_group.name]:
            benchmark_metrics_for_label_var_name = benchmark_metrics.get(label_var_name)

            if benchmark_metrics_for_label_var_name:
                if AbstractPPPBlueprint._is_good_component_blueprint(
                        label_var_name=label_var_name,
                        benchmark_metrics_for_label_var_name=benchmark_metrics_for_label_var_name,
                        blueprint_obj=bp_obj):
                    label_var_names.append(label_var_name)

            else:
                print('*** {}: {}: NO COMPONENT BLUEPRINT ***'
                    .format(bp_obj.uuid, label_var_name))

        return label_var_names

    def _good_ppp_blueprint(self, bp_obj=None, benchmark_metrics=None):
        if isinstance(bp_obj, (str, unicode)):
            bp_obj = self.data.PredMaintBlueprints.get(uuid=bp_obj)

        if not benchmark_metrics:
            benchmark_metrics = bp_obj.benchmark_metrics

        if benchmark_metrics:
            return len(self._good_ppp_label_var_names(
                        bp_obj=bp_obj,
                        benchmark_metrics=benchmark_metrics)) \
                >= (self.MIN_PROPORTION_OF_GOOD_COMPONENT_BLUEPRINTS *
                    len(self.params.equipment_monitoring.equipment_unique_type_groups_monitored_and_included_excluded_data_fields[bp_obj.equipment_unique_type_group.equipment_general_type.name][bp_obj.equipment_unique_type_group.name]))

    def eval_ppp_blueprint(
            self, uuid,
            sql_filter=None,
            _force_re_eval=False,
            verbose=True):
        ppp_blueprint = self._ppp_blueprint(uuid=uuid)

        _bp_obj = self.data.PredMaintBlueprints.get(uuid=ppp_blueprint.params.uuid)

        benchmark_metrics_exist = 'benchmark_metrics' in ppp_blueprint.params

        if not _force_re_eval:
            assert benchmark_metrics_exist == bool(_bp_obj.benchmark_metrics)

        equipment_general_type_name = _bp_obj.equipment_unique_type_group.equipment_general_type.name
        equipment_unique_type_group_name = _bp_obj.equipment_unique_type_group.name
        to_month = str(_bp_obj.trained_to_date)[:7]

        if _force_re_eval or (not benchmark_metrics_exist):
            benchmark_s3_parquet_ddf = \
                self._benchmark_s3_parquet_ddf(
                    equipment_general_type_name=equipment_general_type_name,
                    equipment_unique_type_group_name=equipment_unique_type_group_name,
                    to_month=to_month,
                    set_i_col=False,
                    verbose=verbose)

            if sql_filter:
                try:
                    benchmark_s3_parquet_ddf.filter(
                        condition=sql_filter,
                        inplace=True)

                except Exception as err:
                    print(err)

            ppp_blueprint.eval(
                df=benchmark_s3_parquet_ddf,
                save=True)

        _bp_obj.benchmark_metrics = benchmark_metrics = \
            ppp_blueprint.params.benchmark_metrics.to_dict()

        _bp_obj.active = active = \
            bool(self._good_ppp_blueprint(
                    bp_obj=_bp_obj,
                    benchmark_metrics=benchmark_metrics))

        _bp_obj.save()

        self.profile_ppp_blueprints(
            equipment_general_type_name=equipment_general_type_name,
            equipment_unique_type_group_name=equipment_unique_type_group_name)

        print('{}{} ({})'.format(uuid, '' if active else ' (*** INACTIVATED ***)'))
        for label_var_name, component_blueprint_params in ppp_blueprint.params.model.component_blueprints.items():
            if component_blueprint_params.model.ver:
                print(label_var_name,
                      ppp_blueprint.params.benchmark_metrics[label_var_name][ppp_blueprint._GLOBAL_EVAL_KEY])

    def profile_ppp_blueprints(self, equipment_general_type_name, equipment_unique_type_group_name):
        equipment_unique_type_group = \
            self.data.EquipmentUniqueTypeGroups.get(
                equipment_general_type__name=equipment_general_type_name,
                name=equipment_unique_type_group_name)

        _active_bp_objs = \
            self.data.PredMaintBlueprints.filter(
                equipment_unique_type_group=equipment_unique_type_group,
                active=True)

        if _active_bp_objs.count():
            for _active_bp_obj in _active_bp_objs:
                if _active_bp_obj.timestamp == \
                        max(_bp_obj.timestamp
                            for _bp_obj in _active_bp_objs.filter(
                                trained_to_date=_active_bp_obj.trained_to_date)):
                    for label_var_name, benchmark_metrics in _active_bp_obj.benchmark_metrics.items():
                        global_benchmark_metrics = benchmark_metrics[AbstractPPPBlueprint._GLOBAL_EVAL_KEY]

                        equipment_unique_type_group_data_field_blueprint_benchmark_metric_profile = \
                            self.data.EquipmentUniqueTypeGroupDataFieldPredMaintBlueprintBenchmarkMetricProfiles.update_or_create(
                                equipment_unique_type_group=equipment_unique_type_group,
                                equipment_data_field=
                                    self.data.EquipmentDataFields.get(
                                        equipment_general_type__name=equipment_general_type_name,
                                        name=label_var_name,
                                        equipment_data_field_type__in=
                                            [self.MEASURE_EQUIPMENT_DATA_FIELD_TYPE,
                                             self.CALC_EQUIPMENT_DATA_FIELD_TYPE,
                                             self.ALARM_EQUIPMENT_DATA_FIELD_TYPE]),
                                trained_to_date=_active_bp_obj.trained_to_date,
                                defaults=dict(n=global_benchmark_metrics['n']))[0]

                        equipment_unique_type_group_data_field_blueprint_benchmark_metric_profile.r2 = global_benchmark_metrics['R2']
                        equipment_unique_type_group_data_field_blueprint_benchmark_metric_profile.mae = global_benchmark_metrics['MAE']
                        equipment_unique_type_group_data_field_blueprint_benchmark_metric_profile.medae = global_benchmark_metrics['MedAE']
                        equipment_unique_type_group_data_field_blueprint_benchmark_metric_profile.rmse = global_benchmark_metrics['RMSE']
                        equipment_unique_type_group_data_field_blueprint_benchmark_metric_profile.save()
    
    def ppp_anom_score(
            self,
            equipment_general_type_name, equipment_unique_type_group_name,
            date, to_date=None, monthly=False,
            _force_calc=False, re_calc_daily=False,
            __batch_size__=10 ** 3,
            sql_filter=None):
        equipment_unique_type_group = \
            self.data.EquipmentUniqueTypeGroups.get(
                equipment_general_type__name=equipment_general_type_name,
                name=equipment_unique_type_group_name)

        equipment_unique_type_group_data_set_name = \
            '{}---{}'.format(
                equipment_general_type_name.upper(),
                equipment_unique_type_group_name)

        active_ppp_blueprints = \
            self.data.PredMaintBlueprints.filter(
                equipment_unique_type_group=equipment_unique_type_group,
                active=True)

        _trained_to_dates = \
            sorted(active_ppp_blueprint.trained_to_date
                   for active_ppp_blueprint in active_ppp_blueprints)

        if _force_calc:
            re_calc_daily = True

        calc_daily_for_dates = set()

        if monthly:
            mth_str = date
            assert len(mth_str) == 7

            if to_date:
                to_mth_str = to_date
                assert len(to_mth_str) == 7 and (to_mth_str > mth_str)

                to_date += '-31'

            else:
                to_mth_str = mth_str

            _mth_str = mth_str

            while _mth_str <= to_mth_str:
                print('*** SCORING {} FOR {} ***'.format(equipment_unique_type_group_data_set_name, _mth_str))

                for i, _trained_to_date in enumerate(_trained_to_dates):
                    if str(_trained_to_date) > _mth_str:
                        if i:
                            _trained_to_date = _trained_to_dates[i - 1]

                        break

                active_ppp_blueprints_train_to_date = active_ppp_blueprints.filter(trained_to_date=_trained_to_date)

                active_ppp_blueprint_train_to_date = \
                    active_ppp_blueprints_train_to_date.get(
                        timestamp=max(bp.timestamp
                                      for bp in active_ppp_blueprints_train_to_date))

                blueprint_uuid = active_ppp_blueprint_train_to_date.uuid

                if 'Contents' in \
                       self.s3_client.list_objects_v2(
                           Bucket=self.params.s3.bucket,
                           Prefix=os.path.join(
                                   self.params.s3.ppp.err_mults_dir_prefix,
                                   'monthly',
                                   equipment_unique_type_group_data_set_name + _PARQUET_EXT,
                                   '{}={}'.format(MONTH_COL, _mth_str),
                                   '{}={}'.format(self._BLUEPRINT_UUID_COL, blueprint_uuid))):
                    if re_calc_daily:
                        calc_daily_for_dates.update(
                            (_mth_str + '-{:02d}'.format(d))
                            for d in range(1, 32))

                        if _force_calc:
                            _to_calc = True

                            s3_parquet_ddf = \
                                self.load_equipment_data(
                                    equipment_unique_type_group_data_set_name,
                                    spark=True, set_i_col=False) \
                                .filterByPartitionKeys(
                                    (DATE_COL,
                                     _mth_str + '-01',
                                     _mth_str + '-31'))

                        else:
                            _to_calc = False

                    else:
                        _to_calc = False
                        
                else:
                    try:
                        s3_parquet_ddf = \
                            self.load_equipment_data(
                                equipment_unique_type_group_data_set_name,
                                spark=True, set_i_col=False) \
                            .filterByPartitionKeys(
                                (DATE_COL,
                                 _mth_str + '-01',
                                 _mth_str + '-31'))

                        _to_calc = True

                    except Exception as err:
                        print('*** NO DATA FOR "{}" IN {}: {} ***'.format(
                                equipment_unique_type_group_data_set_name, _mth_str, err))

                        _to_calc = False

                if _to_calc:
                    ppp_blueprint = self._ppp_blueprint(uuid=blueprint_uuid)

                    if sql_filter:
                        try:
                            s3_parquet_ddf.filter(
                                condition=sql_filter,
                                inplace=True)

                        except Exception as err:
                            print(err)

                    ppp_blueprint.err_mults(
                        ppp_blueprint.score(
                            df=s3_parquet_ddf,
                            __batch_size__=__batch_size__),
                        *self._good_ppp_label_var_names(bp_obj=active_ppp_blueprint_train_to_date),
                        max_indiv_ref_benchmark_metric_over_global_ref_benchmark_metric_ratio=
                            self.MAX_INDIV_REF_BENCHMARK_METRIC_OVER_GLOBAL_REF_BENCHMARK_METRIC_RATIO
                        ).withColumn(
                            colName=self._BLUEPRINT_UUID_COL,
                            col=functions.lit(blueprint_uuid)
                        ).save(
                            path=os.path.join(
                                    's3://{}/{}/monthly'.format(
                                        self.params.s3.bucket,
                                        self.params.s3.ppp.err_mults_dir_prefix),
                                    equipment_unique_type_group_data_set_name + _PARQUET_EXT,
                                    '{}={}'.format(MONTH_COL, _mth_str)),
                            format='parquet',
                            partitionBy=(self._BLUEPRINT_UUID_COL, DATE_COL),
                            aws_access_key_id=self.params.s3.access_key_id,
                            aws_secret_access_key=self.params.s3.secret_access_key,
                            verbose=True)

                    calc_daily_for_dates.update(
                        (_mth_str + '-{:02d}'.format(d))
                        for d in range(1, 32))

                _mth_str = month_str(_mth_str, n_months_offset=1)

        else:
            if to_date:
                assert (len(to_date) == 10) and (to_date > date)

            else:
                to_date = date

            blueprints_to_calc_for_dates = {}

            for _date in tqdm.tqdm(pandas.date_range(start=date, end=to_date).date):
                for i, _trained_to_date in enumerate(_trained_to_dates):
                    if _trained_to_date >= _date:
                        if i:
                            _trained_to_date = _trained_to_dates[i - 1]

                        break

                active_ppp_blueprints_train_to_date = active_ppp_blueprints.filter(trained_to_date=_trained_to_date)

                active_ppp_blueprint_train_to_date = \
                    active_ppp_blueprints_train_to_date.get(
                        timestamp=max(bp.timestamp
                                      for bp in active_ppp_blueprints_train_to_date))

                blueprint_uuid = active_ppp_blueprint_train_to_date.uuid

                if 'Contents' in \
                       self.s3_client.list_objects_v2(
                           Bucket=self.params.s3.bucket,
                           Prefix=os.path.join(
                                   self.params.s3.ppp.err_mults_dir_prefix,
                                   'daily',
                                   equipment_unique_type_group_data_set_name + _PARQUET_EXT,
                                   '{}={}'.format(DATE_COL, _date),
                                   '{}={}'.format(self._BLUEPRINT_UUID_COL, blueprint_uuid))):
                    if re_calc_daily:
                        calc_daily_for_dates.add(_date)

                        if _force_calc:
                            if active_ppp_blueprint_train_to_date in blueprints_to_calc_for_dates:
                                blueprints_to_calc_for_dates[active_ppp_blueprint_train_to_date].append(_date)
                            else:
                                blueprints_to_calc_for_dates[active_ppp_blueprint_train_to_date] = [_date]

                else:
                    try:
                        # load to make sure the equipment data does exist properly
                        s3_parquet_ddf = \
                            self.load_equipment_data(
                                equipment_unique_type_group_data_set_name,
                                spark=True, set_i_col=False) \
                            .filterByPartitionKeys(
                                (DATE_COL,
                                 _date))

                        if active_ppp_blueprint_train_to_date in blueprints_to_calc_for_dates:
                            blueprints_to_calc_for_dates[active_ppp_blueprint_train_to_date].append(_date)
                        else:
                            blueprints_to_calc_for_dates[active_ppp_blueprint_train_to_date] = [_date]

                    except Exception as err:
                        print('*** NO DATA FOR {} ON {}: {} ***'.format(
                                equipment_unique_type_group_data_set_name, _date, err))

            if blueprints_to_calc_for_dates:
                print('*** SCORING "{}" BY {} ***'.format(
                        equipment_unique_type_group_data_set_name, blueprints_to_calc_for_dates))

                err_mults_s3_dir_path = \
                    os.path.join(
                        's3://{}/{}/daily'.format(
                            self.params.s3.bucket,
                            self.params.s3.ppp.err_mults_dir_prefix),
                        equipment_unique_type_group_data_set_name + _PARQUET_EXT)

                for bp_obj, dates in blueprints_to_calc_for_dates.items():
                    blueprint_uuid = bp_obj.uuid

                    ppp_blueprint = self._ppp_blueprint(uuid=blueprint_uuid)

                    s3_parquet_ddf = \
                        self.load_equipment_data(
                            equipment_unique_type_group_data_set_name,
                            spark=True, set_i_col=False) \
                        .filterByPartitionKeys(
                            (DATE_COL,
                             dates))

                    if sql_filter:
                        try:
                            s3_parquet_ddf.filter(
                                condition=sql_filter,
                                inplace=True)

                        except Exception as err:
                            print(err)

                    _tmp_dir_path = tempfile.mkdtemp()

                    ppp_blueprint.err_mults(
                        ppp_blueprint.score(
                            df=s3_parquet_ddf,
                            __batch_size__=__batch_size__),
                        *self._good_ppp_label_var_names(bp_obj=bp_obj),
                        max_indiv_ref_benchmark_metric_over_global_ref_benchmark_metric_ratio=
                            self.MAX_INDIV_REF_BENCHMARK_METRIC_OVER_GLOBAL_REF_BENCHMARK_METRIC_RATIO
                        ).withColumn(
                            colName=self._BLUEPRINT_UUID_COL,
                            col=functions.lit(blueprint_uuid)
                        ).save(
                            path=_tmp_dir_path,
                            format='parquet',
                            partitionBy=(DATE_COL, self._BLUEPRINT_UUID_COL),
                            verbose=True)

                    if fs._ON_LINUX_CLUSTER_WITH_HDFS:
                        fs.get(
                            from_hdfs=_tmp_dir_path,
                            to_local=_tmp_dir_path,
                            is_dir=True, overwrite=True, _mv=True,
                            must_succeed=True)

                    for partition_key in \
                            tqdm.tqdm(sorted(
                                partition_key
                                for partition_key in os.listdir(_tmp_dir_path)
                                if partition_key.startswith('{}='.format(DATE_COL)))):
                        s3.sync(
                            from_dir_path=
                                os.path.join(
                                    _tmp_dir_path,
                                    partition_key),
                            to_dir_path=
                                os.path.join(
                                    err_mults_s3_dir_path,
                                    partition_key),
                            delete=True, quiet=True,
                            access_key_id=self.params.s3.access_key_id,
                            secret_access_key=self.params.s3.secret_access_key,
                            verbose=False)

                    fs.rm(path=_tmp_dir_path,
                          is_dir=True,
                          hdfs=False)

                    calc_daily_for_dates.update(dates)

        if calc_daily_for_dates:
            copy_anom_scores_from_date = \
                datetime.datetime.strptime(min(calc_daily_for_dates), '%Y-%m-%d').date() \
                if monthly \
                else min(calc_daily_for_dates)

            print('*** AGGREGATING DAILY ERROR MULTIPLES FOR "{}" ON ~{:,} DATES FROM {} TO {} ***'.format(
                    equipment_unique_type_group_data_set_name,
                    len(calc_daily_for_dates), min(calc_daily_for_dates), max(calc_daily_for_dates)))

            err_mults_s3_parquet_ddf = \
                S3ParquetDistributedDataFrame(
                    path=os.path.join(
                            's3://{}/{}/{}'.format(
                                self.params.s3.bucket,
                                self.params.s3.ppp.err_mults_dir_prefix,
                                'monthly' if monthly else 'daily'),
                            equipment_unique_type_group_data_set_name + _PARQUET_EXT),
                    aws_access_key_id=self.params.s3.access_key_id,
                    aws_secret_access_key=self.params.s3.secret_access_key,
                    reCache=True,
                    verbose=True) \
                .filterByPartitionKeys(
                    (DATE_COL,
                     calc_daily_for_dates))

            label_var_names = []
            n_label_var_names = 0

            for label_var_name in self.params.equipment_monitoring.equipment_unique_type_groups_monitored_and_included_excluded_data_fields[equipment_general_type_name][equipment_unique_type_group_name]:
                if 'MAE__{}'.format(label_var_name) in err_mults_s3_parquet_ddf.columns:
                    label_var_names.append(label_var_name)
                    n_label_var_names += 1

            daily_err_mults_s3_parquet_ddf = \
                AbstractPPPBlueprint.daily_err_mults(
                    err_mults_s3_parquet_ddf,
                    *label_var_names,
                    id_col=self._EQUIPMENT_INSTANCE_ID_COL_NAME,
                    time_col=self._DATE_TIME_COL_NAME)

            daily_err_mults_s3_dir_path = \
                os.path.join(
                    's3://{}/{}'.format(
                        self.params.s3.bucket,
                        self.params.s3.ppp.daily_err_mults_dir_prefix),
                    equipment_unique_type_group_data_set_name + _PARQUET_EXT)

            _tmp_dir_path = tempfile.mkdtemp()

            if len(calc_daily_for_dates) > 1:
                daily_err_mults_s3_parquet_ddf \
                .repartition(DATE_COL) \
                .save(
                    path=_tmp_dir_path,
                    format='parquet',
                    partitionBy=DATE_COL,
                    verbose=True)

                # free up Spark resources for other tasks
                arimo.backend.spark.stop()

                if fs._ON_LINUX_CLUSTER_WITH_HDFS:
                    fs.get(
                        from_hdfs=_tmp_dir_path,
                        to_local=_tmp_dir_path,
                        is_dir=True, overwrite=True, _mv=True,
                        must_succeed=True)

                for partition_key in \
                        tqdm.tqdm(sorted(
                            partition_key
                            for partition_key in os.listdir(_tmp_dir_path)
                            if partition_key.startswith('{}='.format(DATE_COL)))):
                    s3.sync(
                        from_dir_path=
                            os.path.join(
                                _tmp_dir_path,
                                partition_key),
                        to_dir_path=
                            os.path.join(
                                daily_err_mults_s3_dir_path,
                                partition_key),
                        delete=True, quiet=True,
                        access_key_id=self.params.s3.access_key_id,
                        secret_access_key=self.params.s3.secret_access_key,
                        verbose=False)

            else:
                daily_err_mults_s3_parquet_ddf \
                .repartition(1) \
                .save(
                    path=os.path.join(
                            daily_err_mults_s3_dir_path,
                            '{}={}'.format(
                                DATE_COL,
                                calc_daily_for_dates.pop())),
                    format='parquet',
                    aws_access_key_id=self.params.s3.access_key_id,
                    aws_secret_access_key=self.params.s3.secret_access_key,
                    verbose=True)

                # free up Spark resources for other tasks
                arimo.backend.spark.stop()

            daily_mean_abs_mae_mult_prefix = \
                AbstractPPPBlueprint._dailyMean_PREFIX + \
                AbstractPPPBlueprint._ABS_PREFIX + \
                AbstractPPPBlueprint._ERR_MULT_PREFIXES['MAE']

            daily_mean_abs_mae_mult_col_names = \
                [(daily_mean_abs_mae_mult_prefix +
                  label_var_name)
                 for label_var_name in label_var_names]

            daily_err_mults_df = \
                S3ParquetDataFeeder(
                    path=daily_err_mults_s3_dir_path,
                    aws_access_key_id=self.params.s3.access_key_id,
                    aws_secret_access_key=self.params.s3.secret_access_key,
                    verbose=True) \
                .collect(
                    self._EQUIPMENT_INSTANCE_ID_COL_NAME,
                    DATE_COL,
                    *daily_mean_abs_mae_mult_col_names)

            overall_anom_score_col_name = \
                self._OVERALL_PPP_ANOM_SCORE_NAME_PREFIX + \
                AbstractPPPBlueprint._dailyMean_PREFIX + \
                AbstractPPPBlueprint._ABS_PREFIX + \
                AbstractPPPBlueprint._ERR_MULT_COLS['MAE']

            daily_err_mults_df[overall_anom_score_col_name] = \
                daily_err_mults_df[daily_mean_abs_mae_mult_col_names].max(
                    axis='columns',
                    skipna=True,
                    level=None,
                    numeric_only=True) \
                if n_label_var_names > 1 \
                else daily_err_mults_df[daily_mean_abs_mae_mult_col_names[0]]

            anom_scores_df = \
                AbstractPPPBlueprint.ewma_daily_err_mults(
                    daily_err_mults_df,
                    overall_anom_score_col_name,
                    *daily_mean_abs_mae_mult_col_names,
                    id_col=self._EQUIPMENT_INSTANCE_ID_COL_NAME)

            anom_scores_parquet_file_name = 'PPPAnomScores' + _PARQUET_EXT

            _tmp_parquet_file_path = \
                os.path.join(
                    _tmp_dir_path,
                    anom_scores_parquet_file_name)

            fs.mkdir(
                dir=_tmp_parquet_file_path,
                hdfs=False)

            anom_scores_df.columns = anom_scores_df.columns.map(str)   # Arrow Parquet columns cannot be Unicode

            n_rows = len(anom_scores_df)

            print('Writing {:,} Rows of Anom Scores to Parquet Files with Columns {}... '
                .format(n_rows, anom_scores_df.columns.tolist()), end='')
            tic = time.time()

            anom_scores_df.to_parquet(
                fname=_tmp_parquet_file_path,
                engine='pyarrow',
                compression='snappy',
                flavor='spark')

            toc = time.time()
            print('done!   <{:,.1f} m>'.format((toc - tic) / 60))

            print('Uploading Anom Scores Parquet Files... ', end='')
            tic = time.time()

            s3.mv(
                from_path=_tmp_parquet_file_path,
                to_path=os.path.join(
                            's3://{}'.format(self.params.s3.bucket),
                            self.params.s3.anom_scores.dir_prefix,
                            equipment_unique_type_group_data_set_name,
                            anom_scores_parquet_file_name),
                is_dir=False,
                quiet=True,
                access_key_id=self.params.s3.access_key_id,
                secret_access_key=self.params.s3.secret_access_key,
                verbose=True)

            toc = time.time()
            print('done!   <{:,.1f} m>'.format((toc - tic) / 60))

            fs.rm(path=_tmp_dir_path,
                  is_dir=True,
                  hdfs=False)

            self.data.EquipmentInstanceDailyRiskScores.filter(
                equipment_unique_type_group=equipment_unique_type_group,
                risk_score_name__contains='__abs__MAE_Mult',   # TODO: fix hacky way of filtering for PPP Anom Scores
                date__gte=copy_anom_scores_from_date) \
            .delete()

            anom_scores_df = anom_scores_df.loc[anom_scores_df[DATE_COL] >= copy_anom_scores_from_date]

            equipment_general_type = self.data.EquipmentGeneralTypes.get(name=equipment_general_type_name)

            equipment_instances = \
                {equipment_instance_id:
                    self.data.EquipmentInstances.get_or_create(
                        equipment_general_type=equipment_general_type,
                        name=clean_lower_str(str(equipment_instance_id)))[0]
                 for equipment_instance_id in tqdm.tqdm(anom_scores_df[self._EQUIPMENT_INSTANCE_ID_COL_NAME].unique())}

            from arimo.IoT.DataAdmin.PredMaint.models import EquipmentInstanceDailyRiskScore

            msg = 'Writing Anom Scores for {} {} to DB...'.format(equipment_general_type_name.upper(), equipment_unique_type_group_name)
            print(msg)
            tic = time.time()

            for i in tqdm.tqdm(range(int(math.ceil(len(anom_scores_df) / self._MAX_N_ROWS_TO_COPY_TO_DB_AT_ONE_TIME)))):
                _anom_scores_df = \
                    anom_scores_df.iloc[
                        (i * self._MAX_N_ROWS_TO_COPY_TO_DB_AT_ONE_TIME):((i + 1) * self._MAX_N_ROWS_TO_COPY_TO_DB_AT_ONE_TIME)]

                self.data.EquipmentInstanceDailyRiskScores.bulk_create(
                    EquipmentInstanceDailyRiskScore(
                        equipment_unique_type_group=equipment_unique_type_group,
                        equipment_instance=equipment_instances[row[self._EQUIPMENT_INSTANCE_ID_COL_NAME]],
                        risk_score_name=risk_score_name,
                        date=row[DATE_COL],
                        risk_score_value=row[risk_score_name])

                    for _, row in tqdm.tqdm(_anom_scores_df.iterrows(), total=len(_anom_scores_df))
                        for risk_score_name in set(row.index).difference((self._EQUIPMENT_INSTANCE_ID_COL_NAME, DATE_COL))
                            if pandas.notnull(row[risk_score_name]))

            toc = time.time()
            print(msg + ' done!   <{:,.1f} m>'.format((toc - tic) / 60))

            date_time = datetime.datetime.utcnow()

            for date in tqdm.tqdm(anom_scores_df[DATE_COL].unique()):
                self.data.EquipmentUniqueTypeGroupRiskScoringTasks.update_or_create(
                    equipment_unique_type_group=equipment_unique_type_group,
                    date=date,
                    defaults=dict(finished=date_time))

    def save_vae_daily_anom_score_to_db(self, s3_path, from_date, to_date, equipment_general_type_name, equipment_unique_type_group_name):
        import pandas as pd
        df_vae_anom_score = pd.read_parquet(s3_path)
        print(df_vae_anom_score.shape)

        anom_scores_df = df_vae_anom_score[(from_date <= df_vae_anom_score[DATE_COL]) & (df_vae_anom_score[DATE_COL] <= to_date)]
        
        equipment_unique_type_group = \
            self.data.EquipmentUniqueTypeGroups.get(
                equipment_general_type__name=equipment_general_type_name,
                name=equipment_unique_type_group_name)

        equipment_general_type = self.data.EquipmentGeneralTypes.get(name=equipment_general_type_name)

        equipment_instances = \
            {equipment_instance_id:
                self.data.EquipmentInstances.get_or_create(
                    equipment_general_type=equipment_general_type,
                    name=clean_lower_str(str(equipment_instance_id)))[0]
             for equipment_instance_id in tqdm.tqdm(anom_scores_df[self._EQUIPMENT_INSTANCE_ID_COL_NAME].unique())}

        from arimo.IoT.DataAdmin.PredMaint.models import EquipmentInstanceDailyRiskScore

        msg = 'Writing Anom Scores into DB...'
        print(msg)
        tic = time.time()

        for i in tqdm.tqdm(range(int(math.ceil(len(anom_scores_df) / self._MAX_N_ROWS_TO_COPY_TO_DB_AT_ONE_TIME)))):
            _anom_scores_df = \
                anom_scores_df.iloc[
                    (i * self._MAX_N_ROWS_TO_COPY_TO_DB_AT_ONE_TIME):((i + 1) * self._MAX_N_ROWS_TO_COPY_TO_DB_AT_ONE_TIME)]

            self.data.EquipmentInstanceDailyRiskScores.bulk_create(
                EquipmentInstanceDailyRiskScore(
                    equipment_unique_type_group=equipment_unique_type_group,
                    equipment_instance=equipment_instances[row[self._EQUIPMENT_INSTANCE_ID_COL_NAME]],
                    risk_score_name=row['risk_score_name'],
                    date=row[DATE_COL],
                    risk_score_value=row['risk_score_value'])
                for _, row in tqdm.tqdm(_anom_scores_df.iterrows(), total=len(_anom_scores_df))
                    for col_name in set(row.index).difference((self._EQUIPMENT_INSTANCE_ID_COL_NAME, DATE_COL))
                        if pandas.notnull(row[col_name]))

    def ppp_anom_alert(
            self,
            equipment_general_type_name, equipment_unique_type_group_name,
            from_date=None, to_date=None,
            _redo=False):
        equipment_unique_type_group = \
            self.data.EquipmentUniqueTypeGroups.get(
                equipment_general_type__name=equipment_general_type_name,
                name=equipment_unique_type_group_name)

        if from_date:
            from_date = \
                datetime.datetime.strptime(
                    (from_date + '-01')
                        if len(from_date) == 7
                        else from_date,
                    '%Y-%m-%d') \
                .date()

        if to_date:
            to_date = \
                month_end(to_date) \
                if len(to_date) == 7 \
                else datetime.datetime.strptime(to_date, '%Y-%m-%d').date()
        
        def update_or_create_anom_alert(
                equipment_instance_id,
                anom_score_name, threshold,
                start_date, end_date, cumulative_excess_risk_score, last_risk_score,
                ppp_monitored_equipment_data_field_cumulative_excess_risk_scores,
                ongoing=False):
            equipment_instance_id = clean_lower_str(str(equipment_instance_id))

            ppp_monitored_equipment_data_field_cumulative_excess_risk_scores = \
                sorted(
                    ppp_monitored_equipment_data_field_cumulative_excess_risk_scores.items(),
                    key=lambda i: -i[1])

            alerts = \
                self.data.PredMaintAlerts.filter(
                    equipment_unique_type_group=equipment_unique_type_group,
                    equipment_instance__name=equipment_instance_id,

                    risk_score_name=anom_score_name,
                    threshold=threshold,

                    date_range__overlap=
                        DateRange(
                            lower=start_date,
                            upper=end_date,
                            bounds='[]',
                            empty=False))

            n_alerts = alerts.count()
    
            if n_alerts:
                alert = alerts.first()

                for _alert in alerts[1:]:
                    _alert.delete()

                if (not from_date) or (alert.from_date >= from_date):
                    alert.from_date = start_date

                if (not to_date) or (alert.to_date <= to_date):
                    alert.to_date = end_date

                alert.ongoing = ongoing

                alert.cumulative_excess_risk_score = cumulative_excess_risk_score
                alert.last_risk_score = last_risk_score

                if ppp_monitored_equipment_data_field_cumulative_excess_risk_scores:
                    alert.info['ppp_monitored_equipment_data_field_cumulative_excess_risk_scores'] = \
                        ppp_monitored_equipment_data_field_cumulative_excess_risk_scores \

                else:
                    alert.info = {}
    
                alert.save()
    
                print('{} (UPDATED)'.format(alert))
    
            else:
                print('{} (CREATED)'.format(
                    self.data.PredMaintAlerts.create(
                        equipment_unique_type_group=equipment_unique_type_group,

                        equipment_instance=
                            self.data.EquipmentInstances.get(
                                equipment_general_type__name=equipment_general_type_name,
                                name=equipment_instance_id),

                        risk_score_name=anom_score_name,
                        threshold=threshold,

                        from_date=start_date,
                        to_date=end_date,
                        ongoing=ongoing,

                        cumulative_excess_risk_score=cumulative_excess_risk_score,
                        last_risk_score=last_risk_score,

                        info=
                            dict(ppp_monitored_equipment_data_field_cumulative_excess_risk_scores=
                                    ppp_monitored_equipment_data_field_cumulative_excess_risk_scores)
                            if ppp_monitored_equipment_data_field_cumulative_excess_risk_scores
                            else {})))

        equipment_unique_type_group_data_set_name = \
            '{}---{}'.format(
                equipment_general_type_name.upper(),
                equipment_unique_type_group_name)

        if _redo:
            print('*** DELETING EXISTING ANOM ALERTS FOR {}: {} ***'.format(
                    equipment_unique_type_group_data_set_name,
                    self.data.PredMaintAlerts.filter(equipment_unique_type_group=equipment_unique_type_group).delete()))

        ppp_anom_scores_s3_parquet_df = \
            S3ParquetDataFeeder(
                path='s3://{}/{}/{}/PPPAnomScores{}'.format(
                        self.params.s3.bucket,
                        self.params.s3.anom_scores.dir_prefix,
                        equipment_unique_type_group_data_set_name,
                        _PARQUET_EXT),
                aws_access_key_id=self.params.s3.access_key_id,
                aws_secret_access_key=self.params.s3.secret_access_key,
                verbose=True)

        ppp_anom_scores_df = ppp_anom_scores_s3_parquet_df.collect()

        try:
            ppp_anom_scores_df[DATE_COL] = \
                ppp_anom_scores_df[DATE_COL].dt.date
            
        except:
            ppp_anom_scores_df[DATE_COL] = \
                pandas.to_datetime(
                    arg=ppp_anom_scores_df[DATE_COL],
                    errors='raise',
                    dayfirst=False,
                    yearfirst=True,
                    utc=None,
                    box=True,
                    format='%Y-%m-%d',
                    exact=True,
                    unit=None,   # cannot specify both format and unit
                    infer_datetime_format=False,
                    origin='unix',
                    cache=False
                ).dt.date

        if from_date or to_date:
            ppp_anom_scores_df = ppp_anom_scores_df.loc[
                ((ppp_anom_scores_df[DATE_COL] >= from_date) if from_date else True) &
                ((ppp_anom_scores_df[DATE_COL] <= to_date) if to_date else True)]

        ppp_anom_scores_df = \
            ppp_anom_scores_df.sort_values(
                by=[self._EQUIPMENT_INSTANCE_ID_COL_NAME, DATE_COL],
                axis='index',
                ascending=True,
                inplace=False,
                kind='quicksort',
                na_position='last') \
            .reset_index(
                level=None,
                drop=True,
                inplace=False,
                col_level=0,
                col_fill='')

        n_rows = len(ppp_anom_scores_df)

        anom_score_names_and_thresholds = {}

        for anom_score_name, thresholds in self.params.equipment_monitoring.anom_score_names_and_thresholds.items():
            if thresholds:
                anom_score_names_and_thresholds[self._DEFAULT_EWMA_ALPHA_PREFIX + anom_score_name] = \
                    anom_score_names_and_thresholds[anom_score_name] = thresholds

        current_equipment_instance_id = None

        ppp_monitored_equipment_data_field_anom_score_name_prefixes_and_prefix_lengths = {}

        for i, row in ppp_anom_scores_df.iterrows():
            equipment_instance_id = row[self._EQUIPMENT_INSTANCE_ID_COL_NAME]
            date = row[DATE_COL]

            if equipment_instance_id != current_equipment_instance_id:
                if i:
                    for anom_score_name in unfinished_anomalies:
                        for threshold, unfinished_anomaly in unfinished_anomalies[anom_score_name].items():
                            if unfinished_anomaly.start_date and unfinished_anomaly.end_date and unfinished_anomaly.cumulative_excess_risk_score:
                                update_or_create_anom_alert(
                                    equipment_instance_id=current_equipment_instance_id,

                                    anom_score_name=anom_score_name,
                                    threshold=threshold,

                                    start_date=unfinished_anomaly.start_date,
                                    end_date=unfinished_anomaly.end_date,
                                    ongoing=True,

                                    cumulative_excess_risk_score=unfinished_anomaly.cumulative_excess_risk_score,
                                    last_risk_score=unfinished_anomaly.last_risk_score,

                                    ppp_monitored_equipment_data_field_cumulative_excess_risk_scores=
                                        unfinished_anomaly.ppp_monitored_equipment_data_field_cumulative_excess_risk_scores)

                unfinished_anomalies = \
                    {anom_score_name:
                        {threshold:
                            Namespace(
                                start_date=None,
                                end_date=None,
                                cumulative_excess_risk_score=0,
                                ppp_monitored_equipment_data_field_cumulative_excess_risk_scores={},
                                last_risk_score=0)
                         for threshold in thresholds}
                     for anom_score_name, thresholds in anom_score_names_and_thresholds.items()}

                current_equipment_instance_id = equipment_instance_id

            for anom_score_name, thresholds in anom_score_names_and_thresholds.items():
                if anom_score_name in ppp_monitored_equipment_data_field_anom_score_name_prefixes_and_prefix_lengths:
                    ppp_monitored_equipment_data_field_anom_score_name_prefix, \
                    ppp_monitored_equipment_data_field_anom_score_name_prefix_len = \
                        ppp_monitored_equipment_data_field_anom_score_name_prefixes_and_prefix_lengths[anom_score_name]

                else:
                    ppp_monitored_equipment_data_field_anom_score_name_prefix = \
                        (self._DEFAULT_EWMA_ALPHA_PREFIX +
                         anom_score_name[(self._DEFAULT_EWMA_ALPHA_PREFIX_LEN + self._OVERALL_PPP_ANOM_SCORE_NAME_PREFIX_LEN):] + '__') \
                        if anom_score_name.startswith(self._DEFAULT_EWMA_ALPHA_PREFIX) \
                        else (anom_score_name[self._OVERALL_PPP_ANOM_SCORE_NAME_PREFIX_LEN:] + '__')

                    ppp_monitored_equipment_data_field_anom_score_name_prefix_len = \
                        len(ppp_monitored_equipment_data_field_anom_score_name_prefix)

                    ppp_monitored_equipment_data_field_anom_score_name_prefixes_and_prefix_lengths[anom_score_name] = \
                        ppp_monitored_equipment_data_field_anom_score_name_prefix, \
                        ppp_monitored_equipment_data_field_anom_score_name_prefix_len

                anom_score = row[anom_score_name]

                for threshold in thresholds:
                    unfinished_anomaly = unfinished_anomalies[anom_score_name][threshold]

                    if anom_score > threshold:
                        if unfinished_anomaly.start_date is None:
                            unfinished_anomaly.start_date = date

                        unfinished_anomaly.end_date = date

                        unfinished_anomaly.cumulative_excess_risk_score += (anom_score - threshold)

                        unfinished_anomaly.last_risk_score = anom_score

                        for k, v in row.items():
                            if k.startswith(ppp_monitored_equipment_data_field_anom_score_name_prefix) \
                                    and (v > threshold):
                                ppp_monitored_equipment_data_field_name = \
                                    k[ppp_monitored_equipment_data_field_anom_score_name_prefix_len:]

                                if ppp_monitored_equipment_data_field_name in unfinished_anomaly.ppp_monitored_equipment_data_field_cumulative_excess_risk_scores:
                                    unfinished_anomaly.ppp_monitored_equipment_data_field_cumulative_excess_risk_scores[ppp_monitored_equipment_data_field_name] += (v - threshold)
                                else:
                                    unfinished_anomaly.ppp_monitored_equipment_data_field_cumulative_excess_risk_scores[ppp_monitored_equipment_data_field_name] = (v - threshold)

                    elif pandas.notnull(anom_score) and \
                            unfinished_anomaly.start_date and unfinished_anomaly.end_date and \
                            unfinished_anomaly.cumulative_excess_risk_score:
                        update_or_create_anom_alert(
                            equipment_instance_id=current_equipment_instance_id,

                            anom_score_name=anom_score_name,
                            threshold=threshold,

                            start_date=unfinished_anomaly.start_date,
                            end_date=unfinished_anomaly.end_date,
                            ongoing=False,
                                
                            cumulative_excess_risk_score=unfinished_anomaly.cumulative_excess_risk_score,
                            last_risk_score=unfinished_anomaly.last_risk_score,

                            ppp_monitored_equipment_data_field_cumulative_excess_risk_scores=
                                unfinished_anomaly.ppp_monitored_equipment_data_field_cumulative_excess_risk_scores)

                        unfinished_anomaly.start_date = unfinished_anomaly.end_date = None
                        unfinished_anomaly.cumulative_excess_risk_score = unfinished_anomaly.last_risk_score = 0
                        unfinished_anomaly.ppp_monitored_equipment_data_field_cumulative_excess_risk_scores = {}

            if i == (n_rows - 1):
                for anom_score_name in unfinished_anomalies:
                    for threshold, unfinished_anomaly in unfinished_anomalies[anom_score_name].items():
                        if unfinished_anomaly.start_date and unfinished_anomaly.end_date and unfinished_anomaly.cumulative_excess_risk_score:
                            update_or_create_anom_alert(
                                equipment_instance_id=current_equipment_instance_id,

                                anom_score_name=anom_score_name,
                                threshold=threshold,

                                start_date=unfinished_anomaly.start_date,
                                end_date=unfinished_anomaly.end_date,
                                ongoing=True,

                                cumulative_excess_risk_score=unfinished_anomaly.cumulative_excess_risk_score,
                                last_risk_score=unfinished_anomaly.last_risk_score,

                                ppp_monitored_equipment_data_field_cumulative_excess_risk_scores=
                                    unfinished_anomaly.ppp_monitored_equipment_data_field_cumulative_excess_risk_scores)

    def agg_daily_equipment_data(
            self,
            equipment_general_type_name, equipment_unique_type_group_name,
            date, to_date=None, monthly=False, _force_re_agg=False, _force_re_insert_to_db=False):
        equipment_unique_type_group_data_set_name = \
            '{}---{}'.format(
                equipment_general_type_name.upper(),
                equipment_unique_type_group_name)

        equipment_unique_type_group_s3_parquet_ddf = \
            self.load_equipment_data(
                equipment_unique_type_group_data_set_name,
                spark=True, set_i_col=False, set_t_col=False)

        s3_dir_prefix = \
            os.path.join(
                self.params.s3.equipment_data.daily_agg_dir_prefix,
                equipment_unique_type_group_data_set_name + _PARQUET_EXT)

        s3_dir_path = \
            os.path.join(
                self.params.s3.equipment_data.daily_agg_dir_path,
                equipment_unique_type_group_data_set_name + _PARQUET_EXT)

        copy_agg_daily_equipment_data_to_db_for_dates = []

        if monthly:
            mth_str = date
            assert len(mth_str) == 7

            if to_date:
                to_mth_str = to_date
                assert len(to_mth_str) == 7 and (to_mth_str > mth_str)

                to_date += '-31'

            else:
                to_mth_str = mth_str

            _mth_str = mth_str

            while _mth_str <= to_mth_str:
                print('*** AGGREGATING "{}" DATA FOR {} ***'
                    .format(equipment_unique_type_group_data_set_name, _mth_str))

                try:
                    _equipment_unique_type_group_s3_parquet_ddf = \
                        equipment_unique_type_group_s3_parquet_ddf.filterByPartitionKeys(
                            (DATE_COL,
                             _mth_str + '-01',
                             _mth_str + '-31'))

                except Exception as err:
                    print('*** NO DATA FOR "{}" IN {}: {} ***'
                        .format(equipment_unique_type_group_data_set_name, _mth_str, err))

                    _mth_str = month_str(_mth_str, n_months_offset=1)

                    continue

                agg_col_strs = []

                for col in set(_equipment_unique_type_group_s3_parquet_ddf.possibleFeatureContentCols).difference((DATE_COL, self._EQUIPMENT_INSTANCE_ID_COL_NAME, self._DATE_TIME_COL_NAME)):
                    if _equipment_unique_type_group_s3_parquet_ddf.typeIsNum(col):
                        agg_col_strs += \
                            ["COUNT(IF(STRING(`{0}`) = 'NaN', NULL, `{0}`)) AS {0}__dailyCount".format(col),
                             'MIN(`{0}`) AS {0}__dailyMin'.format(col),
                             'PERCENTILE_APPROX(`{0}`, 0.05) AS {0}__dailyOutlierRstMin'.format(col),
                             'PERCENTILE_APPROX(`{0}`, 0.25) AS {0}__dailyQuartile'.format(col),
                             'PERCENTILE_APPROX(`{0}`, 0.5) AS {0}__dailyMedian'.format(col),
                             'AVG(`{0}`) AS {0}__dailyMean'.format(col),
                             'PERCENTILE_APPROX(`{0}`, 0.75) AS {0}__daily3rdQuartile'.format(col),
                             'PERCENTILE_APPROX(`{0}`, 0.95) AS {0}__dailyOutlierRstMax'.format(col),
                             'MAX(`{0}`) AS {0}__dailyMax'.format(col)]

                    if to_date:
                        repr_sample_equipment_unique_type_group_s3_parquet_ddf = \
                            equipment_unique_type_group_s3_parquet_ddf.reprSample

                        n_distinct_values = \
                            len((equipment_unique_type_group_s3_parquet_ddf
                                 if col in repr_sample_equipment_unique_type_group_s3_parquet_ddf.columns
                                 else _equipment_unique_type_group_s3_parquet_ddf).distinct(col))

                    else:
                        n_distinct_values = \
                            len(_equipment_unique_type_group_s3_parquet_ddf.distinct(col))

                    if n_distinct_values <= self._MAX_N_DISTINCT_VALUES_TO_PROFILE:
                        agg_col_strs.append(
                            "COLLECT_LIST(IF(STRING(`{0}`) = 'NaN', NULL, {1})) AS {0}__dailyList"
                                .format(
                                    col,
                                    'INT(`{}`)'.format(col)   # *** Arrow can't yet convert List of Bool to Pandas ***
                                        if _equipment_unique_type_group_s3_parquet_ddf.type(col) == _BOOL_TYPE
                                        else '`{}`'.format(col)))

                _tmp_dir_path = tempfile.mkdtemp()

                _equipment_unique_type_group_s3_parquet_ddf(
                    'SELECT \
                        {0}, \
                        {1}, \
                        {2} \
                    FROM \
                        this \
                    GROUP BY \
                        {0}, \
                        {1}'.format(
                        self._EQUIPMENT_INSTANCE_ID_COL_NAME,
                        DATE_COL,
                        ', '.join(agg_col_strs))) \
                .save(
                    path=_tmp_dir_path,
                    format='parquet',
                    partitionBy=DATE_COL,
                    verbose=True)

                if fs._ON_LINUX_CLUSTER_WITH_HDFS:
                    fs.get(
                        from_hdfs=_tmp_dir_path,
                        to_local=_tmp_dir_path,
                        is_dir=True, overwrite=True, _mv=True,
                        must_succeed=True)

                for partition_key in \
                        tqdm.tqdm(sorted(
                            partition_key
                            for partition_key in os.listdir(_tmp_dir_path)
                            if partition_key.startswith('{}='.format(DATE_COL)))):
                    s3.sync(
                        from_dir_path=
                            os.path.join(
                                _tmp_dir_path,
                                partition_key),
                        to_dir_path=
                            os.path.join(
                                s3_dir_path,
                                partition_key),
                        delete=True, quiet=True,
                        access_key_id=self.params.s3.access_key_id,
                        secret_access_key=self.params.s3.secret_access_key,
                        verbose=False)

                fs.rm(path=_tmp_dir_path,
                      is_dir=True,
                      hdfs=False)

                copy_agg_daily_equipment_data_to_db_for_dates += \
                    pandas.date_range(start=_mth_str + '-01', end=month_end(_mth_str)).date.tolist()

                _mth_str = month_str(_mth_str, n_months_offset=1)

        else:
            if to_date:
                assert (len(to_date) == 10) and (to_date > date)

            else:
                to_date = date

            for _date in tqdm.tqdm(pandas.date_range(start=date, end=to_date).date):
                if (not _force_re_agg) and \
                        ('Contents' in
                            self.s3_client.list_objects_v2(
                                Bucket=self.params.s3.bucket,
                                Prefix=os.path.join(
                                        s3_dir_prefix,
                                        '{}={}'.format(DATE_COL, _date)))):
                    if _force_re_insert_to_db:
                        copy_agg_daily_equipment_data_to_db_for_dates.append(_date)
                            
                    continue

                print('*** AGGREGATING "{}" DATA FOR {} ***'
                    .format(equipment_unique_type_group_data_set_name, _date))

                try:
                    _equipment_unique_type_group_s3_parquet_ddf = \
                        equipment_unique_type_group_s3_parquet_ddf.filterByPartitionKeys(
                            (DATE_COL,
                             _date))

                except Exception as err:
                    print('*** NO DATA FOR "{}" IN {}: {} ***'
                        .format(equipment_unique_type_group_data_set_name, _date, err))

                    continue

                agg_col_strs = []

                for col in set(_equipment_unique_type_group_s3_parquet_ddf.possibleFeatureContentCols).difference((DATE_COL, self._EQUIPMENT_INSTANCE_ID_COL_NAME, self._DATE_TIME_COL_NAME)):
                    if _equipment_unique_type_group_s3_parquet_ddf.typeIsNum(col):
                        agg_col_strs += \
                            ["COUNT(IF(STRING(`{0}`) = 'NaN', NULL, `{0}`)) AS {0}__dailyCount".format(col),
                             'MIN(`{0}`) AS {0}__dailyMin'.format(col),
                             'PERCENTILE_APPROX(`{0}`, 0.05) AS {0}__dailyOutlierRstMin'.format(col),
                             'PERCENTILE_APPROX(`{0}`, 0.25) AS {0}__dailyQuartile'.format(col),
                             'PERCENTILE_APPROX(`{0}`, 0.5) AS {0}__dailyMedian'.format(col),
                             'AVG(`{0}`) AS {0}__dailyMean'.format(col),
                             'PERCENTILE_APPROX(`{0}`, 0.75) AS {0}__daily3rdQuartile'.format(col),
                             'PERCENTILE_APPROX(`{0}`, 0.95) AS {0}__dailyOutlierRstMax'.format(col),
                             'MAX(`{0}`) AS {0}__dailyMax'.format(col)]

                    if to_date > date:
                        repr_sample_equipment_unique_type_group_s3_parquet_ddf = \
                            equipment_unique_type_group_s3_parquet_ddf.reprSample

                        n_distinct_values = \
                            len((equipment_unique_type_group_s3_parquet_ddf
                                 if col in repr_sample_equipment_unique_type_group_s3_parquet_ddf.columns
                                 else _equipment_unique_type_group_s3_parquet_ddf).distinct(col))

                    else:
                        n_distinct_values = \
                            len(_equipment_unique_type_group_s3_parquet_ddf.distinct(col))

                    if n_distinct_values <= self._MAX_N_DISTINCT_VALUES_TO_PROFILE:
                        agg_col_strs.append(
                            "COLLECT_LIST(IF(STRING(`{0}`) = 'NaN', NULL, {1})) AS {0}__dailyList"
                                .format(
                                    col,
                                    'INT(`{}`)'.format(col)   # *** Arrow can't yet convert List of Bool to Pandas ***
                                        if _equipment_unique_type_group_s3_parquet_ddf.type(col) == _BOOL_TYPE
                                        else '`{}`'.format(col)))

                _equipment_unique_type_group_s3_parquet_ddf(
                    'SELECT \
                        {0}, \
                        {1} \
                    FROM \
                        this \
                    GROUP BY \
                        {0}'.format(
                        self._EQUIPMENT_INSTANCE_ID_COL_NAME,
                        ', '.join(agg_col_strs))) \
                .repartition(1) \
                .save(
                    path=os.path.join(
                            s3_dir_path,
                            '{}={}'.format(DATE_COL, _date)),
                    aws_access_key_id=self.params.s3.access_key_id,
                    aws_secret_access_key=self.params.s3.secret_access_key,
                    format='parquet',
                    verbose=True)

                copy_agg_daily_equipment_data_to_db_for_dates.append(_date)

        if copy_agg_daily_equipment_data_to_db_for_dates:
            # free up Spark resources for other tasks
            arimo.backend.spark.stop()

            equipment_unique_type_group_s3_parquet_df = \
                self.load_equipment_data(
                    equipment_unique_type_group_data_set_name,
                    spark=False, set_i_col=False, set_t_col=False) \
                .filterByPartitionKeys(
                    (DATE_COL,
                     copy_agg_daily_equipment_data_to_db_for_dates))

            equipment_unique_type_group_daily_agg_s3_parquet_df = \
                S3ParquetDataFeeder(
                    path=s3_dir_path,
                    aws_access_key_id=self.params.s3.access_key_id,
                    aws_secret_access_key=self.params.s3.secret_access_key,
                    reCache=True,
                    verbose=True) \
                .filterByPartitionKeys(
                    (DATE_COL,
                     copy_agg_daily_equipment_data_to_db_for_dates))

            equipment_general_type = self.data.EquipmentGeneralTypes.get(name=equipment_general_type_name)

            equipment_instances = \
                {equipment_instance_id:
                    self.data.EquipmentInstances.get_or_create(
                        equipment_general_type=equipment_general_type,
                        name=clean_lower_str(str(equipment_instance_id)))[0]
                    for equipment_instance_id in
                        tqdm.tqdm(
                            numpy.unique(
                                equipment_unique_type_group_s3_parquet_df.map(mapper=lambda pandas_df: pandas_df[self._EQUIPMENT_INSTANCE_ID_COL_NAME].unique())
                                .collect(self._EQUIPMENT_INSTANCE_ID_COL_NAME, reducer=numpy.hstack)))}

            self.data.EquipmentInstanceDataFieldDailyAggs.filter(
                equipment_instance__in=equipment_instances.values(),
                date__in=copy_agg_daily_equipment_data_to_db_for_dates) \
            .delete()

            from arimo.IoT.DataAdmin.base.models import EquipmentInstanceDataFieldDailyAgg

            equipment_unique_type_group = \
                self.data.EquipmentUniqueTypeGroups.get(
                    equipment_general_type__name=equipment_general_type_name,
                    name=equipment_unique_type_group_name)

            assert equipment_unique_type_group.equipment_data_fields.count(), \
                '*** {} HAS NO DATA FIELDS ***'.format(equipment_unique_type_group)

            for equipment_unique_type_group_daily_agg_df in \
                    tqdm.tqdm(iter(equipment_unique_type_group_daily_agg_s3_parquet_df),
                              total=equipment_unique_type_group_daily_agg_s3_parquet_df.nPieces):
                date = equipment_unique_type_group_daily_agg_df[DATE_COL].iloc[0]

                for i in tqdm.tqdm(range(int(math.ceil(len(equipment_unique_type_group_daily_agg_df) / self._MAX_N_ROWS_TO_COPY_TO_DB_AT_ONE_TIME)))):
                    _equipment_unique_type_group_daily_agg_df = \
                        equipment_unique_type_group_daily_agg_df.iloc[
                            (i * self._MAX_N_ROWS_TO_COPY_TO_DB_AT_ONE_TIME):((i + 1) * self._MAX_N_ROWS_TO_COPY_TO_DB_AT_ONE_TIME)]

                    equipment_instance_data_field_daily_aggs = []

                    for _, row in \
                            tqdm.tqdm(
                                _equipment_unique_type_group_daily_agg_df.iterrows(),
                                total=len(_equipment_unique_type_group_daily_agg_df)):
                        for equipment_data_field in equipment_unique_type_group.equipment_data_fields.all():
                            equipment_data_field_name = equipment_data_field.name

                            if equipment_data_field_name in equipment_unique_type_group_s3_parquet_df.possibleFeatureContentCols:
                                daily_count_col_name = '{}__dailyCount'.format(equipment_data_field_name)

                                if daily_count_col_name in row.index:
                                    daily_count = row[daily_count_col_name]

                                    if pandas.notnull(daily_count) and daily_count:
                                        equipment_instance_data_field_daily_agg = \
                                            EquipmentInstanceDataFieldDailyAgg(
                                                equipment_instance=equipment_instances[row[self._EQUIPMENT_INSTANCE_ID_COL_NAME]],
                                                equipment_data_field=equipment_data_field,
                                                date=date,
                                                daily_count=daily_count)

                                        if equipment_unique_type_group_s3_parquet_df.typeIsNum(equipment_data_field.name):
                                            equipment_instance_data_field_daily_agg.daily_min = \
                                                row['{}__dailyMin'.format(equipment_data_field_name)]

                                            equipment_instance_data_field_daily_agg.daily_outlier_rst_min = \
                                                row['{}__dailyOutlierRstMin'.format(equipment_data_field_name)]

                                            equipment_instance_data_field_daily_agg.daily_quartile = \
                                                row['{}__dailyQuartile'.format(equipment_data_field_name)]

                                            equipment_instance_data_field_daily_agg.daily_median = \
                                                row['{}__dailyMedian'.format(equipment_data_field_name)]

                                            equipment_instance_data_field_daily_agg.daily_mean = \
                                                row['{}__dailyMean'.format(equipment_data_field_name)]

                                            equipment_instance_data_field_daily_agg.daily_3rd_quartile = \
                                                row['{}__daily3rdQuartile'.format(equipment_data_field_name)]

                                            equipment_instance_data_field_daily_agg.daily_outlier_rst_max = \
                                                row['{}__dailyOutlierRstMax'.format(equipment_data_field_name)]

                                            equipment_instance_data_field_daily_agg.daily_max = \
                                                row['{}__dailyMax'.format(equipment_data_field_name)]

                                        daily_list_col = '{}__dailyList'.format(equipment_data_field_name)

                                        if daily_list_col in row.index:
                                            equipment_instance_data_field_daily_agg.daily_distinct_value_counts = \
                                                {str(k): v   # PostgreSQL JSON keys must be strings
                                                 for k, v in Counter(row[daily_list_col]).items()}

                                        equipment_instance_data_field_daily_aggs.append(equipment_instance_data_field_daily_agg)

                    self.data.EquipmentInstanceDataFieldDailyAggs.bulk_create(equipment_instance_data_field_daily_aggs)


def project(name, download_config_file=True):
    local_project_config_file_name = name + _YAML_EXT

    local_project_config_file_path = \
        os.path.join(
            Project.CONFIG_LOCAL_DIR_PATH,
            local_project_config_file_name)

    if download_config_file:
        if not os.path.isdir(Project.CONFIG_LOCAL_DIR_PATH):
            fs.mkdir(
                dir=Project.CONFIG_LOCAL_DIR_PATH,
                hdfs=False)

        print('Downloading "s3://{}/{}" to "{}"... '
              .format(Project.CONFIG_S3_BUCKET, local_project_config_file_name, local_project_config_file_path),
              end='')

        key, secret = key_pair(profile=Project.AWS_PROFILE_NAME)

        s3.client(
            access_key_id=key,
            secret_access_key=secret) \
        .download_file(
            Bucket=Project.CONFIG_S3_BUCKET,
            Key=local_project_config_file_name,
            Filename=local_project_config_file_path)

        print('done!')

    return Project(
            params=yaml.safe_load(
                    open(local_project_config_file_path, 'r')))
