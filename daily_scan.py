# !/usr/bin/env python
# -*-coding:utf-8-*-
import os, sys
from PyQt4 import QtGui, QtCore
import database, drawing
from datetime import datetime
import scanner
import datetime
   
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
            self.scan_name_linedit.setText("Not working on Linux")
            self.scan_name_linedit.setStyleSheet(
                    "background-color: rgb(255, 165, 84)")
            
    def add_formLayout_lineEdit(self):
        """
        Set the layout of the daily scan page.
        """
        column_maximum_width = 600
        
        form_layout = QtGui.QFormLayout()
        form_layout.setAlignment(QtCore.Qt.AlignVCenter and QtCore.Qt.AlignHCenter)
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
        
        self.drawing_operator_linedit = QtGui.QLineEdit(self)
        self.drawing_operator_linedit.setMaximumWidth(column_maximum_width)
        self.drawing_operator_linedit.setText(self.operator)
        self.drawing_observer_linedit = QtGui.QLineEdit(self)
        self.drawing_observer_linedit.setMaximumWidth(column_maximum_width)
        self.drawing_observer_linedit.setText(self.operator)
        self.drawing_date_linedit = QtGui.QDateEdit()
        self.drawing_date_linedit.setMaximumWidth(column_maximum_width)
        self.drawing_date_linedit.setDisplayFormat("dd/MM/yyyy")
        today = QtCore.QDate.currentDate()
        self.drawing_date_linedit.setDate(today)
        self.drawing_time_linedit = QtGui.QTimeEdit(self)
        self.drawing_time_linedit.setMaximumWidth(column_maximum_width)

        self.drawing_time = datetime.datetime(self.drawing_date_linedit.date().year(),
                                              self.drawing_date_linedit.date().month(),
                                              self.drawing_date_linedit.date().day(),
                                              self.drawing_time_linedit.time().hour(),
                                              self.drawing_time_linedit.time().minute())
      

        self.drawing_operator_linedit.textChanged.connect(
            lambda: self.check_valid_from_db('observers',
                                             'name',
                                             self.drawing_operator_linedit.text(),
                                             'operator'))
        
        self.drawing_observer_linedit.textChanged.connect(
            lambda: self.check_valid_from_db('observers',
                                             'name',
                                             self.drawing_observer_linedit.text(),
                                             'observer'))
        
        self.drawing_time_linedit.timeChanged.connect(self.check_valid_datetime)
        self.drawing_time_linedit.timeChanged.connect(self.update_datetime)
        self.drawing_date_linedit.dateChanged.connect(self.update_datetime)

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
        form_layout.addRow('Operator:', self.drawing_operator_linedit)
        form_layout.addRow('Observer:', self.drawing_observer_linedit)
        form_layout.addRow('Date:', self.drawing_date_linedit)
        form_layout.addRow('Time:', self.drawing_time_linedit)
        form_layout.addRow(self.but_scan)
        form_layout.addRow(self.but_analyse)
        
    def check_valid_from_db(self, table_name, field, value, info_name):
        """
        Check if the name of the observer and operator are valid in the database
        """
        #print("detect a change in the operator or observator name"
        #      "hence, check that this name is valid")
        
        uset_db = database.database()
        if (uset_db.exist_in_db( table_name, field, value )):
            self.info_complete[info_name]=True
            if info_name=='observer':
                self.drawing_observer_linedit.setStyleSheet(
                    "background-color: transparent")
            elif info_name=='operator':
                 self.drawing_operator_linedit.setStyleSheet(
                    "background-color: transparent")
        else:
            self.info_complete[info_name]=False
            if info_name=='observer':
                self.drawing_observer_linedit.setStyleSheet(
                    "background-color: rgb(255, 165, 84)")
            elif info_name=='operator':
                 self.drawing_operator_linedit.setStyleSheet(
                    "background-color: rgb(255, 165, 84)")

                
    def update_datetime(self):
        """
        Update the value of datetime when one modify date or time line edit.
        """
        self.drawing_time = datetime.datetime(self.drawing_date_linedit.date().year(),
                                              self.drawing_date_linedit.date().month(),
                                              self.drawing_date_linedit.date().day(),
                                              self.drawing_time_linedit.time().hour(),
                                              self.drawing_time_linedit.time().minute())
            
    def check_valid_datetime(self):
        """
        Check if the date time is in a reasonable range (hour between 5 and 20)
        and update the drawing time
        """
        hour = self.drawing_time_linedit.time().hour()
        minute = self.drawing_time_linedit.time().minute()    
        if hour in range(5,20) and minute in range(0,60):
            self.info_complete['time']=True
            self.drawing_time_linedit.setStyleSheet(
                    "background-color: transparent")
        else:
            self.info_complete['time']=False
            self.drawing_time_linedit.setStyleSheet(
                    "background-color: rgb(255,165,84)")        
   
    def set_drawing_information(self):
        """
        Method that add an entry to the database
        corresponding to the new drawing scanned
        """

        #print("set the drawing information..", self.drawing_time)
        new_drawing = drawing.Drawing()
        new_drawing.fill_from_daily_scan(drawing_datetime = self.drawing_time,
                                         observer = str(self.drawing_observer_linedit.text()),
                                         operator = str(self.drawing_operator_linedit.text()))

        db = database.database()
        db.replace_drawing(new_drawing) 
        return [new_drawing]
        

    def get_filename(self):

        print("check filename: ", "usd" + self.drawing_time.strftime('%Y%m%d%H%M') + '.jpg')        
        return ("usd" + self.drawing_time.strftime('%Y%m%d%H%M') + '.jpg')
   
    def scan_drawing(self):
        """
        Method called when one click on the scan and save button.
        The scanner object is created here (and hence deleted) to be sure that 
        it does not stay in the memory.
        """
        
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
