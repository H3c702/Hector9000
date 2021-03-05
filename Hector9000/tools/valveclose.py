#!/usr/bin/env python3

import time
from Hector9000.conf import HectorConfig as config
from Hector9000.HectorHardware import HectorHardware


def closeValve():
    hardware = True

    if hardware:
        h = HectorHardware(config)

    print("VENTILE SCHLIESSEN")
    print("")

    if hardware:
        h.light_on()
        time.sleep(1)
        h.arm_in()

        h.pump_stop()
        for vnum in range(12):
            print("Ventil %d wird geschlossen" % (vnum,))
            time.sleep(1)
            h.valve_close(vnum)

    h.light_off()

    print("fertig.")


if __name__ == "__main__":
    closeValve()
