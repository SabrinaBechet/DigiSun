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
from PyQt4 import QtGui, QtCore

__author__ = "Mael Panouillot, Sabrina Bechet"

def inputVoid(self):
    pass


class QLabelClickable(QtGui.QLabel):
    """
    Label on which one can click (used to delete group)
    """
    clicked = QtCore.pyqtSignal()

    def __init__(self):
        super(QtGui.QLabel, self).__init__()

    def mouseReleaseEvent(self, QMouseEvent):
        self.clicked.emit()


class GroupBox(QtGui.QWidget):
    """
    Represent the box associated to a group.
    It is used in the group_widget and in the group_toolbox.
    It consits of
    - combo box for zurich type
    - combo box for mcIntosh type
    - etc...
    Attributes:
    - grid_layout : layout of the group box
    - zurich_dipolar : list of zurich group being dipolar + "x"
    - widget_maximum_width : the maximum width of a widget in the group box
    - area_button: indicate the status of the group area
    - dipole_button: indicate the status of the group dipole
    - delete_button: allow to suppress a group
    - button_up, button_down, button_right, button_left : buttons to udpate
    the positions
    Methods:
    - set_title
    - set_area_button
    - set_dipole_button
    - set_delete_group_button
    - set_arrows_buttons
    - set_spot_count
    - set_zurich_combo_box
    - update_McIntoshc_combo_box
    - set_mcIntosh_combo_box
    - set_longitude
    - set_latitude
    - update_largest_spot_buttons
    - set_largest_spot
    - set_surface
    """

    group_box_clicked = QtCore.pyqtSignal()

    def __init__(self):
        super(GroupBox, self).__init__()
        self.grid_layout = QtGui.QGridLayout()
        self.setStyleSheet("color: darkblue")
        self.setLayout(self.grid_layout)
        self.zurich_dipolar = ["B", "C", "D", "E", "F", "G", "X"]
        self.widget_maximum_width = 60

    def set_title(self, group_id, grid_position):
        """ title on the top of the group box"""
        #title_label = QtGui.QLabel(title)
        title_label = QtGui.QLabel("Group ")
        #title_label.setMaximumWidth()
        self.group_number_linedit = QtGui.QLineEdit(self)
        self.group_number_linedit.setMaximumWidth(self.widget_maximum_width)
        self.group_number_linedit.setDisabled(True)
        title_label.setStyleSheet("background-color: transparent")

        if group_id != 'None': 
            print("found a group id", group_id, type(group_id))
            self.group_number_linedit.setText(group_id)
       
        
        self.group_number_linedit.setStyleSheet(
            "background-color: white; color: black")
        self.grid_layout.addWidget(title_label,
                                   grid_position[0],
                                   grid_position[1])
        self.grid_layout.addWidget(self.group_number_linedit,
                                   grid_position[0],
                                   grid_position[1] + 1)
        
    def set_area_button(self, grid_position):
        """ button orange if surface not complete, transparent otherwhise"""
        self.area_button = QLabelClickable()
        area_pix = QtGui.QPixmap("icons/Freepik/layout_24.png")
        self.area_button.setPixmap(area_pix)
        self.area_button.setMaximumSize(24, 24)
        self.area_button.setStyleSheet(
                    "background-color: transparent")
        self.grid_layout.addWidget(self.area_button,
                                   grid_position[0],
                                   grid_position[1])

    def set_dipole_button(self, grid_position):
        """
        button orange if dipole not complete, transparent otherwhise.
        A dipole is not complete when:
        - if dipolar and position not filled
        - if dipolar and LTS not filled
        """
        self.dipole_button = QLabelClickable()
        dipole_pix = QtGui.QPixmap('icons/mine/my_dipole_icon2_24.png')
        self.dipole_button.setPixmap(dipole_pix)
        self.dipole_button.setMaximumSize(24, 24)
        self.dipole_button.setStyleSheet(
            "background-color: transparent")
        self.grid_layout.addWidget(self.dipole_button,
                                   grid_position[0],
                                   grid_position[1])

    def set_delete_group_button(self, grid_position):
        """ button to suprress a group"""
        self.delete_button = QLabelClickable()
        delete_pix = QtGui.QPixmap("icons/delete_cross_16.png")
        self.delete_button.setPixmap(delete_pix)
        self.delete_button.setMaximumSize(16, 16)
        self.delete_button.setStyleSheet(
            "background-color: transparent")
        self.grid_layout.addWidget(self.delete_button,
                                   grid_position[0],
                                   grid_position[1])

    def set_arrows_buttons(self, grid_position):

        self.button_up = QtGui.QPushButton()
        arrow_up_pix = QtGui.QPixmap("icons/arrow_up.png")
        arrow_up = QtGui.QIcon(arrow_up_pix)
        self.button_up.setIcon(arrow_up)

        self.button_down = QtGui.QPushButton()
        arrow_down_pix = QtGui.QPixmap("icons/arrow_down.png")
        arrow_down = QtGui.QIcon(arrow_down_pix)
        self.button_down.setIcon(arrow_down)

        self.button_left = QtGui.QPushButton()
        arrow_left_pix = QtGui.QPixmap("icons/arrow_left.png")
        arrow_left = QtGui.QIcon(arrow_left_pix)
        self.button_left.setIcon(arrow_left)

        self.button_right = QtGui.QPushButton()
        self.button_right.setMinimumWidth(self.widget_maximum_width)
        self.button_right.setMaximumWidth(self.widget_maximum_width)
        arrow_right_pix = QtGui.QPixmap("icons/arrow_right.png")
        arrow_right = QtGui.QIcon(arrow_right_pix)
        self.button_right.setIcon(arrow_right)

        self.grid_layout.addWidget(self.button_up,
                                   grid_position[0],
                                   grid_position[1] + 1)
        self.grid_layout.addWidget(self.button_down,
                                   grid_position[0] + 2,
                                   grid_position[1] + 1)
        self.grid_layout.addWidget(self.button_left,
                                   grid_position[0] + 1,
                                   grid_position[1])
        self.grid_layout.addWidget(self.button_right,
                                   grid_position[0] + 1,
                                   grid_position[1] + 2)

    def set_spot_count(self, spot_count, grid_position):
        #self.spot_number_linedit = QtGui.QLineEdit(str(spot_count))
        self.spot_number_spinbox = QtGui.QSpinBox(self)#LineEdit(str(spot_count))
        self.spot_number_spinbox.setMinimum(0)
        self.spot_number_spinbox.setMaximum(1000)
        self.spot_number_spinbox.setValue(spot_count)
        
        #self.spot_number_spinbox.setDisabled(True)
        self.spot_number_spinbox.setMaximumWidth(self.widget_maximum_width)
        self.spot_number_spinbox.setStyleSheet(
            "background-color: white; color: black")
        self.grid_layout.addWidget(self.spot_number_spinbox,
                                   grid_position[0],
                                   grid_position[1])

    def set_zurich_combox_box(self, group_zurich_type, grid_position):
        self.zurich_combo = QtGui.QComboBox(self)
        self.zurich_combo.setStyleSheet("background-color: white; color:black")
        # Cancel the usual Mouse Wheel Event by giving to it a void function
        self.zurich_combo.wheelEvent = inputVoid

        zurich_type_lst = ['X', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'J']
        for el in zurich_type_lst:
            self.zurich_combo.addItem(el)

        self.grid_layout.addWidget(self.zurich_combo,
                                   grid_position[0],
                                   grid_position[1])
        self.zurich_combo\
            .setCurrentIndex(self.zurich_combo.findText(group_zurich_type))

        self.zurich_combo\
            .setItemData(0, QtCore.Qt.black, QtCore.Qt.BackgroundRole)

    def update_McIntosh_combo_box(self, zurich_type):
        # this is giving the empty line in the
        # drawing object!!! (signal of change)
        self.McIntosh_combo.clear()

        # Cancel the usual Mouse Wheel Event by giving to it a void function
        self.McIntosh_combo.wheelEvent = inputVoid
        
        zurich_McIntosh = {}
        zurich_McIntosh['X'] = ['Xxx']
        zurich_McIntosh['A'] = ['   ','Axx']
        zurich_McIntosh['B'] = ['   ','Bxo', 'Bxi']
        zurich_McIntosh['C'] = ['   ','Cro', 'Cri',
                                'Cso', 'Csi',
                                'Cao', 'Cai',
                                'Cho', 'Chi',
                                'Cko', 'Cki']
        zurich_McIntosh['D'] = ['   ','Dro', 'Dri',
                                'Dso', 'Dsi', 'Dsc',
                                'Dao', 'Dai', 'Dac',
                                'Dho', 'Dhi', 'Dhc',
                                'Dko', 'Dki', 'Dkc']
        zurich_McIntosh['E'] = ['   ','Esi', 'Esc',
                                'Eai', 'Eac',
                                'Ehi', 'Ehc',
                                'Eki', 'Ekc']
        zurich_McIntosh['F'] = ['   ','Fhi', 'Fhc',
                                'Fki', 'Fkc']
        zurich_McIntosh['G'] = ['   ','Cho', 'Chi',
                                'Cko', 'Cki',
                                'Dho', 'Dhi',
                                'Dko', 'Dki',
                                'Eso', 'Esi',
                                'Eko', 'Eki',
                                'Eho', 'Ehi',
                                'Eao', 'Eai',
                                'Fhi', 'Fhc',
                                'Fki', 'Fkc']
        zurich_McIntosh['H'] = ['   ','Hkx', 'Hhx']
        zurich_McIntosh['J'] = ['   ','Hsx', 'Hax']

        for el in zurich_McIntosh[str(zurich_type)]:
                self.McIntosh_combo.addItem(el)

    def set_mcIntosh_combo_box(self, mcIntosh_type, zurich_type,
                               grid_position):
        self.McIntosh_combo = QtGui.QComboBox(self)
        self.update_McIntosh_combo_box(zurich_type)
        self.McIntosh_combo.setStyleSheet(
            "background-color: white; color: black")
        self.grid_layout.addWidget(self.McIntosh_combo,
                                   grid_position[0],
                                   grid_position[1])
        if mcIntosh_type:
            index = self.McIntosh_combo.findText(mcIntosh_type)
            self.McIntosh_combo.setCurrentIndex(index)


    def set_label_and_linedit(self, label, label_value,
                              linedit, linedit_value, grid_position):
        """
        Standard function to add a label+linedit in the group box
        """
        label.setText(label_value)
        linedit.setText(linedit_value)
        linedit.setStyleSheet(
            "background-color: white; color: black")
        self.grid_layout.addWidget(label,
                                   grid_position[0],
                                   grid_position[1])
        self.grid_layout.addWidget(linedit,
                                   grid_position[0],
                                   grid_position[1] + 1)
        
    def set_longitude(self, longitude, grid_position):

        self.longitude_label = QtGui.QLabel()
        self.longitude_linedit = QtGui.QLineEdit(self)
    
        self.set_label_and_linedit(self.longitude_label,
                                   "Longitude",
                                   self.longitude_linedit,
                                   '{0:.2f}'.format(longitude),
                                   grid_position)
    
    def set_latitude(self, latitude, grid_position):
        self.latitude_label = QtGui.QLabel()
        self.latitude_linedit = QtGui.QLineEdit(self)
    
        self.set_label_and_linedit(self.latitude_label,
                                   "Latitude",
                                   self.latitude_linedit,
                                   '{0:.2f}'.format(latitude),
                                   grid_position)

    """def set_group_number(self, group_number, grid_position):
        self.group_number_label = QtGui.QLabel()
        self.group_number_linedit = QtGui.QLineEdit(self)


        self.set_label_and_linedit(self.group_number_label,
                                   "Group nb",
                                   self.group_number_linedit,
                                   str(group_number),
                                   grid_position)
    """ 
    def set_surface(self, surface, grid_position):
        self.surface_label = QtGui.QLabel()
        self.surface_linedit = QtGui.QLineEdit(self)

        if surface is None:
            surface = 0.
        
        self.set_label_and_linedit(self.surface_label,
                                   "Area",
                                   self.surface_linedit,
                                   '{0:.2f}'.format(surface),
                                   grid_position)
        
        if surface == 0.:
            self.surface_linedit.setStyleSheet(
                "background-color: rgb(255, 165, 84)")
        else:
            self.surface_linedit.setStyleSheet(
                "background-color: white; color: black")


    def set_extra_field1(self, extra1_value, extra1_name, grid_position):
        self.group_extra1_label = QtGui.QLabel()
        self.group_extra1_linedit = QtGui.QLineEdit(self)

        self.set_label_and_linedit(self.group_extra1_label,
                                   str(extra1_name),
                                   self.group_extra1_linedit,
                                   str(extra1_value),
                                   grid_position)

    def set_extra_field2(self, extra2_value, extra2_name, grid_position):
        self.group_extra2_label = QtGui.QLabel()
        self.group_extra2_linedit = QtGui.QLineEdit(self)

        self.set_label_and_linedit(self.group_extra2_label,
                                   str(extra2_name),
                                   self.group_extra2_linedit,
                                   str(extra2_value),
                                   grid_position)

    def set_extra_field3(self, extra3_value, extra3_name, grid_position):
        self.group_extra3_label = QtGui.QLabel()
        self.group_extra3_linedit = QtGui.QLineEdit(self)

        self.set_label_and_linedit(self.group_extra3_label,
                                   str(extra3_name),
                                   self.group_extra3_linedit,
                                   str(extra3_value),
                                   grid_position)
            
            
    def update_largest_spot_buttons(self, largest_spot, zurich_type):
        """
        Update the colors of the LTS buttons if needed.
        - if group not dipolar -> lightblue and disabled
        - if group dipolar and lts not filled -> orange and enabled
        - if group dipolar and lts filled -> L, T or E in green and enabled
        """
        if (zurich_type.upper() not in self.zurich_dipolar):
            self.largest_spot_leading_but.setStyleSheet(
                "background-color: lightblue")
            self.largest_spot_trailing_but.setStyleSheet(
                "background-color: lightblue")
            self.largest_spot_egal_but.setStyleSheet(
                "background-color: lightblue")
            self.largest_spot_leading_but.setDisabled(True)
            self.largest_spot_trailing_but.setDisabled(True)
            self.largest_spot_egal_but.setDisabled(True)
        elif (zurich_type.upper() in self.zurich_dipolar and
              largest_spot is None):
            self.largest_spot_leading_but.setStyleSheet(
                "background-color: rgb(255, 165, 84)")
            self.largest_spot_trailing_but.setStyleSheet(
                "background-color: rgb(255, 165, 84)")
            self.largest_spot_egal_but.setStyleSheet(
                "background-color: rgb(255, 165, 84)")
            self.largest_spot_leading_but.setDisabled(False)
            self.largest_spot_trailing_but.setDisabled(False)
            self.largest_spot_egal_but.setDisabled(False)
        elif largest_spot is 'L':
            self.largest_spot_leading_but.setStyleSheet(
                "background-color: rgb(77, 185, 88)")
            self.largest_spot_trailing_but.setStyleSheet(
                "background-color: lightblue")
            self.largest_spot_egal_but.setStyleSheet(
                "background-color: lightblue")
            self.largest_spot_leading_but.setDisabled(False)
            self.largest_spot_trailing_but.setDisabled(False)
            self.largest_spot_egal_but.setDisabled(False)
        elif largest_spot is 'T':
            self.largest_spot_trailing_but.setStyleSheet(
                "background-color: rgb(77, 185, 88)")
            self.largest_spot_leading_but.setStyleSheet(
                "background-color: lightblue")
            self.largest_spot_egal_but.setStyleSheet(
                "background-color: lightblue")
            self.largest_spot_leading_but.setDisabled(False)
            self.largest_spot_trailing_but.setDisabled(False)
            self.largest_spot_egal_but.setDisabled(False)
        elif largest_spot is 'E':
            self.largest_spot_egal_but.setStyleSheet(
                "background-color: rgb(77, 185, 88)")
            self.largest_spot_leading_but.setStyleSheet(
                "background-color: lightblue")
            self.largest_spot_trailing_but.setStyleSheet(
                "background-color: lightblue")
            self.largest_spot_leading_but.setDisabled(False)
            self.largest_spot_trailing_but.setDisabled(False)
            self.largest_spot_egal_but.setDisabled(False)

    def set_largest_spot(self, largest_spot, zurich_type, grid_position):
        """
        Create the widget and update the value of it.
        """
        self.largest_spot_label = QtGui.QLabel("Lead/Trail")

        self.largest_spot_leading_but = QtGui.QPushButton("L")
        self.largest_spot_leading_but.setShortcut(QtGui.QKeySequence("f"))
        self.largest_spot_leading_but.setToolTip('shortcut: \'f\'')

        self.largest_spot_egal_but = QtGui.QPushButton("=")
        self.largest_spot_egal_but.setShortcut(QtGui.QKeySequence("g"))
        self.largest_spot_egal_but.setToolTip('shortcut: \'g\'')
        
        self.largest_spot_trailing_but = QtGui.QPushButton("T")
        self.largest_spot_trailing_but.setShortcut(QtGui.QKeySequence("h"))
        self.largest_spot_trailing_but.setToolTip('shortcut: \'h\'')

        self.grid_layout.addWidget(self.largest_spot_label,
                                   grid_position[0],
                                   grid_position[1])
        self.grid_layout.addWidget(self.largest_spot_leading_but,
                                   grid_position[0],
                                   grid_position[1] + 1)
        self.grid_layout.addWidget(self.largest_spot_egal_but,
                                   grid_position[0],
                                   grid_position[1] + 2)
        self.grid_layout.addWidget(self.largest_spot_trailing_but,
                                   grid_position[0],
                                   grid_position[1] + 3)

        self.update_largest_spot_buttons(largest_spot, zurich_type)

    
