#!/usr/bin/env bash

apt update
apt upgrade -y

apt install python3 pip3 python3-setuptools mosquitto -y

# install KIVY
sudo apt-get install libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev \
   pkg-config libgl1-mesa-dev libgles2-mesa-dev \
   python-setuptools libgstreamer1.0-dev git-core \
   gstreamer1.0-plugins-{bad,base,good,ugly} \
   gstreamer1.0-{omx,alsa} python-dev libmtdev-dev \
   xclip xsel -y


pip3 install -r requirements.txt
