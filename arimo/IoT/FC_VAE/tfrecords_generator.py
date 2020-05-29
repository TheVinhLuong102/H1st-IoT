import argparse
import glob
import json
import pandas as pd
import os
import numpy as np
import ast
# from os.path import join, dirname
import boto3

import pyspark
from pyspark.sql.functions import mean, min, stddev, abs
from pyspark.sql.types import *
from pyspark.sql import SQLContext
from pyspark.sql import SparkSession
from pyspark.ml.feature import MinMaxScaler
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.feature import StringIndexer
from pyspark.ml.feature import OneHotEncoderEstimator
from pyspark.ml import PipelineModel
from pyspark.sql.functions import date_format
from pyspark.ml import Pipeline
from pyspark_dist_explore import hist
import matplotlib.pyplot as plt


###### Fuel Cell ########

default_cols = ['equipment_instance_id','date_time']

air_sensors = ['bb_fan_speed', 
    'bb_fan_operation_amount',
    'bp_inlet_temperature', # float32 good
    'bh_thermocouple_temperature', # float32
    'p_flow_rate',
    'combustion_air_flow_rate',
    'air_blower_operation_amount',
    'stack_current',
    'fc_power_generation_amount',
    'pcs_input_voltage_dc_voltage',
    'conversion'
    ]

gas_sensors = ['br_thermocouple_temperature',
    'fc_power_generation_amount',
    'pcs_input_voltage_dc_voltage',
    'conversion',
    'stack_current',
    'gas_base_pressure',
    'booster_pump_operation_amount',
    'raw_material_flow_rate_fc_unit_consumption_gas',
    'uf']

water_sensors = ['cd_tank_temperature',
    
    'r_circulation_p_operation_amount', # float32
    'r_circulation_p_rotational_speed',
    # int32
    'c_circulation_p_rotational_speed', # int32
    'c_circulation_p_operation_amount', # float32  ### both 
    'fc_inlet_temperature',
    'fc_outlet_temperature',
    'r_tank_th',
    'sys_inlet_temperature',
    'sys_outlet_temperature',
    'fc_unit_heat_recovery_flow_rate',
    'reformed_water_flow_rate', 
    'reforming_water_pump_operation_amount']

all_sensors = [
    'bp_inlet_temperature', # float32 good
    'bh_thermocouple_temperature', # float32
    'br_thermocouple_temperature', # float32
    
    
    'bb_fan_speed', 
    'bb_fan_operation_amount',
    'cd_tank_temperature',
    
    'r_circulation_p_operation_amount', # float32
    'r_circulation_p_rotational_speed',
    # int32
    'c_circulation_p_rotational_speed', # int32
    'c_circulation_p_operation_amount', # float32  ### both 
    'fc_inlet_temperature',
    'fc_outlet_temperature',
    'fc_power_generation_amount',
    'pcs_input_voltage_dc_voltage',
    'p_flow_rate',
    'r_tank_th',
    'sys_inlet_temperature',
    'sys_outlet_temperature',
    'uf',
    'gas_base_pressure',
    'stack_current',
    'booster_pump_operation_amount',
    'raw_material_flow_rate_fc_unit_consumption_gas',
    'reformed_water_flow_rate', 
    'reforming_water_pump_operation_amount' ,
    'combustion_air_flow_rate',
    'air_blower_operation_amount',
    'conversion',
    'fc_unit_heat_recovery_flow_rate',
    'generated_electric_power_command_value_a_v'
]

selected_columns = default_cols + all_sensors
print(len(selected_columns) ,selected_columns)


def get_column_name_with_type(df, col_type):
    return [item[0] for item in df.dtypes if item[1].startswith(col_type)]


def change_integer_into_type(df, col_name, col_type):
    return df.withColumn(col_name+"_temp", 
                         df[col_name].cast(col_type)) \
            .drop(col_name) \
            .withColumnRenamed(col_name+"_temp", col_name)


def get_metadata_json(df, numeric_columns, string_columns):
    df_numeric_info = df.select(numeric_columns).describe().toPandas()
    num_json = {}
    for col in df_numeric_info:
        if col == 'summary':
            continue
        temp = {}
        for key, val in zip(df_numeric_info['summary'].values, df_numeric_info[col].values):
            temp[key] = val
        num_json[col] = temp


        
    indexers = [StringIndexer(inputCol=column, outputCol=column+"_idx").fit(df) 
                for column in string_columns]

    index_json = {}
    for col, idx in zip(string_columns, indexers):
        index_json[col] = idx.labels

    meta_json = {}
    meta_json['numeric'] = num_json
    meta_json['categoric'] = index_json
    return meta_json


def get_metadata_json_test(df, numeric_columns):
    df_numeric_info = df.select(numeric_columns).describe().toPandas()
    num_json = {}
    for col in df_numeric_info:
        if col == 'summary':
            continue
        temp = {}
        for key, val in zip(df_numeric_info['summary'].values, df_numeric_info[col].values):
            temp[key] = val
        num_json[col] = temp

    meta_json = {}
    meta_json['numeric'] = num_json
    return meta_json


def impute_nan_with_outlier(df, imputation_columns, std_multiplier=1.5):
    imputation = {}
    for col in imputation_columns:
        imputation[col] = df.select(min(col)).collect()[0][0] \
                          - std_multiplier*df.select(stddev(col)).collect()[0][0]
    print "=== imputation === "
    print imputation
    
    # fillna_dic = {}
    # for major_null_col in imputation_columns:
    #     fillna_dic[major_null_col] = imputation[major_null_col]
    df = df.fillna(imputation)
    return df, imputation


def get_categoric_to_onehotencoding_stages(categoric_cols):
    # Make the pipeline of stages
    stages = []

    # Indexing and Onehot-Encoding on Categorical Columns 
    categoric_json = {}    
    for categoric_col in categoric_cols:
        stringIndexer = StringIndexer(inputCol = categoric_col, outputCol = categoric_col + '_idx')
        encoder = OneHotEncoderEstimator(inputCols=[stringIndexer.getOutputCol()], outputCols=[categoric_col + "_onehot"])
        stages += [stringIndexer, encoder]    
    return stages


def get_vectorassembler_stage(categoric_cols, numeric_cols):
    assemblerInputs = [c + "_onehot" for c in categoric_cols] + numeric_cols

    print "assemblerInputs:", len(assemblerInputs), assemblerInputs

    assembler_stage = VectorAssembler(inputCols=assemblerInputs, outputCol="features")
    return assembler_stage


def get_minmaxscaler_stage(vector_assembler_output_name, scaled_output_name):
    scaler_stage = MinMaxScaler(inputCol=vector_assembler_output_name, outputCol=scaled_output_name)
    return scaler_stage


def execute_stages_with_pipeline(df, stages, id_column, datetime_column, scaled_output_name, pipeline_save_path):
    pipeline = Pipeline(stages=stages)
    pipeline_model = pipeline.fit(df)
    pipeline_model.write().overwrite().save(pipeline_save_path)
    df = pipeline_model.transform(df)
    return df.select([id_column, datetime_column, scaled_output_name])


def df_transform_with_pipeline(df,id_column, datetime_column, scaled_output_name, pipeline_save_path):
    pipeline_model = PipelineModel.load(pipeline_save_path)
    df = pipeline_model.transform(df)
    return df.select([id_column, datetime_column, scaled_output_name])    


def preprocess_data(data_config, spark_config):
    
    ### 1. Setup pyspark        
    spark = SparkSession.builder.appName('Test_UDF')\
        .config('spark.jars', spark_config['spark_tensorflow_connector_jar_file'])\
        .config('spark.hadoop.fs.s3a.access.key', spark_config['aws_access_key'])\
        .config('spark.hadoop.fs.s3a.secret.key', spark_config['aws_secret_key'])\
        .config('spark.executor.memory', spark_config['executor_memory'])\
        .config('spark.executor.cores', spark_config['executor_cores'])\
        .getOrCreate() 

    ### 2. Load data 
    df = spark.read.option("mergeSchema", "true").parquet(data_config['parquet_data_path_train']).select(data_config['selected_columns'])
    df = change_integer_into_type(df, 'equipment_instance_id', StringType())
#     df.printSchema()

    ### 3. Change numeric into float type
    string_columns = get_column_name_with_type(df, 'string')
    numeric_columns = [x for x in data_config['selected_columns'] if x not in string_columns and x !=data_config['datetime_column']]
    df = change_integer_into_type(df, 'equipment_instance_id', StringType())
    for column in numeric_columns:
        df = change_integer_into_type(df, column, FloatType()) # FloatType DoubleType   
    if data_config['id_column'] in string_columns:
        string_columns.remove(data_config['id_column'])
    ### 4. Impute Major NaN and drop minor NaN
    df, impute_json = impute_nan_with_outlier(df, data_config['impute_columns'])
    ### Drop Minor NaN
    df = df.na.drop()
#     print((df.count(), len(df.columns)))
    ### 5. Sort DF
    df = df.orderBy([data_config['id_column'], data_config['datetime_column']])
    ### 6. Save Meta Data
    meta_json = get_metadata_json(df, numeric_columns, string_columns)
    meta_json['imputation'] = impute_json
    with open(data_config['metadata_json_save_path'], 'w') as outfile:
        json.dump(meta_json, outfile)
    ### 7. Categoric to Onehot-encoding & Normalization of all columns
    categoric_to_onehotencoding_stages = get_categoric_to_onehotencoding_stages(string_columns)
#     print("Finished Categoricals!")
    vectorassembler_stage = get_vectorassembler_stage(string_columns, numeric_columns)
#     print("Finished vectorassembler_stage")
    minmaxscaler_stage = get_minmaxscaler_stage(
        data_config['vector_assembler_output_name'], 
        data_config['scaled_output_name'])
#     print("Finished minmaxscaler_stage")
    stages = categoric_to_onehotencoding_stages + [vectorassembler_stage, minmaxscaler_stage]
    
    df = execute_stages_with_pipeline(df, stages, data_config['id_column'], data_config['datetime_column'], data_config['scaled_output_name'], data_config['pipeline_save_path'])  
#     print("Finished fitting, transforming and saving pipeline model")
    datetime_column = "date_time"
    df = df.withColumn(datetime_column, date_format(datetime_column, 'yyyy-MM-dd HH:mm:ss'))
#     print "=== final output example ==="
#     print df.show(1, truncate=False)
    ### 8. Save output tfrecords
    df.write.format("tfrecords").option("recordType", "Example")\
        .save(data_config['tfrecord_save_path'])

    
data_config = {
    'id_column': 'equipment_instance_id',
    'datetime_column':'date_time',
    'selected_columns': selected_columns,
    'impute_columns': [],
    'vector_assembler_output_name':'features',
    'scaled_output_name': 'scaledFeatures',
    'metadata_json_save_path': './',

    'parquet_data_path': 's3a://arimo-panasonic-ap-jp-fc-pm/.arimo/PredMaint/EquipmentData/lpg_vae_train',
    'tfrecord_save_path': 's3a://arimo-panasonic-ap-jp-fc-pm/.arimo/PredMaint/VAE/Preprocessed/TFRecords/lpg/test_vae_tf2.tfrecords',
    'pipeline_save_path': 's3a://arimo-panasonic-ap-jp-fc-pm/.arimo/PredMaint/VAE/model_pipelines/test_vae_tf2',
}

spark_config = {
    'aws_access_key': '',
    'aws_secret_key': '',
    'spark_tensorflow_connector_jar_file': 'spark-tensorflow-connector_2.11-1.8.0.jar',
    'executor_memory': '16g',
    'executor_cores': '10'
}


if __name__=="__main__":
    preprocess_data(data_config, spark_config)