from HectorRemote import HectorRemote as Hector


from drinks import available_drinks, ingredients, actions, alcoholic

import re
import paho.mqtt.client as mqtt
import traceback


# settings

MQTTServer = "localhost"
TopicPrefix = "Hector9000/"
initDone = False
hector = Hector()


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe(TopicPrefix + "+")


def on_log(client, userdata, level, buf):
    print("LOG " + str(level) + ": " + str(userdata) + " -- " + str(buf))


def do_get_drinks(msg):
    pass


def on_message(client, userdata, msg):
    try:
        global currentTopic
        currentTopic = msg.topic

        if msg.topic.endswith("/progress"):
            return  # ignore our own progress messages
        elif msg.topic.endswith("/return"):
            return  # ignore our own return messages

        # low-level
        elif msg.topic == TopicPrefix + "get_drinks":
            do_get_drinks(msg)
        elif msg.topic == TopicPrefix + "light_on":
            pass
            #do_light_on(msg)


        # high-level
        elif msg.topic == TopicPrefix + "ring":
            pass
            #ring(msg)
        elif msg.topic == TopicPrefix + "doseDrink":
            pass
            #valve_dose(msg)
        elif msg.topic == TopicPrefix + "cleanMe":
            pass
            #clean(msg)
        elif msg.topic == TopicPrefix + "dryMe":
            pass
            #dry(msg)

        # unknown
        else:
            print("unknown topic: " + msg.topic + ", msg " + str(msg.payload))

        print("done with msg " + msg.topic + " / " + str(msg.payload))

    except Exception as e:
        print("Error! " + str(e))
        print(traceback.format_exc())


# main program

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.on_log = on_log

client.connect(MQTTServer, 1883, 60)