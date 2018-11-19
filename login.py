# !/usr/bin/env python
# -*-coding:utf-8-*-
from PyQt5 import QtGui, QtCore, QtWidgets
import sys, os
import database


class dialog_login(QtWidgets.QDialog):

    def __init__(self):
        super(dialog_login, self).__init__()
        
        #width = self.frameGeometry().width()
        #self.setMinimumWidth(500)
        #height = self.frameGeometry().height()
        #self.setMinimumHeight(500)
        #self.resize(width, height)
        self.setWindowTitle("DigiSun 2018")
        
        self.layout = QtWidgets.QGridLayout()
        self.setLayout(self.layout)
        welcome_msg = QtWidgets.QLabel('DigiSun 2018', self)
        width_widget = 150
        sun_logo = QtWidgets.QLabel()
        
        sun_logo.setPixmap(QtGui.QPixmap("sun-logo-th.png"))
        sun_logo.setMinimumWidth(width_widget)
        sun_logo.setMaximumWidth(width_widget)
        sun_logo.setMaximumHeight(width_widget)
        #layout_welcome.addWidget(welcome_msg)
        #layout_welcome.addWidget(sun_logo)

        self.operator_name = QtWidgets.QLineEdit(self)
        self.operator_name.setMinimumWidth(width_widget)
        self.operator_name.setMaximumWidth(width_widget)
        #form_layout = QtWidgets.QFormLayout()
        #form_layout.addRow('Welcome in DigiSun', sun_logo)
        #form_layout.addRow('operator name:', self.operator_name)
        operator_selection = QtWidgets.QLabel('operator name: ', self)
        operator_selection.setMinimumWidth(width_widget)
        operator_selection.setMaximumWidth(width_widget)
        #widget_form = QtWidgets.QWidget()
        #widget_form.setLayout(form_layout)
        
        #self.layout.addLayout(layout_welcome)
        
        application_selection = QtWidgets.QLabel('Applications: ', self)
        daily_scan_but = QtWidgets.QPushButton("daily scan")
        bulk_analyse_but = QtWidgets.QPushButton("bulk analyse")
        bulk_scan_but = QtWidgets.QPushButton("bulk scan")
        
        application_selection.setMinimumWidth(width_widget)
        application_selection.setMaximumWidth(width_widget)
        daily_scan_but.setMinimumWidth(width_widget)
        daily_scan_but.setMaximumWidth(width_widget)      
        bulk_analyse_but.setMinimumWidth(width_widget)
        bulk_analyse_but.setMaximumWidth(width_widget)
        bulk_scan_but.setMinimumWidth(width_widget)
        bulk_scan_but.setMaximumWidth(width_widget)
        
        self.layout.addWidget(sun_logo, 0,1)
        self.layout.addWidget(welcome_msg, 1,1)
        self.layout.addWidget(operator_selection, 2,0)
        self.layout.addWidget(self.operator_name, 2,1)
        # self.layout.addWidget(welcome_msg)
        #self.layout.addWidget(widget_form)
        self.layout.addWidget(application_selection,3,0 )
        self.layout.addWidget(daily_scan_but, 3,1)
        self.layout.addWidget(bulk_analyse_but, 3,2)
        self.layout.addWidget(bulk_scan_but,4,1)

        #self.operator_name.setFocusPolicy(QtCore.Qt.NoFocus)
        daily_scan_but.setAutoDefault(True)
        #daily_scan_but.setDefault(True)
        #daily_scan_but.setFocus()
        bulk_analyse_but.setAutoDefault(True)
        #bulk_analyse_but.setDefault(True)
        #bulk_analyse_but.setFocus()
        bulk_scan_but.setAutoDefault(True)
        #bulk_scan_but.setDefault(True)
        #bulk_scan_but.setFocus()
        
        
        daily_scan_but.clicked.connect(self.handleLogin)
        daily_scan_but.clicked.connect(lambda: self.set_mode(0))

        bulk_analyse_but.clicked.connect(self.handleLogin)
        bulk_analyse_but.clicked.connect(lambda: self.set_mode(1))

        bulk_scan_but.clicked.connect(self.handleLogin)
        bulk_scan_but.clicked.connect(lambda: self.set_mode(2))

        self.center()

        """welcome_msg = QtWidgets.QLabel('Welcome in DigiSun', self)
        
        self.operator_name = QtWidgets.QLineEdit(self)
        select_application = QtWidgets.QLabel('Select an application:', self)
        self.digiSun_mode = QtWidgets.QComboBox(self)
        self.digiSun_mode.addItem('scan and analyse')
        self.digiSun_mode.addItem('bulk analyse')
        self.digiSun_mode.addItem('bulk scan')
        
        but_login = QtWidgets.QPushButton('Enter', self)
        but_login.clicked.connect(self.handleLogin)

        form_layout = QtWidgets.QFormLayout()
        form_layout.addRow('operator name', self.operator_name)

        self.layout.addWidget(welcome_msg)
        self.layout.addLayout(form_layout)
        self.layout.addWidget(select_application)
        self.layout.addWidget(self.digiSun_mode)
        self.layout.addWidget(but_login)       
        """

    def set_mode(self, mode):
        self.digiSun_mode = mode
        
    def handleLogin(self):

        print("handleLogin...")
        uset_db = database.database()
        if (uset_db.exist_in_db('observers', 'name', self.operator_name.text())):
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
        screen = QtWidgets.QApplication.desktop().screenNumber(QtWidgets.QApplication.desktop().cursor().pos())
        centerPoint = QtWidgets.QApplication.desktop().screenGeometry(screen).center()
        frameGm.moveCenter(centerPoint)
        self.move(frameGm.topLeft())     
    """def show_buttons(self):
        welcome_msg = QtWidgets.QLabel('DigiSun prototype', self)

        my_font = QtWidgets.QFont("Courier",30)
        welcome_msg.setFont(my_font)

        but_scananalyse = QtWidgets.QPushButton('Scanalyse', self)
        but_analyse = QtWidgets.QPushButton('bulk Analyse', self)
        but_scan = QtWidgets.QPushButton('bulk Scan', self)
                
        self.layout.addWidget(welcome_msg, 0, 0, 1, 3)
        
        self.layout.addWidget(but_scananalyse, 2, 0, 1,1)
        self.layout.addWidget(but_analyse, 2, 1,1,1)
        self.layout.addWidget(but_scan, 2, 2,1,1)     

        return but_scananalyse, but_scan, but_analyse
   """ 
"""class Login_old(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(Login, self).__init__(parent)
        self.textName = QtWidgets.QLineEdit(self)
        self.textPass = QtWidgets.QLineEdit(self)
        self.buttonLogin = QtWidgets.QPushButton('Login', self)
        self.buttonLogin.clicked.connect(self.handleLogin)
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.textName)
        layout.addWidget(self.textPass)
        layout.addWidget(self.buttonLogin)

    def handleLogin(self):
        if (self.textName.text() == 'foo' and
            self.textPass.text() == 'bar'):
            self.accept()
        else:
            QtWidgets.QMessageBox.warning(
                self, 'Error', 'Bad user or password')

class Window(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)
        # self.ui = Ui_MainWindow()
        # self.ui.setupUi(self)

if __name__ == '__main__':

    import sys
    app = QtWidgets.QApplication(sys.argv)
    login = Login()

    if login.exec_() == QtWidgets.QDialog.Accepted:
        window = Window()
        window.show()
        sys.exit(app.exec_())
"""
