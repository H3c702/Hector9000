#!/usr/bin/env python3
# -*- coding: utf8 -*-
##
#   HectorRemote.py       Remote class for Hector9000 hardware via MQTT communication
#

from time import sleep
import re
import paho.mqtt.client as mqtt

from HectorAPI import HectorAPI


def debugOut(name, value):
    print("=> %s: %d" % (name, value))


class HectorRemote(HectorAPI):
    # settings

    MQTTServer = "localhost"
    TopicPrefix = "Hector9000/Main/"
    initDone = False
    currentCall = None
    returnValue = None
    currentCallback = None

    # global vars

    pass

    # constructor

    def __init__(self, cfg=None):
        self.initDone = False
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.on_publish = self.on_publish
        self.client.on_subscribe = self.on_subscribe
        self.client.connect(self.MQTTServer, 1883, 60)
        self.client.loop_start()  # fork background thread
        self.progressPattern = re.compile(self.TopicPrefix + r"(\w+)/progress")
        self.returnPattern = re.compile(self.TopicPrefix + r"(\w+)/return")

        sleep(0.5)
        while not self.initDone:
            sleep(1)
            print(".", end="")
        print(" -- HectorRemote init done")

    # methods

    #  callbacks

    def on_connect(self, client, userdata, flags, rc):
        try:
            print("HectorRemote connected with result code " + str(rc))
            self.client.subscribe(self.TopicPrefix + "#")
            print("subscription sent")
            # request configuration
            self.client.publish(self.TopicPrefix + "get_config", "")
            print("published get_config")
            print("done with on_connect()")
        except Exception as e:
            print("error: " + str(e))

    def on_publish(self, client, userdata, mid):
        # print("published: %s" % str(userdata))
        pass

    def on_subscribe(self, client, userdata, mid, granted_qos):
        print("subscribed: %s" % str(userdata))

    def on_message(self, client, userdata, msg):
        try:
            topic = msg.topic
            payload = msg.payload
            print("got message => %s: %s" % (topic, payload))
            if topic.startswith(self.TopicPrefix) and topic.endswith("/progress"):
                print("is progress topic: " + topic)
                m = self.progressPattern.fullmatch(topic)
                if m:
                    subTopic = m.group(1)
                    print("match! " + subTopic)
                    if subTopic == self.currentCall:
                        if self.currentCallback:
                            value = str(msg.payload.decode("utf-8"))
                            if value.isdigit:
                                self.currentCallback(subTopic, int(value))
                else:
                    print("no match-")
            elif topic.startswith(self.TopicPrefix) and topic.endswith("/return"):
                print("is return topic: " + topic)
                m = self.returnPattern.fullmatch(topic)
                if m:
                    subTopic = m.group(1)
                    print("match! " + subTopic)
                    if subTopic == self.currentCall:
                        self.returnValue = str(payload)
                        self.currentCall = None
                        self.currentCallback = None
                    elif subTopic == "get_config":
                        cfg = eval(payload)  # !!
                        self.config = cfg
                        self.valveChannels = cfg["pca9685"]["valvechannels"]
                        self.numValves = len(self.valveChannels)
                        print("Config: " + str(self.config))
                        print("  valveChannels: " + str(self.valveChannels))
                        print("  numValves:     " + str(self.numValves))
                        self.initDone = True
                else:
                    print("no match-")
        except Exception as e:
            print("Error: " + str(e))

    # helpers

    def setCurrentCall(self, topic, callback=None):
        if self.currentCall != None:
            raise Exception("current call conflict: " + topic + " - still waiting for " + self.currentCall)
        self.currentCall = topic
        self.currentCallback = callback

    def waitForReturn(self):
        print("waitForReturn ", end="")
        delay = 0.01
        while self.currentCall:
            sleep(delay)
            delay *= 1.01
            print(".", end="")
        pass

    def waitForReturnValue(self):
        print("waitForReturnValue ", end="")
        delay = 0.01
        while self.currentCall:
            sleep(delay)
            delay *= 1.01
            print(".", end="")
        return self.returnValue

    #  API calls

    def light_on(self):
        self.setCurrentCall("light_on")
        self.client.publish(self.TopicPrefix + self.currentCall, "")
        self.waitForReturn()

    def light_off(self):
        self.setCurrentCall("light_off")
        self.client.publish(self.TopicPrefix + self.currentCall, "")
        self.waitForReturn()

    def arm_out(self, cback=debugOut):
        self.setCurrentCall("arm_out", cback)
        self.client.publish(self.TopicPrefix + self.currentCall, "")
        self.waitForReturn()

    def arm_in(self, cback=debugOut):
        self.setCurrentCall("arm_in", cback)
        self.client.publish(self.TopicPrefix + self.currentCall, "")
        self.waitForReturn()

    def arm_isInOutPos(self):
        self.setCurrentCall("arm_isInOutPos")
        self.client.publish(self.TopicPrefix + self.currentCall, "")
        ret = self.waitForReturnValue()
        return ret

    def scale_readout(self):
        self.setCurrentCall("scale_readout")
        self.client.publish(self.TopicPrefix + self.currentCall, "")
        ret = self.waitForReturnValue()
        return ret

    def scale_tare(self):
        self.setCurrentCall("scale_tare")
        self.client.publish(self.TopicPrefix + self.currentCall, "")
        self.waitForReturn()

    def pump_start(self):
        self.setCurrentCall("pump_start")
        self.client.publish(self.TopicPrefix + self.currentCall, "")
        self.waitForReturn()

    def pump_stop(self):
        self.setCurrentCall("pump_stop")
        self.client.publish(self.TopicPrefix + self.currentCall, "")
        self.waitForReturn()

    def valve_open(self, index, open=1):
        self.setCurrentCall("valve_open")
        self.client.publish(self.TopicPrefix + self.currentCall, "%d,%d" % (index, open))
        self.waitForReturn()

    def valve_close(self, index):
        self.setCurrentCall("valve_close")
        self.client.publish(self.TopicPrefix + self.currentCall, "%d" % index)
        self.waitForReturn()

    def valve_dose(self, index, amount, timeout=30, cback=debugOut):
        self.setCurrentCall("valve_dose", cback)
        self.client.publish(self.TopicPrefix + self.currentCall, "%d,%d,%d" % (index, amount, timeout))
        ret = self.waitForReturnValue()
        return ret

    def finger(self, pos=0):
        self.setCurrentCall("finger")
        self.client.publish(self.TopicPrefix + self.currentCall, "%d" % pos)
        self.waitForReturn()

    def ping(self, num, retract=True, cback=None):
        self.setCurrentCall("ping", cback)
        self.client.publish(self.TopicPrefix + self.currentCall, "%d,%d" % (num, 1 if retract else 0))
        self.waitForReturn()

    def all_valve_close(self):
        self.setCurrentCall("all_valve_close")
        self.client.publish(self.TopicPrefix + self.currentCall, "%d" % 1)
        self.waitForReturn()

    def all_valve_open(self):
        self.setCurrentCall("all_valve_open")
        self.client.publish(self.TopicPrefix + self.currentCall, "%d" % 1)
        self.waitForReturn()

    def cleanAndExit(self):
        self.client.loop_stop()


## main (for testing only)
if __name__ == "__main__":
    # if not DevEnvironment:
    hector = HectorRemote()
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
