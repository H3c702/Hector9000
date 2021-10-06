#!/usr/bin/env python3
# -*- coding: utf8 -*-
##
#   LEDStripAPI.py       API interface class for Hector9000 LED Strip
#

import abc


def debugOut(name: str, value: str):
    print("=> %s: %d" % (name, value))


class LEDStripAPI(object, metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def __init__(self):
        pass

    @abc.abstractmethod
    def standart(self, color=(80, 80, 30), type = 0):
        pass

    @abc.abstractmethod
    def dosedrink(self, color=(20, 20, 255), type = 0):
        pass

    @abc.abstractmethod
    def drinkfinish(self, color=(80, 80, 30), type = 0):
        pass

    @abc.abstractmethod
    def standby(self, color=(80, 80, 30), type = 0):
        pass
