
from PyQt4 import QtGui, QtCore
import sys



class LoginWindow(QtGui.QWidget):

    def __init__(self):
        super(LoginWindow, self).__init__()
        #self.setMinimumHeight(500)
        #self.setMinimumWidth(500)
        self.layout = QtGui.QGridLayout()
        self.setLayout(self.layout)
        #self.layout.setContentsMargins(15, 15, 15, 15) # this line
        self.layout.setSpacing(10)
        #self.layout.setAlignment(QtCore.Qt.AlignHCenter);
        #layout_welcome = QtGui.QHBoxLayout()
        welcome_msg = QtGui.QLabel('DigiSun 2018', self)
        width_widget = 150
        sun_logo = QtGui.QLabel()
        
        sun_logo.setPixmap(QtGui.QPixmap("sun-logo-th.png"))
        sun_logo.setMinimumWidth(width_widget)
        sun_logo.setMaximumWidth(width_widget)
        sun_logo.setMaximumHeight(width_widget)
        #layout_welcome.addWidget(welcome_msg)
        #layout_welcome.addWidget(sun_logo)

        self.operator_name = QtGui.QLineEdit(self)
        self.operator_name.setMinimumWidth(width_widget)
        self.operator_name.setMaximumWidth(width_widget)
        #form_layout = QtGui.QFormLayout()
        #form_layout.addRow('Welcome in DigiSun', sun_logo)
        #form_layout.addRow('operator name:', self.operator_name)
        operator_selection = QtGui.QLabel('operator name: ', self)
        operator_selection.setMinimumWidth(width_widget)
        operator_selection.setMaximumWidth(width_widget)
        #widget_form = QtGui.QWidget()
        #widget_form.setLayout(form_layout)
        
        #self.layout.addLayout(layout_welcome)
        
        application_selection = QtGui.QLabel('Applications: ', self)
        daily_scan_but = QtGui.QPushButton("daily scan")
        bulk_analyse_but = QtGui.QPushButton("bulk analyse")
        bulk_scan_but = QtGui.QPushButton("bulk scan")
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

        self.center()
    
    def center(self):
        frameGm = self.frameGeometry()
        screen = QtGui.QApplication.desktop().screenNumber(QtGui.QApplication.desktop().cursor().pos())
        centerPoint = QtGui.QApplication.desktop().screenGeometry(screen).center()
        frameGm.moveCenter(centerPoint)
        self.move(frameGm.topLeft()) 


if __name__=="__main__":
    
    app  = QtGui.QApplication(sys.argv)
    login = LoginWindow()
    login.show()

    app.exec_()
