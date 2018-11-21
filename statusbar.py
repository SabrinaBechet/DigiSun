# !/usr/bin/env python
# -*-coding:utf-8-*-
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
            "QLabel { background-color : red; color : blue; }");
        self.name.setAlignment(QtCore.Qt.AlignHCenter)
        self.name.setMinimumSize(self.name.sizeHint())
        self.comment = QtGui.QLabel()
        self.comment.setIndent(3)

        self.addWidget(self.name)
        self.addWidget(self.comment)

    def clean(self):
        #print("cleaning function..")
        self.name.setText("")
        self.comment.setText("")
