# !/usr/bin/env python
# -*-coding:utf-8-*-
from PyQt4 import QtGui, QtCore
import sys
import login, daily_scan , bulk_analyse, drawing_analyse

class BulkScanPage(QtGui.QWidget):

    def __init__(self, operator=None):
        super(BulkScanPage, self).__init__()
        
        welcome_msg = QtGui.QLabel('bulk scan...' + operator, self)
        self.layout = QtGui.QGridLayout()
        self.layout.addWidget(welcome_msg, 0, 0, 1, 3)
        self.setLayout(self.layout)

        
class mainWindow(QtGui.QMainWindow):
    """ Represent the Qt interface. It consists of stacked pages:
    index 0 : daily scan
    index 1 : analyse page
    index 2 : bulk scan
    index 3 : drawing analyse
    """
    def __init__(self, operator=None, mode_index=0):
        super(mainWindow, self).__init__()
        self.setWindowTitle("DigiSun 2018")
        self.center()
        screen_available_geometry = QtGui.QDesktopWidget()\
                                         .availableGeometry()
        self.setMaximumWidth(screen_available_geometry.width())
        self.setMaximumHeight(screen_available_geometry.height() - 50)
        self.operator = operator
        
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
        
        self.daily_scan.but_analyse.clicked.connect(
            lambda : self.stack.setCurrentIndex(3)) 
        self.daily_scan.but_analyse.clicked.connect(
            self.daily_switch_to_drawing_analyse)

        self.analyse_page.month_list_page.but_select.clicked.connect(
            self.analyse_page.drawing_selection_per_month)
        self.analyse_page.month_list_page.but_select.clicked.connect(
            lambda : self.stack.setCurrentIndex(3)) 
        self.analyse_page.month_list_page.but_select.clicked.connect(
            self.bulk_switch_to_drawing_analyse)
        
    def center(self):
        frameGm = self.frameGeometry()
        screen = QtGui\
            .QApplication\
            .desktop()\
            .screenNumber(QtGui.QApplication\
                          .desktop()\
                          .cursor()\
                          .pos())
        desktop_rect = QtGui.QDesktopWidget().availableGeometry()
        center = desktop_rect.center()
        frameGm.moveCenter(QtCore.QPoint(center.x()  - self.width()*0.5,
                                         center.y() - self.height()*0.5))
        self.move(frameGm.topLeft()) 

  
    def daily_switch_to_drawing_analyse(self, lst_drawing):
        lst_drawing = self.daily_scan.set_drawing_information()
        self.drawing_analyse.set_drawing_lst(lst_drawing)
        self.drawing_analyse.set_drawing()
        self.drawing_analyse.start_calibration()

    def bulk_switch_to_drawing_analyse(self, lst_drawing):
        lst_drawing = self.analyse_page.set_drawing_information()
        print("list drawing:")
        print(lst_drawing, type(lst_drawing))
        self.drawing_analyse.set_drawing_lst(lst_drawing)
        self.drawing_analyse.set_drawing()   
                      
    def set_menuBar(self):

        menuBar = QtGui.QMenuBar()
        self.setMenuBar(menuBar)
        
        menu_mode = menuBar.addMenu('Mode')
        menu_about = menuBar.addMenu('About')
        
        #action_goTo_login = QtGui.QAction('login', self)
        action_goTo_scanalyse = QtGui.QAction('daily scan', self)
        action_goTo_analyse = QtGui.QAction('bulk analyse', self)
        action_goTo_scan = QtGui.QAction('bulk scan', self)
        action_exit = QtGui.QAction('exit', self)

        #action_goTo_login.triggered.connect(lambda: self.change_login())
        action_goTo_scanalyse.triggered.connect(
            lambda: self.stack.setCurrentIndex(0))
        action_goTo_analyse.triggered.connect(
            lambda: self.stack.setCurrentIndex(1))
        action_goTo_scan.triggered.connect(
            lambda: self.stack.setCurrentIndex(2))
        
        action_exit.triggered.connect(app.quit)
        
        #menu_mode.addAction(action_goTo_login)
        menu_mode.addAction(action_goTo_scanalyse)
        menu_mode.addAction(action_goTo_analyse)
        menu_mode.addAction(action_goTo_scan)
        menu_mode.addAction(action_exit)

        menuBar.show()

    """def change_login(self):
        
        pass
    """
    
if __name__=='__main__':
    app = QtGui.QApplication(sys.argv)
    login = login.dialog_login()
    login.show()

    if login.exec_() == QtGui.QDialog.Accepted:
        operator_name = login.get_operator()
        mode_index = login.get_mode()
        fen = mainWindow(operator_name, mode_index)
        fen.show()
        sys.exit(app.exec_())

    app.quit()
    
