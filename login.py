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
from PyQt5 import QtGui, QtWidgets

__author__ = "Sabrina Bechet"
__date__ = "April 2019"

class DialogLogin(QtWidgets.QDialog):
    """
    The DialogLogin class represents the dialog box to enter to DigiSun.
    It displays the archdrawings directory and the database name and
    checks if they exist (in green) or not (in red).
    It also checks that the login exist in the database.
    """
    def __init__(self):
        super(DialogLogin, self).__init__()
        self.setWindowTitle("DigiSun")

        self.layout = QtWidgets.QGridLayout()
        self.setLayout(self.layout)
        welcome_msg = QtWidgets.QLabel('Welcome to DigiSun!', self)
        width_widget = 180
        sun_logo = QtWidgets.QLabel()

        sun_logo_path = "icons/DigiSun_logo.png"
        
        sun_logo.setPixmap(QtGui.QPixmap(sun_logo_path))
        sun_logo.setMinimumWidth(width_widget)
        sun_logo.setMaximumWidth(width_widget)
        sun_logo.setMaximumHeight(width_widget)
    
        self.config = configuration.Config()
        self.config.set_archdrawing()
        self.config.set_database()

        config_archdrawing = QtWidgets.QLabel("Drawings directory: ")
        self.config_archdrawing_name = QtWidgets.QLineEdit(self)
        
        config_database = QtWidgets.QLabel("Database name: ")
        self.config_database_name = QtWidgets.QLineEdit(self)
        
        self.operator_name = QtWidgets.QLineEdit(self)
        self.operator_name.setMinimumWidth(width_widget)
        self.operator_name.setMaximumWidth(width_widget)

        operator_selection = QtWidgets.QLabel('Operator name: ', self)
        operator_selection.setMinimumWidth(width_widget)
        operator_selection.setMaximumWidth(width_widget)
        
        application_selection = QtWidgets.QLabel('Applications: ', self)
        
        daily_scan_but = QtWidgets.QPushButton("Daily scan")
        bulk_analyse_but = QtWidgets.QPushButton("Bulk analyse")
        change_config_but = QtWidgets.QPushButton("Change config file")
        
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
        self.layout.addWidget(change_config_but, 6, 1)

        daily_scan_but.setAutoDefault(True)
        bulk_analyse_but.setAutoDefault(True)

        daily_scan_but.clicked.connect(self.handleLogin)
        daily_scan_but.clicked.connect(lambda: self.set_mode(0))
        bulk_analyse_but.clicked.connect(self.handleLogin)
        bulk_analyse_but.clicked.connect(lambda: self.set_mode(1))
        change_config_but.clicked.connect(self.change_config_file)

        self.center()

        self.set_config_info()
        
    def set_config_info(self):
        
        self.config_database_name.setDisabled(True)
        self.config_database_name.setText(self.config.db + '@ ' +
                                          self.config.host + ':' +
                                          str(self.config.port))
        self.config_database_name.setStyleSheet(
            "background-color: rgb(255, 165, 84); color:black")
        if (self.config.check_database_connection()):
            self.config_database_name.setStyleSheet(
                "background-color: rgb(77, 185, 88); color:black")
        
        self.config_archdrawing_name.setDisabled(True)
        self.config_archdrawing_name.setText(self.config.archdrawing_directory)
        self.config_archdrawing_name.setStyleSheet(
            "background-color: rgb(255, 165, 84); color:black")
        if os.path.isdir(self.config.archdrawing_directory):
            self.config_archdrawing_name.setStyleSheet(
                "background-color: rgb(77, 185, 88); color:black")

    def get_config(self):
        return self.config
        
    def change_config_file(self):

        config_filename = QtWidgets.QFileDialog.getOpenFileName(
            self,
            "configuration file",
            "",
            "Text files (*.ini)")
        self.config = configuration.Config(config_filename[0])

        self.config.set_archdrawing()
        self.config.set_database()
        self.set_config_info()
    
    def set_mode(self, mode):
        self.digiSun_mode = mode

    def handleLogin(self):
        uset_db = database.database(self.config)
        if (uset_db.exist_in_db('observer',
                                'name',
                                self.operator_name.text())):
            self.accept()
        else:
            QtWidgets.QMessageBox.warning(
                self, 'Error', 'Bad operator name')

    def get_operator(self):
        return self.operator_name.text()

    def get_mode(self):
        return self.digiSun_mode

    def center(self):
        frameGm = self.frameGeometry()
        screen = QtWidgets.QApplication\
                      .desktop()\
                      .screenNumber(
                          QtWidgets.QApplication.desktop().cursor().pos())
        centerPoint = QtWidgets.QApplication\
                           .desktop().screenGeometry(screen).center()
        frameGm.moveCenter(centerPoint)
        self.move(frameGm.topLeft())
