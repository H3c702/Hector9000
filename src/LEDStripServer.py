import LEDStripAPI
import paho.mqtt.client as mqtt
import time

from LEDStripConnector import LEDStripConnector as LEDStrip

MQTT_Server = "localhost"
port = 1883
MainTopic = "Hector9000/LED/"


def debugOut(message):
    print("LED_Strip_Server: => " + message)

def on_message(client, userdata, msg):
    topic = msg.topic
    topic = topic.replace(MainTopic, "")
    if topic is "standart":
        args = tuple(msg.payload.split(","))
        if msg.payload is "":
            pixels.standart()
        elif len(args) == 1:
            pixels.standart(type=args[0])
        elif len(args) == 2:
            pixels.standart(type=args[0], color=tuple(map(int, args[1].split(";"))))
        else:
            debugOut("Error to many args for standart")
    elif topic is "standby":
        args = tuple(msg.payload.split(","))
        if msg.payload is "":
            pixels.standby()
        elif len(args) == 1:
            pixels.standby(type=args[0])
        elif len(args) == 2:
            pixels.standby(type=args[0], color=tuple(map(int, args[1].split(";"))))
        else:
            debugOut("Error to many args for standart")
    elif topic is "dose":
        args = tuple(msg.payload.split(","))
        if msg.payload is "":
            pixels.dosedrink()
        elif len(args) == 1:
            pixels.dosedrink(type=args[0])
        elif len(args) == 2:
            pixels.dosedrink(type=args[0], color=tuple(map(int, args[1].split(";"))))
        else:
            debugOut("Error to many args for standart")
    elif topic is "finish":
        args = tuple(msg.payload.split(","))
        if msg.payload is "":
            pixels.finish()
        elif len(args) == 1:
            pixels.finish(type=args[0])
        elif len(args) == 2:
            pixels.finish(type=args[0], color=tuple(map(int, args[1].split(";"))))
        else:
            debugOut("Error to many args for standart")
    else:
        debugOut("Unknown topic")


def on_connect(client, userdata, flags, rc):
    client.subscribe(MainTopic + "#")

pixels = LEDStrip()
client = mqtt.Client()
client.on_message = on_message
client.on_connect = on_connect
client = client.connect(MQTT_Server, port, 60)
client.loop_start()
while True:
    pixels.led_loop()
