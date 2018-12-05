#
#	HecUtil
#

from PySide2.QtCore import Qt, QObject, Signal, Slot, Property

class HecProperty(Property):
    def __init__(self, value, name='', type_=None, notify=None):
        if type_ and notify:
            super().__init__(type_, self.getter, self.setter, notify=notify)
        self.value = value
        self.name = name

    def getter(self, inst=None):
        return self.value

    def setter(self, inst=None, value=None):
        self.value = value
        getattr(inst, '_%s_prop_signal_' % self.name).emit(value)

class HecPropertyMeta(type(QObject)):
    def __new__(mcs, name, bases, attrs):
        for key in list(attrs.keys()):
            attr = attrs[key]
            if not isinstance(attr, HecProperty):
                continue
            value = attr.value
            notifier = Signal(type(value))
            attrs[key] = HecProperty(
                value, key, type(value), notify=notifier)
            attrs['_%s_prop_signal_' % key] = notifier
        return super().__new__(mcs, name, bases, attrs)
