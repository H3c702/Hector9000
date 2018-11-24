import sys
import time
import json
from HectorConfig import config
from HectorHardware import HectorHardware

import paho.mqtt.client as mqtt

TopicPrefix = "test/"


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

    client.subscribe(TopicPrefix + "#")


def on_message(client, userdata, msg):
    if msg.topic == TopicPrefix + "ring":
        ring(msg.payload)
    else:
        print(msg.topic + " " + str(msg.payload))


def ring(x):
    print(x)


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("10.1.12.10 ", 1883, 60)

client.loop_forever()
