#!/bin/bash

# ${cluster_version}

set -e

sudo mkdir -m 0777 /opt/arimo

TARGET_USER=ubuntu
INSTALLER_VERSION=${installer_version}
CONFIG_LOCATION=${config_file}

sudo chown $TARGET_USER:$TARGET_USER /opt/arimo

# extra python dependencies
sudo pip install boto3 jinja2
sudo pip install -U pyyaml

(
    cd /opt/arimo
    aws s3 cp s3://arimo-bai/installer/$INSTALLER_VERSION/arimo_installer.run .
    chmod 0777 arimo_installer.run
    aws s3 cp $CONFIG_LOCATION config.yaml

    sudo --user $TARGET_USER ./arimo_installer.run install --debug
)
