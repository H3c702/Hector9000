import sys
import time
import json
from HectorConfig import config
from HectorHardware import HectorHardware

import paho.mqtt.client as mqtt

MQTTServer = "localhost"
TopicPrefix = "Hector9000/Main/"

Hector = HectorHardware(config)


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe(TopicPrefix + "#")


def valve_dose(msg):
    ml = str(msg.payload.decode("utf-8"))
    if ml.isdigit():
        Hector.valve_dose(ml)
    else:
        print("Not a numeric message. Cant dose liquid.")
    pass


def clean(msg):
    a = str(msg.payload.decode("utf-8"))
    if a.isdigit():
        pump = a
    else:
        print("Not a numeric message. Cant clean pump")
        pass

    Hector.pump_start()
    Hector.valve_open(pump)
    time.sleep(10)
    times = 0
    while times < 5:
        Hector.valve_open(pump, 0)
        time.sleep(1)
        Hector.valve_open(pump)
        time.sleep(10)
        times += 1
    print("IndexPump: ", pump)
    Hector.valve_open(pump, 0)
    time.sleep(10)
    Hector.pump_stop()
    time.sleep(1)
    pass


def arm_in(msg):
    Hector.arm_in()


def arm_out(msg):
    Hector.arm_out()


def rind(msg):
    timestoring = str(msg.payload.decode("utf-8"))
    if timestoring.isdigit():
        Hector.ping(timestoring)
    else:
        print("Not a numeric message. Cant ring the bell.")


def on_message(client, userdata, msg):
    if msg.topic == TopicPrefix + "ring":
        rind(msg)
    if msg.topic == TopicPrefix + "arm/in":
        arm_in(msg)
    if msg.topic == TopicPrefix + "arm/out":
        arm_out(msg)
    if msg.topic == TopicPrefix + "valvedose":
        valve_dose(msg)
    if msg.topic == TopicPrefix + "cleanMe":
        clean(msg)
    else:
        print(msg.topic + " " + str(msg.payload))


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(MQTTServer, 1883, 60)

client.loop_forever()
