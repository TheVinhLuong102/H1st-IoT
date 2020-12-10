import json
import os

from vae import PredictiveMaintenanceVAE

refrig_display_sensors = [
    "condensing_pressure",
    "evaporation_pressure",
    "return_gas_temp",
    "30_minutes_accumulated_power_consumption",
    "showcase_temp1_f5",
    "showcase_temp1_f7",
    "showcase_temp1_f9",
    "showcase_temp1_f11",
]

refrig_3_display_sensors = [
    "condensing_pressure",
    "evaporation_pressure",
    "return_gas_temp",
    "showcase_temp1_f5",
    "showcase_temp1_f7",
    "showcase_temp1_f9",
]

group_1_cols = [
    "condensing_pressure",
    "evaporation_pressure",
    "return_gas_temp",
    "30_minutes_accumulated_power_consumption",
    "showcase_temp1_f5",
    "showcase_temp1_f7",
    "showcase_temp1_f9",
]

group_2_cols = [
    "condensing_pressure",
    "evaporation_pressure",
    "return_gas_temp",
    "30_minutes_accumulated_power_consumption",
    "showcase_temp1_f5",
    "showcase_temp1_f7",
    "showcase_temp1_f9",
    "showcase_temp1_f11",
]
### Different Sensor Groups
group_5_cols = [
    "condensing_pressure",
    "evaporation_pressure",
    "30_minutes_accumulated_power_consumption",
    "showcase_temp1_f5",
    "showcase_temp1_f7",
    "showcase_temp1_f9",
    "showcase_temp1_f17",
    "showcase_temp2_f18",
]

selected_columns = group_5_cols
print(selected_columns, len(selected_columns))


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


id_column = "store_name"

if __name__ == "__main__":
    for score_idx in range(0, 200, 200):
        score_param = {
            "model_path": "/tf/tim/cn_ccpm/vae/tf2/chkpoints/group_5/",
            "model_checkpoint": None,
            "result_path": "s3://arimo-panasonic-ap-cn-cc-pm/.arimo/PredMaint/VAE/results/group_5/",
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
            "tfr_path": "/tf/tim/cn_ccpm/data/group_5",
            "columns": 8,
            "interval": 1,
            "column_names": {
                "id_key": id_column,
                "datetime_key": "date_time",
                "feature_key": "scaledFeatures",
                "label_key": "label",
            },
        }

        model_param_json_path = os.path.join(
            score_param["model_path"], "model_param.json"
        )
        with open(model_param_json_path) as json_file:
            model_param = json.load(json_file)

        main(score_param, model_param, tfr_info)
