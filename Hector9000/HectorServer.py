#!/usr/bin/env python3
# -*- coding: utf8 -*-
##
#   HectorServer.py       Hector server with MQTT interface
#


import time
import re
import traceback
from Hector9000.conf import mqttTopics
import os

import paho.mqtt.client as mqtt
from Hector9000.conf import HectorConfig as HC

isSim = 0
#isSim = os.environ.get('isHectorSim', 0)

print(isSim)
if isSim != 1:
    from Hector9000.HectorHardware import HectorHardware as Hector
else:
    from Hector9000.HectorSimulator import HectorSimulator as Hector


MainTopic = "Hector9000/Hardware/"
MQTTIP = "localhost"
MQTTPORT = 1883
co = HC.config
hector = Hector(co)
valve_pattern = re.compile(r"[0-9]+\,[0-9]+\,[0-9]+")

VERBOSE_LEVEL = 0


def log(message):
    if VERBOSE_LEVEL == 0:
        print("Server: " + str(message))


def error(message):
    if VERBOSE_LEVEL < 3:
        print("Server ERROR: " + str(message))


def warning(message):
    if VERBOSE_LEVEL < 2:
        print("Server WARNING: " + str(message))


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
    log("reseting")
    do_pump_stop()
    do_all_valve_close()
    do_arm_in()
    do_light_off()
    do_ping(2, 0)


def do_pump_stop():
    log("stop pump")
    hector.pump_stop()


def do_all_valve_open():
    log("opening all valves")
    hector.light_on()
    time.sleep(1)
    hector.arm_in()
    hector.pump_stop()
    for vnum in range(12):
        # log("Ventil %d wird geöffnet" % (vnum,))
        time.sleep(0.5)
        hector.valve_open(vnum)
    hector.light_off()


def do_all_valve_close():
    log("close all valves")
    hector.light_on()
    time.sleep(1)
    hector.arm_in()
    hector.pump_stop()
    for vnum in range(12):
        # log("Ventil %d wird geschlossen" % (vnum,))
        time.sleep(0.5)
        hector.valve_close(vnum)
    hector.light_off()


def do_valve_open(index):
    log("open valve %d" % index)
    hector.valve_open(index)


def do_valve_close(index):
    log("close valve %d" % index)
    hector.valve_close(index)


def do_valve_dose(index, amount, timeout=30):
    log("dose valve %d with amount %d" % (index, amount))
    return hector.valve_dose(index=index, amount=amount, timeout=timeout)


def do_ping(num, retract):
    log("ping %d times" % num)
    hector.ping(num, retract)


def dry(pump):
    log("drying pump %d" % pump)
    hector.valve_open(pump)
    time.sleep(20)
    hector.valve_open(pump, 0)


def clean(pump):
    print("cleaning pump %d" % pump)
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
    hector.valve_open(pump, 0)
    time.sleep(10)
    hector.pump_stop()
    time.sleep(1)


def on_message(client, userdata, msg):
    log("on_message: " + str(msg.topic) + "," + str(msg.payload))
    topic = str(msg.topic)
    if (topic.endswith("return") or topic.endswith("progress")):
        return
    topic = topic.replace(MainTopic, "")
    if topic == "get_config":
        res = do_get_config()
        client.publish(MainTopic + topic + "/return", res)
    elif topic == mqttTopics.HardwareTopics.light_on:
        do_light_on()
    elif topic == mqttTopics.HardwareTopics.light_off:
        do_light_off()
    elif topic == mqttTopics.HardwareTopics.reset:
        do_reset()
    elif topic == mqttTopics.HardwareTopics.arm_out:
        do_arm_out()
    elif topic == mqttTopics.HardwareTopics.arm_in:
        do_arm_in()
    elif topic == mqttTopics.HardwareTopics.arm_position:
        res = do_arm_isInOutPos()
        client.publish(MainTopic + topic + "/return", res)
    elif topic == mqttTopics.HardwareTopics.scale_readout:
        res = do_scale_readout()
        client.publish(MainTopic + topic + "/return", res)
    elif topic == mqttTopics.HardwareTopics.scale_tare:
        do_scale_tare()
    elif topic == mqttTopics.HardwareTopics.pump_stop:
        do_pump_stop()
    elif topic == mqttTopics.HardwareTopics.pump_start:
        do_pump_start()
    elif topic == mqttTopics.HardwareTopics.all_valve_open:
        do_all_valve_open()
    elif topic == mqttTopics.HardwareTopics.all_valve_close:
        do_all_valve_close()
    elif topic == mqttTopics.HardwareTopics.valve_open:
        if not msg.payload.decode("utf-8").isnumeric():
            error("Wrong payload in valve open")
            return
        do_valve_open(int(msg.payload.decode("utf-8")))
    elif topic == mqttTopics.HardwareTopics.valve_close:
        if not msg.payload.decode("utf-8").isnumeric():
            error("Wrong payload in valve close")
            return
        do_valve_close(int(msg.payload.decode("utf-8")))
    elif topic == mqttTopics.HardwareTopics.ping:
        if not msg.payload.decode("utf-8").isnumeric():
            log("error in ping")
            error("Wrong payload in ping")
            return
        do_ping(int(msg.payload.decode("utf-8")), 0)
    elif topic == mqttTopics.HardwareTopics.valve_dose:
        span = valve_pattern.match(msg.payload.decode("utf-8")).span()
        if not (span[0] == 0 and span[1] == len(msg.payload.decode("utf-8"))):
            error("Wrong payload in valve dose")
            return
        args = list(map(int, msg.payload.decode("utf-8").split(",")))
        ret = do_valve_dose(index=args[0], amount=args[1], timeout=args[2])
        res = 1 if ret else -1
        log("Sending return")
        try:
            client.publish(MainTopic + topic + "/return", res)
            # ToDo: this line ^ causes trouble. Sometimes it just doesnt send the
            # publish causing errors. Some tests need to be written to test the
            # most reliable way to fix this
            while not client.want_write():
                pass
        except Exception as e:
            # as first try if error try again :-(
            log(traceback.format_exc())
            client.publish(MainTopic + topic + "/return", res)
            while not client.want_write():
                pass
        log("Return Send - Dosing Complete")
    elif topic == mqttTopics.HardwareTopics.cleanMe:
        clean(int(msg.payload.decode("utf-8")))
    elif topic == mqttTopics.HardwareTopics.dryMe:
        dry(int(msg.payload.decode("utf-8")))
    else:
        warning("Unknown topic")


def on_connect(client, userdata, flags, rc):
    log("Connected to Server")
    client.subscribe(MainTopic + "#")


def on_subscribe(client, userdata, mid, granted_qos):
    log("Subscribed to Topic")


def main():
    do_reset()
    log("starting")
    client = mqtt.Client(client_id="HectorServer")
    client.on_message = on_message
    client.on_connect = on_connect
    client.on_subscribe = on_subscribe
    client.connect(MQTTIP, MQTTPORT, 60)
    log("started")
    while True:
        client.loop()


if __name__ == "__main__":
    main()
