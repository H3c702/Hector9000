#!/usr/bin/env python3
# -*- coding: utf8 -*-
##
#   HectorServer.py       Hector server with MQTT interface
#


# imports

import time
import traceback

import paho.mqtt.client as mqtt

from conf.HectorConfig import config
# from HectorHardware import HectorHardware as Hector
from HectorSimulator import HectorSimulator as Hector

# settings

MQTTServer = "localhost"
TopicPrefix = "Hector9000/Main/"

# global vars

hector = Hector(config)
currentTopic = ""


## functions

# MQTT callbacks

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe(TopicPrefix + "+")


def on_callback(name, value):
    global currentTopic
    print("=> %s: %d" % (name, value))
    client.publish(currentTopic + "/progress", value)
    client.loop()


def on_log(client, userdata, level, buf):
    print("LOG " + str(level) + ": " + str(userdata) + " -- " + str(buf))


# low-level functions

def do_get_config(msg):
    print("get configuration")
    ret = hector.config
    client.publish(currentTopic + "/return", str(ret))


def do_light_on(msg):
    print("turn on light")
    hector.light_on()
    client.publish(currentTopic + "/return", "ok")


def do_light_off(msg):
    print("turn off light")
    hector.light_off()
    client.publish(currentTopic + "/return", "ok")


def do_arm_out(msg):
    print("drive arm out")
    hector.arm_out(on_callback)
    client.publish(currentTopic + "/return", "ok")


def do_arm_in(msg):
    print("drive arm in")
    hector.arm_in(on_callback)
    client.publish(currentTopic + "/return", "ok")


def do_arm_isInOutPos(msg):
    print("check if arm is in OUT position")
    ret = "1" if hector.arm_isInOutPos else "0"
    client.publish(currentTopic + "/return", ret)


def do_scale_readout(msg):
    print("query scale readout")
    ret = hector.scale_readout()
    client.publish(currentTopic + "/return", str(ret))


def do_scale_tare(msg):
    print("set scale tare")
    hector.scale_tare()
    client.publish(currentTopic + "/return", "ok")


def do_pump_start(msg):
    print("start pump")
    hector.pump_start()
    client.publish(currentTopic + "/return", "ok")


def do_pump_stop(msg):
    print("stop pump")
    hector.pump_stop()
    client.publish(currentTopic + "/return", "ok")


def do_valve_open(msg):
    print("open valve")
    args = str(msg.payload.decode("utf-8")).split(',')
    if not args[0].isdigit():
        return
    index = int(args[0])
    open = 1
    if len(args) == 2:
        if not args[1].isdigit():
            return
        open = int(args[1])
    hector.valve_open(index, open)
    client.publish(currentTopic + "/return", "ok")


def do_valve_close(msg):
    print("close valve")
    arg = str(msg.payload.decode("utf-8"))
    if not arg.isdigit():
        return
    index = int(arg)
    hector.valve_close(index)
    client.publish(currentTopic + "/return", "ok")


def do_valve_dose(msg):
    print("dose valve")
    args = str(msg.payload.decode("utf-8")).split(',')
    if not args[0].isdigit():
        return
    index = int(args[0])
    if len(args) < 2:
        return
    if not args[1].isdigit():
        return
    amount = int(args[1])
    timeout = 30
    if len(args) >= 3:
        if not args[2].isdigit():
            return
        timeout = int(args[2])
    ret = hector.valve_dose(index, amount, timeout, on_callback)
    client.publish(currentTopic + "/return", str(ret))


def do_finger(msg):
    print("set finger position")
    arg = str(msg.payload.decode("utf-8"))
    if arg.isdigit():
        pos = int(arg)
    hector.finger(pos)
    client.publish(currentTopic + "/return", "ok")


def do_ping(msg):
    args = str(msg.payload.decode("utf-8")).split(',')
    if not args[0].isdigit():
        return
    num = int(args[0])
    retract = 1
    if len(args) == 2:
        if not args[1].isdigit():
            return
        retract = int(args[1])
    hector.ping(num, retract, on_callback)
    client.publish(currentTopic + "/return", "ok")


# high-level functions


def ring(msg):
    print("ring the bell")
    timesToRing = str(msg.payload.decode("utf-8"))
    if timesToRing.isdigit():
        hector.ping(int(timesToRing))
        client.publish(currentTopic + "/return", "ok")
    else:
        print("Not a numeric message. Cannot ring the bell.")


def valve_dose(msg):
    doseArgs = str(msg.payload.decode("utf-8")).split(',')
    if doseArgs[0].isdigit() and doseArgs[1].isdigit():
        hector.valve_dose(int(doseArgs[0]), int(doseArgs[1]), cback=on_callback)
        client.publish(currentTopic + "/return", "ok")
    else:
        on_callback("valve_dose", "Not a numeric message. Cant dose liquid.")
    pass


def dry(msg):
    a = str(msg.payload.decode("utf-8"))
    if a.isdigit():
        pump = int(a)
    else:
        print("Not a numeric message. Cannot dry pump")
        return
    print("IndexPump: ", pump)
    hector.valve_open(pump)
    time.sleep(20)
    hector.valve_open(pump, 0)
    # on_callback("dry", 1)
    client.publish(currentTopic + "/return", "ok")


def clean(msg):
    a = str(msg.payload.decode("utf-8"))
    if a.isdigit():
        pump = int(a)
    else:
        on_callback("clean", "Not a numeric message. Cant clean pump")
        return

    hector.pump_start()
    hector.valve_open(pump)
    time.sleep(10)
    times = 0
    while times < 5:
        hector.valve_open(pump, 0)
        time.sleep(1)
        hector.valve_open(pump)
        time.sleep(10)
        times += 1
    print("IndexPump: ", pump)
    hector.valve_open(pump, 0)
    time.sleep(10)
    hector.pump_stop()
    time.sleep(1)
    # on_callback("clean", 1)
    client.publish(currentTopic + "/return", "ok")


def on_message(client, userdata, msg):
    try:
        global currentTopic
        currentTopic = msg.topic

        if msg.topic.endswith("/progress"):
            return  # ignore our own progress messages
        elif msg.topic.endswith("/return"):
            return  # ignore our own return messages

        # low-level
        elif msg.topic == TopicPrefix + "get_config":
            do_get_config(msg)
        elif msg.topic == TopicPrefix + "light_on":
            do_light_on(msg)
        elif msg.topic == TopicPrefix + "light_off":
            do_light_off(msg)
        elif msg.topic == TopicPrefix + "arm_out":
            do_arm_out(msg)
        elif msg.topic == TopicPrefix + "arm_in":
            do_arm_in(msg)
        elif msg.topic == TopicPrefix + "arm_isInOutPos":
            do_arm_isInOutPos(msg)
        elif msg.topic == TopicPrefix + "scale_readout":
            do_scale_readout(msg)
        elif msg.topic == TopicPrefix + "scale_tare":
            do_scale_tare(msg)
        elif msg.topic == TopicPrefix + "pump_start":
            do_pump_start(msg)
        elif msg.topic == TopicPrefix + "pump_stop":
            do_pump_stop(msg)
        elif msg.topic == TopicPrefix + "valve_open":
            do_valve_open(msg)
        elif msg.topic == TopicPrefix + "valve_close":
            do_valve_close(msg)
        elif msg.topic == TopicPrefix + "valve_dose":
            do_valve_dose(msg)
        elif msg.topic == TopicPrefix + "finger":
            do_finger(msg)
        elif msg.topic == TopicPrefix + "ping":
            do_ping(msg)

        # high-level
        elif msg.topic == TopicPrefix + "ring":
            ring(msg)
        elif msg.topic == TopicPrefix + "doseDrink":
            valve_dose(msg)
        elif msg.topic == TopicPrefix + "cleanMe":
            clean(msg)
        elif msg.topic == TopicPrefix + "dryMe":
            dry(msg)

        # unknown
        else:
            print("unknown topic: " + msg.topic + ", msg " + str(msg.payload))

        print("done with msg " + msg.topic + " / " + str(msg.payload))

    except Exception as e:
        print("Error! " + str(e))
        print(traceback.format_exc())


# main program
if __name__ == "__main__":
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.on_log = on_log

    client.connect(MQTTServer, 1883, 60)

    while True:
        client.loop()

# EOF
