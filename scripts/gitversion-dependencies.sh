#!/bin/bash

# yq
wget https://github.com/mikefarah/yq/releases/download/3.3.2/yq_linux_amd64
mv yq_linux_amd64 yq
chmod +x yq

# GitVersion
wget https://github.com/GitTools/GitVersion/releases/download/5.3.7/gitversion-ubuntu.18.04-x64-5.3.7.tar.gz
tar -zxvf gitversion-ubuntu.18.04-x64-5.3.7.tar.gz
rm gitversion-ubuntu.18.04-x64-5.3.7.tar.gz
chmod +x gitversion
