# !/usr/bin/env python
# -*-coding:utf-8-*-
import os, sys
from PyQt4 import QtGui, QtCore
import database, drawing
from datetime import datetime

"""class ScanPage(QtGui.QWidget):
    def __init__(self, operator=None):
        super(ScanPage, self).__init__()

        self.widget_left_layout = QtGui.QVBoxLayout()     
        self.widget_left_layout.setContentsMargins(10, 10, 10, 10) 
        self.widget_left_layout.setSpacing(5)
        
        self.widget_left_layout.setAlignment(QtCore.Qt.AlignCenter)
        self.setLayout(self.widget_left_layout)
"""        
class DailyScan(QtGui.QWidget):
    
    def __init__(self, operator=None):
        super(DailyScan, self).__init__()
        
        self.operator = operator
        self.add_formLayout_lineEdit()
        
        self.info_complete ={"operator": True,
                             "observer": False,
                             "date": True,
                             "time": False}
        
        
        #to do: height plus grand pour le bouton du scan. Icon de scanner?
        #self.but_scan = QtGui.QPushButton('Scan and save', self)
        #self.widget_left_layout.addWidget(self.but_scan)

    def add_formLayout_lineEdit(self):

        column_maximum_width = 600
        
        form_layout = QtGui.QFormLayout()
        form_layout.setAlignment(QtCore.Qt.AlignVCenter and QtCore.Qt.AlignHCenter)
        form_layout.setContentsMargins(self.width()/2., self.height()/2., 0,0)
        form_layout.setSpacing(10)
        self.setLayout(form_layout)

        title = QtGui.QLabel("Drawing information")
        title.setMaximumWidth(column_maximum_width)
        title.setAlignment(QtCore.Qt.AlignCenter)
        title.setContentsMargins(10, 10, 10, 10)
        my_font = QtGui.QFont("Comic Sans MS", 20)
        title.setFont(my_font)
        
        self.drawing_operator = QtGui.QLineEdit(self)
        self.drawing_operator.setMaximumWidth(column_maximum_width)
        self.drawing_operator.setText(self.operator)
        self.drawing_observer = QtGui.QLineEdit(self)
        self.drawing_observer.setMaximumWidth(column_maximum_width)
        self.drawing_observer.setText(self.operator)
        self.drawing_date = QtGui.QDateEdit()
        self.drawing_date.setMaximumWidth(column_maximum_width)
        self.drawing_date.setDisplayFormat("dd/MM/yyyy")
        today = QtCore.QDate.currentDate()
        self.drawing_date.setDate(today)
        self.drawing_time = QtGui.QTimeEdit(self)
        self.drawing_time.setMaximumWidth(column_maximum_width)
        #self.drawing_time.setInputMask("99:99")

        
        self.drawing_operator.textChanged.connect(
            lambda: self.check_valid_from_db('observers',
                                             'name',
                                             self.drawing_operator.text(),
                                             self.drawing_operator,
                                             self.operator_right_name,
                                             'observer'))
        
        self.drawing_observer.textChanged.connect(
            lambda: self.check_valid_from_db('observers',
                                             'name',
                                             self.drawing_observer.text(),
                                             self.drawing_observer,
                                             self.observer_right_name,
                                             'operator'))
        
        #self.drawing_time.textChanged.connect(self.check_valid_datetime)

        self.but_scan = QtGui.QPushButton('Scan and save', self)
        self.but_scan.setMaximumWidth(column_maximum_width + 75)
        self.but_analyse = QtGui.QPushButton('analyse', self)
        self.but_analyse.setMaximumWidth(column_maximum_width + 75)
        self.but_scan.clicked.connect(lambda: self.scan_drawing())


        form_layout.addRow(title)
        form_layout.addRow('Operator:', self.drawing_operator)
        form_layout.addRow('Observer:', self.drawing_observer)
        form_layout.addRow('Date:', self.drawing_date)
        form_layout.addRow('Time:', self.drawing_time)
        form_layout.addRow(self.but_scan)
        form_layout.addRow(self.but_analyse)
        
        
        """def check_but_scan_enabled(self):
        print("check that the scan can be enabled")
        print(self.operator_right_name, self.observer_right_name, self.time_right_format )
        
        if (self.operator_right_name and
        self.observer_right_name and
        self.time_right_format ):
        
        self.but_scan.setEnabled(True)
        else:
        self.but_scan.setDisabled(True)
        """
    def check_valid_from_db(self, table_name, field, value, info_name):
        """
        Check if the name of the observer and operator are valid in the database
        """
        uset_db = database.database()
        if (uset_db.exist_in_db( table_name, field, value )):
            self.info_complete[info_name]=True
        else:
            drawing_param.setStyleSheet("background-color: rgb(255, 165, 84)")
            self.info_complete[info_name]=False

            
    """def check_valid_datetime(self):

        time = self.drawing_time.text()
        hour = int(time[0:2])
        minute = int(time[3:5])
        print(time, hour, minute)
        
        if hour in range(5,20) and minute in range(0,60):
            self.info_complete['time']=True
        else:
            self.info_complete['time']=False

        #self.check_but_scan_enabled()
    """    
        
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
        datetime_now = datetime.datetime.now()
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
                response = QtGui.QMessageBox.question(
                    self,
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

            QtGui.QMessageBox.warning(self,
                                      "scanner information",
                                      "Impossible to scan on Linux for the moment...")
