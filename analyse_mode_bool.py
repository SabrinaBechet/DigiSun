# !/usr/bin/env python
# -*-coding:utf-8-*-
from PyQt4 import QtCore


class analyseModeBool(QtCore.QObject):

    value_changed = QtCore.pyqtSignal()

    def __init__(self, input_value='False'):
        super(analyseModeBool, self).__init__()
        self._value = input_value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, input_value):
        self._value = input_value
        self.value_changed.emit()

    def set_opposite_value(self):
        if self._value is True:
            self._value = False
            self.value_changed.emit()
        else:
            self._value = True
            self.value_changed.emit()
