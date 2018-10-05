HECTOR 9000 - Hardware
======================

RasPi-GPIO einrichten:

sudo apt-get update && sudo apt-get install python-dev && sudo apt-get install python-rpi.gpio 

bzw. für python3 entsprechend


Waage:	HX711 (Load Cell Amplifier)

	DAT	-> BCM6 = Pin 31
	CLK	-> BCM5 = Pin 29
	eigenes serielles Protokoll, nicht I²C


PWM:	Adafruit 16-Channel 12-bit PWM/Servo Driver - I2C interface - PCA9685

	SDA -> BCM2 = Pin 3
	SCL -> BCM3 = Pin 5
	per I²C
			-> angeschlossene Kanäle: 
				00..11	= Servos für Dosierer,
				12		= Finger,
				13		= Rundumleuchte

https://tutorials-raspberrypi.de/mehrere-servo-motoren-steuern-raspberry-pi-pca9685/

https://raw.githubusercontent.com/adafruit/Adafruit_Python_PCA9685/master/examples/simpletest.py


Arm:	Pololu A4988 (Motor Driver)

	/ENABLE
	MS1
	MS2
	MS3
	/RESET
	/SLEEP
	STEP	mit 10kΩ-Widerstand
	DIR
	eigenes Interface. Minimum: STEP und DIR; für Microstepping MS1..3
	5V oder 3V3 möglich, für Pi-Betrieb 3V3.


Arm-Lichtschranke:

	GPIO-In


Luftpumpen-Relais:

	GPIO-Out


WS2812:		zwei Streifen, links und rechts. 
	
	Die ersten 15 LEDs sind jeweils fürs "Untergeschoss", die nächsten 30 für die Dosieranlage oben.
			
	DIN A = links
	DIN B = rechts



Development on not Pi-mashine :

	If you are on a not RaspberryPi you can set the Var in Hectorhardware.py 

	devenvirement = True

	If you are in Production or dev direct on a Pi you can set this var to False.