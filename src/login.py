# !/usr/bin/env python
# -*-coding:utf-8-*-
"""
DigiSun: a software to transform sunspot drawings into exploitable data. It allows to scan drawings, extract its information and store it in a database.
Copyright (C) 2019 Royal Observatory of Belgium (ROB)

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

import os
import database
import configuration
from PyQt4 import QtGui


class DialogLogin(QtGui.QDialog):
    """
    The DialogLogin class represents the dialog box to enter to DigiSun.
    It displays the archdrawings directory and the database name and
    checks if they exist (in green) or not (in red).
    It also checks that the login exist in the database.
    """
    def __init__(self):
        super(DialogLogin, self).__init__()
        self.setWindowTitle("DigiSun")

        self.layout = QtGui.QGridLayout()
        self.setLayout(self.layout)
        welcome_msg = QtGui.QLabel('Welcome to DigiSun!', self)
        width_widget = 180
        sun_logo = QtGui.QLabel()

        sun_logo_path = "../data/DigiSun_logo.png"
        
        sun_logo.setPixmap(QtGui.QPixmap(sun_logo_path))
        sun_logo.setMinimumWidth(width_widget)
        sun_logo.setMaximumWidth(width_widget)
        sun_logo.setMaximumHeight(width_widget)

        # config_title = QtGui.QLabel("Configuration settings", self)
        config = configuration.Config()
        config.set_archdrawing()
        config.set_database()
        config_archdrawing = QtGui.QLabel("Drawings directory: ")
        self.config_archdrawing_name = QtGui.QLineEdit(self)
        self.config_archdrawing_name.setDisabled(True)
        self.config_archdrawing_name.setText(config.archdrawing_directory)
        self.config_archdrawing_name.setStyleSheet(
            "background-color: rgb(255, 165, 84); color:black")
        
        if os.path.isdir(config.archdrawing_directory):
            self.config_archdrawing_name.setStyleSheet(
                "background-color: rgb(77, 185, 88); color:black")
        
        config_database = QtGui.QLabel("Database name: ")
        self.config_database_name = QtGui.QLineEdit(self)
        self.config_database_name.setDisabled(True)
        self.config_database_name.setText(config.db + '@ ' + config.host)
        self.config_database_name.setStyleSheet(
            "background-color: rgb(255, 165, 84); color:black")
        
        if (config.check_database_connection()):
            self.config_database_name.setStyleSheet(
                "background-color: rgb(77, 185, 88); color:black")
        
        
        self.operator_name = QtGui.QLineEdit(self)
        self.operator_name.setMinimumWidth(width_widget)
        self.operator_name.setMaximumWidth(width_widget)

        operator_selection = QtGui.QLabel('Operator name: ', self)
        operator_selection.setMinimumWidth(width_widget)
        operator_selection.setMaximumWidth(width_widget)
        
        application_selection = QtGui.QLabel('Applications: ', self)
        
        daily_scan_but = QtGui.QPushButton("Daily scan")
        bulk_analyse_but = QtGui.QPushButton("bulk Analyse")
        
        application_selection.setMinimumWidth(width_widget)
        application_selection.setMaximumWidth(width_widget)
        daily_scan_but.setMinimumWidth(width_widget)
        daily_scan_but.setMaximumWidth(width_widget)
        bulk_analyse_but.setMinimumWidth(width_widget)
        bulk_analyse_but.setMaximumWidth(width_widget)

        self.layout.addWidget(sun_logo, 0, 1)
        self.layout.addWidget(welcome_msg, 1, 1)
        #self.layout.addWidget(config_title, 2, 0)
        self.layout.addWidget(config_archdrawing, 2, 0)
        self.layout.addWidget(self.config_archdrawing_name, 2, 1)
        self.layout.addWidget(config_database, 3, 0)
        self.layout.addWidget(self.config_database_name, 3, 1)
        self.layout.addWidget(operator_selection, 4, 0)
        self.layout.addWidget(self.operator_name, 4, 1)
        self.layout.addWidget(application_selection, 5, 0)
        self.layout.addWidget(daily_scan_but, 5, 1)
        self.layout.addWidget(bulk_analyse_but, 5, 2)

        daily_scan_but.setAutoDefault(True)
        bulk_analyse_but.setAutoDefault(True)

        daily_scan_but.clicked.connect(self.handleLogin)
        daily_scan_but.clicked.connect(lambda: self.set_mode(0))
        bulk_analyse_but.clicked.connect(self.handleLogin)
        bulk_analyse_but.clicked.connect(lambda: self.set_mode(1))

        self.center()

    def set_mode(self, mode):
        self.digiSun_mode = mode

    def handleLogin(self):
        uset_db = database.database()
        if (uset_db.exist_in_db('observer',
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
