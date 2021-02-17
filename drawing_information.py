# !/usr/bin/env python
# -*-coding:utf-8-*-
"""
DigiSun: a software to transform sunspot drawings into exploitable data. It allows to scan drawings, extract its information and store it in a database.
Copyright (C) 2019 Sabrina Bechet at Royal Observatory of Belgium (ROB)

This file is part of DigiSun.

DigiSun is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

DigiSun is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with DigiSun.  If not, see <https://www.gnu.org/licenses/>.
"""

import database
from datetime import datetime
from PyQt5 import QtGui, QtWidgets, QtCore

__author__ = "Sabrina Bechet"
__email__ = "sabrina.bechet@oma.be"
__date__ = "April 2019"


def inputVoid(self):
    pass


class DrawingInformationWidget(QtWidgets.QWidget):

    def __init__(self, config):
        super(DrawingInformationWidget, self).__init__()
        form_layout = QtGui.QFormLayout()
        form_layout.setSpacing(10)

        uset_db = database.database(config)

        self.drawing_operator = QtWidgets.QLineEdit(self)
        self.drawing_operator.setEnabled(True)
        self.drawing_operator.setStyleSheet(
            "background-color: lightgray; color:black")

        self.drawing_last_update = QtWidgets.QLineEdit(self)
        self.drawing_last_update.setEnabled(True)
        self.drawing_last_update.setStyleSheet(
            "background-color: lightgray; color:black")
        self.drawing_observer = QtWidgets.QLineEdit(self)
        self.drawing_observer.setEnabled(True)
        self.drawing_observer.setStyleSheet(
            "background-color: white; color:black")

        self.drawing_date = QtGui.QDateEdit()
        self.drawing_date.setDisplayFormat("dd/MM/yyyy")
        self.drawing_date.setEnabled(False)
        self.drawing_date.setStyleSheet(
            "background-color: lightgray; color:black")

        self.drawing_time = QtWidgets.QLineEdit("00:00", self)
        self.drawing_time.setInputMask("99:99")
        self.drawing_time.setEnabled(False)
        self.drawing_time.setStyleSheet(
            "background-color: lightgray; color:black")

        self.drawing_quality = QtGui.QComboBox(self)
        # Cancel the usual Mouse Wheel Event by giving to it a void function
        self.drawing_quality.wheelEvent = inputVoid
        uset_db.set_combo_box_drawing('name', 'quality', self.drawing_quality)
        self.drawing_quality.setEnabled(True)
        self.drawing_quality.setStyleSheet(
            "background-color: white; color:black")

        self.drawing_type = QtGui.QComboBox(self)
         # Cancel the usual Mouse Wheel Event by giving to it a void function
        self.drawing_type.wheelEvent = inputVoid
        uset_db.set_combo_box_drawing('name',
                                      'drawing_type',
                                      self.drawing_type)
        self.drawing_type.setEnabled(True)
        self.drawing_type.setStyleSheet(
            "background-color: white; color:black")

        self.wolf_number = QtWidgets.QLineEdit(self)
        self.wolf_number.setEnabled(False)
        self.wolf_number.setStyleSheet(
            "background-color: lightgrey; color:black")

        self.angleP = QtWidgets.QLineEdit(self)
        self.angleP.setEnabled(False)
        self.angleP.setStyleSheet(
            "background-color: lightgrey; color:black")

        self.angleB = QtWidgets.QLineEdit(self)
        self.angleB.setEnabled(False)
        self.angleB.setStyleSheet(
            "background-color: lightgrey; color:black")

        self.angleL = QtWidgets.QLineEdit(self)
        self.angleL.setEnabled(False)
        self.angleL.setStyleSheet(
            "background-color: lightgrey; color:black")

        self.rotation_number = QtWidgets.QLineEdit(self)
        self.rotation_number.setEnabled(False)
        self.rotation_number.setStyleSheet(
            "background-color: lightgrey; color:black")

        self.calibrated = QtWidgets.QLineEdit(self)
        self.calibrated.setEnabled(False)
        self.calibrated.setStyleSheet(
            "background-color: lightgrey; color:black")

        self.analyzed = QtWidgets.QLineEdit(self)
        self.analyzed.setEnabled(False)
        self.analyzed.setStyleSheet(
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
        form_layout.addRow('Carrington rotation :', self.rotation_number)

        form_layout.addRow('Last Operator:', self.drawing_operator)
        form_layout.addRow('Last Update:', self.drawing_last_update)
        form_layout.addRow('Calibrated:', self.calibrated)
        form_layout.addRow('All group marked:', self.analyzed)

        self.setLayout(form_layout)

    def set_empty(self):
        self.drawing_operator.setText(" ")
        self.drawing_last_update.setText('00/00/0000')
        self.drawing_observer.setText(" ")
        self.drawing_date.setDate(
            QtCore.QDate(2000, 1, 1))
        self.drawing_time.setText("00:00")
        self.wolf_number.setText(" ")
        self.angleP.setText(" ")
        self.angleB.setText(" ")
        self.angleL.setText(" ")
        self.rotation_number.setText(" ")
        self.calibrated.setText(" ")
        self.analyzed.setText(" ")

    def set_drawing_linedit(self, current_drawing):
        """
        Fill the linEdits with the information of the drawing.
        """
        self.drawing_operator.setText(current_drawing.operator)

        if (current_drawing.last_update_time and
                isinstance(current_drawing.last_update_time, datetime)):
            self.drawing_last_update.setText(
                str(current_drawing.last_update_time.strftime('%d')) + "/" +
                str(current_drawing.last_update_time.strftime('%m')) + "/" +
                str(current_drawing.last_update_time.strftime('%Y')))

        elif (current_drawing.last_update_time and
              isinstance(current_drawing.last_update_time, str)):
            self.drawing_last_update.setText('00/00/0000')

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
        self.rotation_number.setText(str(current_drawing.carrington_rotation))
        self.calibrated.setText(str(current_drawing.calibrated))
        self.analyzed.setText(str(current_drawing.analyzed))
        self.wolf_number.setText(str(current_drawing.wolf))
