# !/usr/bin/env python
# -*-coding:utf-8-*-
import os
from PyQt4 import QtGui, QtCore

import database, drawing, group_box, qlabel_drawing, qlabel_group_surface, coordinates
from datetime import date, time, datetime, timedelta
import math
import configparser
import time
import numpy as np
import cv2

"""
The classes defined here contains only information related to the GUI of the drawing analyse.
Keep the analyse itself somwhere else!
- DrawingViewPage : the template of the DrawingViewPage
- DrawingAnalysePage: the page itself with all the widgets
"""

class DrawingViewPage(QtGui.QWidget):
    """
    Contains the template of the DrawingViewPage
    The attribute are:
    - widget_left_up (the drawing information)
    - widget_left_up_layout 
    - widget_left_middle (the current session)
    - widget_left_middle_layout 
    - widget_left_down (the group information)
    - widget_left_down_layout 
    - widget_right (the right column, where the drawing is displayed)
    - widget_right_layout (the layout of the right column)
    - label_right (the drawing) 
    There is a splitter that divides the right/left columns.
    """

    def __init__(self):
        super(DrawingViewPage, self).__init__()

        self.setLayout(QtGui.QVBoxLayout())

        left_column_maximum_width = 380

        self.scroll_widget_left_up = QtGui.QScrollArea()
        self.scroll_widget_left_up\
            .setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.scroll_widget_left_up\
            .setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.scroll_widget_left_up .setWidgetResizable(True)
        self.widget_left_up = QtGui.QWidget()
        #self.widget_left_up.setMinimumWidth(left_column_maximum_width)
        #self.widget_left_up.setMaximumHeight(self.width()/2.)#500)
        self.widget_left_up.setStyleSheet("background-color:lightgray;")
        self.scroll_widget_left_up.setWidget(self.widget_left_up)
        
        self.widget_left_up_layout = QtGui.QVBoxLayout()
        self.widget_left_up_layout.setContentsMargins(0, 0, 0, 0) 
        self.widget_left_up_layout.setSpacing(0)
        self.widget_left_up_layout.setAlignment(QtCore.Qt.AlignTop)
        self.widget_left_up.setLayout(self.widget_left_up_layout)
        

        self.widget_left_middle = QtGui.QWidget()
        self.widget_left_middle.setMinimumWidth(left_column_maximum_width)
        self.widget_left_middle.setMaximumHeight(self.height()/2.)#200)
        self.widget_left_middle.setStyleSheet("background-color:lightgray;")   
        self.widget_left_middle_layout = QtGui.QVBoxLayout()
        self.widget_left_middle_layout.setContentsMargins(0, 0, 0, 0) 
        self.widget_left_middle_layout.setSpacing(0)
        self.widget_left_middle_layout.setAlignment(QtCore.Qt.AlignTop)
        self.widget_left_middle.setLayout(self.widget_left_middle_layout)
        self.widget_left_middle_layout.setMargin(10)
        
        self.widget_left_down = QtGui.QWidget()
        self.widget_left_down.setMaximumWidth(left_column_maximum_width)
        self.widget_left_down.setMinimumHeight(self.height()/2.)#200)
        self.widget_left_down.setStyleSheet("background-color:lightblue;")   
        self.widget_left_down_layout = QtGui.QVBoxLayout()
        self.widget_left_down_layout.setContentsMargins(0, 0, 0, 0) 
        self.widget_left_down_layout.setSpacing(0)
        self.widget_left_down_layout.setAlignment(QtCore.Qt.AlignTop and
                                                  QtCore.Qt.AlignRight)
        self.widget_left_down.setLayout(self.widget_left_down_layout)
        
        self.widget_left_down_bis = QtGui.QWidget()
        self.widget_left_down_bis.setMaximumWidth(left_column_maximum_width)
        self.widget_left_down_bis.setMaximumHeight(200)
        self.widget_left_down_bis.setStyleSheet("background-color:lightblue;")   
        self.widget_left_down_bis_layout = QtGui.QVBoxLayout()
        self.widget_left_down_bis_layout.setContentsMargins(0, 0, 0, 0) 
        self.widget_left_down_bis_layout.setSpacing(0)
        self.widget_left_down_bis_layout.setAlignment(QtCore.Qt.AlignTop and
                                                      QtCore.Qt.AlignRight)
        self.widget_left_down_bis.setLayout(self.widget_left_down_bis_layout)
        
        self.widget_middle_up = QtGui.QWidget()
        
        # trick to keep the surface panel closed by default
        self.widget_middle_up.setMaximumWidth(10)
        
        #self.widget_middle_up.setMinimumHeight(200)
        self.widget_middle_up.setStyleSheet("background-color:lightgray;")
        self.widget_middle_up_layout = QtGui.QVBoxLayout()
        self.widget_middle_up_layout.setContentsMargins(0, 0, 0, 0) 
        self.widget_middle_up_layout.setSpacing(10)
        self.widget_middle_up_layout.setAlignment(QtCore.Qt.AlignTop)
        self.widget_middle_up.setLayout(self.widget_middle_up_layout)
        #self.label_middle_up = qlabel_group_surface.QLabelGroupSurface()
        
        self.widget_right = QtGui.QWidget()
        self.widget_right.setStyleSheet("background-color:gray;")
        self.widget_right_layout = QtGui.QVBoxLayout()
        self.widget_right_layout.setContentsMargins(0, 0, 0, 0) 
        self.widget_right_layout.setSpacing(0)
        self.widget_right.setLayout(self.widget_right_layout)
        self.label_right = qlabel_drawing.QLabelDrawing()

        #self.label_middle_up = qlabel_drawing.QLabelGroupSurface()
        
        #self.widget_right.layout().addWidget(self.label_middle_up)
        #self.widget_right.layout().addWidget(self.label_right)
  
        self.scroll = QtGui.QScrollArea()
        self.scroll.setWidget(self.label_right)
        
        self.scroll.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.scroll.setWidgetResizable(True)
 
        self.widget_right_layout.addWidget(self.scroll)
        
        splitter_down = QtGui.QSplitter(QtCore.Qt.Vertical, self)
        self.layout().addWidget(splitter_down)
        splitter_down.addWidget(self.widget_left_down)
        splitter_down.addWidget(self.widget_left_down_bis)
        
        splitter_middle_down = QtGui.QSplitter(QtCore.Qt.Vertical, self)
        self.layout().addWidget(splitter_middle_down)
        #splitter_middle_down.addWidget(self.widget_left_up)
        splitter_middle_down.addWidget(self.scroll_widget_left_up)
        splitter_middle_down.addWidget(self.widget_left_middle)
        splitter_middle_down.addWidget(splitter_down)
              
        splitter_main = QtGui.QSplitter(QtCore.Qt.Horizontal, self)
        self.layout().addWidget(splitter_main)
        splitter_main.addWidget(splitter_middle_down)
        splitter_main.addWidget(self.widget_middle_up)
        splitter_main.addWidget(self.widget_right)
    
class DrawingAnalysePage(QtGui.QMainWindow):
    """
    Page that shows the drawing and where the analyse is done.
    """
    def __init__(self, operator=None):
        super(DrawingAnalysePage, self).__init__()

        self.config = configparser.ConfigParser()
        self.config_file = "digisun.ini"
        self.set_configuration()
        self.drawing_page = DrawingViewPage()
        self.vertical_scroll_bar = self.drawing_page.scroll.verticalScrollBar()
        self.horizontal_scroll_bar = self.drawing_page.scroll.horizontalScrollBar()
        
        self.setCentralWidget(self.drawing_page)
        
        self.operator = operator
        #self.column_maximum_width = 400
        self.add_drawing_information()
        self.add_current_session()
        self.add_surface_widget()
        self.drawing_lst = []
        self.set_toolbar()
        self.set_status_bar()
        
        
        self.drawing_page\
            .label_right\
            .group_added\
            .connect(self.add_group_box)
        
        self.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)

        self.zurich_dipolar = ["B","C","D","E","F","G", "X"]

    def set_configuration(self):
        """
        TO DO:
        the prefix should be read from the database (prefix from the drawing_type table)
        and from the initialization file
        """
        try:
            with open(self.config_file) as config_file:
                self.config.read_file(config_file)
                self.prefix = self.config['archdrawings']['prefix']
                self.archdrawing_directory = self.config['archdrawings']['path']
                self.extension = self.config['archdrawings']['extension']
        except IOError:
            print('IOError - config file not found !!')
        
        
    def set_button_color(self, mode_bool, but):
        if mode_bool==True:
            but.setStyleSheet("background-color: lightblue")
        elif mode_bool==False:
            but.setStyleSheet("background-color: lightgray")


    def set_status_bar(self):
        """
        This is maybe heavy, a more elegant and lighter solution?
        """
        #self.statusBar = QtGui.QStatusBar()
        self.status_bar_mode_name = QtGui.QLabel()
        self.status_bar_mode_name.setStyleSheet(
            "QLabel { background-color : red; color : blue; }");
        self.status_bar_mode_name.setAlignment(QtCore.Qt.AlignHCenter)
        self.status_bar_mode_name.setMinimumSize(self.status_bar_mode_name.sizeHint())
        self.status_bar_mode_comment = QtGui.QLabel()
        self.status_bar_mode_comment.setIndent(3)
              
        #locationLabel = QtGui.QLabel(" this is a test of the status bar... ")
        #self.setStatusBar(self.statusBar)
        
        self.statusBar().addWidget(self.status_bar_mode_name)
        self.statusBar().addWidget(self.status_bar_mode_comment)
        
        """
        self.statusBar().setStyleSheet("background-color : red; color : blue; ");
        self.statusBar().showMessage("this is a test")
        self.statusBar().setMinimumSize(locationLabel.sizeHint())
        """ 
    def set_toolbar(self):
        """Note : The QToolBar class inherit from QWidget.
        Icons were designed by "Good Ware" from https://www.flaticon.com
        """

        toolbar = self.addToolBar("view")
        toolbar.setIconSize(QtCore.QSize(30, 30));

        self.zoom_in_but = QtGui.QToolButton(toolbar)
        self.zoom_in_but.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.zoom_in_but.setText("zoom in")
        self.zoom_in_but.setIcon(QtGui.QIcon('icons/Smashicons/zoom-in.svg'))

        self.zoom_out_but = QtGui.QToolButton(toolbar)
        self.zoom_out_but.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.zoom_out_but.setText("zoom out")
        self.zoom_out_but.setIcon(QtGui.QIcon('icons/Smashicons/search.svg'))
   
        self.large_grid_but = QtGui.QToolButton(toolbar)
        self.large_grid_but.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.large_grid_but.setText("large grid")
        self.large_grid_but.setIcon(QtGui.QIcon('icons/Smashicons/internet.svg'))
        self.drawing_page.label_right\
                         .large_grid_overlay\
                         .value_changed\
                         .connect(lambda: self.set_button_color(
                             self.drawing_page.label_right.large_grid_overlay.value,
                             self.large_grid_but ))
        if self.drawing_page.label_right.large_grid_overlay.value :
            self.large_grid_but.setStyleSheet("background-color: lightblue")
            
        self.small_grid_but = QtGui.QToolButton(toolbar)
        self.small_grid_but.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.small_grid_but.setText("small grid")
        self.small_grid_but.setIcon(QtGui.QIcon('icons/Smashicons/internet.svg'))
        self.drawing_page.label_right\
                         .small_grid_overlay\
                         .value_changed\
                         .connect(lambda: self.set_button_color(
                             self.drawing_page.label_right.small_grid_overlay.value,
                             self.small_grid_but))
        if self.drawing_page.label_right.small_grid_overlay.value :
            self.small_grid_but.setStyleSheet("background-color: lightblue")

        self.group_visu_but = QtGui.QToolButton(toolbar)
        self.group_visu_but.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.group_visu_but.setText("group view")
        self.group_visu_but.setIcon(QtGui.QIcon('icons/Smashicons/share_1.svg'))
        self.drawing_page.label_right\
                         .group_visu\
                         .value_changed\
                         .connect(lambda: self.set_button_color(
                             self.drawing_page.label_right.group_visu.value,
                             self.group_visu_but))
        if self.drawing_page.label_right.group_visu.value :
            self.group_visu_but.setStyleSheet("background-color: lightblue")


        self.dipole_visu_but = QtGui.QToolButton(toolbar)
        self.dipole_visu_but.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.dipole_visu_but.setText("dipole view")
        self.dipole_visu_but.setIcon(QtGui.QIcon('icons/Smashicons/share.svg'))
        self.drawing_page.label_right\
                         .dipole_visu\
                         .value_changed\
                         .connect(lambda: self.set_button_color(
                             self.drawing_page.label_right.dipole_visu.value,
                             self.dipole_visu_but))
        if self.drawing_page.label_right.dipole_visu.value :
            self.dipole_visu_but.setStyleSheet("background-color: lightblue")

        self.helper_grid_but = QtGui.QToolButton(toolbar)
        self.helper_grid_but.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.helper_grid_but.setText("helper grid")
        self.helper_grid_but.setIcon(QtGui.QIcon('icons/Smashicons/internet.svg'))
        self.drawing_page.label_right\
                         .helper_grid\
                         .value_changed\
                         .connect(lambda: self.set_button_color(
                             self.drawing_page.label_right.helper_grid.value,
                             self.helper_grid_but))
        if self.drawing_page.label_right.helper_grid.value :
            self.helper_grid_but.setStyleSheet("background-color: lightblue")
            
        self.calibration_but = QtGui.QToolButton(toolbar)
        self.calibration_but.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.calibration_but.setText("calibrate")
        self.calibration_but.setIcon(QtGui.QIcon('icons/Smashicons/target.svg'))
        self.drawing_page.label_right\
                         .calibration_mode\
                         .value_changed\
                         .connect(lambda: self.set_button_color(
                             self.drawing_page.label_right.calibration_mode.value,
                             self.calibration_but))
        if self.drawing_page.label_right.calibration_mode.value :
            self.calibration_but.setStyleSheet("background-color: lightblue")

        self.add_group_but = QtGui.QToolButton(toolbar)
        self.add_group_but.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.add_group_but.setText("add group")
        self.add_group_but.setIcon(QtGui.QIcon('icons/hospital.svg'))
        self.drawing_page.label_right\
                         .add_group_mode\
                         .value_changed\
                         .connect(lambda: self.set_button_color(
                             self.drawing_page.label_right.add_group_mode.value,
                             self.add_group_but))
        if self.drawing_page.label_right.add_group_mode.value :
            self.add_group_but.setStyleSheet("background-color: lightblue")

        self.add_dipole_but = QtGui.QToolButton(toolbar)
        self.add_dipole_but.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.add_dipole_but.setText("add dipole")
        self.add_dipole_but.setIcon(QtGui.QIcon('icons/Smashicons/share.svg'))
        self.drawing_page.label_right\
                         .add_dipole_mode\
                         .value_changed\
                         .connect(lambda: self.set_button_color(
                             self.drawing_page.label_right.add_dipole_mode.value,
                             self.add_dipole_but))
        if self.drawing_page.label_right.add_dipole_mode.value :
            self.add_dipole_but.setStyleSheet("background-color: lightblue")

        self.surface_but = QtGui.QToolButton(toolbar)
        self.surface_but.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.surface_but.setText("surface")
        self.surface_but.setIcon(QtGui.QIcon('icons/layout.svg'))
        self.drawing_page.label_right\
                         .surface_mode\
                         .value_changed\
                         .connect(lambda: self.set_button_color(
                             self.drawing_page.label_right.surface_mode.value,
                             self.surface_but))
        if self.drawing_page.label_right.surface_mode.value :
            self.surface_but.setStyleSheet("background-color: lightblue")
            
         
        vertical_line_widget = QtGui.QWidget()
        vertical_line_widget.setFixedWidth(2)
        vertical_line_widget.setStyleSheet("background-color: black")

        vertical_line_widget2 = QtGui.QWidget()
        vertical_line_widget2.setFixedWidth(2)
        vertical_line_widget2.setStyleSheet("background-color: black")

        toolbar.addWidget(self.zoom_in_but)
        toolbar.addWidget(self.zoom_out_but)
        toolbar.addWidget(self.large_grid_but)
        toolbar.addWidget(self.small_grid_but)
        toolbar.addWidget(self.group_visu_but)
        toolbar.addWidget(self.dipole_visu_but)
        toolbar.addWidget(vertical_line_widget)
        toolbar.addWidget(self.helper_grid_but)
        #toolbar.addWidget(vertical_line_widget2)
        toolbar.addWidget(self.calibration_but)
        toolbar.addWidget(self.add_group_but)
        toolbar.addWidget(self.add_dipole_but)
        toolbar.addWidget(self.surface_but)
        
        self.zoom_in_but\
            .clicked\
            .connect(lambda : self.drawing_page.label_right.zoom_in(1.1))
        self.zoom_out_but\
            .clicked\
            .connect(lambda : self.drawing_page.label_right.zoom_in(1/1.1))
        self.large_grid_but.clicked.connect(self.set_large_grid)
        self.small_grid_but.clicked.connect(self.set_small_grid)
        self.group_visu_but.clicked.connect(self.set_group_visualisation)
        self.dipole_visu_but.clicked.connect(self.set_dipole_visualisation)

        self.helper_grid_but.clicked.connect(self.set_helper_grid)
        self.calibration_but.clicked.connect(self.start_calibration)
        self.add_group_but.clicked.connect(self.set_group_mode)
        self.add_dipole_but.clicked.connect(self.set_dipole_mode)
        self.surface_but.clicked.connect(self.calculate_surface)


    def set_helper_grid(self):
        """
        This set the helper grid. It does :
        - reset the cursor shape to the original one
        - inverse the boolean value of the helper_grid mode
        - show a message in the status bar
        - if helper_grid is active, desactive all the other action modes
        The rest is done in the mouseEvent of the qlabel object.
        """
        #QtGui.QApplication.restoreOverrideCursor()
        self.drawing_page.label_right.setCursor(QtCore.Qt.ArrowCursor)
        self.drawing_page.label_right.helper_grid.set_opposite_value()
        
        if self.drawing_page.label_right.helper_grid.value:
            self.status_bar_mode_name.setText("Helper grid mode")
            if self.drawing_lst[self.current_count].calibrated==0:
                self.status_bar_mode_comment.setText(" Warning :" +
                                                     " The calibration must" +
                                                     " be  done before using" +
                                                     " the helper grid!")
            else:
                self.status_bar_mode_comment.setText("Click on a point" +
                                                     " on the solar disk" +
                                                     " to see the helper" +
                                                     " grid ")
            if self.drawing_page.label_right.calibration_mode.value:
                self.start_calibration()   
            self.drawing_page.label_right.add_group_mode.value = False
            self.drawing_page.label_right.add_dipole_mode.value = False
            self.drawing_page.label_right.surface_mode.value = False
            self.drawing_page.widget_middle_up.setMaximumWidth(10)
            
        else:
            self.clean_status_bar()
            self.drawing_page.label_right.set_img()
       
    def set_group_mode(self):
        """
        This set the adding group mode. It does:
        - reset the cursor to its original shape
        - set all the other action mode to false
        - if group visu mode not activated -> activate it 
        - set the cursor to one showing that we are in the add group mode
        """
        QtGui.QApplication.restoreOverrideCursor()
        self.drawing_page.label_right.add_group_mode.set_opposite_value()
        
        if self.drawing_page.label_right.add_group_mode.value:
            self.status_bar_mode_name.setText("Add group mode")
            
            if not self.drawing_page.label_right.group_visu.value:
                self.drawing_page.label_right.group_visu.value = True
                self.drawing_page.label_right.set_img()

            if self.drawing_lst[self.current_count].calibrated==0:
                self.status_bar_mode_comment.setText(" Warning :" +
                                                     " The calibration must" +
                                                     " be  done before adding" +
                                                     " groups!")
            else:
                self.status_bar_mode_comment.setText("Click on a the group" +
                                                     " position to add it")
                cursor_img = ("/home/sabrinabct/Projets/DigiSun_2018_gitlab/" +
                              "cursor/Pixel_perfect/target_24.png")
                cursor_add_group = QtGui.QCursor(QtGui.QPixmap(cursor_img))
                #QtGui.QApplication.setOverrideCursor(cursor_add_group)
                self.drawing_page.label_right.setCursor(cursor_add_group)
                

            if self.drawing_page.label_right.calibration_mode.value:
                self.start_calibration() 
            self.drawing_page.label_right.helper_grid.value = False
            self.drawing_page.label_right.add_dipole_mode.value = False
            self.drawing_page.label_right.surface_mode.value = False
            self.drawing_page.widget_middle_up.setMaximumWidth(10)

        else:
            print("restore the old cursor")
            #QtGui.QApplication.restoreOverrideCursor()
            self.drawing_page.label_right.setCursor(QtCore.Qt.ArrowCursor)
            self.clean_status_bar()

    def add_group_box(self):
        """
        Fonction associated to the add_group mode, 
        it adds the box associated to each group.
        """
        print("Enter in the add group function..")
        print("group count", self.drawing_lst[self.current_count].group_count)
        
        self.set_group_widget()
        self.set_focus_group_box(self.drawing_lst[self.current_count].group_count - 1)
        self.set_group_toolbox(self.drawing_lst[self.current_count].group_count - 1)
        self.update_group_visu(self.drawing_lst[self.current_count].group_count - 1)
        self.wolf_number.setText(str(self.drawing_lst[self.current_count].wolf))
        
    def set_dipole_mode(self):
        """
        It does:
        - reset the cursor to its original shape
        - set all the other action mode to false
        """
        QtGui.QApplication.restoreOverrideCursor()
        self.drawing_page.label_right.add_dipole_mode.set_opposite_value()
        
        if self.drawing_page.label_right.add_dipole_mode.value:
            self.status_bar_mode_name.setText("Add dipole mode")

            if not self.drawing_page.label_right.dipole_visu.value:
                self.drawing_page.label_right.dipole_visu.value = True
                self.drawing_page.label_right.set_img()

            if self.drawing_lst[self.current_count].calibrated==0:
                self.status_bar_mode_comment.setText(" Warning :" +
                                                     " The calibration must" +
                                                     " be  done before adding" +
                                                     " dipole!")
                
            elif (self.drawing_lst[self.current_count].calibrated==1 and
                  self.drawing_lst[self.current_count].group_count==0):
                self.status_bar_mode_comment.setText(" Warning :" +
                                                     " Dipolar groups must" +
                                                     " be  added before adding" +
                                                     " dipole!")
                
            elif (self.drawing_lst[self.current_count].calibrated==1 and
                  self.drawing_lst[self.current_count].group_count > 0):
                self.check_dipole(self.listWidget_groupBox.currentRow())
                #QtGui.QApplication.setOverrideCursor(QtCore.Qt.SizeFDiagCursor)
                #self.drawing_page.label_right.setCursor(QtCore.Qt.SizeFDiagCursor)
            
            self.drawing_page.label_right.helper_grid.value = False
            self.drawing_page.label_right.calibration_mode.value = False
            self.drawing_page.label_right.add_group_mode.value = False
            self.drawing_page.label_right.surface_mode.value = False
            self.drawing_page.widget_middle_up.setMaximumWidth(10)
        else:
            print("restore the old cursor")
            QtGui.QApplication.restoreOverrideCursor()
            self.clean_status_bar()
            
    def calculate_surface(self, n):
        QtGui.QApplication.restoreOverrideCursor()
        self.drawing_page.label_right.surface_mode.set_opposite_value()

        if self.drawing_page.label_right.surface_mode.value:
            self.drawing_page.label_right.helper_grid.value = False
            self.drawing_page.label_right.calibration_mode.value = False
            self.drawing_page.label_right.add_group_mode.value = False
            self.drawing_page.label_right.add_dipole_mode.value = False
            
            self.drawing_page.label_right.zoom_in(
                5./self.drawing_page.label_right.scaling_factor)
            self.set_focus_group_box(0)
        
        if self.drawing_page.label_right.surface_mode.value:
            self.drawing_page.widget_middle_up.setMaximumWidth(600)
            #self.drawing_page.widget_middle_up.setMinimumHeight(580)
            self.update_surface_qlabel(n)

        elif self.drawing_page.label_right.surface_mode.value == False:
            self.drawing_page.widget_middle_up.setMaximumWidth(10)
            self.drawing_page.label_right.zoom_in(
                1/self.drawing_page.label_right.scaling_factor)
            #self.drawing_page.widget_middle_up.setMinimumHeight(580)


    def update_surface_qlabel(self, n):
        """
        Update the QLabelGroupSurface object which represent an image of the drawing 
        to calculate the surface.
        This method uses heliographic coordinates so it needs 
        the calibration to be done!
        More: it need groups to be added... as it is the group surface!
        """
        print("update surface qlabel number:", n)
        if (self.drawing_lst[self.current_count].calibrated and
            self.drawing_page.label_right.surface_mode):
            
            posX = self.drawing_lst[self.current_count]\
                            .group_lst[n]\
                            .posX
            posY = self.drawing_lst[self.current_count]\
                           .group_lst[n]\
                           .posY

            #coords = posX, posY, 0
            #coords = self.drawing_page.label_right.get_cartesian_coordinate_from_HGC(longitude, latitude)
            #coords = 0,0,0
            #coords = list(coords)
            
            # don't forget to document this:
            print("------------------------------------CHECK!!!!!!!",
                  self.drawing_page.label_right.pixmap().height(),
                  self.drawing_page.label_right.drawing_pixMap.height())

            frame_size = math.floor(self.drawing_lst[self.current_count].calibrated_radius/400.) * 100
            print("the frame size is: ", frame_size)

            img_pix = self.drawing_page.label_right.get_img_array()

            #take a bigger matrix to have the border at 0
            bigger_matrix = np.ones((img_pix.shape[0] + 200,
                                     img_pix.shape[1] + 200), dtype=np.uint8) * 255
            bigger_matrix[100 : 100 + img_pix.shape[0],
                          100 : 100 + img_pix.shape[1]] = img_pix
            
            x_min = int(100 + posX - frame_size/2)
            x_max = int(100 + posX + frame_size/2)
            y_min = int(100 + posY - frame_size/2)
            y_max = int(100 + posY + frame_size/2)

            selection_array = bigger_matrix[y_min:y_max,x_min:x_max]
            self.group_surface_widget.set_array(selection_array)
            self.group_surface_widget.set_radius(self.drawing_lst[self.current_count].calibrated_radius)

            print("coordinates for the pixel matrix:")
            print(type(selection_array))
            print(selection_array.shape)
            print(x_min, x_max, y_min, y_max)
            
            
    def scroll_position(self, horizontal_pos, vertical_pos, point_name=None):
        """
        Automatically scroll to the position given 
        by the self.fraction_width and self.fraction_height.
        """
        """print("************scroll function")
        print("image width:", self.drawing_page.label_right.pixmap().width())
        print("image height: ", self.drawing_page.label_right.pixmap().height())
        print("fraction width: ", self.fraction_width)
        print("fraction height: ", self.fraction_height)
        """
        if point_name:
            self.status_bar_mode_comment.setText("Click on the " +
                                                 point_name +
                                                 " position")
            
        self.vertical_scroll_bar.setMinimum(0)
        self.horizontal_scroll_bar.setMinimum(0)
        self.vertical_scroll_bar.setMaximum(
            self.drawing_page.label_right.pixmap().height() -
            self.vertical_scroll_bar.pageStep())
        self.horizontal_scroll_bar.setMaximum(self.drawing_page.label_right.pixmap().width() -
                                              self.horizontal_scroll_bar.pageStep() )
  
        self.horizontal_scroll_bar.setValue(
            self.horizontal_scroll_bar.maximum() * horizontal_pos)
        self.vertical_scroll_bar.setValue(
            self.vertical_scroll_bar.maximum() * vertical_pos)

    def clean_status_bar(self):
        self.status_bar_mode_name.setText("")
        self.status_bar_mode_comment.setText("")
    
    def start_calibration(self):
        """
        Contains two parts:
        1. put the drawing on the center and click on the center -> signal
        2. put the drawing on the north and click on the norht -> signal
        here it is what happens when one click on the calibrate button
        (the rest is described in the mouse event)
        """
        self.drawing_page.label_right.calibration_mode.set_opposite_value()
        QtGui.QApplication.restoreOverrideCursor()

        if self.drawing_page.label_right.calibration_mode.value:    
            #QtGui.QApplication.setOverrideCursor(QtCore.Qt.CrossCursor)
            self.drawing_page.label_right.setCursor(QtCore.Qt.CrossCursor)
            self.status_bar_mode_name.setText("Calibration mode")
            
            
            print("start calibration",
                  self.drawing_page.label_right.calibration_mode.value)
            self.drawing_page.label_right.calibration_mode.value = True
            self.drawing_page.label_right.center_done = False
            self.drawing_page.label_right.north_done = False
            print("start calibration",
                  self.drawing_page.label_right.calibration_mode.value,
                  self.drawing_page.label_right.center_done,
                  self.drawing_page.label_right.north_done)
        
            self.drawing_page.label_right.group_visu.value = False
            self.drawing_page.label_right.dipole_visu.value = False
            self.drawing_page.label_right.large_grid_overlay.value = False
            self.drawing_page.label_right.small_grid_overlay.value = False

            self.drawing_page.label_right.helper_grid.value = False
            self.drawing_page.label_right.add_group_mode.value = False
            self.drawing_page.label_right.add_dipole_mode.value = False
            self.drawing_page.label_right.surface_mode.value = False
            self.drawing_page.widget_middle_up.setMaximumWidth(10)
            
            self.drawing_page.label_right.zoom_in(
                5./self.drawing_page.label_right.scaling_factor)
            
            fraction_width_pt1 = self.drawing_lst[self.current_count]\
                                      .pt1_fraction_width
            fraction_height_pt1 = self.drawing_lst[self.current_count]\
                                       .pt1_fraction_height
            point_name_pt1 = self.drawing_lst[self.current_count].pt1_name
            self.scroll_position(fraction_width_pt1,
                                 fraction_height_pt1,
                                 point_name_pt1)

            fraction_width_pt2 = self.drawing_lst[self.current_count]\
                                      .pt2_fraction_width
            fraction_height_pt2 = self.drawing_lst[self.current_count]\
                                       .pt2_fraction_height
            point_name_pt2 = self.drawing_lst[self.current_count].pt2_name

            self.drawing_page\
                .label_right\
                .center_clicked\
                .connect(lambda : self.scroll_position(fraction_width_pt2,
                                                       fraction_height_pt2,
                                                       point_name_pt2))
            self.drawing_page\
                .label_right\
                .north_clicked\
                .connect(self.clean_status_bar)
            
            """self.drawing_page.label_right.group_visu.value = True
            self.drawing_page.label_right.dipole_visu.value = False
            self.drawing_page.label_right.large_grid_overlay.value = True
            self.drawing_page.label_right.small_grid_overlay.value = False
            """
            
        else:
            QtGui.QApplication.restoreOverrideCursor()
            self.drawing_page.label_right.zoom_in(
                1/self.drawing_page.label_right.scaling_factor)
            print("out of the calibration")
            self.clean_status_bar()

    def set_group_visualisation(self):
        self.drawing_page.label_right.group_visu.set_opposite_value()
        self.drawing_page.label_right.set_img()
        
    def set_dipole_visualisation(self):
        self.drawing_page.label_right.dipole_visu.set_opposite_value()
        self.drawing_page.label_right.set_img()
        
    def set_large_grid(self):
        self.drawing_page.label_right.large_grid_overlay.set_opposite_value()
        if self.drawing_page.label_right.large_grid_overlay.value :
            self.drawing_page.label_right.small_grid_overlay.value = False
        self.drawing_page.label_right.set_img()
              
    def set_small_grid(self):
        self.drawing_page.label_right.small_grid_overlay.set_opposite_value()
        if self.drawing_page.label_right.small_grid_overlay.value:
            self.drawing_page.label_right.large_grid_overlay.value = False
        self.drawing_page.label_right.set_img()
        
    def set_group_widget(self):
        """
        Associate a widget to each group.
        """
        # A widget is deleted when its parents is deleted.
        for i in reversed(range(self.drawing_page.widget_left_down_layout.count())):
                self.drawing_page.widget_left_down_layout\
                                 .itemAt(i)\
                                 .widget()\
                                 .setParent(None)

        title_left_down = QtGui.QLabel("Group information")
        title_left_down.setAlignment(QtCore.Qt.AlignCenter)
        title_left_down.setContentsMargins(0, 5, 0, 5)
        self.drawing_page.widget_left_down_layout.addWidget(title_left_down)
        
        group_count = self.drawing_lst[self.current_count].group_count
                                         
        self.listWidget_groupBox = QtGui.QListWidget(self)
        self.listWidget_groupBox.setStyleSheet(
            "QListView::item:selected {background : rgb(77, 185, 88);}")
        
        self.groupBoxLineList = []
        for i in range(group_count):
    
            grid_position = [0, 0]
            groupBoxLine = group_box.GroupBox()
            groupBoxLine.set_title(
                "Group " +
                str(self.drawing_lst[self.current_count].group_lst[i].number),
                grid_position)
            
            grid_position[1] += 1
            groupBoxLine.set_spot_count(
                self.drawing_lst[self.current_count].group_lst[i].spots,
                grid_position)
            
            grid_position[1] += 1
            groupBoxLine.set_zurich_combox_box(
                self.drawing_lst[self.current_count].group_lst[i].zurich,
                grid_position)
            
            grid_position[1] += 1
            groupBoxLine.set_mcIntosh_combo_box(
                self.drawing_lst[self.current_count].group_lst[i].McIntosh,
                self.drawing_lst[self.current_count].group_lst[i].zurich,
                grid_position)

            grid_position[1] += 1
            groupBoxLine.set_dipole_button(grid_position)

            grid_position[1] += 1
            groupBoxLine.set_area_button(grid_position)

            if self.drawing_lst[self.current_count].group_lst[i].zurich == "X":
                groupBoxLine.zurich_combo.setStyleSheet(
                    "background-color: rgb(255, 165, 84)")
                
            if self.drawing_lst[self.current_count].group_lst[i].spots==0:
                groupBoxLine.spot_number_linedit.setStyleSheet(
                    "background-color: rgb(255, 165, 84)")
  
            if (self.drawing_lst[self.current_count].group_lst[i].zurich.upper()
                in self.zurich_dipolar and
                (self.drawing_lst[self.current_count].group_lst[i].g_spot==0 or
                 self.drawing_lst[self.current_count].group_lst[i].dipole1_lat is None)):
                groupBoxLine.dipole_button.setStyleSheet(
                    "background-color: rgb(255, 165, 84)")

            if (self.drawing_lst[self.current_count].group_lst[i].surface is None or
                self.drawing_lst[self.current_count].group_lst[i].surface==0):
                groupBoxLine.area_button.setStyleSheet(
                    "background-color: rgb(255, 165, 84)")
        
            groupBoxLine.spot_number_linedit.textEdited.connect(
                lambda: self.modify_drawing_spots(
                    self.listWidget_groupBox.currentRow(),
                    False))
            groupBoxLine.zurich_combo.currentIndexChanged.connect(
                lambda: self.modify_drawing_zurich(
                    self.listWidget_groupBox.currentRow(),
                    False))
            groupBoxLine.McIntosh_combo.currentIndexChanged.connect(
                lambda: self.modify_drawing_mcIntosh(
                    self.listWidget_groupBox.currentRow(),
                    False))
            
            self.groupBoxLineList.append(groupBoxLine)
            
            item = QtGui.QListWidgetItem(self.listWidget_groupBox)
            item.setSizeHint(groupBoxLine.sizeHint())
            self.listWidget_groupBox.setItemWidget(item, groupBoxLine)
           
        self.drawing_page.widget_left_down_layout.addWidget(self.listWidget_groupBox)
        
        # Signals related to the change of item in the group box
        self.listWidget_groupBox.itemSelectionChanged.connect(
            lambda: self.set_focus_group_box(
                self.listWidget_groupBox.currentRow()))
        
        self.listWidget_groupBox.itemSelectionChanged.connect(
            lambda: self.set_group_toolbox(
                self.listWidget_groupBox.currentRow()))
        
        self.listWidget_groupBox.itemSelectionChanged.connect(
            lambda: self.update_group_visu(
                self.listWidget_groupBox.currentRow()))

        self.listWidget_groupBox.itemSelectionChanged.connect(
            lambda: self.update_surface_qlabel(
                self.listWidget_groupBox.currentRow()))

        self.listWidget_groupBox.itemSelectionChanged.connect(
            lambda: self.check_dipole(
                self.listWidget_groupBox.currentRow()))

        
        
    def check_dipole(self, element_number):
        print("check dipole")
        
        if (self.drawing_page.label_right.add_dipole_mode.value and 
            self.drawing_lst[self.current_count]\
            .group_lst[element_number]\
            .zurich.upper() not in self.zurich_dipolar):
            
            self.status_bar_mode_name.setText("Add dipole mode")
            self.status_bar_mode_comment.setStyleSheet("QLabel { color : red; }");
            self.status_bar_mode_comment.setText(
                "Warning this is not a dipolar group!!")
            self.drawing_page.label_right.setCursor(QtCore.Qt.ArrowCursor)

        elif (self.drawing_page.label_right.add_dipole_mode.value and 
              self.drawing_lst[self.current_count].group_lst[element_number]\
              .zurich.upper()
              in self.zurich_dipolar):
            
            self.status_bar_mode_name.setText("Add dipole mode")
            self.status_bar_mode_comment.setStyleSheet("QLabel { color : black; }");
            self.status_bar_mode_comment.setText("Click on a dipole" +
                                                     " positions to add it")
            self.drawing_page.label_right.setCursor(QtCore.Qt.SizeFDiagCursor)

        else:
            self.status_bar_mode_name.setText("") 
            self.status_bar_mode_comment.setText("")
            
    def set_focus_group_box(self, element_number):
        """
        - highlight the element under focus while the others are
        disabled.
        - updates the surface of the element under focus.
        - scroll on the element under focus
        """

        print("enter in the focus group box for the element: ",
              element_number)
        
        if self.listWidget_groupBox.count()>0 and element_number>=0:
            self.listWidget_groupBox.blockSignals(True)
            # itemchanged -> update group tool box
            self.listWidget_groupBox.item(element_number).setSelected(True) 
            self.listWidget_groupBox.blockSignals(False)
            self.update_surface_qlabel(element_number)
            
        self.listWidget_groupBox.setCurrentRow(element_number)
        # to change only the line on which the focus is
        for i in range(0, self.listWidget_groupBox.count()):
            if i==element_number:
                self.groupBoxLineList[i].spot_number_linedit.setEnabled(True)
                self.groupBoxLineList[i].zurich_combo.setEnabled(True)
                self.groupBoxLineList[i].McIntosh_combo.setEnabled(True) 
            else:
                self.groupBoxLineList[i].spot_number_linedit.setEnabled(False)
                self.groupBoxLineList[i].zurich_combo.setEnabled(False)
                self.groupBoxLineList[i].McIntosh_combo.setEnabled(False)

        horizontal_pos = (self.drawing_lst[self.current_count].group_lst[element_number].posX /
                          self.drawing_page.label_right.drawing_pixMap.width())
        vertical_pos = (self.drawing_lst[self.current_count].group_lst[element_number].posY /
                        self.drawing_page.label_right.drawing_pixMap.height())

        print("check scrolling: ", horizontal_pos,
              vertical_pos)
                
        self.scroll_position(horizontal_pos, vertical_pos)

    def set_group_toolbox(self, n=0):
        print("update the group toolbox for the element", n)

        # A widget is deleted when its parents is deleted.
        layout_object = self.drawing_page.widget_left_down_bis_layout.count()
        for i in reversed(range(layout_object)):
            self.drawing_page\
                .widget_left_down_bis_layout\
                .itemAt(i)\
                .widget()\
                .setParent(None)
            
        if len(self.drawing_lst[self.current_count].group_lst)>0:       
            self.group_toolbox = group_box.GroupBox()
            self.drawing_page.widget_left_down_bis_layout\
                             .addWidget(self.group_toolbox)

            # don't forget : [y, x]
            grid_position = [0, 0]
            self.group_toolbox.set_title(
                "Group " +
                str(self.drawing_lst[self.current_count].group_lst[n].number),
                grid_position)
            
            grid_position[1] += 1
            self.group_toolbox.set_spot_count(
                self.drawing_lst[self.current_count].group_lst[n].spots,
                grid_position)
            
            grid_position[1] += 1
            self.group_toolbox.set_zurich_combox_box(
                self.drawing_lst[self.current_count].group_lst[n].zurich,
                grid_position)
            
            grid_position[1]+=1
            self.group_toolbox.set_mcIntosh_combo_box(
                self.drawing_lst[self.current_count].group_lst[n].McIntosh,
                self.drawing_lst[self.current_count].group_lst[n].zurich,
                grid_position)
            
            grid_position[1]+=1
            self.group_toolbox.set_delete_group_button(grid_position)

            grid_position = [1, 0]
            self.group_toolbox.set_latitude(
                self.drawing_lst[self.current_count]\
                .group_lst[n].latitude * 180/math.pi,
                grid_position)
            
            grid_position[0]+=1
            self.group_toolbox.set_longitude(
                self.drawing_lst[self.current_count]\
                .group_lst[n].longitude * 180/math.pi,
                grid_position)

            grid_position[0]+=1
            self.group_toolbox.set_surface(
                self.drawing_lst[self.current_count].group_lst[n].surface,
                grid_position)

            grid_position[0]+=1
            grid_position[1] = 0
            self.group_toolbox.set_largest_spot(
                self.drawing_lst[self.current_count].group_lst[n].largest_spot,
                self.drawing_lst[self.current_count].group_lst[n].zurich,
                grid_position)
            
            grid_position = [1, 2]
            self.group_toolbox.set_arrows_buttons(grid_position)

            self.group_toolbox\
                .spot_number_linedit\
                .textEdited\
                .connect( lambda: self.modify_drawing_spots(
                    self.listWidget_groupBox.currentRow(),
                    True))
            
            self.group_toolbox\
                .zurich_combo\
                .currentIndexChanged\
                .connect(lambda: self.modify_drawing_zurich(
                    self.listWidget_groupBox.currentRow(),
                    True))
            
            self.group_toolbox\
                .McIntosh_combo\
                .currentIndexChanged\
                .connect(lambda: self.modify_drawing_mcIntosh(
                    self.listWidget_groupBox.currentRow(),
                    True))

            self.group_toolbox.delete_button.clicked.connect(self.delete_group)
            
            position_step = 0.1 * math.pi/180 
            self.group_toolbox.button_up.clicked.connect(
                lambda: self.update_HGC_position('latitude', position_step))
            self.group_toolbox.button_down.clicked.connect(
                lambda: self.update_HGC_position('latitude', -position_step))
            self.group_toolbox.button_left.clicked.connect(
                lambda: self.update_HGC_position('longitude', position_step))
            self.group_toolbox.button_right.clicked.connect(
                lambda: self.update_HGC_position('longitude', -position_step))
            
            self.group_toolbox.largest_spot_leading.clicked.connect(
                lambda: self.update_largest_spot('L'))
            self.group_toolbox.largest_spot_egal.clicked.connect(
                lambda: self.update_largest_spot('E'))
            self.group_toolbox.largest_spot_trailing.clicked.connect(
                lambda: self.update_largest_spot('T'))

        else:
            print("no toolbox because there are no groups")
            
            
    def delete_group(self):
        """
        Delete a group by clicking on the red cross in the group_toolbox.
        """
        index = self.current_count
        group_index = self.listWidget_groupBox.currentRow()
        
        self.drawing_lst[index].delete_group(group_index)
        self.set_group_widget()
        self.set_focus_group_box(0)
        self.set_group_toolbox()
        self.drawing_page.label_right.set_img()
        
        self.wolf_number.setText(str(self.drawing_lst[self.current_count].wolf))
        
    def update_largest_spot(self, largest_spot):
        
        group_index = self.listWidget_groupBox.currentRow()
        
        print("update largest spot",
              largest_spot,
              self.drawing_lst[self.current_count].group_lst[group_index].dipole1_lat)
        
        self.drawing_lst[self.current_count]\
            .group_lst[group_index].largest_spot = largest_spot
        
        self.drawing_lst[self.current_count].update_g_spot(
            group_index,
            self.drawing_lst[self.current_count]\
            .group_lst[group_index].McIntosh,
            self.drawing_lst[self.current_count]\
            .group_lst[group_index]\
            .largest_spot)
            
        self.group_toolbox.update_largest_spot_buttons(
            largest_spot,
            self.drawing_lst[self.current_count]\
            .group_lst[group_index].zurich)

        self.update_dipole_button(group_index)
           
    def check_information_complete(self, index, level):
        """
        return the list missing_information with
        all the information not filled for the group
        of a given index and a given level of details.
        """

        group = self.drawing_lst[self.current_count].group_lst[index]

        group_complete = {"posX":False, "posY":False,
                          "zurich":False, "McIntosh":False, "spots":False}
        dipole_complete = {"dipole1_posX":False, "dipole1_posY":False,
                           "dipole2_posX":False, "dipole2_posY":False,
                           "largest_spot":False}
        area_complete = {"area":False}

        if level=='group' or level=='dipole' or level=='area':
            info_complete = group_complete
            if group.posX :
                info_complete["posX"] = True
            if group.posY :
                info_complete["posY"] = True
            if group.zurich!='X' :
                info_complete["zurich"] = True
            if group.McIntosh != 'Xxx' :
                info_complete["McIntosh"] = True
            if group.spots:
                info_complete["spots"] = True

        if level=='dipole' and group.zurich.upper() in self.zurich_dipolar:
            info_complete.update(dipole_complete)
            if group.dipole1_lat :
                info_complete["dipole1_posX"] = True
            if group.dipole1_long :
                info_complete["dipole1_posY"] = True
            if group.dipole2_lat :
                info_complete["dipole2_posX"] = True
            if group.dipole2_long :
                info_complete["dipole2_posY"] = True
            if group.largest_spot :
                info_complete["largest_spot"] = True

        missing_info = []    
        for key, value in info_complete.items():
            if value is False:
                missing_info.append(key)

        return missing_info

        
    def update_dipole_button(self, index):
        """
        The information concerning the dipole (zurich in zurich dipolar) 
        is complete when:
        - position is filled
        - LTS is filled
        if one of the two condition is not met -> dipole button in red
        else -> dipole button in green
        """
        missing_info = self.check_information_complete(index,
                                                       'dipole')
        if missing_info:
            self.groupBoxLineList[index].dipole_button.setStyleSheet(
                "background-color: rgb(255, 165, 84)")
        else:
            self.groupBoxLineList[index]\
                .dipole_button.setStyleSheet(
                    "background-color: transparent")
        
    def update_HGC_position(self, coordinate, value):
        """
        Steps:
         - takes the current values of latitude/longitude.
         - Change it of a given value according to the user modification
         - Convert it to corresponding value of X and Y on the drawing
        !!! the new posX and posY is then not integer !!!
         - Record the new latitude, longitude, X and Y in the drawing object
          (the change group position function change as well Lcm and all 
          other quantity related to the position of the group)
        - Display the new latitude/longitude in the linedit.
        - Show the image with the new position of the group.
        """
        index = self.current_count
        group_index = self.listWidget_groupBox.currentRow()
        
        longitude = self.drawing_lst[index].group_lst[group_index].longitude
        latitude = self.drawing_lst[index].group_lst[group_index].latitude

        drawing_height = self.drawing_page.label_right.drawing_height
        
        if coordinate=='longitude':
            longitude +=value
            longitude = longitude % (2 * math.pi) 
            #if longitude > 2 * math.pi :
            #    longitude -= 2 * math.pi

        if coordinate=='latitude':
            latitude+=value

        posX, posY, posZ =  coordinates.cartesian_from_HGC_upper_left_origin(
            self.drawing_lst[index].calibrated_center.x,
            self.drawing_lst[index].calibrated_center.y,
            self.drawing_lst[index].calibrated_north.x,
            self.drawing_lst[index].calibrated_north.y,
            longitude,
            latitude,
            self.drawing_lst[index].angle_P,
            self.drawing_lst[index].angle_B,
            self.drawing_lst[index].angle_L,
            drawing_height)

        self.drawing_lst[index].change_group_position(group_index,
                                                      latitude,
                                                      longitude,
                                                      posX,
                                                      posY)
        
        self.group_toolbox.longitude_linedit.setText('{0:.2f}'.format(
                self.drawing_lst[index].group_lst[group_index].longitude * 180/math.pi))
        self.group_toolbox.latitude_linedit.setText('{0:.2f}'.format(
                self.drawing_lst[index].group_lst[group_index].latitude * 180/math.pi))
        
        self.drawing_page.label_right.set_img()
      
    def modify_drawing_spots(self, n, is_toolbox):
        """
        A change in the spots number consists in:
        - update the drawing object
        - display the right number in the toolbox and the groupbox
        - put the linedit in orange in case the number is 0, white otherwhise
        TO DO: check that the value entered is a number!
        """
        if is_toolbox:
            new_sunspot_number = self.group_toolbox.spot_number_linedit.text()
            
        else:
            new_sunspot_number = self.groupBoxLineList[n].spot_number_linedit.text()   

        self.drawing_lst[self.current_count].update_spot_number(
            self.listWidget_groupBox.currentRow(),
            int(new_sunspot_number))
        
        if self.drawing_lst[self.current_count].group_lst[n].spots == 0:
            self.groupBoxLineList[n].spot_number_linedit.setStyleSheet(
                "background-color: rgb(255, 165, 84)")
        else:
            self.groupBoxLineList[n].spot_number_linedit.setStyleSheet(
                "background-color: white")

        self.groupBoxLineList[n].spot_number_linedit.setText(
            str(self.drawing_lst[self.current_count].group_lst[n].spots))
        self.group_toolbox.spot_number_linedit.setText(
            str(self.drawing_lst[self.current_count].group_lst[n].spots))

        self.wolf_number.setText(str(self.drawing_lst[self.current_count].wolf))

    def modify_drawing_zurich(self, n, is_toolbox):
        """
        A change in the zurich type consits in :
        - record temporary the old zurich type
        - update the value in the toolbox or group box 
        - change the value of the new zurich type in the drawing object
        - update the list of McIntosh type enabled for the give zurich type
        - enable/disable the LTS buttons depending on the new/old zurich:
          - old zurich unipolar and new zurich unipolar -> no change
          - old zurich unipolar and new zurich dipolar -> enable LTS button
        """
        
        old_zurich_type = self.drawing_lst[self.current_count]\
                              .group_lst[self.listWidget_groupBox.currentRow()]\
                              .zurich
        if is_toolbox:
            new_zurich_type = str(self.group_toolbox.zurich_combo.currentText())
            new_zurich_index = self.group_toolbox.zurich_combo.currentIndex()
        else:
            new_zurich_type = str(self.groupBoxLineList[n].zurich_combo.currentText())
            new_zurich_index = self.groupBoxLineList[n].zurich_combo.currentIndex()

        if new_zurich_type!=old_zurich_type:
            self.drawing_lst[self.current_count]\
                .group_lst[self.listWidget_groupBox.currentRow()]\
                .zurich = new_zurich_type
            
        self.groupBoxLineList[n].zurich_combo.setCurrentIndex(new_zurich_index)
        self.groupBoxLineList[n].update_McIntosh_combo_box(new_zurich_type)
        self.group_toolbox.zurich_combo.setCurrentIndex(new_zurich_index)
        self.group_toolbox.update_McIntosh_combo_box(new_zurich_type)

        if new_zurich_type == "X":
            self.groupBoxLineList[n].zurich_combo.setStyleSheet(
                "background-color: orange")
            self.group_toolbox.zurich_combo.setStyleSheet(
                "background-color: rgb(255, 165, 84)")
        else:
            self.groupBoxLineList[n].zurich_combo.setStyleSheet(
                "background-color: white")
            self.group_toolbox.zurich_combo.setStyleSheet("background-color: white")
    
        if ((new_zurich_type.upper() in self.zurich_dipolar and
            old_zurich_type.upper() not in self.zurich_dipolar) or
            (new_zurich_type.upper() not in self.zurich_dipolar and
            old_zurich_type.upper() in self.zurich_dipolar)):
            self.drawing_lst[self.current_count].group_lst[n].largest_spot = None
            self.drawing_lst[self.current_count].update_g_spot(
                n,
                self.drawing_lst[self.current_count].group_lst[n].McIntosh,
                self.drawing_lst[self.current_count].group_lst[n].largest_spot)

        self.update_dipole_button(n)
        self.group_toolbox.update_largest_spot_buttons(
            self.drawing_lst[self.current_count].group_lst[n].largest_spot,
            new_zurich_type)
        
        
    def modify_drawing_mcIntosh(self, n, is_toolbox):
        old_mcIntosh_type = self.drawing_lst[self.current_count]\
                                .group_lst[self.listWidget_groupBox.currentRow()]\
                                .McIntosh
        
        if is_toolbox:
            new_mcIntosh_type = str(self.group_toolbox.McIntosh_combo.currentText())
            new_mcIntosh_index = self.group_toolbox.McIntosh_combo.currentIndex()
        else:
            new_mcIntosh_type = str(self.groupBoxLineList[n]
                                    .McIntosh_combo.currentText())
            new_mcIntosh_index = self.groupBoxLineList[n].McIntosh_combo.currentIndex()
        
        if new_mcIntosh_type!=old_mcIntosh_type:
            self.drawing_lst[self.current_count]\
                .group_lst[self.listWidget_groupBox.currentRow()]\
                .McIntosh = new_mcIntosh_type
  
        self.groupBoxLineList[n].McIntosh_combo.setCurrentIndex(new_mcIntosh_index)
        self.group_toolbox.McIntosh_combo.setCurrentIndex(new_mcIntosh_index)
        
        
    def update_group_visu(self, n):
        print("update_group_visu")
        self.drawing_page.label_right.group_visu_index = n
        self.drawing_page.label_right.set_img()
        
    def add_drawing_information(self):
        """
        Add the linedit related to the drawing information
        """
        title_left_up = QtGui.QLabel("Drawing information")
        title_left_up.setAlignment(QtCore.Qt.AlignCenter)
        title_left_up.setContentsMargins(0, 5, 0, 5)
        self.drawing_page.widget_left_up_layout.addWidget(title_left_up)
        
        form_layout = QtGui.QFormLayout()
        form_layout.setSpacing(10)
        
        self.drawing_operator = QtGui.QLineEdit(self)
        self.drawing_operator.setEnabled(True)
        self.drawing_operator.setStyleSheet(
            "background-color: lightgray; color:black")

        self.drawing_last_update = QtGui.QLineEdit(self)
        self.drawing_last_update.setEnabled(True)
        self.drawing_last_update.setStyleSheet(
            "background-color: lightgray; color:black")
        
        self.drawing_observer = QtGui.QLineEdit(self)
        self.drawing_observer.setEnabled(True)
        self.drawing_observer.setStyleSheet(
            "background-color: white; color:black")
        
        self.drawing_date = QtGui.QDateEdit()
        self.drawing_date.setDisplayFormat("dd/MM/yyyy")
        today = QtCore.QDate.currentDate()
        self.drawing_date.setDate(today)
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
        
        self.drawing_observer.textEdited.connect(
            lambda: self.update_linedit_drawing('observers',
                                                self.drawing_observer))

        self.drawing_quality.currentIndexChanged.connect(
            lambda: self.update_combo_box_drawing('quality',
                                                  self.drawing_quality))
        
        self.drawing_type.currentIndexChanged.connect(
            lambda: self.update_combo_box_drawing('type',
                                                  self.drawing_type))

        widget_form = QtGui.QWidget()
        widget_form.setLayout(form_layout)
        self.drawing_page.widget_left_up_layout.addWidget(widget_form)

    def set_combo_box_drawing(self, field, table_name, linedit):
        """
        Define automatically the combo box list with all the element 
        named in the database
        """
        uset_db = database.database()
        values = uset_db.get_values(field, table_name)
        for el in values:
            linedit.addItem(el[0])
        
    def update_linedit_drawing(self, field, linedit):
        """
        Update the drawing object with the value given
        in the line edit, check if this value exists in the 
        database.
        """
        uset_db = database.database()
        if uset_db.exist_in_db(field,
                               'name',
                               linedit.text()):
            if field == 'observers':
                self.drawing_lst[self.current_count]\
                    .observer = str(linedit.text())
                
            linedit.setStyleSheet("background-color: white")
        else:
            self.drawing_observer.setStyleSheet(
                "background-color: rgb(232, 103, 101)")
        
    def update_combo_box_drawing(self, parameter_name, combo_box):
        """
        Update the drawing object with the value given
        in the combo box, check if this value exists in the 
        database.
        """
        if parameter_name == 'quality':
            self.drawing_lst[self.current_count]\
                .quality = str(combo_box.currentText())
        elif parameter_name == 'type':
            self.drawing_lst[self.current_count]\
                .drawing_type = str(combo_box.currentText())
        else:
            print("your parameter name: {} does not" +
                  " exist!".format(parameter_name))
            
    def add_surface_widget(self):
        
        self.group_surface_widget = qlabel_group_surface.GroupSurfaceWidget()
        self.drawing_page.widget_middle_up_layout.addWidget(
            self.group_surface_widget)
        self.drawing_page.widget_middle_up_layout.setSpacing(10)
        
    def add_current_session(self):
        
        form_layout = QtGui.QFormLayout()
        form_layout.setSpacing(15)

        title_left_middle = QtGui.QLabel("Current session")
        title_left_middle.setAlignment(QtCore.Qt.AlignCenter)
        title_left_middle.setContentsMargins(0, 5, 0, 5)
        self.drawing_page.widget_left_middle_layout.addWidget(title_left_middle)
        
        current_operator_linedit = QtGui.QLineEdit(
            str(self.operator).upper(), self)
        current_operator_linedit.setEnabled(False)
        current_operator_linedit.setStyleSheet(
            "background-color: lightgray; color: black")
        
        self.but_previous = QtGui.QPushButton('previous', self)
        self.but_previous.setShortcut(QtGui.QKeySequence("Left"))
        self.but_next = QtGui.QPushButton('next', self)
        self.but_next.setShortcut(QtGui.QKeySequence("Right"))

        self.but_next.clicked.connect(
            lambda: self.update_counter(self.current_count+1))
        self.but_next.clicked.connect(self.set_drawing)
        self.but_previous.clicked.connect(
            lambda: self.update_counter(self.current_count-1))
        self.but_previous.clicked.connect(self.set_drawing)

        layout_but = QtGui.QHBoxLayout()
        layout_but.addWidget(self.but_previous)
        layout_but.addWidget(self.but_next)
        
        layout_goto = self.jump_to_drawing_linedit()
        
        self.but_save = QtGui.QPushButton('save', self)
        self.but_save.clicked.connect(self.save_drawing)

        form_layout.addRow("Current operator: ", current_operator_linedit)
        form_layout.setLayout(1, QtGui.QFormLayout.SpanningRole, layout_goto)
        form_layout.setLayout(2, QtGui.QFormLayout.SpanningRole, layout_but)
        form_layout.setWidget(3, QtGui.QFormLayout.SpanningRole, self.but_save)

        self.drawing_page.widget_left_middle_layout.addLayout(form_layout)
        
    def jump_to_drawing_linedit(self):
        self.goto_drawing_linedit = QtGui.QLineEdit()
        self.goto_drawing_label1 = QtGui.QLabel()
        self.goto_drawing_label2 = QtGui.QLabel()
        self.goto_drawing_button = QtGui.QPushButton()
        
        self.goto_drawing_label1.setText("Jump to drawing")
        self.goto_drawing_linedit.setText("1")
        self.goto_drawing_linedit.setStyleSheet(
            "background-color: white; color: black")
        self.goto_drawing_label2.setText("out of 0")
        self.goto_drawing_button.setText("Go!")

        self.goto_drawing_button.clicked.connect(
            lambda: self.update_counter(int(self.goto_drawing_linedit.text())-1))
        self.goto_drawing_button.clicked.connect(
            lambda: self.set_drawing())

        layout_goto = QtGui.QHBoxLayout()
        layout_goto.addWidget(self.goto_drawing_label1)
        layout_goto.addWidget(self.goto_drawing_linedit)
        layout_goto.addWidget(self.goto_drawing_label2)
        layout_goto.addWidget(self.goto_drawing_button)     
        return layout_goto

    def save_drawing(self):
        print("**save the drawing information in the database**")

        self.drawing_lst[self.current_count].operator = str(self.operator).upper()
        self.drawing_lst[self.current_count].last_update_time = datetime.now()

        
        if (self.drawing_lst[self.current_count].calibrated==1 and
            self.drawing_lst[self.current_count].group_count==0):
            # pop up that ask if it is normal?
            pass

        
    def update_counter(self, value):
        
        if value >= self.len_drawing_lst:
            value = self.len_drawing_lst-1
        elif value < 0:
            value = 0

        self.current_count = value
        
        if (self.current_count > 0 and
            self.current_count < self.len_drawing_lst - 1):

            self.but_next.setEnabled(True)
            self.but_previous.setEnabled(True)
            
        elif self.current_count == self.len_drawing_lst - 1:
            self.but_next.setDisabled(True)
            self.but_previous.setEnabled(True)
        
        elif self.current_count == 0:
            self.but_next.setEnabled(True)
            self.but_previous.setDisabled(True)
               
        self.set_drawing_lineEdit()
        self.update_session_lineEdit()

    def drawing_value_changed(self):
        """
        Set the save button in orange as soon as a new value is introduced
        """
        print("*********** the value has changed!!")
        for el in self.drawing_lst:
            print(el, el.changed)
            if el.changed:
                self.but_save.setStyleSheet("background-color: rgb(255, 165, 84)")
          
        
    def set_drawing_lst(self, drawing_lst):
        """
        Get the list of drawings from bulk analysis page.
        Set the counter to 0.
        """
        self.drawing_lst = drawing_lst
        for el in self.drawing_lst:
            el.value_changed.connect(self.drawing_value_changed)
            
        self.len_drawing_lst = len(drawing_lst)
        
        self.current_count = 0
        if len(drawing_lst)>1:
            self.but_next.setEnabled(True)
            self.but_previous.setEnabled(True)
        else:
            self.but_next.setDisabled(True)
            self.but_previous.setDisabled(True)
            
        self.set_drawing_lineEdit()
        self.update_session_lineEdit()
        
    def update_session_lineEdit(self):

        self.goto_drawing_linedit.setText(str(self.current_count + 1))
        self.goto_drawing_label2.setText("out of "+str(self.len_drawing_lst))
  
    def set_drawing_lineEdit(self):
        """
        Fill the linEdits with the information of the drawing.
        """
        self.drawing_operator.setText(
            self.drawing_lst[self.current_count].operator)
        self.drawing_last_update.setText(
            self.drawing_lst[self.current_count].last_update_time)
        self.drawing_observer.setText(
            self.drawing_lst[self.current_count].observer)
        self.drawing_date.setDate(
            QtCore.QDate(self.drawing_lst[self.current_count].datetime.year,
                         self.drawing_lst[self.current_count].datetime.month,
                         self.drawing_lst[self.current_count].datetime.day))
        self.drawing_time.setText(
            str(self.drawing_lst[ self.current_count].datetime.strftime('%H')) +
            ":" +
            str(self.drawing_lst[ self.current_count].datetime.strftime('%M')))
    
        #self.drawing_quality.setText(
        #    str(self.drawing_lst[self.current_count].quality))

        self.drawing_quality.blockSignals(True)
        index_drawing_quality = self.drawing_quality.findText(
            self.drawing_lst[self.current_count].quality)
        self.drawing_quality.setCurrentIndex(index_drawing_quality)
        self.drawing_quality.blockSignals(False)
        
        self.drawing_type.blockSignals(True)
        index_drawing_type = self.drawing_type.findText(
            self.drawing_lst[self.current_count].drawing_type)
        self.drawing_type.setCurrentIndex(index_drawing_type)
        self.drawing_type.blockSignals(False)
        

        print(self.drawing_lst[self.current_count].changed)
        
        if self.drawing_lst[self.current_count].changed:
            self.but_save.setStyleSheet("background-color: rgb(255, 165, 84)")
        else:
            self.but_save.setStyleSheet("background-color: lightgray")

        self.angleP.setText(
            '{0:.2f}'.format(self.drawing_lst[self.current_count].angle_P))
        self.angleB.setText(
            '{0:.2f}'.format(self.drawing_lst[self.current_count].angle_B))
        self.angleL.setText(
            '{0:.2f}'.format(self.drawing_lst[self.current_count].angle_L))
        self.rotation_number.setText(
            str(self.drawing_lst[self.current_count].carington_rotation))

        self.calibrated.setText(
            str(self.drawing_lst[self.current_count].calibrated))
        self.analyzed.setText(
            str(self.drawing_lst[self.current_count].analyzed))

        self.wolf_number.setText(str(self.drawing_lst[self.current_count].wolf))
        
    def set_path_to_qlabel(self):
        """
        set the path to the image of the drawing based 
        on the information contained 
        in the configuration file (digisun.ini).
        Here is fixed the structure of the filename and 
        the structure of the directory.
        """  
        filename = (
            self.prefix +
            str(self.drawing_lst[self.current_count].datetime.year) +
            str(self.drawing_lst[self.current_count].datetime.strftime('%m')) +
            str(self.drawing_lst[self.current_count].datetime.strftime('%d')) +
            str(self.drawing_lst[self.current_count].datetime.strftime('%H')) +
            str(self.drawing_lst[self.current_count].datetime.strftime('%M')) +
            "." +
            self.extension)

        directory = os.path.join(
            self.archdrawing_directory,
            str(self.drawing_lst[self.current_count].datetime.year),
            self.drawing_lst[self.current_count].datetime.strftime('%m'))
        
        #print('directory: ', directory)
        self.drawing_page\
            .label_right\
            .file_path = os.path.join(directory, filename)

            
    def set_drawing(self):
        """
        - Get the right path of the image
        - update the current_drawing of the qlabel image
        - set the group widget
        - set the group toolbox
        - set the img
        Note: this method should be called only when the current drawing change! 
        otherwhise use self.drawing_page.label_right.set_img() to refresh the img
        """
        #print("show drawing")
        self.set_path_to_qlabel()
        self.drawing_page\
            .label_right\
            .current_drawing = self.drawing_lst[self.current_count]
        self.drawing_page.label_right.group_visu_index = 0

        self.drawing_page.label_right.calibration_mode.value = False
        self.drawing_page.label_right.helper_grid.value = False
        self.drawing_page.label_right.add_group_mode.value = False
        self.drawing_page.label_right.add_dipole_mode.value = False
        #self.drawing_page.label_right.surface_mode.value = False

        self.drawing_page.label_right.setCursor(QtCore.Qt.ArrowCursor)
        self.drawing_page.label_right.set_img()

        self.set_group_widget()

        self.set_focus_group_box(0)
        
        
        self.set_group_toolbox()
        self.status_bar_mode_name.setText("")
        self.status_bar_mode_comment.setText("")
        #self.drawing_page.label_right.show()
    
