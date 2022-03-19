#!/usr/bin/env bash

################################################################################
# Help                                                                         #
################################################################################
Help()
{
   # Display Help
   echo "Displays some help for the Setupscript."
   echo
   echo "Syntax: [-c|h]"
   echo "options:"
   echo "c     Configure mosquitto"
   echo "h     Print this Help."
   echo
}

################################################################################
################################################################################
# Main program                                                                 #
################################################################################
################################################################################


echo "-----------------------------------------------------------------------"
echo " _   _  _____  _____  _____  _____ ______   _____  _____  _____  _____"
echo "| | | ||  ___|/  __ \|_   _||  _  || ___ \ |  _  ||  _  ||  _  ||  _  |"
echo "| |_| || |__  | /  \/  | |  | | | || |_/ / | |_| || |/' || |/' || |/' |"
echo "|  _  ||  __| | |      | |  | | | ||    /  \____ ||  /| ||  /| ||  /| |"
echo "| | | || |___ | \__/\  | |  \ \_/ /| |\ \  .___/ /\ |_/ /\ |_/ /\ |_/ /"
echo "\_| |_/\____/  \____/  \_/   \___/ \_| \_| \____/  \___/  \___/  \___/"
echo "-----------------------------------------------------------------------"

if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root"
   exit 1
fi

doconfig=0;

while getopts ":c" option; do
   # shellcheck disable=SC2220
   case $option in
      c)
        doconfig=1;
   esac
done



echo "Upgrade System"
apt update
apt upgrade -y

echo "Install needed packages"
apt install python3 -y
apt install pip3 -y
apt install python3-pip -y
apt install python3-setuptools -y
apt install mosquitto -y
apt install nohup -y

# shellcheck disable=SC1073
if [ "$doconfig" = 1 ];
then
  echo "Update mosquitto config"
  systemctl stop mosquitto
  cp /etc/mosquitto/mosquitto.conf /etc/mosquitto/mosquitto.conf.old
  rm /etc/mosquitto/mosquitto.conf
  touch /etc/mosquitto/mosquitto.conf

  # shellcheck disable=SC2129
  echo "listener 1883" >> /etc/mosquitto/mosquitto.conf
  echo 'listener 9001' >> /etc/mosquitto/mosquitto.conf
  echo 'protocol websockets' >> /etc/mosquitto/mosquitto.conf
  echo 'socket_domain ipv4' >> /etc/mosquitto/mosquitto.conf
  echo 'allow_anonymous true' >> /etc/mosquitto/mosquitto.conf

  systemctl start mosquitto
fi

echo "install Hector9000"
#pip install -e .
python setup.py develop
