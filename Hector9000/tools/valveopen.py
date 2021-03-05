#!/usr/bin/env python3

import time
from Hector.conf import config
from Hector.HectorHardware import HectorHardware


def openValve():
    hardware = True

    if hardware:
        h = HectorHardware(config)

    print("VENTILE OEFFNEN")
    print("")

    if hardware:
        h.light_on()
        time.sleep(1)
        h.arm_in()

        h.pump_stop()
        for vnum in range(12):
            print("Ventil %d wird geoeffnet" % (vnum,))
            time.sleep(1)
            h.valve_open(vnum)

    h.light_off()

    print("fertig.")


if __name__ == "__main__":
    openValve()
