# Nee to install pip install console-menu
from consolemenu import *
from consolemenu.format import *
from consolemenu.items import *

import time

#from Hector9000.conf import HectorConfig as config

from Hector9000.HectorHardware import HectorHardware as Hector
#from Hector9000.HectorSimulator import HectorSimulator as Hector


def Main():
    menu_format = MenuFormatBuilder().set_border_style_type(MenuBorderStyleType.HEAVY_BORDER) \
        .set_prompt("SELECT>") \
        .set_title_align('center') \
        .set_subtitle_align('center') \
        .set_left_margin(4) \
        .set_right_margin(4) \
        .show_header_bottom_border(True)

    menu = ConsoleMenu("Hector9000 - HardwareTestingTool", "Test the hardware of it´s function.", formatter=menu_format)
    menu.clear_screen_before_render = False

    menu.append_item(FunctionItem("Test Arm", testArm))
    menu.append_item(FunctionItem("Test Pump", testPump))
    menu.append_item(FunctionItem("Test Vents", testVent))
    menu.append_item(FunctionItem("Test Scale", testScale()))
    menu.show()


def testVent():
    print("Test Vents:")
    for vnum in range(12):
        print("Open Valve:" + vnum + " for 1 sec")
        Hector.valve_open(vnum)
        time.sleep(1)
        print("Close Valve:" + vnum)
        Hector.valve_close(vnum)

    print("Test End.")


def testScale():
    print("Test Scale:")
    print("Tare:")
    Hector.scale_tare()
    print("Add weight.")
    print("Wait 10 sec.")
    time.sleep(5)
    print("Radout scale")
    readout = Hector.scale_readout()
    print(readout)


def testPump():
    print("Test Pump:")
    print("Start pump for 3 sec")
    Hector.pump_start()
    time.sleep(3)
    print("Stop Pump.")
    Hector.pump_stop()


def testArm():
    print("Test Arm ")
    print("Move Out")
    Hector.arm_out()
    print("Wait 5 sec")
    time.sleep(5)
    print("Arm Pos:" + Hector.arm_isInOutPos())
    print("Move in")
    Hector.arm_in()


if __name__ == "__main__":
    Main()
