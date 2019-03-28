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

from PyQt4 import QtCore, QtGui


class StatusBar(QtGui.QStatusBar):
    """
    Use a Label instead of the Qt status bar to have more precise control
    on the way the text is deplayed.
    """
    def __init__(self):
        super(StatusBar, self).__init__()

        self.name = QtGui.QLabel()
        self.name.setStyleSheet(
            "QLabel { background-color : red; color : blue; }")
        self.name.setAlignment(QtCore.Qt.AlignHCenter)
        self.name.setMinimumSize(self.name.sizeHint())
        self.comment = QtGui.QLabel()
        self.comment.setIndent(3)

        self.addWidget(self.name)
        self.addWidget(self.comment)

    def clean(self):
        self.name.setText("")
        self.comment.setText("")
