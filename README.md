# Arimo Predictive Maintenance


## Deployment

Have an `[arimo]` profile with a key pair set up in `~/.aws/credentials`. 

Sync config files from `arimo-iot-pm` S3 bucket down to `~/.arimo/pm/`.
The names of the YAML config files are the Project Names.
We can create new config files in `~/.arimo/pm/` following the same template as those of existing configs.

Install elasticbeanstalk cli (eb) from this [repo](https://github.com/aws/aws-elastic-beanstalk-cli-setup). You can install directly using `ebcli_installer.py` instead of `bundled_installer`.

Run `bin/deploy <Project-Name>` from repo's root dir.
