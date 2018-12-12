#
#		Dispensing.py
#
from PySide2.QtCore import Qt, QObject, Signal, Slot, Property, QAbstractListModel

from HecUtil import HecProperty


class DispensingModel(QAbstractListModel):

    def __init__(self, num, parent=None):
        super().__init__(parent)
        self.items = [{'channelId': -1, 'channelName': "-",
                       'channelColor': "black", 'indicatorColor': "white"}] * 12

    def data(self, index, role):
        key = self.roleNames()[role]
        return self.items[index.row()][key.decode('utf-8')]

    def rowCount(self, parent=None):
        return len(self.items)

    def roleNames(self):
        return {Qt.UserRole + 1: b'channelId',
                Qt.UserRole + 2: b'channelName',
                Qt.UserRole + 3: b'channelColor',
                Qt.UserRole + 4: b'indicatorColor'}

    def update(self):
        # for it in self.items:
        #    if it["indicatorColor"] != "lightblue":
        #        print(it)
        self.dataChanged.emit(self.createIndex(0, 0), self.createIndex(999, 999))
        # self.modelReset.emit()


class DispensingManager(QObject):

    def __init__(self):
        QObject.__init__(self)

    def setAction(self, action):
        self.actionFunc = action
