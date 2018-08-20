# !/usr/bin/env python
# -*-coding:utf-8-*-
import os
from PyQt4 import QtGui, QtCore
from PIL import Image
from PIL.ImageQt import ImageQt
import database, drawing
from datetime import date, time, datetime

class ScanPage(QtGui.QWidget):
    def __init__(self, operator=None):
        super(ScanPage, self).__init__()

        self.widget_left_layout = QtGui.QVBoxLayout()     
        self.widget_left_layout.setContentsMargins(10, 10, 10, 10) 
        self.widget_left_layout.setSpacing(5)
        
        self.widget_left_layout.setAlignment(QtCore.Qt.AlignCenter)
        self.setLayout(self.widget_left_layout)
        
class DailyScan(ScanPage):
    
    def __init__(self, operator=None):
        super(DailyScan, self).__init__()
 
        self.drawing_lst = []
        
        self.operator_right_name = False
        self.observer_right_name = False
        self.time_right_format = False
        self.scan_on = False
        self.operator = operator
        
        self.column_maximum_width = 600
        #self.but_scan = QtGui.QPushButton('Scan and save', self)
        #self.widget_left_layout.addWidget(self.but_scan)
        self.add_formLayout_lineEdit()
        
        #to do: height plus grand pour le bouton du scan. Icon de scanner?
        #self.but_scan = QtGui.QPushButton('Scan and save', self)
        #self.widget_left_layout.addWidget(self.but_scan)
        self.add_formLayout_button()
        self.fill_default_buttons()
     
    def add_formLayout_lineEdit(self):

        groupBox = QtGui.QGroupBox(self)
        groupBox.setTitle("general information")
        #groupBox.setStyleSheet("QGroupBox { border: 2px solid gray; border-radius: 3px;}")
        
        self.form_layout1 = QtGui.QFormLayout()
        self.form_layout1.setSpacing(10)
        self.form_layout1.addWidget(groupBox)
        
        self.drawing_operator = QtGui.QLineEdit(self)
        #self.drawing_operator.setMaximumWidth(self.column_maximum_width)
        self.drawing_observer = QtGui.QLineEdit(self)
        #self.drawing_observer.setMaximumWidth(self.column_maximum_width)
        self.drawing_date = QtGui.QDateEdit()
        #self.drawing_date.setMaximumWidth(self.column_maximum_width)
        self.drawing_date.setDisplayFormat("dd/MM/yyyy")
        today = QtCore.QDate.currentDate()
        self.drawing_date.setDate(today)
        self.drawing_time = QtGui.QLineEdit("00:00",self)
        #self.drawing_time.setMaximumWidth(self.column_maximum_width)
        self.drawing_time.setInputMask("99:99")
        self.drawing_time.setStyleSheet("background-color: red")
        
        self.drawing_quality = QtGui.QSpinBox(self)
        #self.drawing_quality.setMaximumWidth(self.column_maximum_width)
        self.drawing_quality.setMinimum(1)
        self.drawing_quality.setMaximum(5)
        self.drawing_quality.setValue(3)
        self.drawing_type = QtGui.QComboBox(self)
        #self.drawing_type.setMaximumWidth(self.column_maximum_width)
        self.drawing_type.addItem('USET')
        self.drawing_type.addItem('USET77')
        self.drawing_type.addItem('USET41')

        self.form_layout1.addRow('Operator:', self.drawing_operator)
        self.form_layout1.addRow('Observer:', self.drawing_observer)
        self.form_layout1.addRow('Date:', self.drawing_date)
        self.form_layout1.addRow('Time:', self.drawing_time)
        self.form_layout1.addRow('Quality:', self.drawing_quality)
        self.form_layout1.addRow('Type:', self.drawing_type)
        #self.form_layout.addWidget(self.but_scan)
        #self.form_layout.addWidget(self.but_analyse)
        
        self.drawing_operator.textChanged.connect(lambda:
                                                  self.check_valid_from_db('observers',
                                                                           'namecode',
                                                                           self.drawing_operator.text(),
                                                                           self.drawing_operator,
                                                                           self.operator_right_name))
        
        self.drawing_observer.textChanged.connect(lambda:
                                                  self.check_valid_from_db('observers',
                                                                           'namecode',
                                                                           self.drawing_observer.text(),
                                                                           self.drawing_observer,
                                                                           self.observer_right_name))
        self.drawing_time.textChanged.connect(self.check_valid_datetime)


        widget_form = QtGui.QWidget()
        widget_form.setMaximumWidth(self.column_maximum_width)
        widget_form.setLayout(self.form_layout1)
        
        self.widget_left_layout.addWidget(widget_form)

    def add_formLayout_button(self):
        
        self.form_layout2 = QtGui.QFormLayout()
        self.form_layout2.setSpacing(15)
        
        self.but_scan = QtGui.QPushButton('Scan and save', self)
        self.but_scan.setMaximumWidth(self.column_maximum_width + 75)
        self.but_scan.setDisabled(True)
        self.but_analyse = QtGui.QPushButton('analyse', self)
        self.but_analyse.setMaximumWidth(self.column_maximum_width + 75)
       
        self.but_scan.clicked.connect(lambda: self.scan_drawing())
        #self.but_analyse.clicked.connect(lambda: self.show_drawing())
        
        self.form_layout2.setWidget(6,
                                   QtGui.QFormLayout.SpanningRole,
                                   self.but_scan)
        self.form_layout2.setWidget(7,
                                   QtGui.QFormLayout.SpanningRole,
                                   self.but_analyse)
        
        #groupBox.setLayout(self.form_layout)
    
        self.widget_left_layout.addLayout(self.form_layout2)
        #self.widget_right_layout.addWidget(self.but_scan)
        #self.widget_right_layout.addWidget(self.but_analyse)
  
    def check_but_scan_enabled(self):
        if (self.operator_right_name and
            self.observer_right_name and
            self.time_right_format and
            self.scan_on ):
            self.but_scan.setEnabled(True)
        else:
            self.but_scan.setDisabled(True)

    def check_valid_from_db(self, table_name, field, value, drawing_param, drawing_param_name):
        
        uset_db = database.database()
        if (uset_db.exist_in_db( table_name, field, value )):
            drawing_param.setStyleSheet("background-color: green")
            drawing_param_name = True
        else:
            drawing_param.setStyleSheet("background-color: red")
            drawing_param_name = False
                    
    def check_valid_datetime(self):
        time = self.drawing_time.text()
        hour = int(time[0:2])
        minute = int(time[3:5])
        print(time, hour, minute)
        
        if hour in range(5,20) and minute in range(0,60):
            self.drawing_time.setStyleSheet("background-color: green")
            self.time_right_format = True
        else:
            self.drawing_time.setStyleSheet("background-color: red")
            self.time_right_format = False

        self.check_but_scan_enabled()
        
        
    def set_drawing_information(self):
        """
        Fill the drawing information based on 
        what has been filled on the screen.
        """
        print("daily scan get set drawing information")
        drawing_lst = []
        my_drawing = drawing.Drawing()
        my_drawing.drawing_type = str(self.drawing_type.currentText())

        time = self.drawing_time.text()
        date = self.drawing_date.text()
        my_drawing.datetime = datetime(int(date[6:10]),
                                    int(date[3:5]),
                                    int(date[0:2]),
                                    int(time[0:2]),
                                    int(time[3:5]))
        my_drawing.quality = str(self.drawing_quality.text())
        my_drawing.observer = str(self.drawing_observer.text()).upper()
        my_drawing.operator = str(self.drawing_operator.text()).upper()
        datetime_now = datetime.now()
        my_drawing.last_update_time = datetime(datetime_now.year,
                                                 datetime_now.month,
                                                 datetime_now.day,
                                                 datetime_now.hour,
                                                 datetime_now.minute,
                                                 datetime_now.second)
        
        my_drawing.path = ("usd" + date[6:10] +
                           date[3:5] + date[0:2] +
                           time[0:2] + time[3:5] + ".jpg")
        
        
        drawing_lst.append(my_drawing)
        return drawing_lst
    
    def fill_default_buttons(self):
        """
        Fill by default the name of the observer and the operator 
        based on the login name.
        """
        self.drawing_operator.setText(self.operator)
        self.drawing_observer.setText(self.operator)
    
    def set_button_scan_on(self, my_scanner):
        self.scan_on = True
        
    def scan_drawing(self):
        """
        Method called when one click on the scan and save button.
        The scanner object is created here (and hence deleted) to be sure that 
        it does not stay in the memory.
        """
        init_success = False
        if sys.platform == "win32":

            print(self.drawing_time.text())
            
            my_scanner = scanner.scanner()
            scanner_name = my_scanner.get_scanner()
            my_scanner.set_scanner(scanner_name[0], 'technical_settings')
            my_scanner.set_scan_area()
            init_success = True

            date = str(self.drawing_date.text())
            time = str(self.drawing_time.text())
            filename = ("usd" + date[6:10] +
                        date[3:5] + date[0:2] +
                        time[0:2] + time[3:5] + ".jpg")
            
            #filename = self.get_filename()

            directory = my_scanner.get_directory()
            file_input = os.path.join(directory, filename)
            if os.path.isfile(file_input):
                response = QtGui.QMessageBox.question(self,
                                                      'same drawing found'
                                                      '',
                                                      'This drawing alreay exists. Re-scan?',
                                                      QtGui.QMessageBox.Yes| QtGui.QMessageBox.No)
                if response == QtGui.QMessageBox.Yes:
                    pass
                elif response == QtGui.QMessageBox.No:
                    return
            drawing_scanned = my_scanner.scan(self.filename)
            self.set_drawing()
            
            uset_db = database.database()
            uset_db.replace_drawing(self.drawing)

            self.show_drawing(drawing_scanned)
        else:
            print("No scanner on linux..")
