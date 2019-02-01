# !/usr/bin/env python
# -*-coding:utf-8-*-
"""
The DialogLogin class represents the dialiog box to enter the user login.
It checks if the login exist in the database
"""
import database
from PyQt4 import QtGui


class DialogLogin(QtGui.QDialog):

    def __init__(self):
        super(DialogLogin, self).__init__()
        self.setWindowTitle("DigiSun")

        self.layout = QtGui.QGridLayout()
        self.setLayout(self.layout)
        welcome_msg = QtGui.QLabel('Welcome in DigiSun!', self)
        width_widget = 120
        sun_logo = QtGui.QLabel()

        sun_logo.setPixmap(QtGui.QPixmap("DigiSun_logo2.png"))
        sun_logo.setMinimumWidth(width_widget)
        sun_logo.setMaximumWidth(width_widget)
        sun_logo.setMaximumHeight(width_widget)

        self.operator_name = QtGui.QLineEdit(self)
        self.operator_name.setMinimumWidth(width_widget)
        self.operator_name.setMaximumWidth(width_widget)
        operator_selection = QtGui.QLabel('Operator name: ', self)
        operator_selection.setMinimumWidth(width_widget)
        operator_selection.setMaximumWidth(width_widget)

        application_selection = QtGui.QLabel('Applications: ', self)
        daily_scan_but = QtGui.QPushButton("daily scan")
        bulk_analyse_but = QtGui.QPushButton("bulk analyse")

        # not developped yet
        # bulk_scan_but = QtGui.QPushButton("bulk scan")

        application_selection.setMinimumWidth(width_widget)
        application_selection.setMaximumWidth(width_widget)
        daily_scan_but.setMinimumWidth(width_widget)
        daily_scan_but.setMaximumWidth(width_widget)
        bulk_analyse_but.setMinimumWidth(width_widget)
        bulk_analyse_but.setMaximumWidth(width_widget)
        # bulk_scan_but.setMinimumWidth(width_widget)
        # bulk_scan_but.setMaximumWidth(width_widget)

        self.layout.addWidget(sun_logo, 0, 1)
        self.layout.addWidget(welcome_msg, 1, 1)
        self.layout.addWidget(operator_selection, 2, 0)
        self.layout.addWidget(self.operator_name, 2, 1)
        self.layout.addWidget(application_selection, 3, 0)
        self.layout.addWidget(daily_scan_but, 3, 1)
        self.layout.addWidget(bulk_analyse_but, 3, 2)
        # self.layout.addWidget(bulk_scan_but, 4, 1)

        daily_scan_but.setAutoDefault(True)
        bulk_analyse_but.setAutoDefault(True)
        # bulk_scan_but.setAutoDefault(True)

        daily_scan_but.clicked.connect(self.handleLogin)
        daily_scan_but.clicked.connect(lambda: self.set_mode(0))
        bulk_analyse_but.clicked.connect(self.handleLogin)
        bulk_analyse_but.clicked.connect(lambda: self.set_mode(1))
        # bulk_scan_but.clicked.connect(self.handleLogin)
        # bulk_scan_but.clicked.connect(lambda: self.set_mode(2))

        self.center()

    def set_mode(self, mode):
        self.digiSun_mode = mode

    def handleLogin(self):
        uset_db = database.database()
        if (uset_db.exist_in_db('observers',
                                'name',
                                self.operator_name.text())):
            self.accept()
        else:
            QtGui.QMessageBox.warning(
                self, 'Error', 'Bad operator name')

    def get_operator(self):
        return self.operator_name.text()

    def get_mode(self):
        return self.digiSun_mode

    def center(self):
        frameGm = self.frameGeometry()
        screen = QtGui.QApplication\
                      .desktop()\
                      .screenNumber(
                          QtGui.QApplication.desktop().cursor().pos())
        centerPoint = QtGui.QApplication\
                           .desktop().screenGeometry(screen).center()
        frameGm.moveCenter(centerPoint)
        self.move(frameGm.topLeft())
