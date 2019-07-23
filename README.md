# Arimo IoT Data Admin

Arimo's framework for managing IoT equipment data


## Deployment

Sync config files from `arimo-iot-pm` S3 bucket down to `~/.arimo/IoT/`.

The names of the YAML config files are the Project Names.

Have an `[arimo]` profile with a key pair set up in `~/.aws/credentials`. 

Install elasticbeanstalk cli (eb) from this [repo](https://github.com/aws/aws-elastic-beanstalk-cli-setup). You can install directly using `ebcli_installer.py` instead of `bundled_installer`.

Run `bin/deploy <Project-Name>` from repo's root dir.
