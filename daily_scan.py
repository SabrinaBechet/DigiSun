# !/usr/bin/env python
# -*-coding:utf-8-*-
import os, sys
from PyQt4 import QtGui, QtCore
import database, drawing
from datetime import datetime
import scanner
   
class DailyScan(QtGui.QWidget):
    
    def __init__(self, operator=None):
        super(DailyScan, self).__init__()
        
        self.operator = operator
        self.add_formLayout_lineEdit()
        self.info_complete ={"operator": True,
                             "observer": True,
                             "date": True,
                             "time": False}

        self.check_scanner()
        
        #to do: height plus grand pour le bouton du scan. Icon de scanner?
        #self.but_scan = QtGui.QPushButton('Scan and save', self)
        #self.widget_left_layout.addWidget(self.but_scan)

    def check_scanner(self):
        """
        Check if there is a scanner connected and
        print the settings of the scan.
        """
        if sys.platform == "win32":
            my_scanner = scanner.scanner()
            scanner_name = my_scanner.get_scanner_name()
            if scanner_name:
                self.scan_name_linedit.setText(scanner_name[0])
                self.scan_dpi.setText(str(my_scanner.dpi))
                self.drawing_directory.setText(my_scanner.directory)
                self.but_scan.setEnabled(True)
        else:
            self.scan_name_linedit.setText("No working on Linux")
            self.scan_name_linedit.setStyleSheet(
                    "background-color: rgb(255, 165, 84)")
            
    def add_formLayout_lineEdit(self):
        """
        Set the layout of the daily scan page.
        """
        column_maximum_width = 600
        
        form_layout = QtGui.QFormLayout()
        form_layout.setAlignment(QtCore.Qt.AlignVCenter and QtCore.Qt.AlignHCenter)
        #form_layout.setContentsMargins(self.width()/2., self.height()/2., 0,0)
        form_layout.setSpacing(10)
        self.setLayout(form_layout)

        scan_settings_title = QtGui.QLabel("Scanner settings")
        scan_settings_title.setMaximumWidth(column_maximum_width)
        scan_settings_title.setAlignment(QtCore.Qt.AlignCenter)
        scan_settings_title.setContentsMargins(10, 10, 10, 10)
        my_font = QtGui.QFont("Comic Sans MS", 10)
        scan_settings_title.setFont(my_font)

        self.scan_name_linedit = QtGui.QLineEdit(self)
        self.scan_name_linedit.setMaximumWidth(column_maximum_width)
        self.scan_name_linedit.setDisabled(True)
        self.scan_dpi = QtGui.QLineEdit(self)
        self.scan_dpi.setMaximumWidth(column_maximum_width)
        self.scan_dpi.setDisabled(True)
        self.drawing_directory = QtGui.QLineEdit(self)
        self.drawing_directory.setMaximumWidth(column_maximum_width)
        self.drawing_directory.setDisabled(True)
        
        title = QtGui.QLabel("Drawing information")
        title.setMaximumWidth(column_maximum_width)
        title.setAlignment(QtCore.Qt.AlignCenter)
        title.setContentsMargins(10, 10, 10, 10)
        my_font = QtGui.QFont("Comic Sans MS", 10)
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
                                             'operator'))
        
        self.drawing_observer.textChanged.connect(
            lambda: self.check_valid_from_db('observers',
                                             'name',
                                             self.drawing_observer.text(),
                                             'observer'))
        
        self.drawing_time.timeChanged.connect(self.check_valid_datetime)

        self.but_scan = QtGui.QPushButton('Scan and save', self)
        self.but_scan.setMaximumWidth(column_maximum_width + 75)
        self.but_scan.setDisabled(True)
        self.but_analyse = QtGui.QPushButton('analyse', self)
        self.but_analyse.setMaximumWidth(column_maximum_width + 75)
        self.but_scan.clicked.connect(lambda: self.scan_drawing())

        form_layout.addRow(scan_settings_title)
        form_layout.addRow('Scan found:', self.scan_name_linedit)
        form_layout.addRow('dpi:', self.scan_dpi)
        form_layout.addRow('drawings directory:', self.drawing_directory)
        form_layout.addRow(title)
        form_layout.addRow('Operator:', self.drawing_operator)
        form_layout.addRow('Observer:', self.drawing_observer)
        form_layout.addRow('Date:', self.drawing_date)
        form_layout.addRow('Time:', self.drawing_time)
        form_layout.addRow(self.but_scan)
        form_layout.addRow(self.but_analyse)
        
    def check_valid_from_db(self, table_name, field, value, info_name):
        """
        Check if the name of the observer and operator are valid in the database
        """
        print("detect a change in the operator or observator name"
              "hence, check that this name is valid")
        
        uset_db = database.database()
        if (uset_db.exist_in_db( table_name, field, value )):
            self.info_complete[info_name]=True
            if info_name=='observer':
                self.drawing_observer.setStyleSheet(
                    "background-color: transparent")
            elif info_name=='operator':
                 self.drawing_operator.setStyleSheet(
                    "background-color: transparent")
        else:
            self.info_complete[info_name]=False
            if info_name=='observer':
                self.drawing_observer.setStyleSheet(
                    "background-color: rgb(255, 165, 84)")
            elif info_name=='operator':
                 self.drawing_operator.setStyleSheet(
                    "background-color: rgb(255, 165, 84)")

            
    def check_valid_datetime(self):

        #print(self.drawing_time.text())
        time = self.drawing_time.text()
        hour = int(time[0:2])
        minute = int(time[3:5])
        print(time, hour, minute)
        
        if hour in range(5,20) and minute in range(0,60):
            self.info_complete['time']=True
            self.drawing_time.setStyleSheet(
                    "background-color: transparent")
        else:
            self.info_complete['time']=False
            self.drawing_time.setStyleSheet(
                    "background-color: rgb(255,165,84)")
        #self.check_but_scan_enabled()
            
        
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

    def add_to_database(self):
        """
        Method that add an entry to the database
        corresponding to the new drawing scanned
        """
        pass

    def get_filename(self):
        date = str(self.drawing_date.text())
        time = str(self.drawing_time.text())
        return ("usd" + date[6:10] +
                date[3:5] + date[0:2] +
                time[0:2] + time[3:5] + '.jpg')
   
    def scan_drawing(self):
        """
        Method called when one click on the scan and save button.
        The scanner object is created here (and hence deleted) to be sure that 
        it does not stay in the memory.
        """

        print("enter in the scan drawing method of daily scan ",
              self.drawing_time.text())
        print(self.info_complete.values())
        if False in self.info_complete.values():
            QtGui.QMessageBox.warning(self,
                                      'information incomplete',
                                    'One of the information is not correct')
            return
        
        my_scanner = scanner.scanner()
        scanner_name = my_scanner.get_scanner_name()    
        my_scanner.set_scanner(scanner_name[0])
        my_scanner.set_scan_area()
             
        if os.path.isfile(os.path.join(my_scanner.directory,
                                       self.get_filename())):
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

        drawing_scanned = my_scanner.scan(self.get_filename())
        
        print("Image Info:", drawing_scanned.info)
        print(drawing_scanned.size)
