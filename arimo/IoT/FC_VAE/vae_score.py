from vae import PredictiveMaintenanceVAE

import boto3
import json
import os
import sys
import s3fs

ssm = boto3.client("ssm")
s3_fs = s3fs.S3FileSystem()


def get_parameter(name):
    return ssm.get_parameter(Name=name)["Parameter"]["Value"]


def main(score_param, model_param, tfr_info):
    pm_vae = PredictiveMaintenanceVAE(
        input_dim=tfr_info["columns"],
        n_window=model_param["n_window"],
        h_dim=model_param["h_dim"],
        z_dim=model_param["n_z"],
        n_layer=model_param["n_layer"],
        batch_norm=model_param["batch_norm"],
        alpha=model_param["alpha"],
        n_rank=model_param["n_rank"],
    )

    pm_vae.score(
        selected_columns=score_param["selected_columns"],
        input_path=tfr_info["tfr_path"],
        model_path=score_param["model_path"],
        save_path=score_param["result_path"],
        tfr_id_key=tfr_info["column_names"]["id_key"],
        tfr_datetime_key=tfr_info["column_names"]["datetime_key"],
        tfr_feature_key=tfr_info["column_names"]["feature_key"],
        n_feature=tfr_info["columns"],
        n_window=model_param["n_window"],
        interval=tfr_info["interval"],
        n_row=tfr_info["rows"],
        tfr_score_index=tfr_info["tfr_score_index"],
        pre_fix=tfr_info["tfr_file_prefix"],
        checkpoint=score_param["model_checkpoint"],
        num_sample=score_param["num_sample"],
        batch_size=score_param["batch_size"],
        individual_sensor_prob=score_param["individual_sensor_prob"],
        summary=score_param["summary"],
    )


TFRECORDS_PREFIX = os.environ["TFRECORDS_PREFIX"]
CHECKPOINT_PREFIX = os.environ.get("CHECKPOINT_PREFIX")
OUTPUT_PREFIX = os.environ.get("OUTPUT_PREFIX")
MODEL_VERSION = os.environ.get("MODEL_VERSION", "latest")


if __name__ == "__main__":
    type_group, sensor_group, target_date = sys.argv[1:]

    unique_type_group = "FUEL_CELL---%s" % type_group

    selected_columns = get_parameter("/fuelcell/%s_sensors" % sensor_group).split(",")
    print(selected_columns, len(selected_columns))
    n_columns = len(selected_columns)

    tfrecords_prefix = "%s/%s.tfrecords/date=%s" % (
        TFRECORDS_PREFIX,
        unique_type_group,
        target_date,
    )
    checkpoint_prefix = "%s/%s/%s" % (
        CHECKPOINT_PREFIX,
        unique_type_group,
        MODEL_VERSION,
    )
    output_prefix = "%s/%s/date=%s" % (OUTPUT_PREFIX, unique_type_group, target_date)

    for score_idx in range(0, 200, 200):
        score_param = {
            "model_path": checkpoint_prefix,
            "model_checkpoint": None,
            "result_path": output_prefix,
            "num_sample": 20,
            "batch_size": 64,
            "selected_columns": selected_columns,
            "individual_sensor_prob": True,
            "summary": True,
        }
        tfr_info = {
            "tfr_score_index": [score_idx, score_idx + 200],
            "tfr_file_prefix": "part",
            "rows": None,
            "tfr_path": tfrecords_prefix,
            "columns": n_columns,
            "interval": 1,
            "column_names": {
                "id_key": "equipment_instance_id",
                "datetime_key": "date_time",
                "feature_key": "scaledFeatures",
                "label_key": "label",
            },
        }

        model_param_json_path = os.path.join(
            score_param["model_path"], "model_param.json"
        )
        with s3_fs.open(model_param_json_path) as json_file:
            model_param = json.load(json_file)

        main(score_param, model_param, tfr_info)
