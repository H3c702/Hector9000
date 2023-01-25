import paho.mqtt.client as mqtt

from Hector9000.utils.Simple_LED_Connector import Simple_LED_Connector as LEDStrip

MQTT_Server = "localhost"
port = 1883
MainTopic = "Hector9000/LEDStrip/"


def debugOut(message):
    print("LED_Strip_Server: => " + message)


def on_message(client, userdata, msg):
    print("message recieved")
    pixels.drinkfinish()
    return
    print("err")
    debugOut("abc")
    # print("LED_Server on_message: " + str(mgs.topic) + " , " + msg.payload.decode("utf-8"))
    topic = msg.topic
    topic = topic.replace(MainTopic, "")
    print("topic: " + topic)
    if topic == "standart":
        print("standart")
        args = tuple(msg.payload.decode("utf-8").split(","))
        if msg.payload.decode("utf-8") == "":
            pixels.standart()
        elif len(args) == 1:
            pixels.standart(type=args[0])
        elif len(args) == 2:
            pixels.standart(type=args[0], color=tuple(
                map(int, args[1].split(";"))))
        else:
            debugOut("Error to many args for standart")
    elif topic == "standby":
        print("standby")
        args = tuple(msg.payload.decode("utf-8").split(","))
        if msg.payload.decode("utf-8") == "":
            pixels.standby()
        elif len(args) == 1:
            pixels.standby(type=args[0])
        elif len(args) == 2:
            pixels.standby(type=args[0], color=tuple(
                map(int, args[1].split(";"))))
        else:
            debugOut("Error to many args for standby")
    elif topic == "dosedrink":
        print("dosedrink")
        args = list(msg.payload.decode("utf-8").split(","))
        if msg.payload.decode("utf-8") == "":
            print("no args")
            pixels.dosedrink()
        elif len(args) == 1:
            print("one arg")
            pixels.dosedrink(type=args[0])
        elif len(args) == 2:
            print("two args")
            print(args[1])
            args[1] = args[1].replace("(", "")
            print(args[1])
            args[1] = args[1].replace(")", "")
            print(args[1])
            # temp = [int(i) for i in args[1].split(";"
            temp = tuple(map(int, args[1].split(";")))
            print(temp)
            pixels.dosedrink(type=args[0], color=temp)
            print("after dose_drink")
        else:
            debugOut("Error to many args for dosedrink")
    elif topic == "drinkfinish":
        print("drinkfinish")
        pixels.finish()
        return
    # args = tuple(msg.payload.decode("utf-8").split(","))
    # if msg.payload.decode("utf-8") is "":
    #    pixels.finish()
    # elif len(args) == 1:
    #    pixels.finish(type=args[0])
    # elif len(args) == 2:
    #    pixels.finish(type=args[0], color=tuple(map(int, args[1].split(";"))))
    # else:
    #    debugOut("Error to many args for drinkfinish")
    else:
        debugOut("Unknown topic")


def on_connect(client, userdata, flags, rc):
    print("Server connected")
    print("subb ret1: " + str(client.subscribe(MainTopic + "drinkfinish", 1)))
    a = MainTopic + "#"


# print("sub ret 2: " + str(client.subscribe(a, 1)))
# client.publish(MainTopic + "abc", "test")

def on_subscribe(client, userdata, mid, granted_qos):
    print("Subscribed to Topic")


print("server started")
pixels = LEDStrip()
client = mqtt.Client(client_id="HectorLED")
client.on_message = on_message
client.on_connect = on_connect
client.on_subscribe = on_subscribe
client.connect(MQTT_Server, port, 60)
client.loop_start()
while True:
    pixels.loop()
