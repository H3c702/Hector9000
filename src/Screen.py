#
#		Screen.py
#
from PySide2.QtCore import Qt, QObject, Signal, Slot, Property, QAbstractListModel

from HecUtil import HecProperty, HecPropertyMeta

import time

class ScreenManager(QObject, metaclass=HecPropertyMeta):

    updateGUI = Signal()
    
    title = HecProperty('TITLE')
    status = HecProperty('STATUS')
    alert = HecProperty('ALERT')
    gaugeValue = HecProperty(50.0)
    barValue = HecProperty(50.0)
    contentValue = HecProperty("000 g")
    buttonMenuVisible = HecProperty(True)
    dispensingVisible = HecProperty(False)
    alertVisible = HecProperty(True)
    alertButtonVisible = HecProperty(True)

    @Slot()
    def debug(self):
        self.foo = 'I modified foo!'

    
    def setAction(self, action):
        self.actionFunc = action

    def defaultActionFunc(self, value):
        print("actionFunc: %s" % value)
        
    def showAlert(self, txt, isModal):
        
        self.alert = txt
        self.alertVisible = True
        self.alertButtonVisible = isModal
        self.updateGUI.emit()
        if isModal:
            time.sleep(3)
        
        self.alert = ""
        self.alertVisible = False
        self.updateGUI.emit()


    def __init__(self):
        QObject.__init__(self)
        #self.Changed.connect(self.on_Changed)
        self.setAction(self.defaultActionFunc)
        #self.debug()
        #self.foo = "TEST!"
    
    

