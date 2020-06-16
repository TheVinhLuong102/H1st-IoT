from vae import PredictiveMaintenanceVAE

import json
import os
import sys
import s3fs

s3_fs = s3fs.S3FileSystem()

gas_sensors = ['br_thermocouple_temperature',
               'fc_power_generation_amount',
               'pcs_input_voltage_dc_voltage',
               'conversion',
               'stack_current',
               'gas_base_pressure',
               'booster_pump_operation_amount',
               'raw_material_flow_rate_fc_unit_consumption_gas',
               'uf']

selected_columns = gas_sensors
print(selected_columns, len(selected_columns))


def main(score_param, model_param, tfr_info):
    pm_vae = PredictiveMaintenanceVAE(
        input_dim=tfr_info['columns'],
        n_window=model_param['n_window'],
        h_dim=model_param['h_dim'],
        z_dim=model_param['n_z'],
        n_layer=model_param['n_layer'],
        batch_norm=model_param['batch_norm'],
        alpha=model_param['alpha'],
        n_rank=model_param['n_rank'])

    pm_vae.score(
        selected_columns=score_param['selected_columns'],
        input_path=tfr_info['tfr_path'],
        model_path=score_param['model_path'],
        save_path=score_param['result_path'],
        tfr_id_key=tfr_info['column_names']['id_key'],
        tfr_datetime_key=tfr_info['column_names']['datetime_key'],
        tfr_feature_key=tfr_info['column_names']['feature_key'],
        n_feature=tfr_info['columns'],

        n_window=model_param['n_window'],
        interval=tfr_info['interval'],

        n_row=tfr_info['rows'],
        tfr_score_index=tfr_info['tfr_score_index'],
        pre_fix=tfr_info['tfr_file_prefix'],
        checkpoint=score_param['model_checkpoint'],
        num_sample=score_param['num_sample'],
        batch_size=score_param['batch_size'],
        individual_sensor_prob=score_param['individual_sensor_prob'],
        summary=score_param['summary'])


INPUT_PREFIX = os.environ["INPUT_PREFIX"]
OUTPUT_PREFIX = os.environ.get("OUTPUT_PREFIX", INPUT_PREFIX)
MODEL_VERSION = os.environ.get("MODEL_VERSION", "latest")
N_COLUMNS = int(os.environ.get("N_COLUMNS", 30))


if __name__ == "__main__":
    type_group, target_date = sys.argv[1:]
    tfrecords_prefix = "%s/preprocessed/FUEL_CELL---%s.tfrecords/date=%s" % (INPUT_PREFIX, type_group, target_date)
    model_prefix = "%s/checkpoints/FUEL_CELL---%s/%s" % (INPUT_PREFIX, type_group, MODEL_VERSION)
    output_prefix = "%s/results/FUEL_CELL---%s/date=%s" % (OUTPUT_PREFIX, type_group, target_date)

    for score_idx in range(0, 200, 50):
        score_param = {
            "model_path": model_prefix,
            "model_checkpoint": None,
            "result_path": output_prefix,
            "num_sample": 20,
            "batch_size": 64,
            "selected_columns": selected_columns,
            "individual_sensor_prob": True,
            "summary": True
        }
        tfr_info = {
            "tfr_score_index": [score_idx, score_idx + 50],
            "tfr_file_prefix": "part",
            "rows": None,
            "tfr_path": tfrecords_prefix,
            "columns": N_COLUMNS,
            "interval": 1,
            "column_names": {"id_key": "equipment_instance_id", "datetime_key": "date_time",
                             "feature_key": "scaledFeatures", "label_key": "label"}
        }

        model_param_json_path = os.path.join(score_param['model_path'], 'model_param.json')
        with s3_fs.open(model_param_json_path) as json_file:
            model_param = json.load(json_file)

        main(score_param, model_param, tfr_info)
