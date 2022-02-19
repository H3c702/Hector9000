#!/usr/bin/env bash

echo "-----------------------------------------------------------------------"
echo " _   _  _____  _____  _____  _____ ______   _____  _____  _____  _____"
echo "| | | ||  ___|/  __ \|_   _||  _  || ___ \ |  _  ||  _  ||  _  ||  _  |"
echo "| |_| || |__  | /  \/  | |  | | | || |_/ / | |_| || |/' || |/' || |/' |"
echo "|  _  ||  __| | |      | |  | | | ||    /  \____ ||  /| ||  /| ||  /| |"
echo "| | | || |___ | \__/\  | |  \ \_/ /| |\ \  .___/ /\ |_/ /\ |_/ /\ |_/ /"
echo "\_| |_/\____/  \____/  \_/   \___/ \_| \_| \____/  \___/  \___/  \___/"
echo "-----------------------------------------------------------------------"


echo "Start Hector-Server and Cntroller"
nohup python3 Hector9000/HectorServer.py > Server.out 2>&1 &
nohup python3 Hector9000/HectorController.py > Controller.out 2>&1 &

echo "Start HectorLED-Server"
nohup sudo python3 Hector9000/LEDStripServer.py > /dev/null 2>&1 &
