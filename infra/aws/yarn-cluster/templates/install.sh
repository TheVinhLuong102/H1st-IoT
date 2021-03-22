#!/bin/bash

# ${cluster_version}

set -e

sudo mkdir -m 0777 /opt/h1st

TARGET_USER=ubuntu
INSTALLER_VERSION=${installer_version}
CONFIG_LOCATION=${config_file}

sudo chown $TARGET_USER:$TARGET_USER /opt/h1st

# extra python dependencies
sudo pip install boto3 jinja2
sudo pip install -U pyyaml

(
    cd /opt/h1st
    aws s3 cp s3://h1st-bai/installer/$INSTALLER_VERSION/h1st_installer.run .
    chmod 0777 h1st_installer.run
    aws s3 cp $CONFIG_LOCATION config.yaml

    sudo --user $TARGET_USER ./h1st_installer.run install --debug
)
