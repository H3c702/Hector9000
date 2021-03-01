#!/usr/bin/env bash

echo "-----------------------------------------------------------------------"
echo " _   _  _____  _____  _____  _____ ______   _____  _____  _____  _____"
echo "| | | ||  ___|/  __ \|_   _||  _  || ___ \ |  _  ||  _  ||  _  ||  _  |"
echo "| |_| || |__  | /  \/  | |  | | | || |_/ / | |_| || |/' || |/' || |/' |"
echo "|  _  ||  __| | |      | |  | | | ||    /  \____ ||  /| ||  /| ||  /| |"
echo "| | | || |___ | \__/\  | |  \ \_/ /| |\ \  .___/ /\ |_/ /\ |_/ /\ |_/ /"
echo "\_| |_/\____/  \____/  \_/   \___/ \_| \_| \____/  \___/  \___/  \___/"
echo "-----------------------------------------------------------------------"

echo "Upgrade System"
apt update
apt upgrade -y

echo "Install needed packages"
apt install python3 pip3 python3-pip python3-setuptools mosquitto nohup -y

echo "install Hector9000"
python3 setup.py install
