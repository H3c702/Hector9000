#!/usr/bin/env python3
# -*- coding: utf8 -*-
##
#   HectorHardware.py       API class for Hector9000 hardware
#


## imports
from __future__ import division

from time import sleep, time
import sys

from HectorAPI import HectorAPI
from HectorConfig import config


## settings
DevEnvironment = True
# Uncomment to enable debug output:
import logging


## conditional imports
if not DevEnvironment:
    import Adafruit_PCA9685
    import RPi.GPIO as GPIO
    from hx711 import HX711


## initialization
logging.basicConfig(level=logging.DEBUG)


def debugOut(name, value):
    print("=> %s: %d" % (name, value))


## classes

class HectorHardware(HectorAPI):

    def __init__(self, cfg):
    
        print("HectorHardware: development mode is " + "active" if DevEnvironment else "inactive")

        self.config = cfg
        if not DevEnvironment:
            GPIO.setmode(GPIO.BOARD)

            # setup scale (HX711)
            hx1 = cfg["hx711"]["CLK"]
            hx2 = cfg["hx711"]["DAT"]
            hxref = cfg["hx711"]["ref"]
        if not DevEnvironment:
            self.hx = HX711(hx1, hx2)
            self.hx.set_reading_format("LSB", "MSB")
            self.hx.set_reference_unit(hxref)
            self.hx.reset()
            self.hx.tare()

        # setup servos (PCA9685)
        self.valveChannels = cfg["pca9685"]["valvechannels"]
        self.numValves = len(self.valveChannels)
        self.valvePositions = cfg["pca9685"]["valvepositions"]
        self.fingerChannel = cfg["pca9685"]["fingerchannel"]
        self.fingerPositions = cfg["pca9685"]["fingerpositions"]
        self.lightPin = cfg["pca9685"]["lightpin"]
        self.lightChannel = cfg["pca9685"]["lightpwmchannel"]
        self.lightPositions = cfg["pca9685"]["lightpositions"]
        if not DevEnvironment:
            pcafreq = cfg["pca9685"]["freq"]
            self.pca = Adafruit_PCA9685.PCA9685()
            self.pca.set_pwm_freq(pcafreq)

        # setup arm stepper (A4988)
        self.armEnable = cfg["a4988"]["ENABLE"]
        self.armReset = cfg["a4988"]["RESET"]
        self.armSleep = cfg["a4988"]["SLEEP"]
        self.armStep = cfg["a4988"]["STEP"]
        self.armDir = cfg["a4988"]["DIR"]
        self.armNumSteps = cfg["a4988"]["numSteps"]
        self.simulatedArmPos = self.armNumSteps / 2  # 50%
        print("arm step %d, dir %d" % (self.armStep, self.armDir))
        self.arm = cfg["arm"]["SENSE"]
        if not DevEnvironment:
            GPIO.setup(self.armEnable, GPIO.OUT)
            GPIO.output(self.armEnable, True)
            GPIO.setup(self.armReset, GPIO.OUT)
            GPIO.output(self.armReset, True)
            GPIO.setup(self.armSleep, GPIO.OUT)
            GPIO.output(self.armSleep, True)
            GPIO.setup(self.armStep, GPIO.OUT)
            GPIO.setup(self.armDir, GPIO.OUT)
            GPIO.setup(self.arm, GPIO.IN)

        # setup air pump (GPIO)
        self.pump = cfg["pump"]["MOTOR"]
        if not DevEnvironment:
            GPIO.setup(self.pump, GPIO.IN)  # pump off; will be turned on with GPIO.OUT (?!?)

    def getConfig(self):
        return self.config

    def light_on(self):
        print("turn on light")
        if not DevEnvironment:
            GPIO.output(self.lightPin, True)

    def light_off(self):
        print("turn off light")
        if not DevEnvironment:
            GPIO.output(self.lightPin, False)

    def arm_out(self, cback=debugOut):
        armMaxSteps = int(self.armNumSteps * 1.1)
        if not DevEnvironment:
            GPIO.output(self.armEnable, False)
        print("move arm out")
        if not DevEnvironment:
            GPIO.output(self.armDir, True)
            for i in range(armMaxSteps):
                if self.arm_isInOutPos():
                    GPIO.output(self.armEnable, True)
                    print("arm is in OUT position")
                    if cback: cback("arm_out", 100)
                    return
                GPIO.output(self.armStep, False)
                sleep(.001)
                GPIO.output(self.armStep, True)
                sleep(.001)
                if cback: cback("arm_out", i * 100 / self.armNumSteps)
            GPIO.output(self.armEnable, True)
        else:
            for i in range(armMaxSteps):
                self.simulatedArmPos += 1
                if self.arm_isInOutPos():
                    print("arm is in OUT position")
                    if cback: cback("arm_out", 100)
                    return
                sleep(.002)
                if cback: cback("arm_out", i * 100 / self.armNumSteps)
        print("arm is in OUT position (with timeout)")

    def arm_in(self, cback=debugOut):
        self.arm_out(cback)
        if not DevEnvironment:
            GPIO.output(self.armEnable, False)
        print("move arm in")
        if not DevEnvironment:
            GPIO.output(self.armDir, False)
            for i in range(self.armNumSteps, 0, -1):
                GPIO.output(self.armStep, False)
                sleep(.001)
                GPIO.output(self.armStep, True)
                sleep(.001)
                if cback and (i % 10 == 0): cback("arm_in", i * 100 / self.armNumSteps)
            GPIO.output(self.armEnable, True)
        else:
            for i in range(self.armNumSteps, 0, -1):
                self.simulatedArmPos -= 1
                sleep(.002)
                if cback and (i % 10 == 0): cback("arm_in", i * 100 / self.armNumSteps)
        print("arm is in IN position")

    def arm_isInOutPos(self):
        if DevEnvironment:
            pos = (self.simulatedArmPos >= self.armNumSteps)
        else:
            pos = GPIO.input(self.arm)
        print("arm_isInOutPos: %d" % pos)
        pos = (pos != 0)
        if pos:
            print("arm_isInOutPos = True")
        else:
            print("arm_isInOutPos = False")
        return pos

    def scale_readout(self):
        if not DevEnvironment:
            weight = self.hx.get_weight(5)
            print("weight = %.1f" % weight)
        else:
            weight = 0
        return weight

    def scale_tare(self):
        if not DevEnvironment:
            self.hx.tare()

    def pump_start(self):
        print("start pump")
        if not DevEnvironment:
            GPIO.setup(self.pump, GPIO.OUT)

    def pump_stop(self):
        print("stop pump")
        if not DevEnvironment:
            GPIO.setup(self.pump, GPIO.IN)

    def valve_open(self, index, open=1):
        if open == 0:
            print("close valve")
        else:
            print("open valve")
        if (index < 0 and index >= len(self.valveChannels) - 1):
            return
        if open == 0:
            print("close valve no. %d" % index)
        else:
            print("open valve no. %d" % index)
        ch = self.valveChannels[index]
        pos = self.valvePositions[index][1 - open]
        print("ch %d, pos %d" % (ch, pos))
        if not DevEnvironment:
            self.pca.set_pwm(ch, 0, pos)

    def valve_close(self, index):
        if not DevEnvironment:
            self.valve_open(index, open=0)

    def valve_dose(self, index, amount, timeout=30, cback=debugOut):
        print("dose channel %d, amount %d" % (index, amount))
        if cback: cback("valve_dose", 0)
        sr = 0
        if not DevEnvironment:
            if (index < 0 and index >= len(self.valveChannels) - 1):
                return -1
            t0 = time.time()
            self.scale_tare()
            self.pump_start()
            self.valve_open(index)
            sr = self.scale_readout()
            while sr < amount:
                sr = self.scale_readout()
                if cback: cback("valve_dose", sr)
                if (time.time() - t0) > timeout:
                    self.pump_stop()
                    self.valve_close(index)
                    if cback: cback("valve_dose", amount)
                    return -1
                sleep(0.1)
            self.pump_stop()
            self.valve_close(index)
        else:
            for i in range(amount):
                sleep(.1)
                if cback: cback("valve_dose", i)
            if cback: cback("valve_dose", amount)
            sr = amount
        return sr

    def finger(self, pos=0):
        if not DevEnvironment:
            self.pca.set_pwm(self.fingerChannel, 0, self.fingerPositions[pos])

    def ping(self, num, retract=True, cback=None):
        if not DevEnvironment:
            print("ping :-)")
            self.pca.set_pwm(self.fingerChannel, 0, self.fingerPositions[1])
            for i in range(num):
                self.pca.set_pwm(self.fingerChannel, 0, self.fingerPositions[1])
                sleep(.15)
                self.pca.set_pwm(self.fingerChannel, 0, self.fingerPositions[2])
                sleep(.15)
            if retract:
                self.pca.set_pwm(self.fingerChannel, 0, self.fingerPositions[1])
            else:
                self.pca.set_pwm(self.fingerChannel, 0, self.fingerPositions[0])
        else:
            print("PING! " * num)

    def cleanAndExit(self):
        print("Cleaning...")
        if not DevEnvironment:
            GPIO.cleanup()
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
        if not DevEnvironment:
            self.pca.set_pwm(channel, 0, pulse)


# end class HectorHardware


## main (for testing only)
if __name__ == "__main__":
    # if not DevEnvironment:
    hector = HectorHardware(config)
    hector.finger(0)
    hector.arm_in()
    for i in range(hector.numValves):
        print("close valve %d = channel %d" % (i, hector.valveChannels[i]))
        hector.valve_close(hector.valveChannels[i])
    input("Bitte Glas auf die Markierung stellen")
    # hector.ping(1)
    hector.arm_out()
    hector.valve_dose(1, 100)
    hector.valve_dose(3, 20)
    hector.finger(1)
    hector.valve_dose(11, 100)
    hector.arm_in()
    hector.ping(3)
    hector.finger(0)
    hector.cleanAndExit()
    print("done.")
