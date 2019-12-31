
nohup python3 src/main.py &
nohup python3 src/HectorServer.py &
nohup sudo python3 src/LEDStripServer.py &
mosquitto_sub -t "Hector900/#"

