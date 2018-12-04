# !/usr/bin/env python
# -*-coding:utf-8-*-
import os
from PyQt4 import QtGui, QtCore

import database
from datetime import datetime


class DrawingInformationWidget(QtGui.QWidget):

    def __init__(self):
        super(DrawingInformationWidget, self).__init__()
        form_layout = QtGui.QFormLayout()
        form_layout.setSpacing(10)
        
        self.drawing_operator = QtGui.QLineEdit(self)
        self.drawing_operator.setEnabled(True)
        self.drawing_operator.setStyleSheet(
            "background-color: lightgray; color:black")

        self.drawing_last_update = QtGui.QDateEdit()
        self.drawing_last_update.setDisplayFormat("dd/MM/yyyy")
        self.drawing_last_update.setEnabled(True)
        self.drawing_last_update.setStyleSheet(
            "background-color: lightgray; color:black")
        self.drawing_observer = QtGui.QLineEdit(self)
        self.drawing_observer.setEnabled(True)
        self.drawing_observer.setStyleSheet(
            "background-color: white; color:black")
        
        self.drawing_date = QtGui.QDateEdit()
        self.drawing_date.setDisplayFormat("dd/MM/yyyy")
        #today = QtCore.QDate.currentDate()
        #self.drawing_date.setDate(today)
        self.drawing_date.setEnabled(False)
        self.drawing_date.setStyleSheet(
            "background-color: lightgray; color:black")
        
        self.drawing_time = QtGui.QLineEdit("00:00",self)
        self.drawing_time.setInputMask("99:99")
        self.drawing_time.setEnabled(False)
        self.drawing_time.setStyleSheet(
            "background-color: lightgray; color:black")
        
        self.drawing_quality = QtGui.QComboBox(self) 
        self.set_combo_box_drawing('name', 'quality', self.drawing_quality)
        self.drawing_quality.setEnabled(True)
        self.drawing_quality.setStyleSheet(
            "background-color: white; color:black")
        
        self.drawing_type = QtGui.QComboBox(self)
        self.set_combo_box_drawing('name', 'drawing_type', self.drawing_type)
        self.drawing_type.setEnabled(True)
        self.drawing_type.setStyleSheet(
            "background-color: white; color:black")
        
        self.wolf_number = QtGui.QLineEdit(self)
        self.wolf_number.setEnabled(False)
        self.wolf_number.setStyleSheet(
            "background-color: lightgrey; color:black")
        
        self.angleP = QtGui.QLineEdit(self)
        self.angleP.setEnabled(False)
        self.angleP.setStyleSheet(
            "background-color: lightgrey; color:black")
        
        self.angleB = QtGui.QLineEdit(self)
        self.angleB.setEnabled(False)
        self.angleB.setStyleSheet(
            "background-color: lightgrey; color:black")
        
        self.angleL = QtGui.QLineEdit(self)
        self.angleL.setEnabled(False)
        self.angleL.setStyleSheet(
            "background-color: lightgrey; color:black")
        
        self.rotation_number = QtGui.QLineEdit(self)
        self.rotation_number.setEnabled(False)
        self.rotation_number.setStyleSheet(
            "background-color: lightgrey; color:black")

        self.calibrated = QtGui.QLineEdit(self)
        self.calibrated.setEnabled(False)
        self.calibrated.setStyleSheet(
            "background-color: lightgrey; color:black")
        
        self.analyzed = QtGui.QLineEdit(self)
        self.analyzed.setEnabled(False)
        self.analyzed.setStyleSheet(
            "background-color: lightgrey; color:black")
        
        self.area_done = QtGui.QLineEdit(self)
        self.area_done.setEnabled(False)
        self.area_done.setStyleSheet(
            "background-color: lightgrey; color:black")

        form_layout.addRow('Date:', self.drawing_date)
        form_layout.addRow('Time:', self.drawing_time)
        form_layout.addRow('Observer:', self.drawing_observer)
        form_layout.addRow('Wolf number:', self.wolf_number)
        form_layout.addRow('Quality:', self.drawing_quality)
        form_layout.addRow('Type:', self.drawing_type)
        form_layout.addRow('P angle:', self.angleP)
        form_layout.addRow('B angle:', self.angleB)
        form_layout.addRow('L angle:', self.angleL)
        form_layout.addRow('Carington rotation :', self.rotation_number)
        
        form_layout.addRow('Last Operator:', self.drawing_operator)
        form_layout.addRow('Last Update:', self.drawing_last_update)
        form_layout.addRow('Calibrated:', self.calibrated)
        form_layout.addRow('Analysed:', self.analyzed)
        form_layout.addRow('Area done:', self.area_done)

        #widget_form = QtGui.QWidget()
        
        #widget_form = QtGui.QWidget()
        self.setLayout(form_layout)

        #self.addWidget(title_left_up)
        #self.addWidget(widget_form)

    def set_combo_box_drawing(self, field, table_name, linedit):
        """
        Define automatically the combo box list with all the element 
        named in the database
        """
        uset_db = database.database()
        values = uset_db.get_values(field, table_name)
        for el in values:
            linedit.addItem(el[0])

    def set_drawing_linedit(self, current_drawing):
        """
        Fill the linEdits with the information of the drawing.
        """
        self.drawing_operator.setText(current_drawing.operator)

        if (current_drawing.last_update_time and
            isinstance(current_drawing.last_update_time, datetime)):
            self.drawing_last_update.setDate(
                QtCore.QDate(current_drawing.last_update_time.year,
                             current_drawing.last_update_time.month, 
                             current_drawing.last_update_time.day))
        else:
            #self.drawing_last_update.clear()
            self.drawing_last_update.setDate(
                QtCore.QDate(00,
                             00, 
                             00))
            
        #elif (current_drawing.last_update_time and
        #      isinstance(current_drawing.last_update_time, str)):
        #self.drawing_last_update.setText(
        # str(current_drawing.last_update_time))
                
        self.drawing_observer.setText(current_drawing.observer)

        self.drawing_date.setDate(
            QtCore.QDate(current_drawing.datetime.year,
                         current_drawing.datetime.month,
                         current_drawing.datetime.day))

        self.drawing_time.setText(
            str(current_drawing.datetime.strftime('%H')) + ":" +
            str(current_drawing.datetime.strftime('%M')))
    
        self.drawing_quality.blockSignals(True)
        index_drawing_quality = self.drawing_quality.findText(
            current_drawing.quality)
        self.drawing_quality.setCurrentIndex(index_drawing_quality)
        self.drawing_quality.blockSignals(False)
        
        self.drawing_type.blockSignals(True)
        index_drawing_type = self.drawing_type.findText(
            current_drawing.drawing_type)
        self.drawing_type.setCurrentIndex(index_drawing_type)
        self.drawing_type.blockSignals(False)
        
        self.angleP.setText('{0:.2f}'.format(current_drawing.angle_P))
        self.angleB.setText('{0:.2f}'.format(current_drawing.angle_B))
        self.angleL.setText('{0:.2f}'.format(current_drawing.angle_L))
        self.rotation_number.setText(str(current_drawing.carington_rotation))
        self.calibrated.setText(str(current_drawing.calibrated))
        self.analyzed.setText(str(current_drawing.analyzed))
        self.wolf_number.setText(str(current_drawing.wolf))
        
