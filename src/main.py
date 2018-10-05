from kivy.app import App
from kivy.config import Config
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from MyPanelWidgetScreen import MyPanelWidget
from ConfigureScreen import Configure

Config.set('graphics', 'fullscreen', '0') # 'auto' -> Fullscreen | '0' -> NormalMode


class MyScreenManager(ScreenManager):
    pass


myfile = open('windowconf', 'r')

root_widget = Builder.load_string(myfile.read())


class Panel(App):
    def build(self):
        return root_widget


if __name__ == "__main__":
    Panel().run()
