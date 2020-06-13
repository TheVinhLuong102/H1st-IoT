from vae import PredictiveMaintenanceVAE

import sys


def main(train_param, tfr_info):
    pm_vae = PredictiveMaintenanceVAE(
        input_dim=tfr_info['columns'],
        n_window=train_param['n_window'],
        h_dim=train_param['h_dim'],
        z_dim=train_param['z_dim'],
        n_layer=train_param['n_layer'],
        batch_norm=train_param['batch_norm'],
        alpha=train_param['alpha'],
        n_rank=train_param['n_rank'])

    pm_vae.train(
        input_path=tfr_info['tfr_path'],
        save_path=train_param['save_model_path'],
        tfr_id_key=tfr_info['column_names']['id_key'],
        tfr_datetime_key=tfr_info['column_names']['datetime_key'],
        tfr_feature_key=tfr_info['column_names']['feature_key'],
        pre_fix=tfr_info['tfr_file_prefix'],
        data_cache=train_param['data_cache'],

        n_feature=tfr_info['columns'],
        n_window=train_param['n_window'],
        n_row=tfr_info['rows'],
        batch_size=train_param['batch_size'],

        interval=tfr_info['interval'],

        num_epochs=train_param['num_epochs'],

        beta=train_param['beta'],

        learning_rate_init=train_param['learning_rate_init'],
        learning_rate_decay_epoch=train_param['learning_rate_decay_epoch'],
        learning_rate_decay_rate=train_param['learning_rate_decay_rate'],
        max_to_keep=train_param['max_to_keep'],
        model_saving_interval=train_param['model_saving_interval'],
        summary_step=train_param['summary_step'],
        printing_step=train_param['printing_step'])


INPUT_PREFIX = "s3://arimo-panasonic-ap-jp-fc-pm/.arimo/PredMaint/VAE/preprocessed"
OUTPUT_PREFIX = "s3://arimo-panasonic-ap-jp-fc-pm/.arimo/PredMaint/VAE/checkpoints"


if __name__ == "__main__":
    type_group = sys.argv[1]
    target_date = sys.argv[2] if len(sys.argv) > 2 else "*"

    input_prefix = "%s/FUEL_CELL---%s.tfrecords/date=%s" % (INPUT_PREFIX, type_group, target_date)
    output_prefix = "%s/FUEL_CELL---%s/date=%s" % (OUTPUT_PREFIX, type_group, target_date)

    train_param = {
        "data_cache": True,
        "z_dim": 3,
        "h_dim": 256,
        "n_window": 1,
        "n_layer": 3,
        "batch_norm": True,
        "alpha": 0.1,
        "beta": 100,
        "n_rank": 3,
        "batch_size": 4096,
        "num_epochs": 5,
        "learning_rate_init": 0.00001,
        "learning_rate_decay_epoch": 1,
        "learning_rate_decay_rate": 0.7,
        "max_to_keep": 3,
        "model_saving_interval": 1,
        "summary_step": 1024,
        "printing_step": 1024,
        "save_model_path": output_prefix
    }
    tfr_info = {
        "tfr_file_prefix": "part",
        "rows": None,
        "tfr_path": input_prefix,
        "columns": 9,
        "interval": 1,
        "column_names": {"id_key": "equipment_instance_id", "datetime_key": "date_time",
                         "feature_key": "scaledFeatures", "label_key": "label"}
    }

    main(train_param, tfr_info)
