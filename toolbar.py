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
from PyQt4 import QtGui, QtCore


class Toolbar(QtGui.QToolBar):
    """Note : The QToolBar class inherit from QWidget.
    """

    def __init__(self, label_right, level_info):
        super(Toolbar, self).__init__()

        self.setContextMenuPolicy(QtCore.Qt.PreventContextMenu)
        
        self.zoom_in_but = QtGui.QToolButton(self)
        if sys.platform=='darwin':                                                                                                        
            self.zoom_in_but.setAttribute(QtCore.Qt.WA_MacNormalSize)
            self.zoom_in_but.setToolTip("zoom in: \'+\'")
        else:
            self.zoom_in_but.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
            self.zoom_in_but.setText("zoom in")
            self.zoom_in_but.setToolTip("\'+\'")
        self.zoom_in_but.setIcon(QtGui.QIcon('icons/Smashicons/zoom-in.png'))
        self.zoom_in_but.setShortcut(QtGui.QKeySequence("+"))
        
        self.zoom_out_but = QtGui.QToolButton(self)
        if sys.platform=='darwin':
            self.zoom_out_but.setAttribute(QtCore.Qt.WA_MacNormalSize)
            self.zoom_out_but.setToolTip("zoom out: \'-\'")            
        else:
            self.zoom_out_but.setToolTip("\'-\'")
            self.zoom_out_but.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
            self.zoom_out_but.setText("zoom out")
        self.zoom_out_but.setIcon(QtGui.QIcon('icons/Smashicons/zoom-out.png'))
        self.zoom_out_but.setShortcut(QtGui.QKeySequence("-"))

        self.quick_zoom_but = QtGui.QToolButton(self)
        if sys.platform=='darwin':
            self.quick_zoom_but.setAttribute(QtCore.Qt.WA_MacNormalSize)
            self.quick_zoom_but.setToolTip("zoom-to-fit: \'5\'")
        else:
            self.quick_zoom_but.setToolTip("\'5\'")
            self.quick_zoom_but.setToolButtonStyle(
                QtCore.Qt.ToolButtonTextUnderIcon)
            self.quick_zoom_but.setText("zoom-to-fit")
        self.quick_zoom_but.setIcon(QtGui.QIcon('icons/mine/zoom_5.png'))
        self.quick_zoom_but.setShortcut(QtGui.QKeySequence("5"))

        self.large_grid_but = QtGui.QToolButton(self)
        if sys.platform=='darwin':
            self.large_grid_but.setAttribute(QtCore.Qt.WA_MacNormalSize)
            self.large_grid_but.setToolTip("large grid: \'Alt+a\'")
        else:
            self.large_grid_but.setToolTip("\'Alt+a\'")
            self.large_grid_but.setToolButtonStyle(
                QtCore.Qt.ToolButtonTextUnderIcon)
            self.large_grid_but.setText("l&arge grid")
        self.large_grid_but.setIcon(
            QtGui.QIcon('icons/Smashicons/internet.png'))
        self.large_grid_but.setShortcut(QtGui.QKeySequence("Alt+a"))

        self.small_grid_but = QtGui.QToolButton(self)
        if sys.platform=='darwin':
            self.small_grid_but.setAttribute(QtCore.Qt.WA_MacNormalSize)
            self.small_grid_but.setToolTip("small grid: \'Alt+s\'")
        else:
            self.small_grid_but.setToolTip("\'Alt+s\'")
            self.small_grid_but.setToolButtonStyle(
                QtCore.Qt.ToolButtonTextUnderIcon)
            self.small_grid_but.setText("&small grid")
        self.small_grid_but.setIcon(
            QtGui.QIcon('icons/Smashicons/internet.png'))
        self.small_grid_but.setShortcut(QtGui.QKeySequence("Alt+s"))

        self.group_visu_but = QtGui.QToolButton(self)
        if sys.platform=='darwin':
            self.group_visu_but.setAttribute(QtCore.Qt.WA_MacNormalSize)
            self.group_visu_but.setToolTip("group visu: \'Alt+r\'")
        else:
            self.group_visu_but.setToolTip("\'Alt+r\'")
            self.group_visu_but.setToolButtonStyle(
                QtCore.Qt.ToolButtonTextUnderIcon)
            self.group_visu_but.setText("g&roup view")
        self.group_visu_but.setIcon(
            QtGui.QIcon('icons/Smashicons/share_1.png'))
        self.group_visu_but.setShortcut(QtGui.QKeySequence("Alt+r"))

        self.dipole_visu_but = QtGui.QToolButton(self)
        if sys.platform=='darwin':
            self.dipole_visu_but.setAttribute(QtCore.Qt.WA_MacNormalSize)
            self.dipole_visu_but.setToolTip("dipole visu: \'Alt+d\'")
        else:
            self.dipole_visu_but.setToolTip("\'Alt+d\'")
            self.dipole_visu_but.setToolButtonStyle(
                QtCore.Qt.ToolButtonTextUnderIcon)
            self.dipole_visu_but.setText("&dipole view")
        self.dipole_visu_but.setIcon(
            QtGui.QIcon('icons/mine/my_dipole_icon2.png'))
        self.dipole_visu_but.setShortcut(QtGui.QKeySequence("Alt+d"))

        self.helper_grid_but = QtGui.QToolButton(self)
        if sys.platform=='darwin':
            self.helper_grid_but.setAttribute(QtCore.Qt.WA_MacNormalSize)
            self.helper_grid_but.setToolTip("helper grid: \'z\'")
        else:
            self.helper_grid_but.setToolTip("\'z\'")
            self.helper_grid_but.setToolButtonStyle(
                QtCore.Qt.ToolButtonTextUnderIcon)
            self.helper_grid_but.setText("helper grid")
        self.helper_grid_but.setIcon(
            QtGui.QIcon('icons/Smashicons/internet.png'))
        self.helper_grid_but.setShortcut(QtGui.QKeySequence("z"))
        
        self.calibration_but = QtGui.QToolButton(self)
        if sys.platform=='darwin':
            self.calibration_but.setAttribute(QtCore.Qt.WA_MacNormalSize)
            #self.calibration_but.setToolTip("calibration: \'c\'")
        else:
            #self.calibration_but.setToolTip("\'c\'")
            self.calibration_but.setToolButtonStyle(
                QtCore.Qt.ToolButtonTextUnderIcon)
            self.calibration_but.setText("calibrate")
        self.calibration_but.setIcon(
            QtGui.QIcon('icons/Smashicons/target.png'))
        #self.calibration_but.setShortcut(QtGui.QKeySequence("c"))

        self.add_group_but = QtGui.QToolButton(self)
        if sys.platform=='darwin':
            self.add_group_but.setAttribute(QtCore.Qt.WA_MacNormalSize)
            self.add_group_but.setToolTip("add group: \'e\'")
        else:
            self.add_group_but.setToolTip("\'e\'")
            self.add_group_but.setToolButtonStyle(
                QtCore.Qt.ToolButtonTextUnderIcon)
            self.add_group_but.setText("add group")
        self.add_group_but.setIcon(QtGui.QIcon('icons/hospital.png'))
        self.add_group_but.setShortcut(QtGui.QKeySequence("r"))

        self.change_group_pos_but = QtGui.QToolButton(self)
        if sys.platform=='darwin':
            self.change_group_pos_but.setAttribute(QtCore.Qt.WA_MacNormalSize)
            self.change_group_pos_but.setToolTip("group pos: \'r\'")
        else:
            self.change_group_pos_but.setToolTip("\'r\'")
            self.change_group_pos_but.setToolButtonStyle(
                QtCore.Qt.ToolButtonTextUnderIcon)
            self.change_group_pos_but.setText("group pos")
        self.change_group_pos_but.setIcon(QtGui.QIcon('icons/Smashicons/map-location.png'))
        self.change_group_pos_but.setShortcut(QtGui.QKeySequence("r"))

        vertical_line_widget = QtGui.QWidget()
        vertical_line_widget.setFixedWidth(2)
        vertical_line_widget.setStyleSheet("background-color: black")

        self.addWidget(self.zoom_in_but)
        self.addWidget(self.zoom_out_but)
        self.addWidget(self.quick_zoom_but)
        self.addWidget(self.large_grid_but)
        self.addWidget(self.small_grid_but)
        self.addWidget(self.group_visu_but)
        self.addWidget(self.dipole_visu_but)
        self.addWidget(vertical_line_widget)
        self.addWidget(self.helper_grid_but)
        self.addWidget(self.calibration_but)
        self.addWidget(self.add_group_but)
        self.addWidget(self.change_group_pos_but)

        if 'dipole' in level_info:
            self.add_dipole_but = QtGui.QToolButton(self)
            if sys.platform=='darwin':
                self.add_dipole_but.setAttribute(QtCore.Qt.WA_MacNormalSize)
                self.add_dipole_but.setToolTip("add dipole:\'t\'")
            else:
                self.add_dipole_but.setToolTip("\'t\'")
                self.add_dipole_but.setToolButtonStyle(
                    QtCore.Qt.ToolButtonTextUnderIcon)
                self.add_dipole_but.setText("add dipole")
            self.add_dipole_but.setIcon(
                QtGui.QIcon('icons/mine/my_dipole_icon2.png'))
            self.add_dipole_but.setShortcut(QtGui.QKeySequence("d"))
            self.addWidget(self.add_dipole_but)

        if 'area' in level_info:
            self.surface_but = QtGui.QToolButton(self)
            if sys.platform=='darwin':
                self.surface_but.setAttribute(QtCore.Qt.WA_MacNormalSize)
                self.surface_but.setToolTip("Area: \'y\'")
            else:
                self.surface_but.setToolTip("\'y\'")
                self.surface_but.setToolButtonStyle(
                    QtCore.Qt.ToolButtonTextUnderIcon)
                self.surface_but.setText("group area")
            self.surface_but.setIcon(QtGui.QIcon('icons/Freepik/layout.png'))
            self.surface_but.setShortcut(QtGui.QKeySequence("y"))
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

        label_right.add_dipole_mode.value_changed.connect(
            lambda: self.set_button_color(
                label_right.add_dipole_mode.value,
                self.add_dipole_but))
        if label_right.add_dipole_mode.value:
            self.add_dipole_but.setStyleSheet("background-color: lightblue")

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
