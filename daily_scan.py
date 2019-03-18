# !/usr/bin/env python
# -*-coding:utf-8-*-
"""
The page for the daily scan interface
"""
import os
import sys
import datetime
import database
import drawing
import scanner
import configuration
from PyQt4 import QtGui, QtCore

class DailyScan(QtGui.QWidget):

    def __init__(self, operator=None):
        super(DailyScan, self).__init__()

        self.daily_scan_layout = QtGui.QVBoxLayout()
        self.daily_scan_layout.setAlignment(QtCore.Qt.AlignCenter)
        self.setLayout(self.daily_scan_layout)

        self.config = configuration.Config()
        self.config.set_archdrawing()
        self.config.set_scanner()
        
        self.operator = operator
        self.add_formLayout_lineEdit()
        self.info_complete = {"operator": True,
                              "observer": True,
                              "date": True,
                              "time": False}

        self.check_scanner()

        # to do: height plus grand pour le bouton du scan. Icon de scanner?
        # self.but_scan = QtGui.QPushButton('Scan and save', self)
        # self.widget_left_layout.addWidget(self.but_scan)

    
        
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
                self.scan_dpi.setText(str(self.config.dpi))
                self.drawing_directory.setText(self.config.archdrawing_directory)
                self.but_scan.setEnabled(True)
        else:
            self.scan_name_linedit.setText("Not working on Unix system")
            self.scan_name_linedit.setStyleSheet(
                    "background-color: rgb(255, 165, 84)")

    def add_formLayout_lineEdit(self):
        """
        Set the layout of the daily scan page.
        """
        column_maximum_width = 600

        form_layout = QtGui.QFormLayout()
        form_layout.setAlignment(self, QtCore.Qt.AlignCenter)
        form_layout.setSpacing(10)

        scan_settings_title = QtGui.QLabel("Scanner settings")
        scan_settings_title.setAlignment(QtCore.Qt.AlignCenter)
        scan_settings_title.setContentsMargins(10, 10, 10, 10)
        my_font = QtGui.QFont("Comic Sans MS", 10)
        scan_settings_title.setFont(my_font)

        self.scan_name_linedit = QtGui.QLineEdit(self)
        self.scan_name_linedit.setDisabled(True)
        self.scan_dpi = QtGui.QLineEdit(self)
        self.scan_dpi.setDisabled(True)
        self.drawing_directory = QtGui.QLineEdit(self)
        self.drawing_directory.setDisabled(True)

        title = QtGui.QLabel("Drawing information")
        title.setAlignment(QtCore.Qt.AlignCenter)
        title.setContentsMargins(10, 10, 10, 10)
        my_font = QtGui.QFont("Comic Sans MS", 10)
        title.setFont(my_font)

        uset_db = database.database()

        self.drawing_operator_linedit = QtGui.QLineEdit(self)
        self.drawing_operator_linedit.setText(str(self.operator).upper())
        self.drawing_observer_linedit = QtGui.QLineEdit(self)
        self.drawing_observer_linedit.setText(str(self.operator).upper())
        self.drawing_type = QtGui.QComboBox(self)
        uset_db.set_combo_box_drawing('name',
                                      'drawing_type',
                                      self.drawing_type)
        self.drawing_quality = QtGui.QComboBox(self)
        uset_db.set_combo_box_drawing('name',
                                      'quality',
                                      self.drawing_quality)

        self.drawing_date_linedit = QtGui.QDateEdit()
        self.drawing_date_linedit.setDisplayFormat("dd/MM/yyyy")
        today = QtCore.QDate.currentDate()
        self.drawing_date_linedit.setDate(today)
        self.drawing_time_linedit = QtGui.QTimeEdit(self)
        self.drawing_time_linedit.setDisplayFormat("hh:mm")

        self.drawing_time = datetime.datetime(
            self.drawing_date_linedit.date().year(),
            self.drawing_date_linedit.date().month(),
            self.drawing_date_linedit.date().day(),
            self.drawing_time_linedit.time().hour(),
            self.drawing_time_linedit.time().minute())

        self.drawing_operator_linedit.textChanged.connect(
            lambda: self.check_valid_from_db(
                'observer',
                'name',
                self.drawing_operator_linedit.text(),
                'operator'))

        self.drawing_observer_linedit.textChanged.connect(
            lambda: self.check_valid_from_db(
                'observer',
                'name',
                self.drawing_observer_linedit.text(),
                'observer'))

        self.drawing_time_linedit.timeChanged.connect(
            self.check_valid_datetime)
        self.drawing_time_linedit.timeChanged.connect(self.update_datetime)
        self.drawing_date_linedit.dateChanged.connect(self.update_datetime)

        self.but_scan = QtGui.QPushButton('Scan and save', self)
        self.but_scan.setDisabled(True)
        self.but_analyse = QtGui.QPushButton('Drawing analyse', self)
        self.but_scan.clicked.connect(lambda: self.scan_drawing())

        form_layout.addRow(scan_settings_title)
        form_layout.addRow('Scanner found:', self.scan_name_linedit)
        form_layout.addRow('dpi:', self.scan_dpi)
        form_layout.addRow('drawings directory:', self.drawing_directory)
        form_layout.addRow(title)
        form_layout.addRow('Operator:', self.drawing_operator_linedit)
        form_layout.addRow('Observer:', self.drawing_observer_linedit)
        form_layout.addRow('Date:', self.drawing_date_linedit)
        form_layout.addRow('Time:', self.drawing_time_linedit)
        form_layout.addRow('Type:', self.drawing_type)
        form_layout.addRow('Quality:', self.drawing_quality)
        form_layout.addRow(self.but_scan)
        form_layout.addRow(self.but_analyse)

        widget_form = QtGui.QWidget()
        widget_form.setMaximumWidth(column_maximum_width)
        form_layout.setAlignment(QtCore.Qt.AlignCenter)
        widget_form.setLayout(form_layout)

        self.daily_scan_layout.addWidget(widget_form)

    def check_valid_from_db(self, table_name, field, value, info_name):
        """
        Check if the name of the observer and
        operator are valid in the database
        """
        uset_db = database.database()
        if (uset_db.exist_in_db(table_name, field, value)):
            self.info_complete[info_name] = True
            if info_name == 'observer':
                self.drawing_observer_linedit.setStyleSheet(
                    "background-color: transparent")
            elif info_name == 'operator':
                self.drawing_operator_linedit.setStyleSheet(
                    "background-color: transparent")
        else:
            self.info_complete[info_name] = False
            if info_name == 'observer':
                self.drawing_observer_linedit.setStyleSheet(
                    "background-color: rgb(255, 165, 84)")
            elif info_name == 'operator':
                self.drawing_operator_linedit.setStyleSheet(
                    "background-color: rgb(255, 165, 84)")

    def update_datetime(self):
        """
        Update the value of datetime when one modify date or time line edit.
        """
        self.drawing_time = datetime.datetime(
            self.drawing_date_linedit.date().year(),
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
        if hour in range(5, 20) and minute in range(0, 60):
            self.info_complete['time'] = True
            self.drawing_time_linedit.setStyleSheet(
                    "background-color: transparent")
        else:
            self.info_complete['time'] = False
            self.drawing_time_linedit.setStyleSheet(
                    "background-color: rgb(255,165,84)")

    def set_drawing_information(self):
        """
        Method that add an entry to the database
        corresponding to the new drawing scanned
        """
        db = database.database()
        answer = QtGui.QMessageBox.Yes
        lst_groups = []
        
        if db.exist_in_db('drawings', 'DateTime', self.drawing_time):
            tuple_drawings = db\
                .get_all_in_time_interval("drawings",
                                          self.drawing_time,
                                          self.drawing_time)
            tuple_calibrations = db\
                .get_all_in_time_interval("calibrations",
                                          self.drawing_time,
                                          self.drawing_time)
            tuple_groups = db\
                    .get_all_in_time_interval("groups",
                                              self.drawing_time,
                                              self.drawing_time)
            lst_groups = [el for el in tuple_groups]
            drawing_type = tuple_drawings[0][2]
            tuple_drawing_type = db.get_drawing_information("drawing_type",
                                                                drawing_type)
            answer = QtGui\
                .QMessageBox\
                .question(self,
                          "new drawing",
                          "An entry corresponding to this drawing was found in the database. "
                          "Do you want to delete previous data ?",
                          QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
             
            new_drawing = drawing.Drawing(tuple_drawings[0])
            new_drawing.set_drawing_type(tuple_drawing_type[0])
            if self.drawing_time == tuple_calibrations[0][1]:
                new_drawing.set_calibration(tuple_calibrations[0])
            for group in lst_groups:
                new_drawing.set_group(group)

            if answer == QtGui.QMessageBox.No:
                db.replace_drawing(new_drawing)

            if answer == QtGui.QMessageBox.Yes:
                # delete the existing groups
                for index in reversed(range(0, len(lst_groups))):
                    new_drawing.delete_group(index)
                    
                
        if answer == QtGui.QMessageBox.Yes:
            new_drawing = drawing.Drawing()

            self.config.set_file_path(self.drawing_time)
            filename = self.config.filename
            
            new_drawing.fill_from_daily_scan(
                drawing_datetime=self.drawing_time,
                observer=str(self.drawing_observer_linedit.text()).upper(),
                operator=str(self.drawing_operator_linedit.text()).upper(),
                drawing_type=str(self.drawing_type.currentText()),
                drawing_quality=str(self.drawing_quality.currentText()),
                drawing_name=filename)
            
            #db.replace_drawing(new_drawing)
            
            tuple_drawing_type = db.get_drawing_information(
                "drawing_type",
                str(self.drawing_type.currentText()))
            new_drawing.set_drawing_type(tuple_drawing_type[0])
            
        return [new_drawing]
            
   

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

        """filename = self.get_filename()
        def get_filename(self):
        return (self.config.prefix +
                self.drawing_time.strftime('%Y%m%d%H%M') +
                self.config.suffix +
                '.' +
                self.config.extension)
        
        output_name = os.path.join(self.config.archdrawing_directory,
                                   self.drawing_time.strftime('%Y'),
                                   self.drawing_time.strftime('%m'),
                                   filename)
        """
        self.config.set_file_path(self.drawing_time)
        drawing_path = self.config.file_path
        
                
        print('file path: ',drawing_path)
        
        if os.path.isfile(drawing_path):    
            response = QtGui.QMessageBox.question(
                self,
                'same drawing found'
                '',
                'This drawing alreay exists. Re-scan?',
                QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
            if response == QtGui.QMessageBox.Yes:
                pass
            elif response == QtGui.QMessageBox.No:
                return

        my_scanner.scan(drawing_path)
