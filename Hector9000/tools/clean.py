#!/usr/bin/env python3

import sys
import time
from Hector.conf import HectorConfig as config
from Hector.HectorHardware import HectorHardware

hardware = True

if hardware:
    h = HectorHardware(config)

print("REINIGUNG")
print("")

if hardware:
    h.light_on()
    time.sleep(1)
    h.arm_out()

if True:
    vlist = sys.argv[1:]
    valves = []
    print("Die folgenden Kanäle werden jetzt gereinigt:")
    for v in vlist:
        if v == "":
            continue
        i = int(v)
        print("  %d" % i)
        valves.append(i)
if hardware:
    h.pump_start()
    for i in range(10):
        print("STEP: " + str(i))
        for vnum in valves:
            print("Ventil %d wird geöffnet, Ende mit <Return>" % (vnum,))
            h.valve_open(vnum)
            time.sleep(10)
            h.valve_close(vnum)
    h.pump_stop()
