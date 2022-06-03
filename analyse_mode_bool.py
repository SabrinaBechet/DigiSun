# !/usr/bin/env python
# -*-coding:utf-8-*-
"""
DigiSun: a software to transform sunspot drawings into exploitable data. It allows to scan drawings, extract its information and store it in a database.
Copyright (C) 2019 Sabrina Bechet at Royal Observatory of Belgium (ROB)

This file is part of DigiSun.

DigiSun is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

DigiSun is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with DigiSun.  If not, see <https://www.gnu.org/licenses/>.
"""
from PyQt5 import QtCore



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
