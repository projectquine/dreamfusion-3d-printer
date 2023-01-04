#!/bin/bash

#Install missing pybind11.h file for pytorch
sudo apt-get update && sudo apt-get install pybind11-dev python3-pybind11 jq -y

#Install ngrok
curl -s https://ngrok-agent.s3.amazonaws.com/ngrok.asc | \
      sudo tee /etc/apt/trusted.gpg.d/ngrok.asc >/dev/null && \
      echo "deb https://ngrok-agent.s3.amazonaws.com buster main" | \
      sudo tee /etc/apt/sources.list.d/ngrok.list && \
      sudo apt update && sudo apt install ngrok -y

# Get stable-dreamfusion repo
git clone https://github.com/ashawkey/stable-dreamfusion.git
cd stable-dreamfusion

# Install dreamfusion deps
pip install -r requirements.txt
#install nvdiffrast for exporting textured mesh
pip install git+https://github.com/NVlabs/nvdiffrast/

# Install deps for our repo
cd ..
pip install -r requirements.txt