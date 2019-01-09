import sys
import time
from kivy.core.text import Label
from kivy.properties import ListProperty, BooleanProperty, ObjectProperty
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from HectorConfig import config
from HectorHardware import HectorHardware
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition


class Configure(Screen):

    def exit(self):
        print("exit")
        root = BoxLayout(orientation='vertical')
        root2 = BoxLayout()
        root2.add_widget(
            Label(text='Do you realy want to close Hector9000 ? \nThere will be no more drinks ....'))
        root.add_widget(root2)

        buttOK = Button(text='OK', font_size=60, size_hint_y=0.15)
        root.add_widget(buttOK)

        buttCancel = Button(text='Cancel', font_size=60, size_hint_y=0.15)
        root.add_widget(buttCancel)

        popup = Popup(title='WAIT !!!', content=root,
                      auto_dismiss=False)

        buttOK.bind(on_press=self.shutdown)
        buttCancel.bind(on_press=popup.dismiss)
        #popup.bind(on_dismiss=self.shutdown)
        popup.open()

    def shutdown(self, instance):
        hector = HectorHardware(config)
        hector.cleanAndExit()
        sys.exit()

    pass


class Cleaner(Screen):
    drytime = 1800
    colorOK = [0, 1, 0, 1]
    colorNOTOK = [1, 0, 0, 1]
    buttonColor = ListProperty([ListProperty(),
                                ListProperty(),
                                ListProperty(),
                                ListProperty(),
                                ListProperty(),
                                ListProperty(),
                                ListProperty(),
                                ListProperty(),
                                ListProperty(),
                                ListProperty(),
                                ListProperty(),
                                ListProperty(),
                                ListProperty(),
                                ListProperty()])

    def __init__(self, **kwargs):
        super(Cleaner, self).__init__(**kwargs)
        count = 0
        while count < 12:
            self.buttonColor[count] = self.colorOK
            count += 1

    def changeButton(self, buttonid):
        if self.buttonColor[buttonid] == self.colorOK:
            self.buttonColor[buttonid] = self.colorNOTOK
        else:
            self.buttonColor[buttonid] = self.colorOK

    popup = None

    def dowork(self, workIndex):
        root = BoxLayout(orientation='vertical')
        self.popup = Popup(title='Life, the Universe, and Everything. There is an answer.', content=root,
                           auto_dismiss=False)
        if workIndex == 1:
            content = Label(
                text='Take a long break: \n\n Hectoe9000 is cleaning and drying himself. \nThis will take some time.')
            self.popup.bind(on_open=self.clean)
        if workIndex == 2:
            content = Label(text='Take a break: \n\n Hectoe9000 is drying. \nThis will take some time.')
            self.popup.bind(on_open=self.dry)

        root.add_widget(content)
        self.popup.open()

    def clean(self, item):
        print("clean")
        i = 0
        hector = HectorHardware(config)
        hector.arm_out()
        for x in self.buttonColor:
            if x == self.colorOK:
                hector.pump_start()
                hector.valve_open(i)
                time.sleep(10)
                times = 0
                while times < 5:
                    hector.valve_open(i,0)
                    time.sleep(1)
                    hector.valve_open(i)
                    time.sleep(10)
                    times += 1
                print("IndexPump: ", i)
                hector.valve_open(i, 0)
                time.sleep(10)
                hector.pump_stop()
            i += 1
        self.popup.dismiss()
        # self.dry()

    def dry(self, item):
        print("dry")
        hector = HectorHardware(config)
        hector.arm_out()
        hector.pump_start()
        i = 0
        for x in self.buttonColor:
            if x == self.colorOK:
                print("IndexPump: ", i)
                hector.valve_open(i)
                time.sleep(self.drytime)
                hector.valve_open(i, 0)
            i += 1
        hector.pump_stop()

    pass
