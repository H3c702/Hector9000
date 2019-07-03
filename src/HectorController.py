from HectorRemote import HectorRemote as Hector

import json
import conf.drinks as drinks

import paho.mqtt.client as mqtt
import traceback


# settings
class HectorController:
    MQTTServer = "localhost"
    TopicPrefix = "Hector9000/"
    initDone = False
    client = mqtt.Client()

    def available_drinks_as_JSON(self):
        datalist = []
        idOfDrink = 1
        for drinkitem in drinks.available_drinks:
            data = {"name": drinkitem["name"], "id": idOfDrink, "alcohol": drinks.alcoholic(drinkitem)}
            datalist.append(data)
            idOfDrink = idOfDrink + 1
        return json.dumps({"drinks": datalist})

    def get_drink_as_JSON(self, id):
        return json.dumps(drinks.available_drinks[id])

    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code " + str(rc))
        client.subscribe(self.TopicPrefix + "+")

    def on_log(self, client, userdata, level, buf):
        print("LOG " + str(level) + ": " + str(userdata) + " -- " + str(buf))

    def do_get_drinks(self, msg, topic):
        self.client.publish(topic + "/return", drinks.available_drinks_as_JSON())
        pass

    def on_message(self, client, userdata, msg):
        try:
            global currentTopic
            currentTopic = msg.topic

            if msg.topic.endswith("/progress"):
                return  # ignore our own progress messages
            elif msg.topic.endswith("/return"):
                return  # ignore our own return messages

            # low-level
            elif msg.topic == self.TopicPrefix + "get_drinks":
                self.do_get_drinks(msg, msg.topic)
            elif msg.topic == self.TopicPrefix + "get_ingredients":
                pass
            elif msg.topic == self.TopicPrefix + "light_on":
                pass
            elif msg.topic == self.TopicPrefix + "light_off":
                pass
                # do_light_on(msg)

            # high-level
            elif msg.topic == self.TopicPrefix + "ring":
                pass
                # ring(msg)
            elif msg.topic == self.TopicPrefix + "doseDrink":
                pass
                # valve_dose(msg)
            elif msg.topic == self.TopicPrefix + "cleanMe":
                pass
                # clean(msg)
            elif msg.topic == self.TopicPrefix + "dryMe":
                pass
                # dry(msg)

            # unknown
            else:
                print("unknown topic: " + msg.topic + ", msg " + str(msg.payload))

            print("done with msg " + msg.topic + " / " + str(msg.payload))

        except Exception as e:
            print("Error! " + str(e))
            print(traceback.format_exc())

    def connect(self):
        # main program

        self.hector = Hector()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.on_log = self.on_log

        self.client.connect(self.MQTTServer, 1883, 60)
