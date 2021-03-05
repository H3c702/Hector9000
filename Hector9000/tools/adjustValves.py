#!/usr/bin/env python3

import sys
from Hector9000.conf.HectorConfig import config
from Hector9000.HectorHardware import HectorHardware

h = HectorHardware(config)

while True:
    vnum = int(input("Bitte Ventilnr. eingeben (0..11); Ende mit -1:  "))
    if vnum == -1:
        sys.exit()
    cpos = h.valvePositions[vnum][1]
    print("Ventil %d wird geschlossen, Servoposition = %d" % (vnum, cpos))
    while cpos != -1:
        h.pca.set_pwm(vnum, 0, cpos)
        cpos = int(input("Bitte neue Servoposition eingeben:"))
