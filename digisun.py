# !/usr/bin/env python
# -*-coding:utf-8-*-
from PyQt4 import QtGui, QtCore
import sys, os
import pymysql
from PyQt4.QtCore import QCoreApplication
import scanner, database, daily_scan, drawing_analyse, login, bulk_analyse
from datetime import date, time, datetime
from PIL import Image
from PIL.ImageQt import ImageQt

###############################################################
###############################################################     
class BulkScanPage(QtGui.QWidget):

    def __init__(self, operator=None):
        super(BulkScanPage, self).__init__()
        
        welcome_msg = QtGui.QLabel('bulk scan...' + operator, self)
        self.layout = QtGui.QGridLayout()
        self.layout.addWidget(welcome_msg, 0, 0, 1, 3)
        self.setLayout(self.layout)
          
class mainWindow(QtGui.QMainWindow):
    " Represent the Qt interface."

    def __init__(self, operator=None, mode_index=0):
        super(mainWindow, self).__init__()
        #width = self.frameGeometry().width()
        #self.setMinimumWidth(width)
        #height = self.frameGeometry().height()
        #self.setMinimumHeight(height)
        #print("frame geometry", width, height)
        
        self.setWindowTitle("DigiSun 2018")

        self.center()
        screen_available_geometry = QtGui.QDesktopWidget()\
                                         .availableGeometry()
        self.setMinimumWidth(screen_available_geometry.width())
        self.setMinimumHeight(screen_available_geometry.height() - 50)
        print("screen available geometry",
              screen_available_geometry.width(),
              screen_available_geometry.height())
        #self.resize(screenShape.width()/5., screenShape.height()/5.)

        self.operator = operator
        print("check opearator ", self.operator)
        
        self.stack = QtGui.QStackedLayout()
        self.daily_scan = daily_scan.DailyScan(self.operator)
        self.analyse_page = bulk_analyse.BulkAnalysePage()
        self.bulk_scan_page = BulkScanPage(self.operator)
        self.drawing_analyse = drawing_analyse.DrawingAnalysePage(self.operator)
 
        self.central_zone = QtGui.QWidget()
        self.central_zone.setLayout(self.stack)
        self.setCentralWidget(self.central_zone)
        
        self.stack.addWidget(self.daily_scan)   
        self.stack.addWidget(self.analyse_page)
        self.stack.addWidget(self.bulk_scan_page)
        self.stack.addWidget(self.drawing_analyse)

        self.set_menuBar()
        self.stack.setCurrentIndex(mode_index)
        
        if mode_index==0:
            self.init_scanner()
        
        self.daily_scan\
            .but_analyse\
            .clicked\
            .connect(lambda : self.stack.setCurrentIndex(3)) 
        self.daily_scan\
            .but_analyse\
            .clicked\
            .connect(self.daily_switch_to_drawing_analyse)

        self.analyse_page\
            .month_list_page\
            .but_select\
            .clicked\
            .connect(self.analyse_page.drawing_selection_per_month)
        self.analyse_page\
            .month_list_page\
            .but_select\
            .clicked\
            .connect(lambda : self.stack.setCurrentIndex(3)) 
        self.analyse_page\
            .month_list_page\
            .but_select\
            .clicked\
            .connect(self.bulk_switch_to_drawing_analyse)
        

    def center(self):
        frameGm = self.frameGeometry()
        screen = QtGui\
                 .QApplication\
                 .desktop()\
                 .screenNumber(QtGui.QApplication\
                               .desktop()\
                               .cursor()\
                               .pos())
        centerPoint = QtGui\
                      .QApplication\
                      .desktop()\
                      .screenGeometry(screen)\
                      .center()
        frameGm.moveCenter(centerPoint)
        self.move(frameGm.topLeft()) 

  
    def daily_switch_to_drawing_analyse(self, lst_drawing):
        lst_drawing = self.daily_scan.set_drawing_information()
        self.drawing_analyse.set_drawing_lst(lst_drawing)
        self.drawing_analyse.set_drawing()

    def bulk_switch_to_drawing_analyse(self, lst_drawing):
        lst_drawing = self.analyse_page.set_drawing_information()
        self.drawing_analyse.set_drawing_lst(lst_drawing)
        self.drawing_analyse.set_drawing()   
        
    def init_scanner(self):
        """"
        Load the library to talk to the scanner.
        For the moment, works only on windows with twain
        """
        if sys.platform == "win32":
            my_scanner = scanner.scanner()
            scanner_name = my_scanner.get_scanner()
            if  my_scanner.set_scanner(scanner_name[0], 'technical_settings'):
                self.daily_scan.set_button_scan_on(my_scanner)
        else:
            print("No scanner on linux..")
                  
    def set_menuBar(self):

        menuBar = QtGui.QMenuBar()
        self.setMenuBar(menuBar)
        
        menu_mode = menuBar.addMenu('Mode')
        menu_about = menuBar.addMenu('About')
        
        action_goTo_login = QtGui.QAction('login', self)
        action_goTo_scanalyse = QtGui.QAction('daily scan', self)
        action_goTo_analyse = QtGui.QAction('bulk analyse', self)
        action_goTo_scan = QtGui.QAction('bulk scan', self)
        action_exit = QtGui.QAction('exit', self)

        action_goTo_login\
            .triggered\
            .connect(lambda: self.change_login())
        action_goTo_scanalyse\
            .triggered\
            .connect(lambda: self.stack.setCurrentIndex(0))
        action_goTo_analyse\
            .triggered\
            .connect(lambda: self.stack.setCurrentIndex(1))
        action_goTo_scan\
            .triggered\
            .connect(lambda: self.stack.setCurrentIndex(2))
        
        action_exit.triggered.connect(app.quit)
        
        menu_mode.addAction(action_goTo_login)
        menu_mode.addAction(action_goTo_scanalyse)
        menu_mode.addAction(action_goTo_analyse)
        menu_mode.addAction(action_goTo_scan)
        menu_mode.addAction(action_exit)

        menuBar.show()

    def change_login(self):
        
        pass

if __name__=='__main__':
    app = QtGui.QApplication(sys.argv)

    login = login.dialog_login()
    login.show()

    if login.exec_() == QtGui.QDialog.Accepted:
        operator_name = login.get_operator()
        print("get op")
        mode_index = login.get_mode()
        print("get mode")
        fen = mainWindow(operator_name, mode_index)
        print("main windows")
        fen.show()
        sys.exit(app.exec_())

    app.quit()
    
