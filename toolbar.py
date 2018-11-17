# !/usr/bin/env python
# -*-coding:utf-8-*-
import os
from PyQt4 import QtGui, QtCore


class Toolbar(QtGui.QToolBar):
    """Note : The QToolBar class inherit from QWidget.
    """
    
    def __init__(self, drawing_page, level_info):
        super(Toolbar, self).__init__()

        self.zoom_in_but = QtGui.QToolButton(self)
        self.zoom_in_but.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.zoom_in_but.setText("zoom in")
        self.zoom_in_but.setIcon(QtGui.QIcon('icons/Smashicons/zoom-in.svg'))

        self.zoom_out_but = QtGui.QToolButton(self)
        self.zoom_out_but.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.zoom_out_but.setText("zoom out")
        self.zoom_out_but.setIcon(QtGui.QIcon('icons/Smashicons/search.svg'))
   
        self.large_grid_but = QtGui.QToolButton(self)
        self.large_grid_but.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.large_grid_but.setText("large grid")
        self.large_grid_but.setIcon(QtGui.QIcon('icons/Smashicons/internet.svg'))

        self.small_grid_but = QtGui.QToolButton(self)
        self.small_grid_but.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.small_grid_but.setText("small grid")
        self.small_grid_but.setIcon(QtGui.QIcon('icons/Smashicons/internet.svg'))

        self.group_visu_but = QtGui.QToolButton(self)
        self.group_visu_but.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.group_visu_but.setText("group view")
        self.group_visu_but.setIcon(QtGui.QIcon('icons/Smashicons/share_1.svg'))

        self.dipole_visu_but = QtGui.QToolButton(self)
        self.dipole_visu_but.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.dipole_visu_but.setText("dipole view")
        self.dipole_visu_but.setIcon(QtGui.QIcon('icons/Smashicons/share.svg'))

        self.helper_grid_but = QtGui.QToolButton(self)
        self.helper_grid_but.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.helper_grid_but.setText("helper grid")
        self.helper_grid_but.setIcon(QtGui.QIcon('icons/Smashicons/internet.svg'))

        self.calibration_but = QtGui.QToolButton(self)
        self.calibration_but.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.calibration_but.setText("calibrate")
        self.calibration_but.setIcon(QtGui.QIcon('icons/Smashicons/target.svg'))

        self.add_group_but = QtGui.QToolButton(self)
        self.add_group_but.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.add_group_but.setText("add group")
        self.add_group_but.setIcon(QtGui.QIcon('icons/hospital.svg'))

        vertical_line_widget = QtGui.QWidget()
        vertical_line_widget.setFixedWidth(2)
        vertical_line_widget.setStyleSheet("background-color: black")

        self.addWidget(self.zoom_in_but)
        self.addWidget(self.zoom_out_but)
        self.addWidget(self.large_grid_but)
        self.addWidget(self.small_grid_but)
        self.addWidget(self.group_visu_but)
        self.addWidget(self.dipole_visu_but)
        self.addWidget(vertical_line_widget)
        self.addWidget(self.helper_grid_but)
        self.addWidget(self.calibration_but)
        self.addWidget(self.add_group_but)
        
        if 'dipole' in level_info:
            self.add_dipole_but = QtGui.QToolButton(self)
            self.add_dipole_but.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
            self.add_dipole_but.setText("add dipole")
            self.add_dipole_but.setIcon(QtGui.QIcon('icons/Smashicons/share.svg'))
            self.addWidget(self.add_dipole_but)

        if 'area' in level_info:
            self.surface_but = QtGui.QToolButton(self)
            self.surface_but.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
            self.surface_but.setText("surface")
            self.surface_but.setIcon(QtGui.QIcon('icons/layout.svg'))
            self.addWidget(self.surface_but)
            
        drawing_page.label_right.large_grid_overlay.value_changed.connect(
            lambda: self.set_button_color(
                drawing_page.label_right.large_grid_overlay.value,
                self.large_grid_but ))
        if drawing_page.label_right.large_grid_overlay.value :
            self.large_grid_but.setStyleSheet("background-color: lightblue")
                
        drawing_page.label_right.small_grid_overlay.value_changed.connect(
            lambda: self.set_button_color(
                drawing_page.label_right.small_grid_overlay.value,
                self.small_grid_but))
        if drawing_page.label_right.small_grid_overlay.value :
            self.small_grid_but.setStyleSheet("background-color: lightblue")

        drawing_page.label_right.group_visu.value_changed.connect(
            lambda: self.set_button_color(
                drawing_page.label_right.group_visu.value,
                self.group_visu_but))
        if drawing_page.label_right.group_visu.value :
            self.group_visu_but.setStyleSheet("background-color: lightblue")

        drawing_page.label_right.dipole_visu.value_changed.connect(
            lambda: self.set_button_color(
                drawing_page.label_right.dipole_visu.value,
                self.dipole_visu_but))
        if drawing_page.label_right.dipole_visu.value :
            self.dipole_visu_but.setStyleSheet("background-color: lightblue")

       
        drawing_page.label_right.helper_grid.value_changed.connect(
            lambda: self.set_button_color(
                drawing_page.label_right.helper_grid.value,
                self.helper_grid_but))
        if drawing_page.label_right.helper_grid.value :
            self.helper_grid_but.setStyleSheet("background-color: lightblue")
            
       
        drawing_page.label_right.calibration_mode.value_changed.connect(
            lambda: self.set_button_color(
                drawing_page.label_right.calibration_mode.value,
                self.calibration_but))
        if drawing_page.label_right.calibration_mode.value :
            self.calibration_but.setStyleSheet("background-color: lightblue")
        
        drawing_page.label_right.add_group_mode.value_changed.connect(
            lambda: self.set_button_color(
                drawing_page.label_right.add_group_mode.value,
                self.add_group_but))
        if drawing_page.label_right.add_group_mode.value :
            self.add_group_but.setStyleSheet("background-color: lightblue")
        
        drawing_page.label_right.add_dipole_mode.value_changed.connect(
            lambda: self.set_button_color(
                drawing_page.label_right.add_dipole_mode.value,
                self.add_dipole_but))
        if drawing_page.label_right.add_dipole_mode.value :
            self.add_dipole_but.setStyleSheet("background-color: lightblue")

        drawing_page.label_right.surface_mode.value_changed.connect(
            lambda: self.set_button_color(
                drawing_page.label_right.surface_mode.value,
                self.surface_but))
        if drawing_page.label_right.surface_mode.value :
            self.surface_but.setStyleSheet("background-color: lightblue")
                 
    def set_button_color(self, mode_bool, but):
        if mode_bool==True:
            but.setStyleSheet("background-color: lightblue")
        elif mode_bool==False:
            but.setStyleSheet("background-color: lightgray")
