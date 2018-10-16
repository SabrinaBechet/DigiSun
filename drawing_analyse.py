# !/usr/bin/env python
# -*-coding:utf-8-*-
import os
from PyQt4 import QtGui, QtCore

import database, drawing, group_box, qlabel_drawing, qlabel_group_surface
from datetime import date, time, datetime, timedelta
import math
import configparser
import time

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
      
        self.widget_left_up = QtGui.QWidget()
        #self.widget_left_up.setMinimumWidth(350)
        self.widget_left_up.setMaximumHeight(500)
        self.widget_left_up.setStyleSheet("background-color:lightgray;")   
        self.widget_left_up_layout = QtGui.QVBoxLayout()
        self.widget_left_up_layout.setContentsMargins(0, 0, 0, 0) 
        self.widget_left_up_layout.setSpacing(0)
        self.widget_left_up_layout.setAlignment(QtCore.Qt.AlignTop)
        self.widget_left_up.setLayout(self.widget_left_up_layout)

        self.widget_left_middle = QtGui.QWidget()
        self.widget_left_middle.setMinimumWidth(350)
        self.widget_left_middle.setMaximumHeight(200)
        self.widget_left_middle.setStyleSheet("background-color:lightgray;")   
        self.widget_left_middle_layout = QtGui.QVBoxLayout()
        self.widget_left_middle_layout.setContentsMargins(0, 0, 0, 0) 
        self.widget_left_middle_layout.setSpacing(0)
        self.widget_left_middle_layout.setAlignment(QtCore.Qt.AlignTop)
        self.widget_left_middle.setLayout(self.widget_left_middle_layout)

        self.widget_left_down = QtGui.QWidget()
        self.widget_left_down.setMaximumWidth(350)
        self.widget_left_down.setMinimumHeight(200)
        self.widget_left_down.setStyleSheet("background-color:lightblue;")   
        self.widget_left_down_layout = QtGui.QVBoxLayout()
        self.widget_left_down_layout.setContentsMargins(0, 0, 0, 0) 
        self.widget_left_down_layout.setSpacing(0)
        self.widget_left_down_layout.setAlignment(QtCore.Qt.AlignTop and QtCore.Qt.AlignRight)
        self.widget_left_down.setLayout(self.widget_left_down_layout)
        
        self.widget_left_down_bis = QtGui.QWidget()
        self.widget_left_down_bis.setMaximumWidth(350)
        self.widget_left_down_bis.setMaximumHeight(200)
        self.widget_left_down_bis.setStyleSheet("background-color:lightblue;")   
        self.widget_left_down_bis_layout = QtGui.QVBoxLayout()
        self.widget_left_down_bis_layout.setContentsMargins(0, 0, 0, 0) 
        self.widget_left_down_bis_layout.setSpacing(0)
        self.widget_left_down_bis_layout.setAlignment(QtCore.Qt.AlignTop and QtCore.Qt.AlignRight)
        self.widget_left_down_bis.setLayout(self.widget_left_down_bis_layout)
        
        self.widget_middle_up = QtGui.QWidget()
        self.widget_middle_up.setMaximumWidth(10)
        self.widget_middle_up.setMinimumHeight(200)
        self.widget_middle_up.setStyleSheet("background-color:lightgray;")
        self.widget_middle_up_layout = QtGui.QVBoxLayout()
        self.widget_middle_up_layout.setContentsMargins(0, 0, 0, 0) 
        self.widget_middle_up_layout.setSpacing(0)
        self.widget_middle_up_layout.setAlignment(QtCore.Qt.AlignTop)
        self.widget_middle_up.setLayout(self.widget_middle_up_layout)
        self.label_middle_up = qlabel_group_surface.QLabelGroupSurface()
        
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
        splitter_middle_down.addWidget(self.widget_left_up)
        splitter_middle_down.addWidget(self.widget_left_middle)
        splitter_middle_down.addWidget(splitter_down)
        
        
        splitter_main = QtGui.QSplitter(QtCore.Qt.Horizontal, self)
        self.layout().addWidget(splitter_main)
        splitter_main.addWidget(splitter_middle_down)
        splitter_main.addWidget(self.widget_middle_up)
        splitter_main.addWidget(self.widget_right)
    
   
    """def widget_left_down_add_box(self):
        new_layout = QtGui.QVBoxLayout()
        label = QtGui.QLabel("Ninja")
        self.widget_left_down_layout.addWidget(label)"""
    
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

        """print("scroll bar properties:")
        print("width: ",  self.vertical_scroll_bar.width())
        print("height: ",  self.vertical_scroll_bar.height())
        """
        self.setCentralWidget(self.drawing_page)
        
        self.operator = operator
        self.column_maximum_width = 600
        self.add_drawing_information()
        self.add_current_session()
        self.add_surface()
        self.drawing_lst = []
        self.set_toolbar()
        self.set_status_bar()
        
        self.drawing_page.label_right.center_clicked.connect(self.scroll_position)
        self.drawing_page.label_right.north_clicked.connect(self.clean_status_bar)
        self.drawing_page.label_right.group_added.connect(self.add_group_box)
        
        
        self.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)

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
        self.status_bar_mode_name.setStyleSheet("QLabel { background-color : red; color : blue; }");
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
            
        else:
            self.clean_status_bar()
       
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
                cursor_img = "/home/sabrinabct/Projets/DigiSun_2018_gitlab/cursor/Pixel_perfect/target_24.png"
                cursor_add_group = QtGui.QCursor(QtGui.QPixmap(cursor_img))
                #QtGui.QApplication.setOverrideCursor(cursor_add_group)
                self.drawing_page.label_right.setCursor(cursor_add_group)
                

            if self.drawing_page.label_right.calibration_mode.value:
                self.start_calibration() 
            self.drawing_page.label_right.helper_grid.value = False
            self.drawing_page.label_right.add_dipole_mode.value = False
            self.drawing_page.label_right.surface_mode.value = False

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

        
        if self.drawing_page.label_right.surface_mode.value:
            self.drawing_page.widget_middle_up.setMaximumWidth(600)
            #self.drawing_page.widget_middle_up.setMinimumHeight(580)
        
            self.update_surface_qlabel(n)

        elif self.drawing_page.label_right.surface_mode.value == False:
            self.drawing_page.widget_middle_up.setMaximumWidth(10)
            #self.drawing_page.widget_middle_up.setMinimumHeight(580)


    def update_surface_qlabel(self, n):
        """
        Update the QLabelGroupSurface object which represent an image of the drawing 
        to calculate the surface.
        This method uses heliographic coordinates so it needs the calibration to be done!
        """
        #print("update surface qlabel number:", n)
        if self.drawing_lst[self.current_count].calibrated:
            longitude = self.drawing_lst[self.current_count]\
                            .group_lst[n]\
                            .longitude
            latitude = self.drawing_lst[self.current_count]\
                           .group_lst[n]\
                           .latitude
            coords = self.drawing_page.label_right.get_cartesian_coordinate_from_HGC(longitude, latitude)
            coords = list(coords)
            
            # don't forget to document this:
            #print("------------------------------------CHECK!!!!!!!",
            #      self.drawing_page.label_right.pixmap().height(),
            #      self.drawing_page.label_right.drawing_pixMap.height())
            
            #self.drawing_page.label_middle_up = qlabel_drawing.QLabelGroupSurface()
            #Shift the coordinates to centre the group
            if coords[0] > 150:
                coords[0] = coords[0]-150
            else:
                coords[0] = 0
            
            if coords[1] > 150:
                coords[1] = coords[1]-150
            else: coords[1] = 0

            large_grid_tmp = self.drawing_page.label_right.large_grid_overlay.value
            small_grid_tmp = self.drawing_page.label_right.small_grid_overlay.value
            group_tmp = self.drawing_page.label_right.group_visu.value
            dipole_tmp = self.drawing_page.label_right.dipole_visu.value
            
            self.drawing_page.label_right.large_grid_overlay.value = False
            self.drawing_page.label_right.small_grid_overlay.value = False
            self.drawing_page.label_right.group_visu.value = False
            self.drawing_page.label_right.dipole_visu.value = False
            self.drawing_page.label_right.set_img()
            
            pixmap_group_surface = self.drawing_page.label_right.drawing_pixMap.copy(coords[0],coords[1],300,300)
            self.drawing_page.label_middle_up.original_pixmap = pixmap_group_surface.copy()
            self.drawing_page.label_middle_up.setPixmap(pixmap_group_surface)
            #self.drawing_page.label_middle_up.set_img()
            
            self.drawing_page.label_middle_up.threshold.value = False 
            self.drawing_page.label_middle_up.threshold_done.value = False
            self.drawing_page.label_middle_up.polygon.value = False
            self.drawing_page.label_middle_up.crop_done.value = False
            self.drawing_page.label_middle_up.pencil.value = False
            self.drawing_page.label_middle_up.bucket.value = False
            
            self.drawing_page.label_right.large_grid_overlay.value = large_grid_tmp
            self.drawing_page.label_right.small_grid_overlay.value = small_grid_tmp
            self.drawing_page.label_right.group_visu.value = group_tmp
            self.drawing_page.label_right.dipole_visu.value = dipole_tmp
            
            self.drawing_page.label_right.set_img()


    def scroll_position(self):
        """
        Automatically scroll to the position given 
        by the self.fraction_width and self.fraction_height.
        """
        print("************scroll function")
        print("image width:", self.drawing_page.label_right.pixmap().width())
        print("image height: ", self.drawing_page.label_right.pixmap().height())
        print("fraction width: ", self.fraction_width)
        print("fraction height: ", self.fraction_height)
        
        self.status_bar_mode_comment.setText("Click on the " + self.point_name + " position")
        
        self.vertical_scroll_bar.setMinimum(0)
        self.horizontal_scroll_bar.setMinimum(0)
        self.vertical_scroll_bar.setMaximum(self.drawing_page.label_right.pixmap().height() -
                                            self.vertical_scroll_bar.pageStep())
        self.horizontal_scroll_bar.setMaximum(self.drawing_page.label_right.pixmap().width() -
                                              self.horizontal_scroll_bar.pageStep() )
  
        self.horizontal_scroll_bar.setValue(self.horizontal_scroll_bar.maximum() * self.fraction_width)
        self.vertical_scroll_bar.setValue(self.vertical_scroll_bar.maximum() * self.fraction_height)

    def clean_status_bar(self):
        self.status_bar_mode_name.setText("")
        self.status_bar_mode_comment.setText("")

    """def status_not_dipolar(self):
        self.status_bar_mode_name.setText("Add dipole mode")
        self.status_bar_mode_comment.setStyleSheet("QLabel { color : red; }");
        self.status_bar_mode_comment.setText("Warning this is not a dipolar group!!")
       # self.status_bar_mode_comment.setStyleSheet("QLabel { color : black; }");
    """    
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
                  self.drawing_page.label_right.center_done, self.drawing_page.label_right.north_done)
        
            self.drawing_page.label_right.group_visu.value = False
            self.drawing_page.label_right.dipole_visu.value = False
            self.drawing_page.label_right.large_grid_overlay.value = False
            self.drawing_page.label_right.small_grid_overlay.value = False

            self.drawing_page.label_right.helper_grid.value = False
            self.drawing_page.label_right.add_group_mode.value = False
            self.drawing_page.label_right.add_dipole_mode.value = False
            self.drawing_page.label_right.surface_mode.value = False
            
            self.drawing_page.label_right.zoom_in(5./self.drawing_page.label_right.scaling_factor)
            
            self.fraction_width = self.drawing_lst[self.current_count].pt1_fraction_width
            self.fraction_height = self.drawing_lst[self.current_count].pt1_fraction_height
            self.point_name = self.drawing_lst[self.current_count].pt1_name
            self.scroll_position()
            
            self.fraction_width = self.drawing_lst[self.current_count].pt2_fraction_width
            self.fraction_height = self.drawing_lst[self.current_count].pt2_fraction_height
            self.point_name = self.drawing_lst[self.current_count].pt2_name
            
            """self.drawing_page.label_right.group_visu.value = True
            self.drawing_page.label_right.dipole_visu.value = False
            self.drawing_page.label_right.large_grid_overlay.value = True
            self.drawing_page.label_right.small_grid_overlay.value = False
            """
            
        else:
            QtGui.QApplication.restoreOverrideCursor()
            self.drawing_page.label_right.zoom_in(1/self.drawing_page.label_right.scaling_factor)
            print("out of the calibration")
            self.clean_status_bar()

            
    def get_click_coordinates(self):
        print("get click coordinate")
        print(self.drawing_page.label_right.x_drawing)
        print(self.drawing_page.label_right.y_drawing)
        print(self.drawing_page.label_right.HGC_longitude)
        print(self.drawing_page.label_right.HGC_latitude)
        

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
                self.drawing_page.widget_left_down_layout.itemAt(i).widget().setParent(None)

        print("a")
        title_left_down = QtGui.QLabel("Group information")
        title_left_down.setAlignment(QtCore.Qt.AlignCenter)
        title_left_down.setContentsMargins(0, 5, 0, 5)
        self.drawing_page.widget_left_down_layout.addWidget(title_left_down)
        
        group_count = self.drawing_lst[self.current_count].group_count
                                         
        self.listWidget_groupBox = QtGui.QListWidget(self)
        self.listWidget_groupBox.setStyleSheet(
            "QListView::item:selected {background : rgb(77, 185, 88);}")
        
        self.groupBoxLineList = []
        print("b")
        for i in range(group_count):
            self.grid_position = [0, 0]
            groupBoxLine = group_box.GroupBox()
            """colorised = False
            if ((self.drawing_lst[self.current_count].group_lst[i].surface == 0) or
                (self.drawing_lst[self.current_count].group_lst[i].surface == None)):
                colorised = True
            if ((self.drawing_lst[self.current_count].group_lst[i].zurich.upper() in
                 ["B","C","D","E","F","G"]) and
                (self.drawing_lst[self.current_count].group_lst[i].g_spot == 0)):
                colorised = True
            """
            groupBoxLine.set_title(
                "Group " +
                str(self.drawing_lst[self.current_count].group_lst[i].number),
                self.grid_position, 0)           
            groupBoxLine.set_spot_count(
                self.drawing_lst[self.current_count].group_lst[i].spots,
                self.grid_position)
            groupBoxLine.set_zurich_combox_box(
                self.drawing_lst[self.current_count].group_lst[i].zurich,
                self.grid_position)
            groupBoxLine.set_mcIntosh_combo_box(
                self.drawing_lst[self.current_count].group_lst[i].McIntosh,
                self.drawing_lst[self.current_count].group_lst[i].zurich,
                self.grid_position)

            
            groupBoxLine.set_dipole_button(self.grid_position)
            groupBoxLine.set_area_button(self.grid_position)

            
            
            if self.drawing_lst[self.current_count].group_lst[i].zurich == "X":
                groupBoxLine.get_zurich().setStyleSheet(
                    "background-color: orange")


            print("*********",
                  self.drawing_lst[self.current_count].group_lst[i].zurich,
                  self.drawing_lst[self.current_count].group_lst[i].g_spot)
                
            if (self.drawing_lst[self.current_count].group_lst[i].zurich.upper()
                in ["B","C","D","E","F","G"] and
                self.drawing_lst[self.current_count].group_lst[i].g_spot==0):
                print("the button should be orange")
                groupBoxLine.get_dipole_button().setStyleSheet(
                    "background-color: orange")

            if self.drawing_lst[self.current_count].group_lst[i].surface is None:
                groupBoxLine.get_area_button().setStyleSheet(
                    "background-color: orange")
                
      
            groupBoxLine.get_spots().textEdited.connect(
                lambda: self.modify_drawing_spots(
                    self.listWidget_groupBox.currentRow(),
                    False))
            groupBoxLine.get_zurich().currentIndexChanged.connect(
                lambda: self.modify_drawing_zurich(
                    self.listWidget_groupBox.currentRow(),
                    False))
            groupBoxLine.get_McIntosh().currentIndexChanged.connect(
                lambda: self.modify_drawing_mcIntosh(
                    self.listWidget_groupBox.currentRow(),
                    False))
            
            self.groupBoxLineList.append(groupBoxLine)
            
            item = QtGui.QListWidgetItem(self.listWidget_groupBox)
            item.setSizeHint(groupBoxLine.sizeHint())
            self.listWidget_groupBox.setItemWidget(item, groupBoxLine)
           
        self.drawing_page.widget_left_down_layout.addWidget(self.listWidget_groupBox)
        print("c")
        # not sure it is still needed??
        # self.listWidget_group_toolbox.set_empty()
        #self.listWidget_group_toolbox.set_welcome()

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

        if (self.drawing_page.label_right.add_dipole_mode.value and 
            self.drawing_lst[self.current_count]\
            .group_lst[element_number]\
            .zurich.upper() not in ["B","C","D","E","F","G"]):
            
            self.status_bar_mode_name.setText("Add dipole mode")
            self.status_bar_mode_comment.setStyleSheet("QLabel { color : red; }");
            self.status_bar_mode_comment.setText("Warning this is not a dipolar group!!")
            self.drawing_page.label_right.setCursor(QtCore.Qt.ArrowCursor)

        elif (self.drawing_page.label_right.add_dipole_mode.value and 
              self.drawing_lst[self.current_count].group_lst[element_number].zurich.upper()
              in ["B","C","D","E","F","G"]):
            
            self.status_bar_mode_name.setText("Add dipole mode")
            self.status_bar_mode_comment.setStyleSheet("QLabel { color : black; }");
            self.status_bar_mode_comment.setText("Click on a dipole" +
                                                     " positions to add it")
            self.drawing_page.label_right.setCursor(QtCore.Qt.SizeFDiagCursor)

        else:
            print("condition 3")
            self.status_bar_mode_name.setText("") 
            self.status_bar_mode_comment.setText("")
            
    def set_focus_group_box(self, element_number):

        print("enter in the focus group box for the element: ", element_number)
        
        # first element of the list widget initially highlighted and other disabled
        # first element surface updated
       
        if self.listWidget_groupBox.count()>0 and element_number>=0:
            self.listWidget_groupBox.blockSignals(True)
            self.listWidget_groupBox.item(element_number).setSelected(True) # itemchanged -> update group tool box
            self.listWidget_groupBox.blockSignals(False)
            self.update_surface_qlabel(element_number)
            
        #self.listWidget_groupBox.setFocus()
        self.listWidget_groupBox.setCurrentRow(element_number)
        # to change only the line on which the focus is
        for i in range(0, self.listWidget_groupBox.count()):
            if i==element_number:
                self.groupBoxLineList[i].get_spots().setEnabled(True)
                self.groupBoxLineList[i].get_zurich().setEnabled(True)
                self.groupBoxLineList[i].get_McIntosh().setEnabled(True) 
            else:
                self.groupBoxLineList[i].get_spots().setEnabled(False)
                self.groupBoxLineList[i].get_zurich().setEnabled(False)
                self.groupBoxLineList[i].get_McIntosh().setEnabled(False)

    def set_group_toolbox(self, n=0):
        #print("update the group toolbox for the element", n)
        # A widget is deleted when its parents is deleted.
        for i in reversed(range(self.drawing_page.widget_left_down_bis_layout.count())):
            self.drawing_page.widget_left_down_bis_layout.itemAt(i).widget().setParent(None)
                
        self.group_toolbox = group_box.GroupBox()
        self.drawing_page.widget_left_down_bis_layout\
                         .addWidget(self.group_toolbox)
       
        self.grid_position = [0, 0]
        
        #self.self.group_toolbox.set_empty()
        self.group_toolbox.set_title(
            "Group " +
            str(self.drawing_lst[self.current_count].group_lst[n].number),
            self.grid_position,
            0)
        self.group_toolbox.set_spot_count(
            self.drawing_lst[self.current_count].group_lst[n].spots,
            self.grid_position)

        self.group_toolbox.set_zurich_combox_box(
            self.drawing_lst[self.current_count].group_lst[n].zurich,
            self.grid_position)
        
        self.group_toolbox.set_mcIntosh_combo_box(
            self.drawing_lst[self.current_count].group_lst[n].McIntosh,
            self.drawing_lst[self.current_count].group_lst[n].zurich,
            self.grid_position)

        self.group_toolbox.set_delete_group_button(self.grid_position)
            
        delete_button = self.group_toolbox.get_del_button()
        delete_button.clicked.connect(self.delete_group)
        
        self.group_toolbox.set_latitude(
            self.drawing_lst[self.current_count].group_lst[n].latitude * 180/math.pi,
            self.grid_position)
        
        self.group_toolbox.set_longitude(
            self.drawing_lst[self.current_count].group_lst[n].longitude * 180/math.pi,
            self.grid_position)
        
        self.group_toolbox.set_surface(
            self.drawing_lst[self.current_count].group_lst[n].surface,
            self.grid_position)
        
        self.group_toolbox.set_arrows_buttons()
        
      
        self.group_toolbox.set_largest_spot(
            0,
            self.drawing_lst[self.current_count].group_lst[n].zurich,
            self.grid_position)
        
        self.group_toolbox\
            .get_spots()\
            .textEdited\
            .connect( lambda: self.modify_drawing_spots(self.listWidget_groupBox.currentRow(),
                                                        True))
        self.group_toolbox\
            .get_zurich()\
            .currentIndexChanged\
            .connect(lambda: self.modify_drawing_zurich(self.listWidget_groupBox.currentRow(),
                                                        True))
        self.group_toolbox\
            .get_McIntosh()\
            .currentIndexChanged\
            .connect(lambda: self.modify_drawing_mcIntosh(self.listWidget_groupBox.currentRow(),
                                                          True))

        position_step = 0.1 * math.pi/180 
        up, down, left, right = self.group_toolbox.get_arrows()
        up.clicked.connect(
            lambda: self.update_HGC_position('latitude', position_step))
        down.clicked.connect(
            lambda: self.update_HGC_position('latitude', -position_step))
        left.clicked.connect(
            lambda: self.update_HGC_position('longitude', position_step))
        right.clicked.connect(
            lambda: self.update_HGC_position('longitude', -position_step))

        (largest_spot_leading,
         largest_spot_egal,
         largest_spot_trailing) = self.group_toolbox.get_largest_spot_buttons()

        largest_spot_leading.clicked.connect(
            lambda: self.update_g_spot('leading'))
        largest_spot_egal.clicked.connect(
            lambda: self.update_g_spot('egal'))
        largest_spot_trailing.clicked.connect(
            lambda: self.update_g_spot('trailing'))
      
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
        
    def update_g_spot(self, largest_spot):
        """ according to the USSPS defintion 
        g = relative importance of the leading spot and 
        density of the sunspot population
        """
        
        sunspot_population_density = self.drawing_lst[self.current_count]\
                                         .group_lst[self.listWidget_groupBox.currentRow()]\
                                         .McIntosh[2]
        print("enter in update g spot", largest_spot, sunspot_population_density)
        
        if largest_spot=='leading' and sunspot_population_density=='o':
            self.drawing_lst[self.current_count]\
                .group_lst[self.listWidget_groupBox.currentRow()]\
                .g_spot = 1
            
        elif largest_spot=='trailing' and sunspot_population_density=='o':
             self.drawing_lst[self.current_count]\
                .group_lst[self.listWidget_groupBox.currentRow()]\
                .g_spot = 2
        elif largest_spot=='egal' and sunspot_population_density=='o':
             self.drawing_lst[self.current_count]\
                .group_lst[self.listWidget_groupBox.currentRow()]\
                .g_spot = 3
        elif largest_spot=='leading' and sunspot_population_density=='i':
            self.drawing_lst[self.current_count]\
                .group_lst[self.listWidget_groupBox.currentRow()]\
                .g_spot = 4
        elif largest_spot=='trailing' and sunspot_population_density=='i':
             self.drawing_lst[self.current_count]\
                .group_lst[self.listWidget_groupBox.currentRow()]\
                .g_spot = 5
        elif largest_spot=='egal' and sunspot_population_density=='i':
             self.drawing_lst[self.current_count]\
                .group_lst[self.listWidget_groupBox.currentRow()]\
                .g_spot = 6
        elif largest_spot=='leading' and sunspot_population_density=='c':
            self.drawing_lst[self.current_count]\
                .group_lst[self.listWidget_groupBox.currentRow()]\
                .g_spot = 7
        elif largest_spot=='trailing' and sunspot_population_density=='c':
             self.drawing_lst[self.current_count]\
                .group_lst[self.listWidget_groupBox.currentRow()]\
                .g_spot = 8
        elif largest_spot=='egal' and sunspot_population_density=='c':
             self.drawing_lst[self.current_count]\
                .group_lst[self.listWidget_groupBox.currentRow()]\
                .g_spot = 9
             
        self.set_group_toolbox.update_largest_spot(
            self.drawing_lst[self.current_count]\
            .group_lst[self.listWidget_groupBox.currentRow()]\
            .g_spot,
            self.drawing_lst[self.current_count]\
            .group_lst[self.listWidget_groupBox.currentRow()]\
            .zurich)
        
    def update_HGC_position(self, coordinate, value):
        """
        Update the position of the group via the arrows in the group_toolbox
        The longitude and latitude are displayed in degrees.
        The drawing is updated to show the new position of the group.
        """
        index = self.current_count
        group_index = self.listWidget_groupBox.currentRow()
        
        if coordinate=='longitude':
            self.drawing_lst[index].group_lst[group_index].longitude += value
            if self.drawing_lst[index].group_lst[group_index].longitude > 2 * math.pi :
                self.drawing_lst[index].group_lst[group_index].longitude -= 2 * math.pi
                 
            self.group_toolbox.update_longitude(self.drawing_lst[index]\
                                                .group_lst[group_index]\
                                                .longitude * 180/math.pi)
            
        elif coordinate=='latitude':
            self.drawing_lst[index].group_lst[group_index].latitude += value 
            self.group_toolbox.update_latitude(self.drawing_lst[index]\
                                               .group_lst[group_index]\
                                               .latitude * 180/math.pi)
            
        self.drawing_page.label_right.set_img()
      
    def modify_drawing_spots(self, n, is_toolbox):
        if is_toolbox:
            self.drawing_lst[self.current_count]\
                .group_lst[self.listWidget_groupBox.currentRow()]\
                .spots = self.group_toolbox.get_spots().text()
        else:
            self.drawing_lst[self.current_count]\
                .group_lst[self.listWidget_groupBox.currentRow()]\
                .spots = self.groupBoxLineList[n].get_spots().text()
     
        self.groupBoxLineList[n].update_spots(self.drawing_lst[self.current_count].group_lst[n].spots)
        self.group_toolbox.update_spots(self.drawing_lst[self.current_count].group_lst[n].spots)

    def modify_drawing_zurich(self, n, is_toolbox):
        
        old_zurich_type = self.drawing_lst[self.current_count]\
                              .group_lst[self.listWidget_groupBox.currentRow()]\
                              .zurich
        if is_toolbox:
            new_zurich_type = str(self.group_toolbox.get_zurich().currentText())
        else:
            new_zurich_type = str(self.groupBoxLineList[n].get_zurich().currentText())

        if new_zurich_type!=old_zurich_type:
            self.drawing_lst[self.current_count]\
                .group_lst[self.listWidget_groupBox.currentRow()]\
                .zurich = new_zurich_type
            
        self.groupBoxLineList[n].update_zurich(
            self.drawing_lst[self.current_count].group_lst[n].zurich)
        self.group_toolbox.update_zurich(
            self.drawing_lst[self.current_count].group_lst[n].zurich)
        self.groupBoxLineList[n].update_McIntosh_combo_box(
            self.drawing_lst[self.current_count].group_lst[n].zurich)
        self.group_toolbox.update_McIntosh_combo_box(
            self.drawing_lst[self.current_count].group_lst[n].zurich)
        
        if new_zurich_type == "X":
            self.groupBoxLineList[n].get_zurich().setStyleSheet("background-color: orange")
            self.group_toolbox.get_zurich().setStyleSheet("background-color: orange")
        else:
            self.groupBoxLineList[n].get_zurich().setStyleSheet("background-color: white")
            self.group_toolbox.get_zurich().setStyleSheet("background-color: white")


        self.group_toolbox.update_largest_spot(
            new_zurich_type,
            self.drawing_lst[self.current_count].group_lst[n].g_spot)
        
        if (new_zurich_type.upper() in ["B","C","D","E","F","G"] and
            self.drawing_lst[self.current_count].group_lst[n].g_spot==0):
                self.groupBoxLineList[n].get_dipole_button().setStyleSheet(
                    "background-color: orange")        
        else:
           self.groupBoxLineList[n].get_dipole_button().setStyleSheet(
                    "background-color: transparent")

    def modify_drawing_mcIntosh(self, n, is_toolbox):
        print("modif value of mc intosh", n, is_toolbox)
        old_mcIntosh_type = self.drawing_lst[self.current_count]\
                                .group_lst[self.listWidget_groupBox.currentRow()]\
                                .McIntosh
        print("modif value of mc intosh a")
        if is_toolbox:
            new_mcIntosh_type = str(self.group_toolbox.get_McIntosh().currentText())
        else:
            new_mcIntosh_type = str(self.groupBoxLineList[n].get_McIntosh().currentText())

        print("modif value of mc intosh b", new_mcIntosh_type)
        if new_mcIntosh_type!=old_mcIntosh_type:
            self.drawing_lst[self.current_count]\
                .group_lst[self.listWidget_groupBox.currentRow()]\
                .McIntosh = new_mcIntosh_type

        print("modif value of mc intosh c")
        self.groupBoxLineList[n].update_McIntosh(self.drawing_lst[self.current_count].group_lst[n].McIntosh)
        self.group_toolbox.update_McIntosh(self.drawing_lst[self.current_count].group_lst[n].McIntosh)
        print("modif value of mc intosh d")
        
    def update_group_visu(self, n):
        self.drawing_page.label_right.group_visu_index = n
        self.drawing_page.label_right.set_img()
        
    def add_drawing_information(self):

        title_left_up = QtGui.QLabel("Drawing information")
        title_left_up.setAlignment(QtCore.Qt.AlignCenter)
        title_left_up.setContentsMargins(0, 5, 0, 5)
        self.drawing_page.widget_left_up_layout.addWidget(title_left_up)
        self.form_layout1 = QtGui.QFormLayout()
        self.form_layout1.setSpacing(10)
        
        self.drawing_operator = QtGui.QLineEdit(self)
        self.drawing_operator.setMaximumWidth(self.column_maximum_width)
        self.drawing_operator.setEnabled(True)
        self.drawing_operator.setStyleSheet("background-color: lightgray; color:black")
        
        self.drawing_observer = QtGui.QLineEdit(self)
        self.drawing_observer.setMaximumWidth(self.column_maximum_width)
        self.drawing_observer.setEnabled(True)
        self.drawing_observer.setStyleSheet("background-color: white; color:black")
        
        self.drawing_date = QtGui.QDateEdit()
        self.drawing_date.setMaximumWidth(self.column_maximum_width)
        self.drawing_date.setDisplayFormat("dd/MM/yyyy")
        today = QtCore.QDate.currentDate()
        self.drawing_date.setDate(today)
        self.drawing_date.setEnabled(False)
        self.drawing_date.setStyleSheet("background-color: lightgray; color:black")
        
        self.drawing_time = QtGui.QLineEdit("00:00",self)
        self.drawing_time.setMaximumWidth(self.column_maximum_width)
        self.drawing_time.setInputMask("99:99")
        self.drawing_time.setEnabled(False)
        self.drawing_time.setStyleSheet("background-color: lightgray; color:black")
        
        self.drawing_quality = QtGui.QLineEdit(self)
        self.drawing_quality.setMaximumWidth(self.column_maximum_width)
        #self.drawing_quality.setMinimum(1)
        #self.drawing_quality.setMaximum(5)
        #self.drawing_quality.setValue(3)
        self.drawing_quality.setEnabled(True)
        self.drawing_quality.setStyleSheet("background-color: white; color:black")
        
        self.drawing_type = QtGui.QComboBox(self)
        self.drawing_type.setMaximumWidth(self.column_maximum_width)
        self.drawing_type.setEnabled(True)
        self.drawing_type.setStyleSheet("background-color: white; color:black")
        self.drawing_type.addItem('USET')
        self.drawing_type.addItem('USET77')
        self.drawing_type.addItem('USET41')

        self.wolf_number = QtGui.QLineEdit(self)
        self.wolf_number.setMaximumWidth(self.column_maximum_width)
        self.wolf_number.setStyleSheet("background-color: white; color:black")
        
        self.angleP = QtGui.QLineEdit(self)
        self.angleP.setMaximumWidth(self.column_maximum_width)
        self.angleP.setEnabled(False)
        self.angleP.setStyleSheet("background-color: lightgrey; color:black")
        
        self.angleB = QtGui.QLineEdit(self)
        self.angleB.setMaximumWidth(self.column_maximum_width)
        self.angleB.setEnabled(False)
        self.angleB.setStyleSheet("background-color: lightgrey; color:black")
        
        self.angleL = QtGui.QLineEdit(self)
        self.angleL.setMaximumWidth(self.column_maximum_width)
        self.angleL.setEnabled(False)
        self.angleL.setStyleSheet("background-color: lightgrey; color:black")
        
        self.rotation_number = QtGui.QLineEdit(self)
        self.rotation_number.setMaximumWidth(self.column_maximum_width)
        self.rotation_number.setEnabled(False)
        self.rotation_number.setStyleSheet("background-color: lightgrey; color:black")

        self.calibrated = QtGui.QLineEdit(self)
        self.calibrated.setMaximumWidth(self.column_maximum_width)
        self.calibrated.setEnabled(False)
        self.calibrated.setStyleSheet("background-color: lightgrey; color:black")
        
        self.analyzed = QtGui.QLineEdit(self)
        self.analyzed.setMaximumWidth(self.column_maximum_width)
        self.analyzed.setEnabled(False)
        self.analyzed.setStyleSheet("background-color: lightgrey; color:black")
        
        self.area_done = QtGui.QLineEdit(self)
        self.area_done.setMaximumWidth(self.column_maximum_width)
        self.area_done.setEnabled(False)
        self.area_done.setStyleSheet("background-color: lightgrey; color:black")

        self.form_layout1.addRow('Date:', self.drawing_date)
        self.form_layout1.addRow('Time:', self.drawing_time)
        self.form_layout1.addRow('P angle:', self.angleP)
        self.form_layout1.addRow('B angle:', self.angleB)
        self.form_layout1.addRow('L angle:', self.angleL)
        self.form_layout1.addRow('Carington rotation :', self.rotation_number)
        
        self.form_layout1.addRow('Observer:', self.drawing_observer)
        self.form_layout1.addRow('Last Operator:', self.drawing_operator)
        self.form_layout1.addRow('Quality:', self.drawing_quality)
        self.form_layout1.addRow('Type:', self.drawing_type)
        
        self.form_layout1.addRow('Wolf number:', self.wolf_number)
        
        self.form_layout1.addRow('Calibrated:', self.calibrated)
        self.form_layout1.addRow('Analysed:', self.analyzed)
        self.form_layout1.addRow('Area done:', self.area_done)
        
        
        self.drawing_observer.textEdited.connect(self.update_observer)
        self.drawing_quality.textEdited.connect(self.update_quality)
        self.drawing_type.currentIndexChanged.connect(self.update_type)
        self.wolf_number.textEdited.connect(self.update_wolf_number)

        widget_form = QtGui.QWidget()
        widget_form.setMaximumWidth(self.column_maximum_width)
        widget_form.setLayout(self.form_layout1)
        self.drawing_page.widget_left_up_layout.addWidget(widget_form)

    def update_wolf_number(self):
        #check that the value from the linedit is a number between 1 and xxx
        self.drawing_lst[self.current_count].wolf = self.wolf_number.text()

    def update_observer(self):
        # check that the value is in the database
        uset_db = database.database()
        if uset_db.exist_in_db('observers', 'namecode', self.drawing_observer.text()):
            self.drawing_lst[self.current_count].observer = self.drawing_observer.text()
            self.drawing_observer.setStyleSheet("background-color: white")
        else:
            self.drawing_observer.setStyleSheet("background-color: rgb(232, 103, 101)")

    def update_quality(self):
        # check that the value is in the database
        # to do: create the table in the database!!
        uset_db = database.database()
        
        self.drawing_lst[self.current_count].quality = self.drawing_quality.text()
        #    self.drawing_observer.setStyleSheet("background-color: rgb(125, 232, 164)")
        #else:
        #    self.drawing_observer.setStyleSheet("background-color: rgb(232, 103, 101)")
        
    def update_type(self):
        # check that the value is in the database
        # to do: create the table in the database!!
        uset_db = database.database()
        
        self.drawing_lst[self.current_count].drawing_type = self.drawing_type.currentText()
        #    self.drawing_observer.setStyleSheet("background-color: rgb(125, 232, 164)")
        #else:
        #    self.drawing_observer.setStyleSheet("background-color: rgb(232, 103, 101)")
                
    def add_surface(self):
        
        qlabel_title = QtGui.QLabel("Surface calculation")
        qlabel_title.setAlignment(QtCore.Qt.AlignCenter)
        qlabel_title.setContentsMargins(0, 5, 0, 5)
        
        self.drawing_page.widget_middle_up_layout.setSpacing(10)
        qlabel_polygon = QtGui.QLabel("Selection tools:")
        selection_layout = QtGui.QHBoxLayout()
        
        self.draw_polygon_but = QtGui.QToolButton()
        self.draw_polygon_but.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.draw_polygon_but.setText("Select mode")
        self.draw_polygon_but.setIcon(QtGui.QIcon('icons/Darrio_Ferrando/polygon.svg'))
        self.drawing_page\
            .label_middle_up\
            .polygon\
            .value_changed\
            .connect(lambda: self.set_button_color(self.drawing_page.label_middle_up.polygon.value,
                                                self.draw_polygon_but))
        
        self.crop_but = QtGui.QToolButton()
        self.crop_but.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.crop_but.setText("Crop")
        self.crop_but.setDisabled(True)
        
        self.zoom_in_but = QtGui.QToolButton()
        self.zoom_in_but.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.zoom_in_but.setText("zoom in")
        self.zoom_in_but.setIcon(QtGui.QIcon('icons/Smashicons/zoom-in.svg'))

        self.zoom_out_but = QtGui.QToolButton()
        self.zoom_out_but.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.zoom_out_but.setText("zoom out")
        self.zoom_out_but.setIcon(QtGui.QIcon('icons/Smashicons/search.svg'))

        self.reset_but = QtGui.QToolButton()
        self.reset_but.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.reset_but.setText("Reset")

        selection_layout.addWidget(self.draw_polygon_but)
        selection_layout.addWidget(self.crop_but)
        selection_layout.addWidget(self.zoom_in_but)
        selection_layout.addWidget(self.zoom_out_but)
        selection_layout.addWidget(self.reset_but)
        
        qlabel_threshold = QtGui.QLabel("Threshold:")
        self.slider_threshold = QtGui.QSlider(QtCore.Qt.Horizontal)
        self.slider_threshold.setRange(0,256)
        self.slider_threshold.setValue(self.drawing_page.label_middle_up.threshold_value)
        self.slider_threshold.setDisabled(True)
        
        self.threshold_but = QtGui.QToolButton()
        self.threshold_but.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.threshold_but.setText("threshold mode")
        self.drawing_page\
            .label_middle_up\
            .threshold\
            .value_changed\
            .connect(lambda: self.set_button_color(self.drawing_page.label_middle_up.threshold.value,
                                                self.threshold_but))
        
        self.qlabel_paint_tool = QtGui.QLabel("Paint tool:")
        paint_layout = QtGui.QHBoxLayout()

        self.pencil_but = QtGui.QToolButton()
        self.pencil_but.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.pencil_but.setText("Draw")
        self.pencil_but.setIcon(QtGui.QIcon('icons/Darrio_Ferrando/pencil.svg'))
        self.pencil_but.setDisabled(True)
        
        self.bucket_fill_but = QtGui.QToolButton()
        self.bucket_fill_but.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.bucket_fill_but.setText("Fill")
        self.bucket_fill_but.setIcon(QtGui.QIcon('icons/Darrio_Ferrando/bucket.svg'))
        self.bucket_fill_but.setDisabled(True)
               
        self.rubber_but = QtGui.QToolButton()
        self.rubber_but.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.rubber_but.setText("Erase")
        self.rubber_but.setIcon(QtGui.QIcon('icons/Freepik/erase-text.svg'))
        self.rubber_but.setDisabled(True)

        form_layout = QtGui.QFormLayout()
        self.pixel_number_linedit = QtGui.QLineEdit()
        surface_linedit = QtGui.QLineEdit()

        form_layout.addRow("Pixel Number:", self.pixel_number_linedit)
        form_layout.addRow("Surface:", surface_linedit)
        
        paint_layout.addWidget(self.pencil_but)
        paint_layout.addWidget(self.bucket_fill_but)
        paint_layout.addWidget(self.rubber_but)

        self.convert_but = QtGui.QToolButton()
        self.convert_but.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.convert_but.setText("Convert")
        #self.convert_but.setIcon(QtGui.QIcon('icons/Darrio_Ferrando/pencil.svg'))
        self.convert_but.setDisabled(True)

        
        save_but = QtGui.QToolButton()
        save_but.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        save_but.setText("Save area")

        next_but = QtGui.QToolButton()
        next_but.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        next_but.setText("Next group")
        
        self.calculate_but = QtGui.QToolButton()
        self.calculate_but.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.calculate_but.setText("Calculate")
        
        self.drawing_page.widget_middle_up_layout.setMargin(10)

        self.drawing_page.widget_middle_up_layout.addWidget(qlabel_title)
        self.drawing_page.widget_middle_up_layout.addWidget(qlabel_polygon)
        self.drawing_page.widget_middle_up_layout.addLayout(selection_layout)
        
        self.drawing_page.widget_middle_up_layout.addWidget(qlabel_threshold)
        self.drawing_page.widget_middle_up_layout.addWidget(self.threshold_but)
        self.drawing_page.widget_middle_up_layout.addWidget(self.slider_threshold)
        
        self.drawing_page.widget_middle_up_layout.addWidget(self.qlabel_paint_tool)
        self.drawing_page.widget_middle_up_layout.addLayout(paint_layout)
        self.drawing_page.widget_middle_up_layout.addWidget(self.convert_but)
        
        self.drawing_page.widget_middle_up_layout.addWidget(self.drawing_page.label_middle_up)
        self.drawing_page.widget_middle_up_layout.addWidget(self.calculate_but)
        self.drawing_page.widget_middle_up_layout.addLayout(form_layout)
        self.drawing_page.widget_middle_up_layout.addWidget(save_but)
        self.drawing_page.widget_middle_up_layout.addWidget(next_but)
        
        
        self.draw_polygon_but.clicked.connect(self.draw_polygon)
        self.crop_but.clicked.connect(self.crop_method)
        self.reset_but.clicked.connect(self.reset)

        self.slider_threshold.valueChanged.connect(self.update_threshold_value)
       
        self.threshold_but\
            .clicked.connect(self.threshold)

        self.pencil_but.clicked.connect(self.draw_pencil)
        self.bucket_fill_but.clicked.connect(self.draw_bucket)
        self.rubber_but.clicked.connect(self.rubber_method)
        self.calculate_but.clicked.connect(self.calculate_method)

    def update_threshold_value(self):
        print("check the slider value",self.slider_threshold.value() )
        self.drawing_page.label_middle_up.threshold_value = self.slider_threshold.value()
        if self.drawing_page.label_middle_up.threshold.value:
            self.drawing_page.label_middle_up.set_img()
            
    def crop_method(self):
        self.drawing_page.label_middle_up.crop()
        self.draw_polygon_but.setDisabled(True)

    def rubber_method(self):
        self.drawing_page.label_middle_up.modify_rubber_color()

    def calculate_method(self):
        count = self.drawing_page.label_middle_up.calculate_area()
        self.pixel_number_linedit.setText(str(count))

    def threshold(self):
        if self.drawing_page.label_middle_up.threshold.value :
            self.drawing_page.label_middle_up.threshold.value = False
            self.slider_threshold.setDisabled(True)
        else:
            print("set the threshold to true")
            self.drawing_page.label_middle_up.threshold.value = True
            self.slider_threshold.setEnabled(True)
            
        self.drawing_page.label_middle_up.polygon.value = False
        self.drawing_page.label_middle_up.bucket.value = False
        self.drawing_page.label_middle_up.pencil.value = False

        
        
        #self.threshold_but.setDisabled(True)
        self.drawing_page.label_middle_up.set_img()

        #print(self.drawing_page.label_middle_up.crop_done.value)
        if self.drawing_page.label_middle_up.crop_done.value :
            self.draw_polygon_but.setDisabled(True)
            self.crop_but.setDisabled(True)
            
        self.pencil_but.setEnabled(True)
        self.bucket_fill_but.setEnabled(True)
        self.rubber_but.setEnabled(True)
            
    def draw_pencil(self):
        self.drawing_page.label_middle_up.pencil.value = True
        self.drawing_page.label_middle_up.threshold.value = False
        self.drawing_page.label_middle_up.polygon.value = False
        self.drawing_page.label_middle_up.crop_done.value= False
        self.drawing_page.label_middle_up.bucket.value = False
    
    def draw_bucket(self):
        self.drawing_page.label_middle_up.bucket.value = True
        self.drawing_page.label_middle_up.threshold.value = False
        self.drawing_page.label_middle_up.polygon.value = False
        self.drawing_page.label_middle_up.crop_done.value = False
        self.drawing_page.label_middle_up.pencil.value = False
        
    def draw_polygon(self):
        if self.drawing_page.label_middle_up.polygon.value :
            self.drawing_page.label_middle_up.polygon.value = False
        else:
            self.drawing_page.label_middle_up.polygon.value = True
            
        self.drawing_page.label_middle_up.threshold.value = False
        self.drawing_page.label_middle_up.crop_done.value = False
        self.drawing_page.label_middle_up.pencil.value = False
        self.drawing_page.label_middle_up.bucket.value = False
        self.crop_but.setEnabled(True)
        
        # no function here but the click on the image
        # will call set_img in the qlabel
        
        #if not self.drawing_page.label_middle_up.mode_draw_polygon.value:
        #    self.drawing_page.label_middle_up.pointsList = []

    def reset(self):
        
        self.drawing_page.label_middle_up.threshold.value = False
        self.drawing_page.label_middle_up.polygon.value = False
        self.drawing_page.label_middle_up.crop_done.value = False
        self.drawing_page.label_middle_up.pencil.value = False
        self.drawing_page.label_middle_up.bucket.value = False
        
        self.threshold_but.setEnabled(True)
        self.draw_polygon_but.setEnabled(True)
        self.crop_but.setEnabled(True)
        self.drawing_page.label_middle_up.reset_img()
        self.pencil_but.setDisabled(True)
        self.bucket_fill_but.setDisabled(True)
        self.rubber_but.setDisabled(True)
        self.drawing_page.label_middle_up.crop_done.value = False
        self.drawing_page.label_middle_up.threshold_done.value = False
        
    def add_current_session(self):
        
        form_layout2 = QtGui.QFormLayout()
        form_layout2.setSpacing(15)

        title_left_middle = QtGui.QLabel("Current session")
        title_left_middle.setAlignment(QtCore.Qt.AlignCenter)
        title_left_middle.setContentsMargins(0, 5, 0, 5)
        self.drawing_page.widget_left_middle_layout.addWidget(title_left_middle)
        
        self.current_operator = QtGui.QLineEdit(str(self.operator).upper(), self)
        self.current_operator.setEnabled(False)
        self.current_operator.setStyleSheet("background-color: white; color: black")
        self.current_operator.setMaximumWidth(self.column_maximum_width)
        
        self.but_previous = QtGui.QPushButton('previous', self)
        self.but_previous.setShortcut(QtGui.QKeySequence("Left"))
        self.but_next = QtGui.QPushButton('next', self)
        self.but_next.setShortcut(QtGui.QKeySequence("Right"))

        self.but_next.clicked.connect(lambda: self.update_counter(self.current_count+1))
        self.but_next.clicked.connect(self.set_drawing)
        self.but_previous.clicked.connect(lambda: self.update_counter(self.current_count-1))
        self.but_previous.clicked.connect(self.set_drawing)

        layout_but = QtGui.QHBoxLayout()
        layout_but.addWidget(self.but_previous)
        layout_but.addWidget(self.but_next)
        
        layout_goto = self.jump_to_drawing_linedit()
        
        self.but_save = QtGui.QPushButton('save', self)
        self.but_save.setMaximumWidth(self.column_maximum_width + 75)
        #self.but_save.setStyleSheet("background-color: ")
        #self.but_save.clicked.connect(lambda: self.set_drawing())

        form_layout2.addRow("Current operator: ", self.current_operator)
        form_layout2.setLayout(1,QtGui.QFormLayout.SpanningRole,layout_goto)
        form_layout2.setLayout(2,
                               QtGui.QFormLayout.SpanningRole,
                               layout_but)
        
        form_layout2.setWidget(3,
                               QtGui.QFormLayout.SpanningRole,
                               self.but_save)

        
        self.drawing_page.widget_left_middle_layout.addLayout(form_layout2)
        
    def jump_to_drawing_linedit(self):
        """
        TO DO: It should update the drawing and the group box which is not case now!!!
        """
        self.goto_drawing_linedit = QtGui.QLineEdit()
        self.goto_drawing_label1 = QtGui.QLabel()
        self.goto_drawing_label2 = QtGui.QLabel()
        self.goto_drawing_button = QtGui.QPushButton()
        
        self.goto_drawing_label1.setText("Jump to drawing")
        self.goto_drawing_linedit.setText("1")
        self.goto_drawing_linedit.setStyleSheet("background-color: white; color: black")
        self.goto_drawing_label2.setText("out of 0")
        self.goto_drawing_button.setText("Go!")

        self.goto_drawing_button.clicked.connect(
            lambda: self.update_counter(int(self.goto_drawing_linedit.text())-1))
        self.goto_drawing_button.clicked.connect(
            lambda: self.drawing_page.label_right.set_img())

        layout_goto = QtGui.QHBoxLayout()
        layout_goto.addWidget(self.goto_drawing_label1)
        layout_goto.addWidget(self.goto_drawing_linedit)
        layout_goto.addWidget(self.goto_drawing_label2)
        layout_goto.addWidget(self.goto_drawing_button)     
        return layout_goto
       
    def update_counter(self, value):
        
        if value >= self.len_drawing_lst:
            value = self.len_drawing_lst-1
        elif value < 0:
            value = 0

        self.current_count = value
        
        if self.current_count > 0 and self.current_count < self.len_drawing_lst - 1:
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
        self.drawing_operator.setText(self.drawing_lst[self.current_count].operator)
        self.drawing_observer.setText(self.drawing_lst[self.current_count].observer)
        self.drawing_date.setDate(QtCore.QDate(self.drawing_lst[self.current_count].datetime.year,
                                               self.drawing_lst[self.current_count].datetime.month,
                                               self.drawing_lst[self.current_count].datetime.day))
        self.drawing_time.setText(str(self.drawing_lst[ self.current_count].datetime.strftime('%H')) +
                                  ":" +
                                  str(self.drawing_lst[ self.current_count].datetime.strftime('%M')))
        
        self.drawing_quality.setText(str(self.drawing_lst[self.current_count].quality))
        
        self.drawing_type.blockSignals(True)
        index_drawing_type = self.drawing_type\
                                 .findText(self.drawing_lst[self.current_count].drawing_type)
        self.drawing_type.setCurrentIndex(index_drawing_type)
        self.drawing_type.blockSignals(False)
        

        print(self.drawing_lst[self.current_count].changed)
        
        if self.drawing_lst[self.current_count].changed:
            self.but_save.setStyleSheet("background-color: rgb(255, 165, 84)")
        else:
            self.but_save.setStyleSheet("background-color: lightgray")

        self.angleP.setText('{0:.2f}'.format(self.drawing_lst[self.current_count].angle_P))
        self.angleB.setText('{0:.2f}'.format(self.drawing_lst[self.current_count].angle_B))
        self.angleL.setText('{0:.2f}'.format(self.drawing_lst[self.current_count].angle_L))
        self.rotation_number.setText(str(self.drawing_lst[self.current_count].carington_rotation))

        self.calibrated.setText(str(self.drawing_lst[self.current_count].calibrated))
        self.analyzed.setText(str(self.drawing_lst[self.current_count].analyzed))

        self.wolf_number.setText(str(self.drawing_lst[self.current_count].wolf))
        
    def set_path_to_qlabel(self):
        """
        set the path to the image of the drawing based on the information contained 
        in the configuration file (digisun.ini).
        Here is fixed the structure of the filename and 
        the structure of the directory.
        """  
        filename = (self.prefix +
                    str(self.drawing_lst[self.current_count].datetime.year) +
                    str(self.drawing_lst[self.current_count].datetime.strftime('%m')) +
                    str(self.drawing_lst[self.current_count].datetime.strftime('%d')) +
                    str(self.drawing_lst[self.current_count].datetime.strftime('%H')) +
                    str(self.drawing_lst[self.current_count].datetime.strftime('%M')) +
                    "." +
                    self.extension)

        directory = os.path.join(self.archdrawing_directory,
                                 str(self.drawing_lst[self.current_count].datetime.year),
                                 self.drawing_lst[self.current_count].datetime.strftime('%m'))
        
        #print('directory: ', directory)
        self.drawing_page.label_right.file_path = os.path.join(directory, filename)

            
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
        self.drawing_page.label_right.current_drawing = self.drawing_lst[self.current_count]
        self.drawing_page.label_right.group_visu_index = 0

        self.drawing_page.label_right.calibration_mode.value = False
        self.drawing_page.label_right.helper_grid.value = False
        self.drawing_page.label_right.add_group_mode.value = False
        self.drawing_page.label_right.add_dipole_mode.value = False
        self.drawing_page.label_right.surface_mode.value = False

        self.drawing_page.label_right.setCursor(QtCore.Qt.ArrowCursor)
        self.drawing_page.label_right.set_img()

        self.set_group_widget()

        self.set_focus_group_box(0)
        
        
        self.set_group_toolbox()
        self.status_bar_mode_name.setText("")
        self.status_bar_mode_comment.setText("")
        #self.drawing_page.label_right.show()
    
