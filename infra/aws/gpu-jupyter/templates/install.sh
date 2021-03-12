#!/bin/bash

apt-mark hold `uname -r`
apt-mark hold linux-image-aws

sleep 10

mkdir -p /opt/h1st/data

ebsinit --mount /opt/h1st/data
sudo chown ubuntu:ubuntu -R /opt/h1st/data

has_gpu=$(lspci | grep NV)
if [ ! -z "$has_gpu" ]; then
    runtime="--runtime nvidia"

    nvidia-smi
else
    runtime=""
fi

ldconfig -v

# this is so weird ???
export PATH=/usr/local/cuda:/usr/local/cuda/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin
tf_version=2.0.0-gpu-py3-jupyter

docker run --name jupyter -d -it --restart always --privileged \
    -u $(id -u):$(id -g) \
    -e NVIDIA_REQUIRE_CUDA="cuda>=10" \
    -e JUPYTER_TOKEN=h1stiscool \
    -e PS1="\\W \\$ " \
    -v /opt/h1st/data:/tf \
    -p 80:8888 $runtime \
    tensorflow/tensorflow:$tf_version
