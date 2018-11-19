# !/usr/bin/env python
# -*-coding:utf-8-*-
import os
from PyQt5 import QtCore, QtWidgets

class StatusBar(QtWidgets.QStatusBar):
    """
    Use a Label instead of the Qt status bar to have more precise control
    on the way the text is deplayed.
    """
    def __init__(self):
        super(StatusBar, self).__init__()

        self.name = QtWidgets.QLabel()
        self.name.setStyleSheet(
            "QLabel { background-color : red; color : blue; }");
        self.name.setAlignment(QtCore.Qt.AlignHCenter)
        self.name.setMinimumSize(self.name.sizeHint())
        self.comment = QtWidgets.QLabel()
        self.comment.setIndent(3)

        self.addWidget(self.name)
        self.addWidget(self.comment)

    def clean(self):
        print("cleaning function..")
        self.name.setText("")
        self.comment.setText("")
