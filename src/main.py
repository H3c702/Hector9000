#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, sys, urllib.request, json, time, math
import PySide2.QtQml
#from OpenGL import GL
from PySide2.QtQuick import QQuickView
from PySide2.QtCore import Qt, QCoreApplication, QUrl, QThread
from PySide2.QtCore import QObject, Signal
from PySide2.QtGui import QGuiApplication
from PySide2.QtQml import QQmlApplicationEngine

from Menu import MenuModel, MenuManager
from Screen import ScreenManager
from Dispensing import DispensingModel

from HectorHardware import HectorHardware
from HectorConfig import config

from drinks import available_drinks, ingredients, actions, alcoholic

isocolors = ["black", "brown", "red", "orange", "yellow", "green", "blue", "purple", "grey", "white"]

def readChannelConfiguration():
    x = json.load(open('conf/channel_config.json'))
    global channelList
    channelList = {}
    for key in x:
        chan = x[key]
        ingr = chan['value']
        if ingr:
            channelList[ingr] = chan['channel']
    #print("channel list:")
    print(channelList)

class DispenserWorker(QThread):

    #This is the signal that will be emitted during the processing.
    #By including int as an argument, it lets the signal know to expect
    #an integer argument when emitting.
    updateGUI = Signal()

    def setBar(self, name, value):
        print("setBar: %s, %d" % (name, value))
        screenMgr.barValue = value
        self.updateGUI.emit()

    def setGauge(self, name, value):
        global content, total
        print("setGauge: %s, %d" % (name, value))
        screenMgr.gaugeValue = 100 * (content+value) / total
        scaleTxt = "%03d g" % (content+value)
        print("scaleTxt: " + scaleTxt)
        screenMgr.contentValue = scaleTxt
        self.updateGUI.emit()

    def __init__(self, drinkId):
        QThread.__init__(self)
        self.drinkId = drinkId

    # A QThread is run by calling its start() function, which calls this run()
    # function in its own thread. 
    def run(self):

        global hector, content, total

        screenMgr.gaugeValue = 0
        screenMgr.buttonMenuVisible = False
        screenMgr.dispensingVisible = True
        self.updateGUI.emit()

        drink = available_drinks[int(self.drinkId)]
        drinkname = drink["name"]
        recipe = drink["recipe"]
        screenMgr.status = drinkname
        print("Drink requested: %s" % drinkname)

        screenMgr.title = "Dispensing " + drinkname
        screenMgr.gaugeValue = 0

        # prepare for recipe
        total = 0
        for step in recipe:
            if step[0] == "ingr":
                _, ingredient, amount = step
                total += amount
                chan = channelList[ingredient]
                # mark ingredient as "to do"
                dispensingModel.items[chan]["channelColor"] = "white"
                dispensingModel.items[chan]["indicatorColor"] = "blue"
                dispensingModel.update()

        self.updateGUI.emit()

        screenMgr.status = "Initializing Hector"
        self.updateGUI.emit()

        hector.finger(0)
        hector.arm_in(self.setBar)
        for i in range(hector.numValves):
            ##print("close valve %d = channel %d" % (i, hector.valveChannels[i]))
            hector.valve_close(hector.valveChannels[i])
        print("Bitte Glas auf die Markierung stellen, Volumen mind. %d ml" % total)
        screenMgr.showAlert("Place your glass on the mark,\nmin. vol. %d ml" % total, isModal=True)
        self.updateGUI.emit()
        # hector.ping(1)
        hector.arm_out(self.setBar)

        content = 0
        for step in recipe:
            if step[0] == "ingr":
                _, ingredient, amount = step
                chan = channelList[ingredient]
                ingName, isAlcoholic = ingredients[ingredient]
                txt = "now adding %d g of %s (%s)" % (amount, ingName, ("" if isAlcoholic else "non-") + "alcoholic")
                print(txt)
                screenMgr.status = txt
                dispensingModel.items[chan]["indicatorColor"] = "orange"
                dispensingModel.update()
                self.updateGUI.emit()

                if 0:
                    screenMgr.alert = txt
                    screenMgr.alertVisible = True
                    self.updateGUI.emit()
                    time.sleep(3)
                    screenMgr.alert = ""
                    screenMgr.alertVisible = False
                    self.updateGUI.emit()

                hector.valve_dose(chan, amount, cback=self.setGauge)
                
                content += amount
                screenMgr.gaugeValue = 100 * content / total
                dispensingModel.items[chan]["indicatorColor"] = "green"
                dispensingModel.update()
            else:
                action, wait = step
                actionName, isAuto = actions[action]
                if isAuto:
                    txt = "automatic action: " + actionName
                    print(txt)
                    screenMgr.status = txt
                    self.updateGUI.emit()
                else:
                    txt = "please " + actionName + " now."
                    print(txt)
                    screenMgr.showAlert(txt, isModal=wait)
        hector.arm_in(self.setBar)
        screenMgr.status = "PING!"
        self.updateGUI.emit()
        hector.ping(3)
        hector.finger(0)

        time.sleep(1)
        print("done.")
        screenMgr.status = "Done."
        self.updateGUI.emit()

        time.sleep(1)
        screenMgr.title = "Main Menu"
        screenMgr.status = "ready."
        screenMgr.gaugeValue = 0
        for chan in range(12):
            dispensingModel.items[chan]["channelColor"] = "grey"
            dispensingModel.items[chan]["indicatorColor"] = "lightgrey"
        dispensingModel.update()

        self.updateGUI.emit()
        screenMgr.buttonMenuVisible = True
        screenMgr.dispensingVisible = False
        self.updateGUI.emit()

def drinkRequested(id):
    screenMgr.buttonMenuVisible = False
    screenMgr.dispensingVisible = True
    global worker
    worker = DispenserWorker(id)
    worker.start()


if __name__ == "__main__":

    global hector
    hector = HectorHardware(config)
    readChannelConfiguration()
    
    #os.environ["QT_QUICK_CONTROLS_STYLE"] = "Material"
    app = QGuiApplication(sys.argv)
    global view
    view = QQuickView()
    view.setResizeMode(QQuickView.SizeRootObjectToView)

    global screenMgr
    screenMgr = ScreenManager()
    view.rootContext().setContextProperty("screenManager", screenMgr)

    menuModel = MenuModel()
    for idx, drink in enumerate(available_drinks):
        menuModel.items.append( {
            'menuId': '%d' % idx, 
            'name': drink["name"] + ("\n\n‰" if alcoholic(drink) else ""), 
            'colorCode': drink["color"] } )
    view.rootContext().setContextProperty("menuModel", menuModel)
    
    menuMgr = MenuManager()
    menuMgr.setAction(drinkRequested)
    view.rootContext().setContextProperty("menuManager", menuMgr)
    
    dispensingModel = DispensingModel(12)
    for idx, ingr in enumerate(channelList):
        dispensingModel.items[idx] = {
            'channelId': idx,
            'channelName': ingredients[ingr][0],
            'channelColor': "grey",
            'indicatorColor': "lightgrey"
        }
    view.rootContext().setContextProperty("dispensingModel", dispensingModel)
    
    qml_file = os.path.join(os.path.dirname(__file__), "UI/main.qml")
    view.setSource(QUrl.fromLocalFile(os.path.abspath(qml_file)))
    
    screenMgr.title = "Main Menu"
    screenMgr.status = "ready."
    screenMgr.gaugeValue = 0
    screenMgr.buttonMenuVisible = True
    screenMgr.dispensingVisible = False
    screenMgr.alertVisible = False

    #print(view.findChild(QObject, "label4"))
    
    if view.status() == QQuickView.Error:
        sys.exit(-1)
    view.show()

    ret = app.exec_()
    del view
    hector.cleanAndExit()

    sys.exit(ret)

