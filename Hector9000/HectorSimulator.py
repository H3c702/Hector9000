#!/usr/bin/env python3
# -*- coding: utf8 -*-
##
#   HectorSimulator.py       API class for simulating the Hector9000 hardware (same as old HectorHardware with
#   DevEnvironment = True)
#


# imports
from __future__ import division

from time import sleep, time
import sys

from Hector9000.utils import HectorAPI as api

from Hector9000.conf import HectorConfig


# settings

# Uncomment to enable debug output:
import logging

# initialization
logging.basicConfig(level=logging.DEBUG)


def debugOut(name, value):
    print("=> %s: %d" % (name, value))


class HectorSimulator(api.HectorAPI):

    def __init__(self, cfg=HectorConfig.config):

        print("HectorSimulator")

        self.config = cfg

        # setup servos (PCA9685)
        self.valveChannels = cfg["pca9685"]["valvechannels"]
        self.numValves = len(self.valveChannels)
        self.valvePositions = cfg["pca9685"]["valvepositions"]
        self.fingerChannel = cfg["pca9685"]["fingerchannel"]
        self.fingerPositions = cfg["pca9685"]["fingerpositions"]
        self.lightPin = cfg["pca9685"]["lightpin"]
        self.lightChannel = cfg["pca9685"]["lightpwmchannel"]
        self.lightPositions = cfg["pca9685"]["lightpositions"]

        # setup arm stepper (A4988)
        self.armEnable = cfg["a4988"]["ENABLE"]
        self.armReset = cfg["a4988"]["RESET"]
        self.armSleep = cfg["a4988"]["SLEEP"]
        self.armStep = cfg["a4988"]["STEP"]
        self.armDir = cfg["a4988"]["DIR"]
        self.armNumSteps = cfg["a4988"]["numSteps"]
        self.simulatedArmPos = self.armNumSteps / 2  # 50%
        # print("arm step %d, dir %d" % (self.armStep, self.armDir))
        self.arm = cfg["arm"]["SENSE"]

        # setup air pump (GPIO)
        self.pump = cfg["pump"]["MOTOR"]

        # setup weight
        self.weight = 0
        self.openedValveAt = 0

    def getConfig(self):
        return self.config

    def light_on(self):
        print("turn on light")
        return 1

    def light_off(self):
        print("turn off light")
        return 0

    def arm_out(self, cback=debugOut):
        armMaxSteps = int(self.armNumSteps * 1.1)
        print("move arm out")
        for i in range(armMaxSteps):
            self.simulatedArmPos += 1
            if self.arm_isInOutPos():
                print("arm is in OUT position")
                if cback:
                    cback("arm_out", 100)
                return
            sleep(.002)
            if cback:
                cback("arm_out", i * 100 / self.armNumSteps)
        print("arm is in OUT position (with timeout)")

    def arm_in(self, cback=debugOut):
        self.arm_out(cback)
        print("move arm in")
        for i in range(self.armNumSteps, 0, -1):
            self.simulatedArmPos -= 1
            sleep(.002)
            if cback and (i % 10 == 0):
                cback("arm_in", i * 100 / self.armNumSteps)
        print("arm is in IN position")

    def arm_isInOutPos(self):
        pos = (self.simulatedArmPos >= self.armNumSteps)
        # print("arm_isInOutPos: %d" % pos)
        pos = (pos != 0)
        # if pos:
        #    print("arm_isInOutPos = True")
        # else:
        #    print("arm_isInOutPos = False")
        return pos

    def scale_readout(self):
        if self.openedValveAt == 0:
            return self.weight

        return (self.weight + (time() - self.openedValveAt)) * 5

    def scale_tare(self):
        self.weight = 0
        print("scale tare")
        return self.weight

    def pump_start(self):
        print("start pump")
        return 1

    def pump_stop(self):
        print("stop pump")
        return 0

    def valve_open(self, index, openValve=1):
        if 0 > index >= len(self.valveChannels) - 1:
            return 0

        if openValve == 0:
            print("close valve no. %d" % index)
            self.weight = self.scale_readout()
        else:
            print("open valve no. %d" % index)
            self.openedValveAt = time()

        ch = self.valveChannels[index]
        pos = self.valvePositions[index][1 - openValve]

        print("ch %d, pos %d" % (ch, pos))
        return 1

    def valve_close(self, index):
        return self.valve_open(index, 0)

    def valve_dose(
            self,
            index,
            amount,
            timeout=30,
            cback=None,
            progress=(
                0,
                100),
            topic=""):
        print("dose channel %d, amount %d" % (index, amount))
        if not self.arm_isInOutPos():
            return False
        for i in range(amount):
            sleep(.1)
            if cback:
                cback("valve_dose", i)
        if cback:
            cback(progress[0] + progress[1])
        return False

    def finger(self, pos=0):
        print("finger")

    def ping(self, num, retract=True, cback=None):
        print("PING! " * num)

    def cleanAndExit(self):
        print("Cleaning...")
        print("Bye!")
        sys.exit()

    # Helper function to make setting a servo pulse width simpler.
    def set_servo_pulse(self, channel, pulse):
        pulse_length = 1000000  # 1,000,000 us per second
        pulse_length //= 60  # 60 Hz
        print('{0} µs per period'.format(pulse_length))
        pulse_length //= 4096  # 12 bits of resolution
        print('{0} µs per bit'.format(pulse_length))
        pulse *= 1000
        pulse //= pulse_length


# end class HectorHardware

#
# ## main (for testing only)
# if __name__ == "__main__":
# 	hector = HectorSimulator(config)
# 	hector.finger(0)
# 	hector.arm_in()
# 	for i in range(hector.numValves):
# 		print("close valve %d = channel %d" % (i, hector.valveChannels[i]))
# 		hector.valve_close(hector.valveChannels[i])
# 	input("Bitte Glas auf die Markierung stellen")
# 	# hector.ping(1)
# 	hector.arm_out()
# 	hector.valve_dose(1, 100)
# 	hector.valve_dose(3, 20)
# 	hector.finger(1)
# 	hector.valve_dose(11, 100)
# 	hector.arm_in()
# 	hector.ping(3)
# 	hector.finger(0)
# 	hector.cleanAndExit()
# 	print("done.")
