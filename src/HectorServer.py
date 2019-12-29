#!/usr/bin/env python3
# -*- coding: utf8 -*-
##
#   HectorServer.py       Hector server with MQTT interface
#

# imports

import time
import traceback
import re

import paho.mqtt.client as mqtt

from conf.HectorConfig import config

#from HectorHardware import HectorHardware as Hector

from HectorSimulator import HectorSimulator as Hector


# global vars


MainTopic = "Hector9000/Hardware/"
MQTTIP = "localhost"
MQTTPORT = 1883
hector = Hector(config)
valve_pattern = re.compile("[0-9]+\,[0-9]+\,[0-9]+")


VERBOSE_LEVEL = "DEBUG"
# DEBUG - Everthing
# NORMAL - Only Errors
# SILENT - Nothing



def log(message):
    if VERBOSE_LEVEL == "DEBUG":
        print("HARDWARE-LOG: " + message)


def error(message):
    if VERBOSE_LEVEL == "DEBUG" or VERBOSE_LEVEL == "NORMAL":
        print("HARDWARE-ERROR: " + message)

# low-level functions


def do_get_config():
    log("get configuration")
    return hector.getConfig()


def do_light_on():
    log("turn on light")
    hector.light_on()


def do_light_off():
    log("turn off light")
    hector.light_off()


def do_arm_out():
    log("drive arm out")
    hector.arm_out()


def do_arm_in():
    log("drive arm in")
    hector.arm_in()


def do_arm_isInOutPos():
    log("check if arm is in OUT position")
    return "1" if hector.arm_isInOutPos else "0"


def do_scale_readout():
    log("query scale readout")
    return hector.scale_readout()


def do_scale_tare():
    log("set scale tare")
    hector.scale_tare()


def do_pump_start():
    log("start pump")
    hector.pump_start()

def do_reset():
    do_pump_stop()
    do_all_valve_close()
    do_arm_in()
    do_light_off()
    do_ping(2, 0)


def do_pump_stop():
    log("stop pump")
    hector.pump_stop()


def do_all_valve_open():
    hector.light_on()
    time.sleep(1)
    hector.arm_in()
    hector.pump_stop()
    for vnum in range(12):
        log("Ventil %d wird geöffnet" % (vnum,))
        time.sleep(1)
        hector.valve_open(vnum)
    hector.light_off()


def do_all_valve_close():
    hector.light_on()
    time.sleep(1)
    hector.arm_in()
    hector.pump_stop()
    for vnum in range(12):
        log("Ventil %d wird geschlossen" % (vnum,))
        time.sleep(1)
        hector.valve_close(vnum)
    hector.light_off()


def do_valve_open(index, open):
    log("open valve")
    hector.valve_open(index, open)


def do_valve_close(index):
    log("close valve")
    hector.valve_close(index)


def do_valve_dose(index, amount, timeout=30):
    print("do_valve_dose")
    log("dose valve")
    return hector.valve_dose(index=index, amount=amount, timeout=timeout)

# not implemented yet
#def do_finger(pos):
#    log("set finger position")
#    hector.finger(pos)


def do_ping(num, retract):
    hector.ping(num, retract)


# high-level functions

def dry(pump):
    log("IndexPump: " + pump)
    hector.valve_open(pump)
    time.sleep(20)
    hector.valve_open(pump, 0)


def clean(pump):
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
    log("IndexPump: ", pump)
    hector.valve_open(pump, 0)
    time.sleep(10)
    hector.pump_stop()
    time.sleep(1)

def on_message(client, userdata, msg):
    print("Server: on_message: " + str(msg.topic) + "," + str(msg.payload))
    topic = str(msg.topic)
    if (topic.endswith("return") or topic.endswith("progress")):
        return
    topic = topic.replace(MainTopic, "")
    if topic == "get_config":
        res = do_get_config()
        client.publish(MainTopic + topic + "/return", res)
    elif topic == "light_on":
        do_light_on()
    elif topic == "light_off":
        do_light_off()
    elif topic == "reset":
        do_reset()
    elif topic == "arm_out":
        do_arm_out()
    elif topic == "arm_in":
        do_arm_in()
    elif topic == "arm_position":
        res = do_arm_isInOutPos()
        client.publish(MainTopic + topic + "/return", res)
    elif topic == "scale_readout":
        res = do_scale_readout()
        client.publish(MainTopic + topic + "/return", res)
    elif topic == "scale_tare":
        do_scale_tare()
    elif topic == "pump_stop":
        do_pump_stop()
    elif topic == "pump_start":
        do_pump_start()
    elif topic == "all_valve_open":
        do_all_valve_open()
    elif topic == "all_valve_close":
        do_all_valve_close()
    elif topic == "valve_open":
        if not msg.payload.decode("utf-8").isnumeric():
            error("Wrong payload in valve open")
            return
        do_valve_open(int(msg.payload.decode("utf-8")))
    elif topic == "valve_close":
        if not msg.payload.decode("utf-8").isnumeric():
            error("Wrong payload in valve close")
            return
        do_valve_close(int(msg.payload.decode("utf-8")))
    elif topic == "ping":
        if not msg.payload.decode("utf-8").isnumeric():
            print("error in ping")
            error("Wrong payload in ping")
            return
        do_ping(int(msg.payload.decode("utf-8")), 0)
        print("PING PING")
    elif topic == "valve_dose":
        print("dosing valve")
        span = valve_pattern.match(msg.payload.decode("utf-8")).span()
        if not (span[0] == 0 and span[1] == len(msg.payload.decode("utf-8"))):
            error("Wrong payload in valve dose")
            print("error")
            return
        args = list(map(int, msg.payload.decode("utf-8").split(",")))
        ret = do_valve_dose(index=args[0], amount=args[1], timeout=args[2])
        res = 1 if ret else -1
        print("Sending return")
        client.publish(MainTopic + topic + "/return", res, qos=1)
        if client.want_write():
            client.loop_write()
        print("Dosed Valve")
    else:
        error("Unknown topic")


def on_connect(client, userdata, flags, rc):
    print("subscribed")
    client.subscribe(MainTopic + "#")

print(__name__)
print(__name__ == "__main__")
if __name__ == "__main__":
    print("start")
    client = mqtt.Client()
    client.on_message = on_message
    client.on_connect = on_connect
    client.connect(MQTTIP, MQTTPORT, 60)
    print("abc")
    ac = 0
    while True:
        ac = ac + 1
        if ac % 100 == 0:
            ac = 0
            #print("100")
        client.loop()
