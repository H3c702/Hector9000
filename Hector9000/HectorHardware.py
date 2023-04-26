#!/usr/bin/env python3
# -*- coding: utf8 -*-
##
#   HectorHardware.py       API class for Hector9000 hardware
#


# imports
from __future__ import division

from time import sleep, time
import sys

from Hector9000.utils import HectorAPI as api
from Hector9000.conf import HectorConfig

# hardware modules
import Adafruit_PCA9685
import RPi.GPIO as GPIO
from Hector9000.conf.hx711 import HX711

# settings

# Uncomment to enable debug output:
import logging

# initialization
logging.basicConfig(level=logging.CRITICAL)

VERBOSE_LEVEL = 0


def log(message):
    if VERBOSE_LEVEL == 0:
        logging.log(VERBOSE_LEVEL, "" + str(message))


def error(message):
    if VERBOSE_LEVEL < 3:
        print("Hardware ERROR: " + str(message))


def warning(message):
    if VERBOSE_LEVEL < 2:
        print("Hardware WARNING: " + str(message))


class HectorHardware(api.HectorAPI):

    def __init__(self, cfg):

        log("initialization HectorHardware")

        self.config = cfg
        GPIO.setmode(GPIO.BOARD)

        # setup scale (HX711)
        hx1 = cfg["hx711"]["CLK"]
        hx2 = cfg["hx711"]["DAT"]
        hxref = cfg["hx711"]["ref"]
        self.hx = HX711(hx1, hx2)
        self.hx.set_reading_format("LSB", "MSB")
        self.hx.set_reference_unit(hxref)
        self.hx.reset()
        self.hx.tare()

        # setup servos (PCA9685)
        self.valveChannels = self.config["pca9685"]["valvechannels"]
        self.numValves = len(self.valveChannels)
        self.valvePositions = cfg["pca9685"]["valvepositions"]
        self.fingerChannel = cfg["pca9685"]["fingerchannel"]
        self.fingerPositions = cfg["pca9685"]["fingerpositions"]
        self.lightPin = cfg["pca9685"]["lightpin"]
        self.lightChannel = cfg["pca9685"]["lightpwmchannel"]
        self.lightPositions = cfg["pca9685"]["lightpositions"]
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
        self.arm = cfg["arm"]["SENSE"]
        GPIO.setup(self.armEnable, GPIO.OUT)
        GPIO.output(self.armEnable, True)
        GPIO.setup(self.armReset, GPIO.OUT)
        GPIO.output(self.armReset, True)
        GPIO.setup(self.armSleep, GPIO.OUT)
        GPIO.output(self.armSleep, True)
        GPIO.setup(self.armStep, GPIO.OUT)
        GPIO.setup(self.armDir, GPIO.OUT)
        GPIO.setup(self.arm, GPIO.IN)
        GPIO.setup(self.lightPin, GPIO.OUT)

        # setup air pump (GPIO)
        self.pump = cfg["pump"]["MOTOR"]
        # pump off; will be turned on with GPIO.OUT (?!?)
        GPIO.setup(self.pump, GPIO.IN)

    def getConfig(self):
        return self.config

    def light_on(self):
        log("turn on light")
        GPIO.output(self.lightPin, True)

    def light_off(self):
        log("turn off light")
        GPIO.output(self.lightPin, False)

    def arm_out(self, cback=None):
        armMaxSteps = int(self.armNumSteps * 1.1)
        GPIO.output(self.armEnable, False)
        log("move arm out")
        GPIO.output(self.armDir, True)
        for i in range(armMaxSteps):
            if self.arm_isInOutPos():
                GPIO.output(self.armEnable, True)
                log("arm is in OUT position")
                if cback:
                    cback("arm_out", 100)
                return
            GPIO.output(self.armStep, False)
            sleep(.001)
            GPIO.output(self.armStep, True)
            sleep(.001)
            if cback:
                cback("arm_out", i * 100 / self.armNumSteps)
        GPIO.output(self.armEnable, True)
        log("arm is in OUT position (with timeout)")

    def arm_in(self, cback=None):
        self.arm_out(cback)
        GPIO.output(self.armEnable, False)
        log("move arm in")
        GPIO.output(self.armDir, False)
        for i in range(self.armNumSteps, 0, -1):
            GPIO.output(self.armStep, False)
            sleep(.001)
            GPIO.output(self.armStep, True)
            sleep(.001)
            if cback and (i % 10 == 0):
                cback("arm_in", i * 100 / self.armNumSteps)
        GPIO.output(self.armEnable, True)
        log("arm is in IN position")

    def arm_isInOutPos(self):
        pos = GPIO.input(self.arm)
        pos = (pos != 0)
        if pos:
            log("arm_isInOutPos = True")
        else:
            log("arm_isInOutPos = False")
        return pos

    def scale_readout(self) -> object:
        """

        :rtype: object
        """
        weight = self.hx.get_weight(5)
        return weight

    def scale_tare(self):
        log("scale tare")
        self.hx.tare()

    def pump_start(self):
        log("start pump")
        GPIO.setup(self.pump, GPIO.OUT)

    def pump_stop(self):
        log("stop pump")
        GPIO.setup(self.pump, GPIO.IN)

    def valve_open(self, index, open=1):
        if open == 0:
            log("close valve")
        else:
            log("open valve")
        if (index < 0 and index >= len(self.valveChannels) - 1):
            return
        if open == 0:
            log("close valve no. %d" % index)
        else:
            log("open valve no. %d" % index)
        ch = self.valveChannels[index]
        pos = self.valvePositions[index][1 - open]
        log("ch %d, pos %d" % (ch, pos))
        self.pca.set_pwm(ch, 0, pos)

    def valve_close(self, index):
        log("close valve")
        self.valve_open(index, open=0)

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
        log("dose channel %d, amount %d" % (index, amount))
        if index < 0 and index >= len(self.valveChannels) - 1:
            return -1
        if not self.arm_isInOutPos():
            return -1
        t0 = time()
        balance = True
        self.scale_tare()
        self.pump_start()
        self.valve_open(index)
        sr: float = self.scale_readout()
        if sr < -10:
            amount = amount + sr
            balance = False
        last_over = False
        last: float = sr
        while True:
            sr = self.scale_readout()
            if balance and sr < -10:
                warning("weight abnormality: scale balanced")
                amount = amount + sr
                balance = False
            if sr > amount:
                if last_over:
                    log("dosing complete")
                    break
                else:
                    last_over = True
            else:
                last_over = False
            log("Read scale: %d" % sr)
            if (sr - last) > 5:
                log("reset timeout")
                t0 = time()
                last = sr
            if (time() - t0) > timeout:
                error("timeout reached")
                self.pump_stop()
                self.valve_close(index)
                if cback:
                    cback(progress[0] + progress[1])
                return False
            sleep(0.1)
        self.pump_stop()
        self.valve_close(index)
        if cback:
            cback(progress[0] + progress[1])
        log("completed reset after dosing")
        return True

    def finger(self, pos=0):
        self.pca.set_pwm(self.fingerChannel, 0, self.fingerPositions[pos])

    def ping(self, num, retract=True, cback=None):
        log("ping")
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

    def cleanAndExit(self):
        log("Cleaning...")
        GPIO.cleanup()
        log("Bye!")
        sys.exit()

    # Helper function to make setting a servo pulse width simpler.
    def set_servo_pulse(self, channel, pulse):
        pulse_length = 1000000  # 1,000,000 us per second
        pulse_length //= 60  # 60 Hz
        log('{0} µs per period'.format(pulse_length))
        pulse_length //= 4096  # 12 bits of resolution
        log('{0} µs per bit'.format(pulse_length))
        pulse *= 1000
        pulse //= pulse_length
        self.pca.set_pwm(channel, 0, pulse)


# end class HectorHardware
