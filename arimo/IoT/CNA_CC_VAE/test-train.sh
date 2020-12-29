export TFRECORDS_PREFIX=s3://arimo-panasonic-ap-cn-cc-pm/.arimo/PredMaint/VAE/Preprocessed/TFRecords
export CHECKPOINT_PREFIX=s3://arimo-panasonic-ap-cn-cc-pm/.arimo/PredMaint/VAE/checkpoints
python vae_train.py group_1
