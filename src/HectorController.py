from HectorRemote import HectorRemote as Hector

import json
import conf.drinks as drinks

import paho.mqtt.client as mqtt
import time
import traceback


def log(obj):
    print("Controller: " + str(obj))


def error(obj):
    print("CONTROLLER ERROR: " + str(obj))

# settings
class HectorController:

    @staticmethod
    def get_returnTopic(topic):
        return topic + "/return"

    @staticmethod
    def get_progressTopic(topic):
        return topic + "/progress"

    def __init__(self):
        self.MQTTServer = "localhost"
        self.TopicPrefix = "Hector9000/"
        self.initDone = False
        self.client = mqtt.Client()
        self.hector = Hector()

    def available_drinks_as_JSON(self):
        datalist = []
        idOfDrink = 1
        for drinkitem in drinks.available_drinks:
            data = {"name": drinkitem["name"], "id": idOfDrink, "alcohol": drinks.alcoholic(drinkitem)}
            datalist.append(data)
            idOfDrink = idOfDrink + 1
        return json.dumps({"drinks": datalist})

    def _get_drink_as_JSON(self, msg):
        id = int(msg.payload)
        drink = drinks.available_drinks[id]
        inglist = [{"name": drinks.ingredients[step[1]][0], "ammount": step[2]} for step in drink["recipe"] if
                   step[0] == "ingr"]
        data = {"id": id, "name": drink["name"], "ingredients": inglist}
        log(data)
        return json.dumps(data)

    def on_connect(self, client, userdata, flags, rc):
        log("Connected with result code " + str(rc))
        self.client.subscribe(self.TopicPrefix + "#")

    def on_log(self, client, userdata, level, buf):
        pass  # log("LOG " + str(level) + ": " + str(userdata) + " -- " + str(buf))

    def _do_get_drinks(self, msg):
        self.client.publish(self.get_returnTopic(msg.topic), self.available_drinks_as_JSON())

    def _do_get_drink(self, msg):
        self.client.publish(self.get_returnTopic(msg.topic), self._get_drink_as_JSON(msg))

    def _do_dose_drink(self, msg):
        print("do dose drink")
        id = int(msg.payload)
        drink = drinks.available_drinks[id]
        # Return ID of drink to identify that drink creation starts
        self.client.publish(self.get_returnTopic(msg.topic), msg.payload)
        progress = 0
        self.client.publish(self.get_progressTopic(msg.topic), progress)
        steps = 100 / len(drink["recipe"])
        self.client.loop()
        self.hector.pump_start()
        self.hector.light_on()
        self.hector.arm_out()
        print("preparation complete")
        for step in drink["recipe"]:
            print("dose :" + str(progress))
            # could be other things than ingr.
            if step[0] == "ingr":
                pump = drinks.available_ingredients.index(step[1])
                if not self.hector.valve_dose(index=int(pump), amount=int(step[2]), cback=self.dose_callback, progress=(progress, steps), topic="Hector9000/doseDrink/progress"):
                    error("DOSE NOT SUCESFULL: " + str(pump) + "; " + str(step[2]))
                    self.hector.arm_in()
                    self.hector.light_off()
                    self.hector.pump_stop()
                    self.hector.ping(3, 0)
                    self.client.publish(self.get_progressTopic(msg.topic), msg.payload.decode("utf-8") + ",end")
                    return
            progress = progress + steps
        print("dose sucessfull")
        time.sleep(1)
        self.hector.arm_in()
        self.hector.light_off()
        self.hector.pump_stop()
        self.hector.ping(3,0)
        print("ended dose")
        self.client.publish(self.get_progressTopic(msg.topic), msg.payload.decode("utf-8") + ",end")

    def dose_callback(self, progress):
        self.client.publish(self.TopicPrefix + "/doseDrink/progress", progress)

    def on_message(self, client, userdata, msg):
        print("test")
        log("on_message: topic " + str(msg.topic) + ", msg: " + str(msg.payload))
        try:
            global currentTopic
            currentTopic = msg.topic

            if currentTopic is self.TopicPrefix + "doseDrink/Hardware/progress":
                pass

            if currentTopic.endswith("/progress"):
                return  # ignore our own progress messages
            elif currentTopic.endswith("/return"):
                return  # ignore our own return messages

            # low-level
            elif currentTopic == self.TopicPrefix + "get_drinks":
                self._do_get_drinks(msg)
            elif currentTopic == self.TopicPrefix + "get_ingredientsForDrink":
                self._do_get_drink(msg)
                pass
            elif currentTopic == self.TopicPrefix + "get_ingredientsList":
                # gibt liste aller Ing aus der DB
                pass
            elif currentTopic == self.TopicPrefix + "set_ingredients":
                # Setzt die Ing in der DB
                pass
            elif currentTopic == self.TopicPrefix + "light_on":
                self.hector.do_light_on()
                pass
            elif currentTopic == self.TopicPrefix + "light_off":
                self.hector.do_light_off()
                pass

            # high-level
            elif currentTopic == self.TopicPrefix + "ring":
                self.hector.do_ping(2, 1)
                pass
            elif currentTopic == self.TopicPrefix + "doseDrink":
                self._do_dose_drink(msg)
                pass
            elif currentTopic == self.TopicPrefix + "cleanMe":
                # ToDo: Develop proper methode in Server
                for i in range(12):
                    self.hector.clean(1)
                pass
                # clean(msg)
            elif currentTopic == self.TopicPrefix + "dryMe":
                pass
            elif currentTopic == self.TopicPrefix + "openAllValves":
                self.hector.all_valve_open()
                pass
            elif currentTopic == self.TopicPrefix + "closeAllValves":
                self.hector.all_valve_close()
                pass
            else:
                log("unknown topic: " + currentTopic + ", msg " + str(msg.payload))

            log("handled message " + currentTopic + " / " + str(msg.payload))

        except Exception as e:
            log("Error! " + str(e))
            log(traceback.format_exc())

    def connect(self):
        print("connect")
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.on_log = self.on_log
        self.client.connect(self.MQTTServer, 1883, 60)
        while True:
            self.client.loop()
