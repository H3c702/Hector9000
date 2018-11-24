import sys
import time
import json
from HectorConfig import config
from HectorHardware import HectorHardware

import paho.mqtt.client as mqtt

MQTTServer = "localhost"
TopicPrefix = "Hector9000/"

Hector = HectorHardware(config)


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe(TopicPrefix + "#")


def on_message(client, userdata, msg):
    if msg.topic == TopicPrefix + "ring":
        timestoring = str(msg.payload.decode("utf-8"))
        if timestoring.isdigit():
            ring(timestoring)
        else:
            print("Not a numeric message. Cant ring the bell.")
    else:
        print(msg.topic + " " + str(msg.payload))


def ring(x):
    print(x)


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(MQTTServer, 1883, 60)

client.loop_forever()
