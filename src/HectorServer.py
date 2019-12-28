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

from HectorHardware import HectorHardware as Hector

# from HectorSimulator import HectorSimulator as Hector

hector = Hector(config)


def log(message):
    print("HARDWARELOG: " + message)


# low-level functions


def do_get_config():
    log("get configuration")
    return  hector.getConfig()


def do_light_on():
    log("turn on light")
    hector.light_on()
    return "ok"


def do_light_off():
    log("turn off light")
    hector.light_off()
    return "ok"


def do_arm_out():
    log("drive arm out")
    hector.arm_out(on_callback)
    return "ok"


def do_arm_in():
    log("drive arm in")
    hector.arm_in(on_callback)
    return "ok"


def do_arm_isInOutPos():
    log("check if arm is in OUT position")
    return "1" if hector.arm_isInOutPos else "0"


def do_scale_readout():
    log("query scale readout")
    return hector.scale_readout()


def do_scale_tare():
    log("set scale tare")
    hector.scale_tare()
    return "ok"


def do_pump_start():
    log("start pump")
    hector.pump_start()
    return "ok"


def do_pump_stop():
    log("stop pump")
    hector.pump_stop()
    return "ok"


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
    return "ok"


def do_valve_close(index):
    log("close valve")
    hector.valve_close(index)
    return "ok"


def do_valve_dose(index, amount, timeout=30):
    log("dose valve")
    return hector.valve_dose(index, amount, timeout, on_callback)


def do_finger(pos):
    log("set finger position")
    hector.finger(pos)
    return "ok"


def do_ping(num, retract):
    hector.ping(num, retract, on_callback)
    return "ok"


# high-level functions


def ring(timesToRing):
    hector.ping(int(timesToRing))
    return "ok"


def valve_dose(index, amount):
    hector.valve_dose(index, amount, cback=on_callback)
    return "ok"


def dry(pump):
    log("IndexPump: " + pump)
    hector.valve_open(pump)
    time.sleep(20)
    hector.valve_open(pump, 0)
    return "ok"


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
    # on_callback("clean", 1)
    return "ok"
