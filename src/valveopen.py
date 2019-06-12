#!/usr/bin/env python3

import sys, time
from conf.HectorConfig import config
from HectorHardware import HectorHardware

hardware = True

if hardware:
    h = HectorHardware(config)

print("VENTILE ÖFFNEN")
print("")

if hardware:
    h.light_on()
    time.sleep(1)
    h.arm_in()

    h.pump_stop()
    for vnum in range(12):
            print("Ventil %d wird geöffnet" % (vnum,))
            time.sleep(1)
            h.valve_open(vnum)

h.light_off()

print("fertig.")


