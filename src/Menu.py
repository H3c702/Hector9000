#
#		Menu.py
#
from PySide2.QtCore import Qt, QObject, Signal, Slot, Property, QAbstractListModel


class MenuModel(QAbstractListModel):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.items = []

    def data(self, index, role):
        key = self.roleNames()[role]
        return self.items[index.row()][key.decode('utf-8')]

    def rowCount(self, parent=None):
        return len(self.items)

    def roleNames(self):
        return {Qt.UserRole + 1: b'menuId',
                Qt.UserRole + 2: b'name',
                Qt.UserRole + 3: b'colorCode'}


class MenuManager(QObject):
    clickedIdChanged = Signal()

    def __init__(self):
        QObject.__init__(self)
        self.m_clickedId = ""
        self.clickedIdChanged.connect(self.on_clickedIdChanged)

    def setAction(self, action):
        self.actionFunc = action

    @Property(str, notify=clickedIdChanged)
    def clickedId(self):
        return self.m_clickedId

    @clickedId.setter
    def setclickedId(self, val):
        # if self.m_clickedId == val:
        #    return
        self.m_clickedId = val
        self.clickedIdChanged.emit()

    @Slot()
    def on_clickedIdChanged(self):
        print(self.m_clickedId)
        self.actionFunc(self.m_clickedId)
