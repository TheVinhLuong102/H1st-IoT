export TFRECORDS_PREFIX=s3://arimo-panasonic-ap-cn-cc-pm/.arimo/PredMaint/VAE/Preprocessed/TFRecords
export CHECKPOINT_PREFIX=s3://arimo-panasonic-ap-cn-cc-pm/.arimo/PredMaint/VAE/checkpoints
export OUTPUT_PREFIX=s3://arimo-panasonic-ap-cn-cc-pm/.arimo/PredMaint/VAE/results
python vae_score.py group_1
