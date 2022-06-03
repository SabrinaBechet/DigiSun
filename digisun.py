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

import sys
import login
import daily_scan
import bulk_analyse
#import configuration
import drawing_analyse
from PyQt5 import QtGui, QtWidgets, QtCore

__author__ = "Sabrina Bechet"
__email__ = "digisun@oma.be"
__date__ = "April 2019"
__version__ = "1.0.0"

#sys.stderr = open('data/err.txt', 'w')
#sys.stdout = open("data/file.txt", "w")

class BulkScanPage(QtWidgets.QWidget):
    """
    Module to make many scans in a row.
    If needed, should be expanded later
    """
    def __init__(self, operator=None):
        super(BulkScanPage, self).__init__()

        welcome_msg = QtWidgets.QLabel('bulk scan...' + operator, self)
        self.layout = QtWidgets.QGridLayout()
        self.layout.addWidget(welcome_msg, 0, 0, 1, 3)
        self.setLayout(self.layout)


class mainWindow(QtWidgets.QMainWindow):
    """ Represent the Qt interface. It consists of stacked pages:
    index 0 : daily scan
    index 1 : analyse page
    index 2 : drawing analyse
    """
    def __init__(self, config, operator=None, mode_index=0):
        super(mainWindow, self).__init__()
        self.setWindowTitle("DigiSun")
        self.center()
        #self.showMaximized()
        screen_available_geometry = QtWidgets.QDesktopWidget()\
                                         .availableGeometry()
        self.setMinimumWidth(screen_available_geometry.width()/2.)
        self.setMinimumHeight(screen_available_geometry.height()/2.)
        self.setMaximumWidth(screen_available_geometry.width())
        self.setMaximumHeight(screen_available_geometry.height() - 50)

        self.operator = operator

        self.config = config
        

        self.stack = QtWidgets.QStackedLayout()
        self.daily_scan = daily_scan.DailyScan(self.config, self.operator)
        self.analyse_page = bulk_analyse.BulkAnalysePage(self.config)
        #self.bulk_scan_page = BulkScanPage(self.operator)
        self.drawing_analyse = drawing_analyse\
            .DrawingAnalysePage(config, self.operator)

        self.central_zone = QtWidgets.QWidget()
        self.central_zone.setLayout(self.stack)
        self.setCentralWidget(self.central_zone)

        self.stack.addWidget(self.daily_scan)
        self.stack.addWidget(self.analyse_page)
        self.stack.addWidget(self.drawing_analyse)
        #self.stack.addWidget(self.bulk_scan_page)
        
        self.set_menuBar()
        self.stack.setCurrentIndex(mode_index)

        self.daily_scan.but_analyse.clicked.connect(
            lambda: self.stack.setCurrentIndex(2))
        self.daily_scan.but_analyse.clicked.connect(
            self.daily_switch_to_drawing_analyse)
        self.daily_scan.but_add.clicked.connect(
            lambda: self.daily_switch_to_drawing_analyse(loc=1))

        self.analyse_page.date_selection_page.but_select.clicked.connect(
            self.selection_analyse_view)
        
        self.analyse_page.month_list_page.but_select.clicked.connect(
            self.select_month_analyse_view)
        
        self.analyse_page.day_list_page.but_select.clicked.connect(
            self.select_day_analyse_view)

    def selection_analyse_view(self):
        good_selection = self.analyse_page.get_selection_interval()
        if good_selection:
            self.stack.setCurrentIndex(2)
            self.bulk_switch_to_drawing_analyse()
        
    def select_day_analyse_view(self):
        day_selected = self.analyse_page.get_day()
        if day_selected:
            self.stack.setCurrentIndex(2)
            self.bulk_switch_to_drawing_analyse()
        
    def select_month_analyse_view(self):
        month_selected = self.analyse_page.get_day_interval()
        if month_selected:
            self.stack.setCurrentIndex(2)
            self.bulk_switch_to_drawing_analyse()
            
    def center(self):
        frameGm = self.frameGeometry()
        desktop_rect = QtWidgets.QDesktopWidget().availableGeometry()
        center = desktop_rect.center()
        frameGm.moveCenter(QtCore.QPoint(center.x() - self.width()*0.5,
                                         center.y() - self.height()*0.5))
        self.move(frameGm.topLeft())

    def daily_switch_to_drawing_analyse(self, loc=0):
        lst_drawing = self.daily_scan.set_drawing_information(loc)
        print(lst_drawing)
        self.drawing_analyse.set_drawing_lst(lst_drawing)
        self.drawing_analyse.set_drawing()
        self.drawing_analyse.start_calibration()

    def bulk_switch_to_drawing_analyse(self):
        lst_drawing = self.analyse_page.set_drawing_information()
        self.drawing_analyse.set_drawing_lst(lst_drawing)
        self.drawing_analyse.set_drawing()


    def set_menuBar(self):
        menuBar = QtWidgets.QMenuBar()
        menuBar.setNativeMenuBar(False)
        self.setMenuBar(menuBar)

        menu_mode = menuBar.addMenu('Mode')
        #menu_parameters = menuBar.addMenu('Config')
        menu_help = menuBar.addMenu('Help')

        #action_change_directory = QtWidgets.QAction('Drawings directory', self)
        #action_change_directory.triggered.connect(self.change_config_file)
        
        action_goTo_daily_scan= QtWidgets.QAction('Daily scan', self)
        action_goTo_analyse = QtWidgets.QAction('Bulk analyse', self)

        action_goTo_analyse.setShortcuts(QtGui.QKeySequence("b"))
        action_exit = QtWidgets.QAction('Exit', self)

        action_about = QtWidgets.QAction('About', self)

        action_goTo_daily_scan.triggered.connect(
            lambda: self.stack.setCurrentIndex(0))
        action_goTo_analyse.triggered.connect(
            lambda: self.stack.setCurrentIndex(1))
        action_exit.triggered.connect(app.quit)

        action_about.triggered.connect(
            lambda: QtWidgets.QMessageBox.about(
                self,
                "DigiSun",
                "<h2 >About DigiSun </h2>"+
                " <p> Copyright (c) 2019 Sabrina Bechet at Royal Observatory of Belgium (ROB)." +
                " <p> This is a software to transform sunspot drawings into exploitable data. " + 
                " It allows to scan drawings, extract its information and store it in a database." +
                "<p> Version: 1.0.0. (30/03/2019)"+
                "<p> Contact: digisun@oma.be " +
                "<p> Contributors:  see README."))

        #menu_parameters.addAction(action_change_directory)
        
        menu_mode.addAction(action_goTo_daily_scan)
        menu_mode.addAction(action_goTo_analyse)
        menu_mode.addAction(action_exit)

        menu_help.addAction(action_about)

        menuBar.show()
        
if __name__ == '__main__':

    app = QtWidgets.QApplication(sys.argv)

    login = login.DialogLogin()
    login.show()

    if login.exec_() == QtWidgets.QDialog.Accepted:
        operator_name = login.get_operator()
        mode_index = login.get_mode()
        
        config = login.get_config()
        
        fen = mainWindow(config, operator_name, mode_index)

        fen.show()
        sys.exit(app.exec_())

    app.quit()
