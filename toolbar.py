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

import sys
from PyQt5 import QtGui, QtWidgets, QtCore


class Toolbar(QtWidgets.QToolBar):
    """Note : The QToolBar class inherit from QWidget.
    """

    def __init__(self, label_right, level_info):
        super(Toolbar, self).__init__()

        self.setContextMenuPolicy(QtCore.Qt.PreventContextMenu)

        zoom_in_dict = {'name':'zoom in', 'path':"icons/Smashicons/zoom-in.png",
                        'tooltip': "\'+\'", 'shortcut' : "+"}
        zoom_out_dict = {'name':'zoom out', 'path':"icons/Smashicons/zoom-out.png",
                        'tooltip': "\'-\'", 'shortcut' : "-"}
        zoom_to_fit_dict = {'name':'zoom to 5', 'path':'icons/mine/zoom_5.png',
                            'tooltip': "\'Alt+f\'", 'shortcut' : "Alt+f"}
        large_grid_dict = {'name':'l&arge grid', 'path':'icons/Smashicons/internet.png',
                           'tooltip': "\'Alt+a\'", 'shortcut' : "Alt+a"}
        
        small_grid_dict = {'name':'&small grid', 'path':'icons/Smashicons/internet.png',
                           'tooltip': "\'Alt+s\'", 'shortcut' : "Alt+s"}
        
        group_visu_dict = {'name':'g&roup view', 'path':'icons/Smashicons/share_1.png',
                           'tooltip': "\'Alt+r\'", 'shortcut' : "Alt+r"}
        
        dipole_visu_dict = {'name':'&dipole view', 'path':'icons/mine/my_dipole_icon2.png',
                           'tooltip': "\'Alt+d\'", 'shortcut' : "Alt+d"}

        helper_grid_dict = {'name':'h&elper grid', 'path':'icons/Smashicons/internet.png',
                           'tooltip': "\'e\''", 'shortcut' : "e"}
        
        calibration_dict = {'name':'&calibrate', 'path':'icons/Smashicons/target.png',
                           'tooltip': "\'c\'", 'shortcut' : "c"}
        
        add_group_dict = {'name':'add g&roup', 'path':'icons/hospital.png',
                           'tooltip': "\'r\'", 'shortcut' : "r"}
        change_group_pos_dict = {'name':'group pos', 'path':'icons/Smashicons/map-location.png',
                           'tooltip': "\'z\'", 'shortcut' : "z"}
        add_dipole_dict = {'name':'add &dipole', 'path':'icons/mine/my_dipole_icon2.png',
                           'tooltip': "\'d\'", 'shortcut' : "d"}
        area_dict = {'name':'group &area', 'path':'icons/Freepik/layout.png',
                           'tooltip': "\'a\'", 'shortcut' : "a"}
        
        
        self.zoom_in_but = QtWidgets.QToolButton(self)
        if sys.platform=='darwin':
            self.zoom_in_but.setAttribute(QtCore.Qt.WA_MacNormalSize)
            self.zoom_in_but.setToolTip("zoom in: \'+\'")
        else:
            self.zoom_in_but.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
            self.zoom_in_but.setText(zoom_in_dict['name'])
            self.zoom_in_but.setToolTip(zoom_in_dict['tooltip'])
        self.zoom_in_but.setIcon(QtGui.QIcon(zoom_in_dict['path']))
        self.zoom_in_but.setShortcut(QtGui.QKeySequence(zoom_in_dict['shortcut']))
        
        self.zoom_out_but = QtWidgets.QToolButton(self)
        if sys.platform=='darwin':
            self.zoom_out_but.setAttribute(QtCore.Qt.WA_MacNormalSize)
            self.zoom_out_but.setToolTip("zoom out: \'-\'")            
        else:
            self.zoom_out_but.setToolTip(zoom_out_dict['tooltip'])
            self.zoom_out_but.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
            self.zoom_out_but.setText(zoom_out_dict['name'])
        self.zoom_out_but.setIcon(QtGui.QIcon(zoom_out_dict['path']))
        self.zoom_out_but.setShortcut(QtGui.QKeySequence(zoom_out_dict['shortcut']))

        self.quick_zoom_but = QtWidgets.QToolButton(self)
        if sys.platform=='darwin':
            self.quick_zoom_but.setAttribute(QtCore.Qt.WA_MacNormalSize)
            self.quick_zoom_but.setToolTip("zoom-to-fit: \'Alt+f\'")
        else:
            self.quick_zoom_but.setToolTip(zoom_to_fit_dict['tooltip'])
            self.quick_zoom_but.setToolButtonStyle(
                QtCore.Qt.ToolButtonTextUnderIcon)
            self.quick_zoom_but.setText(zoom_to_fit_dict['name'])
        self.quick_zoom_but.setIcon(QtGui.QIcon(zoom_to_fit_dict['path']))
        self.quick_zoom_but.setShortcut(QtGui.QKeySequence(zoom_to_fit_dict['shortcut']))

        self.large_grid_but = QtWidgets.QToolButton(self)
        if sys.platform=='darwin':
            self.large_grid_but.setAttribute(QtCore.Qt.WA_MacNormalSize)
            self.large_grid_but.setToolTip("large grid: \'Alt+a\'")
        else:
            self.large_grid_but.setToolTip(large_grid_dict['tooltip'])
            self.large_grid_but.setToolButtonStyle(
                QtCore.Qt.ToolButtonTextUnderIcon)
            self.large_grid_but.setText(large_grid_dict['name'])
        self.large_grid_but.setIcon(QtGui.QIcon(large_grid_dict['path']))
        self.large_grid_but.setShortcut(QtGui.QKeySequence("Alt+a"))
             

        self.small_grid_but = QtWidgets.QToolButton(self)
        if sys.platform=='darwin':
            self.small_grid_but.setAttribute(QtCore.Qt.WA_MacNormalSize)
            self.small_grid_but.setToolTip("small grid: \'Alt+s\'")
        else:
            self.small_grid_but.setToolTip(small_grid_dict['tooltip'])
            self.small_grid_but.setToolButtonStyle(
                QtCore.Qt.ToolButtonTextUnderIcon)
            self.small_grid_but.setText(small_grid_dict['name'])
        self.small_grid_but.setIcon(QtGui.QIcon(small_grid_dict['path']))
        self.small_grid_but.setShortcut(QtGui.QKeySequence("Alt+s"))

        self.group_visu_but = QtWidgets.QToolButton(self)
        if sys.platform=='darwin':
            self.group_visu_but.setAttribute(QtCore.Qt.WA_MacNormalSize)
            self.group_visu_but.setToolTip("group visu: \'Alt+r\'")
        else:
            self.group_visu_but.setToolTip(group_visu_dict['tooltip'])
            self.group_visu_but.setToolButtonStyle(
                QtCore.Qt.ToolButtonTextUnderIcon)
            self.group_visu_but.setText(group_visu_dict['name'])
        self.group_visu_but.setIcon(QtGui.QIcon(group_visu_dict['path']))
        self.group_visu_but.setShortcut(QtGui.QKeySequence("Alt+r"))

        if 'dipole' in level_info:
            self.dipole_visu_but = QtWidgets.QToolButton(self)
            if sys.platform=='darwin':
                self.dipole_visu_but.setAttribute(QtCore.Qt.WA_MacNormalSize)
                self.dipole_visu_but.setToolTip("dipole visu: \'Alt+d\'")
            else:
                self.dipole_visu_but.setToolTip(dipole_visu_dict['tooltip'])
                self.dipole_visu_but.setToolButtonStyle(
                    QtCore.Qt.ToolButtonTextUnderIcon)
                self.dipole_visu_but.setText(dipole_visu_dict['name'])
            self.dipole_visu_but.setIcon(QtGui.QIcon(dipole_visu_dict['path']))
            self.dipole_visu_but.setShortcut(QtGui.QKeySequence("Alt+d"))

        self.helper_grid_but = QtWidgets.QToolButton(self)
        if sys.platform=='darwin':
            self.helper_grid_but.setAttribute(QtCore.Qt.WA_MacNormalSize)
            self.helper_grid_but.setToolTip("helper grid: \'z\'")
        else:
            self.helper_grid_but.setToolTip(helper_grid_dict['tooltip'])
            self.helper_grid_but.setToolButtonStyle(
                QtCore.Qt.ToolButtonTextUnderIcon)
            self.helper_grid_but.setText(helper_grid_dict['name'])
        self.helper_grid_but.setIcon(QtGui.QIcon(helper_grid_dict['path']))
        self.helper_grid_but.setShortcut(QtGui.QKeySequence("e"))
        
        self.calibration_but = QtWidgets.QToolButton(self)
        if sys.platform=='darwin':
            self.calibration_but.setAttribute(QtCore.Qt.WA_MacNormalSize)
            self.calibration_but.setToolTip("calibration: \'c\'")
        else:
            self.calibration_but.setToolTip(calibration_dict['tooltip'])
            self.calibration_but.setToolButtonStyle(
                QtCore.Qt.ToolButtonTextUnderIcon)
            self.calibration_but.setText(calibration_dict['name'])
        self.calibration_but.setIcon(QtGui.QIcon(calibration_dict['path']))
        self.calibration_but.setShortcut(QtGui.QKeySequence("c"))

        self.add_group_but = QtWidgets.QToolButton(self)
        if sys.platform=='darwin':
            self.add_group_but.setAttribute(QtCore.Qt.WA_MacNormalSize)
            self.add_group_but.setToolTip("add group: \'r\'")
        else:
            self.add_group_but.setToolTip(add_group_dict['tooltip'])
            self.add_group_but.setToolButtonStyle(
                QtCore.Qt.ToolButtonTextUnderIcon)
            self.add_group_but.setText(add_group_dict['name'])
        self.add_group_but.setIcon(QtGui.QIcon(add_group_dict['path']))
        self.add_group_but.setShortcut(QtGui.QKeySequence("r"))

        self.change_group_pos_but = QtWidgets.QToolButton(self)
        if sys.platform=='darwin':
            self.change_group_pos_but.setAttribute(QtCore.Qt.WA_MacNormalSize)
            self.change_group_pos_but.setToolTip("group pos: \'z\'")
        else:
            self.change_group_pos_but.setToolTip(change_group_pos_dict['tooltip'])
            self.change_group_pos_but.setToolButtonStyle(
                QtCore.Qt.ToolButtonTextUnderIcon)
            self.change_group_pos_but.setText(change_group_pos_dict['name'])
        self.change_group_pos_but.setIcon(QtGui.QIcon(change_group_pos_dict['path']))
        self.change_group_pos_but.setShortcut(QtGui.QKeySequence("z"))

        vertical_line_widget = QtWidgets.QWidget()
        vertical_line_widget.setFixedWidth(2)
        vertical_line_widget.setStyleSheet("background-color: black")

        self.addWidget(self.zoom_in_but)
        self.addWidget(self.zoom_out_but)
        self.addWidget(self.quick_zoom_but)
        self.addWidget(self.large_grid_but)
        self.addWidget(self.small_grid_but)
        self.addWidget(self.group_visu_but)
        if 'dipole' in level_info:
            self.addWidget(self.dipole_visu_but)
        self.addWidget(vertical_line_widget)
        self.addWidget(self.helper_grid_but)
        self.addWidget(self.calibration_but)
        self.addWidget(self.add_group_but)
        self.addWidget(self.change_group_pos_but)


        
        if 'dipole' in level_info:
            self.add_dipole_but = QtWidgets.QToolButton(self)
            if sys.platform=='darwin':
                self.add_dipole_but.setAttribute(QtCore.Qt.WA_MacNormalSize)
                self.add_dipole_but.setToolTip("add dipole:\'d\'")
            else:
                self.add_dipole_but.setToolTip(add_dipole_dict['tooltip'])
                self.add_dipole_but.setToolButtonStyle(
                    QtCore.Qt.ToolButtonTextUnderIcon)
                self.add_dipole_but.setText(add_dipole_dict['name'])
            self.add_dipole_but.setIcon(QtGui.QIcon(add_dipole_dict['path']))
            self.add_dipole_but.setShortcut(QtGui.QKeySequence("d"))
            self.addWidget(self.add_dipole_but)

        if 'area' in level_info:
            self.surface_but = QtWidgets.QToolButton(self)
            if sys.platform=='darwin':
                self.surface_but.setAttribute(QtCore.Qt.WA_MacNormalSize)
                self.surface_but.setToolTip("Area: \'a\'")
            else:
                self.surface_but.setToolTip(area_dict['tooltip'])
                self.surface_but.setToolButtonStyle(
                    QtCore.Qt.ToolButtonTextUnderIcon)
                self.surface_but.setText(area_dict['name'])
            self.surface_but.setIcon(QtGui.QIcon(area_dict['path']))
            self.surface_but.setShortcut(QtGui.QKeySequence("a"))
            self.addWidget(self.surface_but)

        label_right.quick_zoom.value_changed.connect(
            lambda: self.set_button_color(
                label_right.quick_zoom.value,
                self.quick_zoom_but))
        if label_right.quick_zoom.value:
            self.quick_zoom_but.setStyleSheet("background-color: lightblue")

        label_right.large_grid_overlay.value_changed.connect(
            lambda: self.set_button_color(
                label_right.large_grid_overlay.value,
                self.large_grid_but))
        if label_right.large_grid_overlay.value:
            self.large_grid_but.setStyleSheet("background-color: lightblue")

        label_right.small_grid_overlay.value_changed.connect(
            lambda: self.set_button_color(
                label_right.small_grid_overlay.value,
                self.small_grid_but))
        if label_right.small_grid_overlay.value:
            self.small_grid_but.setStyleSheet("background-color: lightblue")

        label_right.group_visu.value_changed.connect(
            lambda: self.set_button_color(
                label_right.group_visu.value,
                self.group_visu_but))
        if label_right.group_visu.value:
            self.group_visu_but.setStyleSheet("background-color: lightblue")

        if 'dipole' in level_info:
            label_right.dipole_visu.value_changed.connect(
                lambda: self.set_button_color(
                    label_right.dipole_visu.value,
                    self.dipole_visu_but))
            if label_right.dipole_visu.value:
                self.dipole_visu_but.setStyleSheet("background-color: lightblue")

        label_right.helper_grid.value_changed.connect(
            lambda: self.set_button_color(
                label_right.helper_grid.value,
                self.helper_grid_but))
        if label_right.helper_grid.value:
            self.helper_grid_but.setStyleSheet("background-color: lightblue")

        label_right.calibration_mode.value_changed.connect(
            lambda: self.set_button_color(
                label_right.calibration_mode.value,
                self.calibration_but))
        if label_right.calibration_mode.value:
            self.calibration_but.setStyleSheet("background-color: lightblue")

        label_right.add_group_mode.value_changed.connect(
            lambda: self.set_button_color(
                label_right.add_group_mode.value,
                self.add_group_but))
        if label_right.add_group_mode.value:
            self.add_group_but.setStyleSheet("background-color: lightblue")

        label_right.change_group_position_mode.value_changed.connect(
            lambda: self.set_button_color(
                label_right.change_group_position_mode.value,
                self.change_group_pos_but))
        if label_right.change_group_position_mode.value:
            self.change_group_pos_but.setStyleSheet("background-color: lightblue")

        if 'dipole' in level_info:    
            label_right.add_dipole_mode.value_changed.connect(
                lambda: self.set_button_color(
                    label_right.add_dipole_mode.value,
                    self.add_dipole_but))
            if label_right.add_dipole_mode.value:
                self.add_dipole_but.setStyleSheet("background-color: lightblue")

        if 'area' in level_info:
            label_right.surface_mode.value_changed.connect(
                lambda: self.set_button_color(
                    label_right.surface_mode.value,
                    self.surface_but))
            if label_right.surface_mode.value:
                self.surface_but.setStyleSheet("background-color: lightblue")

    def set_button_color(self, mode_bool, but):
        if mode_bool is True:
            but.setStyleSheet("background-color: lightblue")
        elif mode_bool is False:
            but.setStyleSheet("background-color: lightgray")
