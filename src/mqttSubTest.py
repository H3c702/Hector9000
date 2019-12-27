

import paho.mqtt.client as mqtt
import traceback


# settings
class HectorController:
    MQTTServer = "localhost"
    TopicPrefix = "Hector9000/"
    initDone = False
    client = mqtt.Client()

    @staticmethod
    def get_returnTopic(topic):
        return topic + "/return"

    @staticmethod
    def get_progressTopic(topic):
        return topic + "/progress"

    def __init__(self):
        pass

    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code " + str(rc))
        client.subscribe(self.TopicPrefix + "#")
        print("done subscribing")

    def on_log(self, client, userdata, level, buf):
        print("LOG " + str(level) + ": " + str(userdata) + " -- " + str(buf))

    def on_message2(self, client, userdata, msg):
        print("on_message: topic " + str(msg.topic) + ", msg: " + str(msg.payload))

    def on_message(self, client, userdata, msg):
        print("on_message: topic " + str(msg.topic) + ", msg: " + str(msg.payload))
        try:
            global currentTopic
            currentTopic = msg.topic

            if currentTopic.endswith("/progress"):
                return  # ignore our own progress messages
            elif currentTopic.endswith("/return"):
                return  # ignore our own return messages

            # low-level
            elif currentTopic == self.TopicPrefix + "get_drinks":
                self.do_get_drinks(msg)
            elif currentTopic == self.TopicPrefix + "get_ingredients":
                self.do_get_drink(msg)
                pass
            elif currentTopic == self.TopicPrefix + "light_on":
                Hector.light_on()
                pass
            elif currentTopic == self.TopicPrefix + "light_off":
                Hector.light_off()
                pass

            # high-level
            elif currentTopic == self.TopicPrefix + "ring":
                Hector.ping()
                pass
            elif currentTopic == self.TopicPrefix + "doseDrink":
                pass
            elif currentTopic == self.TopicPrefix + "cleanMe":
                #ToDo: Develop proper methode in Server
                Hector.all_valve_open()
                Hector.cleanAndExit()
                pass
                # clean(msg)
            elif currentTopic == self.TopicPrefix + "dryMe":
                pass
            elif currentTopic == self.TopicPrefix + "openAllValves":
                Hector.all_valve_open()
                pass
            elif currentTopic == self.TopicPrefix + "closeAllValves":
                Hector.all_valve_close()
                pass
            # unknown
            else:
                print("unknown topic: " + currentTopic + ", msg " + str(msg.payload))

            print("done with msg " + currentTopic + " / " + str(msg.payload))

        except Exception as e:
            print("Error! " + str(e))
            print(traceback.format_exc())

    def connect(self):
        # main program
        print("register callbacks")
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.on_log = self.on_log

        print("connect to server")
        self.client.connect(self.MQTTServer, 1883, 60)

        while True:
            self.client.loop()

print("start test");
hc = HectorController()
hc.connect()
print("done.")

