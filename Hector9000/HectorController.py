from Hector9000 import HectorRemote as remote
from Hector9000.conf import mqttTopics
import json
from Hector9000.conf import drinks as drinks
from Hector9000.conf import database as db
import webcolors
import paho.mqtt.client as mqtt
import time
import traceback

VERBOSE_LEVEL = 0


def debug(obj):
    if VERBOSE_LEVEL == 0:
        print("Controller: " + str(obj))


def warning(obj):
    if VERBOSE_LEVEL < 2:
        print("Controller WARNING: " + str(obj))


def error(obj):
    if VERBOSE_LEVEL < 3:
        print("Controller ERROR: " + str(obj))


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
        self.client = mqtt.Client(client_id="HectorController")
        self.hector = remote.HectorRemote()
        self.LED = True
        self.db = db.Database()

    # todo: When drinks are impl in DB this has to be refactored
    def available_drinks_as_JSON(self):
        datalist = []
        idOfDrink = 1
        for drinkitem in drinks.available_drinks:
            data = {
                "name": drinkitem["name"],
                "id": idOfDrink,
                "alcohol": drinks.alcoholic(drinkitem)}
            datalist.append(data)
            idOfDrink = idOfDrink + 1
        return json.dumps({"drinks": datalist})

    # todo: give all Infos for stearing or ....
    def _get_drink_as_JSON(self, msg):
        drinkid = int(msg.payload)
        drink = drinks.available_drinks[drinkid - 1]
        inglist = [{"name": drinks.ingredients[step[1]][0], "ammount": step[2]}
                   for step in drink["recipe"] if step[0] == "ingr"]
        data = {"id": drinkid, "name": drink["name"], "ingredients": inglist}
        debug(data)
        return json.dumps(data)

    def _get_ingredients(self, msg = None):
        debug("get_AllIngredients_asJson")
        return self.db.get_AllIngredients_asJson()

    def _get_servo(self, msg):
        debug("_get_servo: " + msg)
        servoid = int(msg.payload)
        return self.db.get_Servo(servoid)

    def _get_all_servos(self, msg = None):
        debug("get_all_servos")
        return self.db.get_Servos_asJson()

    def _set_servo(self, msg):
        debug("set_Servo")
        ing = json.loads(msg.payload)
        code = ing['code']
        servo = ing['servo']
        return self.db.set_Servo(servo, code)

    def on_connect(self, client, userdata, flags, rc):
        debug("Connected with result code " + str(rc))
        self.client.subscribe(self.TopicPrefix + "#")
        if self.LED:
            self.hector.standart(type=3)

    def on_log(self, client, userdata, level, buf):
        pass  # log("LOG " + str(level) + ": " + str(userdata) + " -- " + str(buf))

    def _do_get_drinks(self, msg):
        self.client.publish(
            self.get_returnTopic(
                msg.topic),
            self.available_drinks_as_JSON())

    def _do_get_drink(self, msg):
        self.client.publish(
            self.get_returnTopic(
                msg.topic),
            self._get_drink_as_JSON(msg))

    def _do_get_ingredients(self, msg):
        self.client.publish(
            self.get_returnTopic(
                msg.topic),
            self._get_ingredients(msg))

    def _do_get_servo(self, msg):
        self.client.publish(
            self.get_returnTopic(
                msg.topic),
            self._get_servo(msg))

    def _do_get_all_servos(self, msg):
        self.client.publish(
            self.get_returnTopic(
                msg.topic),
            self._get_all_servos(msg))

    def _do_set_servo(self, msg):
        self.client.publish(
            self.get_returnTopic(
                msg.topic),
            self._set_servo(msg))

    def _do_dose_drink(self, msg):
        debug("start dosing drink")
        drinkid = int(msg.payload)
        drink = drinks.available_drinks[drinkid - 1]
        # Return ID of drink to identify that drink creation starts
        self.client.publish(self.get_returnTopic(msg.topic), msg.payload)
        progress = 0
        self.client.publish(self.get_progressTopic(msg.topic), progress)
        steps = 100 / len(drink["recipe"])
        if self.LED:
            if "color" in drink.keys():
                self.hector.dosedrink(
                    color=webcolors.name_to_rgb(
                        drink["color"]))
            else:
                self.hector.dosedrink()
        if self.client.want_write():
            self.client.loop_write()
        self.hector.light_on()
        self.hector.arm_out()
        debug("dose drink preparation complete")
        for step in drink["recipe"]:
            debug("dosing progress: " + str(progress))
            if step[0] == "ingr":
                pump = drinks.available_ingredients.index(step[1])
                # todo: cash value
                cupsize = int(self.db.get_Setting("cupsize"))
                ingamount = int((int(step[2]) / 400) * cupsize)
                # Return False to UI ?
                self.hector.valve_dose(
                    index=int(pump),
                    amount=ingamount,
                    cback=self.dose_callback,
                    progress=(
                        progress,
                        steps),
                    topic="Hector9000/doseDrink/progress")
                self.client.publish(
                    self.get_progressTopic(
                        msg.topic), progress + steps)
                if self.client.want_write():
                    self.client.loop_write()
            progress = progress + steps
        debug("dosing drink finished")
        if self.LED:
            self.hector.drinkfinish()
        time.sleep(1)
        self.hector.arm_in()
        self.hector.light_off()
        self.hector.ping(3, 0)
        debug("reset hardware")
        self.client.publish(self.get_progressTopic(msg.topic), "end", qos=1)
        while not self.client.want_write():
            pass
        self.client.loop_write()

    def dose_callback(self, progress):
        self.client.publish(self.TopicPrefix + "doseDrink/progress", progress)

    def on_message(self, client, userdata, msg):
        debug("on_message: topic " + str(msg.topic) +
              ", msg: " + str(msg.payload))
        try:
            currentTopic = msg.topic
            if "/Hardware/" in currentTopic:
                return  # ignore own Hardware calls
            elif currentTopic.endswith("/progress"):
                return  # ignore our own progress messages
            elif currentTopic.endswith("/return"):
                return  # ignore our own return messages
            elif currentTopic == self.TopicPrefix + "standby":
                self.hector.standby()
            elif currentTopic == self.TopicPrefix + "standart":
                color = tuple(msg.payload.decode("utf-8").split(","))
                self.hector.standart(color=color)
            elif currentTopic == self.TopicPrefix + mqttTopics.APITopics.get_drinks:
                self._do_get_drinks(msg)
            elif currentTopic == self.TopicPrefix + mqttTopics.APITopics.get_ingredientsForDrink:
                self._do_get_drink(msg)
            elif currentTopic == self.TopicPrefix + mqttTopics.APITopics.get_ingredientsList:
                self._do_get_ingredients(msg)
            elif currentTopic == self.TopicPrefix + mqttTopics.APITopics.get_servo:
                self._do_get_servo(msg)
            elif currentTopic == self.TopicPrefix + mqttTopics.APITopics.get_allservos:
                self._do_get_all_servos(msg)
            elif currentTopic == self.TopicPrefix + mqttTopics.APITopics.set_servo:
                self._do_set_servo(msg)
            elif currentTopic == self.TopicPrefix + mqttTopics.APITopics.light_on:
                self.hector.light_on()
            elif currentTopic == self.TopicPrefix + mqttTopics.APITopics.light_off:
                self.hector.light_off()
            elif currentTopic == self.TopicPrefix + mqttTopics.APITopics.ring:
                self.hector.ping(2, 1)
            elif currentTopic == self.TopicPrefix + mqttTopics.APITopics.doseDrink:
                self._do_dose_drink(msg)
                pass
            elif currentTopic == self.TopicPrefix + mqttTopics.APITopics.cleanMe:
                # ToDo: Develop proper methode in Server
                for i in range(12):
                    self.hector.clean(i)
                pass
            elif currentTopic == self.TopicPrefix + mqttTopics.APITopics.dryMe:
                for i in range(12):
                    self.hector.dry(i)
                pass
            elif currentTopic == self.TopicPrefix + mqttTopics.APITopics.openAllValves:
                self.hector.all_valve_open()
                pass
            elif currentTopic == self.TopicPrefix + mqttTopics.APITopics.closeAllValves:
                self.hector.all_valve_close()
                pass
            else:
                warning("unknown topic: " + currentTopic +
                        ", msg " + str(msg.payload))

            debug("handled message " + currentTopic + " / " + str(msg.payload))
            while self.client.want_write():
                self.client.loop_write()

        except Exception as e:
            error(str(e) + "\n" + traceback.format_exc())

    def connect(self):
        debug("starting")
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.on_log = self.on_log
        self.client.connect(self.MQTTServer, 1883, 60)
        debug("started")
        while True:
            self.client.loop()


def main():
    controller = HectorController()
    controller.connect()


if __name__ == "__main__":
    main()
