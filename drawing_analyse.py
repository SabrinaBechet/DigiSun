# !/usr/bin/env python
# -*-coding:utf-8-*-
import os
from PyQt4 import QtGui, QtCore

import database, drawing, group_box, qlabel_drawing
from datetime import date, time, datetime, timedelta
import math

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
        self.widget_left_up.setMaximumHeight(300)
        self.widget_left_up.setStyleSheet("background-color:lightgray;")   
        self.widget_left_up_layout = QtGui.QVBoxLayout()
        self.widget_left_up_layout.setContentsMargins(0, 0, 0, 0) 
        self.widget_left_up_layout.setSpacing(0)
        self.widget_left_up_layout.setAlignment(QtCore.Qt.AlignTop)
        self.widget_left_up.setLayout(self.widget_left_up_layout)

        self.widget_left_middle = QtGui.QWidget()
        self.widget_left_middle.setMinimumWidth(350)
        self.widget_left_middle.setMaximumHeight(320)
        self.widget_left_middle.setStyleSheet("background-color:lightgray;")   
        self.widget_left_middle_layout = QtGui.QVBoxLayout()
        self.widget_left_middle_layout.setContentsMargins(0, 0, 0, 0) 
        self.widget_left_middle_layout.setSpacing(0)
        self.widget_left_middle_layout.setAlignment(QtCore.Qt.AlignTop)
        self.widget_left_middle.setLayout(self.widget_left_middle_layout)

        self.widget_left_down = QtGui.QWidget()
        self.widget_left_down.setMaximumWidth(350)
        self.widget_left_down.setMinimumHeight(580)
        self.widget_left_down.setStyleSheet("background-color:lightblue;")   
        self.widget_left_down_layout = QtGui.QVBoxLayout()
        self.widget_left_down_layout.setContentsMargins(0, 0, 0, 0) 
        self.widget_left_down_layout.setSpacing(0)
        self.widget_left_down_layout.setAlignment(QtCore.Qt.AlignTop and QtCore.Qt.AlignRight)
        self.widget_left_down.setLayout(self.widget_left_down_layout)

        self.widget_middle_up = QtGui.QWidget()
        self.widget_middle_up.setMaximumWidth(10)
        self.widget_middle_up.setMinimumHeight(200)
        self.widget_middle_up.setStyleSheet("background-color:lightgray;")
        self.widget_middle_up_layout = QtGui.QVBoxLayout()
        self.widget_middle_up_layout.setContentsMargins(0, 0, 0, 0) 
        self.widget_middle_up_layout.setSpacing(0)
        self.widget_middle_up_layout.setAlignment(QtCore.Qt.AlignTop)
        self.widget_middle_up.setLayout(self.widget_middle_up_layout)
        self.label_middle_up = qlabel_drawing.QLabelSurfaceThreshold()
           
        self.widget_right = QtGui.QWidget()
        self.widget_right.setStyleSheet("background-color:gray;")
        self.widget_right_layout = QtGui.QVBoxLayout()
        self.widget_right_layout.setContentsMargins(0, 0, 0, 0) 
        self.widget_right_layout.setSpacing(0)
        self.widget_right.setLayout(self.widget_right_layout)
        self.label_right = qlabel_drawing.QLabelDrawing()

        #self.label_middle_up = qlabel_drawing.QLabelSurfaceThreshold()
        
        #self.widget_right.layout().addWidget(self.label_middle_up)
        self.widget_right.layout().addWidget(self.label_right)
  
        self.scroll = QtGui.QScrollArea()
        self.scroll.setWidget(self.label_right)
        
        self.scroll.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.scroll.setWidgetResizable(True)
 
        self.widget_right_layout.addWidget(self.scroll)
        
        splitter_middle_down = QtGui.QSplitter(QtCore.Qt.Vertical, self)
        self.layout().addWidget(splitter_middle_down)
        splitter_middle_down.addWidget(self.widget_left_up)
        splitter_middle_down.addWidget(self.widget_left_middle)
        splitter_middle_down.addWidget(self.widget_left_down)
        
        """splitter_left = QtGui.QSplitter(QtCore.Qt.Vertical, self)
        self.layout().addWidget(splitter_left)
        splitter_left.addWidget(splitter_middle_down)       
        splitter_left.addWidget(self.widget_left_down)
        """
        
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

        self.drawing_page = DrawingViewPage()
        self.vertical_scroll_bar = self.drawing_page.scroll.verticalScrollBar()
        self.horizontal_scroll_bar = self.drawing_page.scroll.horizontalScrollBar()
        
        self.setCentralWidget(self.drawing_page)
        
        self.operator = operator
        self.column_maximum_width = 600
        self.add_drawing_information()
        self.add_current_session()
        self.add_surface()
        self.drawing_lst = []
        self.set_toolbar()
        
        self.drawing_page.label_right.drawing_clicked.connect(self.slot_calibrate)
        self.drawing_page.label_right.drawing_clicked.connect(self.slot_add_group)
        
        self.center_done = False
        self.north_done = False
        self.approximate_center = [0., 0.]

        self.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)

    def set_but_color(self, mode_bool, but):
        if mode_bool==True:
            but.setStyleSheet("background-color: lightblue")
        elif mode_bool==False:
            but.setStyleSheet("background-color: lightgray")
   
    def set_toolbar(self):
        """Note : The QToolBar class inherit from QWidget.
        Icons were designed by "Good Ware" from https://www.flaticon.com
        """

        toolbar = self.addToolBar("view")
        toolbar.setIconSize(QtCore.QSize(30, 30));

        self.zoom_in_but = QtGui.QToolButton(toolbar)
        self.zoom_in_but.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.zoom_in_but.setText("zoom in")
        self.zoom_in_but.setIcon(QtGui.QIcon('icons/zoom-in.svg'))

        self.zoom_out_but = QtGui.QToolButton(toolbar)
        self.zoom_out_but.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.zoom_out_but.setText("zoom out")
        self.zoom_out_but.setIcon(QtGui.QIcon('icons/search.svg'))
   
        self.large_grid_but = QtGui.QToolButton(toolbar)
        self.large_grid_but.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.large_grid_but.setText("large grid")
        self.large_grid_but.setIcon(QtGui.QIcon('icons/internet.svg'))
        self.drawing_page.label_right\
                         .large_grid_overlay\
                         .value_changed\
                         .connect(lambda: self.set_but_color(self.drawing_page.label_right.large_grid_overlay.value,
                                                             self.large_grid_but ))
        if self.drawing_page.label_right.large_grid_overlay.value :
            self.large_grid_but.setStyleSheet("background-color: lightblue")
            
        self.small_grid_but = QtGui.QToolButton(toolbar)
        self.small_grid_but.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.small_grid_but.setText("small grid")
        self.small_grid_but.setIcon(QtGui.QIcon('icons/internet.svg'))
        self.drawing_page.label_right\
                         .small_grid_overlay\
                         .value_changed\
                         .connect(lambda: self.set_but_color(self.drawing_page.label_right.small_grid_overlay.value,
                                                             self.small_grid_but))
        if self.drawing_page.label_right.small_grid_overlay.value :
            self.small_grid_but.setStyleSheet("background-color: lightblue")

        self.group_visu_but = QtGui.QToolButton(toolbar)
        self.group_visu_but.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.group_visu_but.setText("group view")
        self.group_visu_but.setIcon(QtGui.QIcon('icons/share_1.svg'))
        self.drawing_page.label_right\
                         .group_visu\
                         .value_changed\
                         .connect(lambda: self.set_but_color(self.drawing_page.label_right.group_visu.value,
                                                             self.group_visu_but))
        if self.drawing_page.label_right.group_visu.value :
            self.group_visu_but.setStyleSheet("background-color: lightblue")


        self.dipole_visu_but = QtGui.QToolButton(toolbar)
        self.dipole_visu_but.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.dipole_visu_but.setText("dipole view")
        self.dipole_visu_but.setIcon(QtGui.QIcon('icons/share.svg'))
        self.drawing_page.label_right\
                         .dipole_visu\
                         .value_changed\
                         .connect(lambda: self.set_but_color(self.drawing_page.label_right.dipole_visu.value,
                                                             self.dipole_visu_but))
        if self.drawing_page.label_right.dipole_visu.value :
            self.dipole_visu_but.setStyleSheet("background-color: lightblue")

        self.calibration_but = QtGui.QToolButton(toolbar)
        self.calibration_but.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.calibration_but.setText("calibration")
        self.calibration_but.setIcon(QtGui.QIcon('icons/target.svg'))
        self.drawing_page.label_right\
                         .calibration_mode\
                         .value_changed\
                         .connect(lambda: self.set_but_color(self.drawing_page.label_right.calibration_mode.value,
                                                             self.calibration_but))
        if self.drawing_page.label_right.calibration_mode.value :
            self.calibration_but.setStyleSheet("background-color: lightblue")

        self.add_group_but = QtGui.QToolButton(toolbar)
        self.add_group_but.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.add_group_but.setText("add_group")
        self.add_group_but.setIcon(QtGui.QIcon('icons/hospital.svg'))
        self.drawing_page.label_right\
                         .add_group_mode\
                         .value_changed\
                         .connect(lambda: self.set_but_color(self.drawing_page.label_right.add_group_mode.value,
                                                             self.add_group_but))
        if self.drawing_page.label_right.add_group_mode.value :
            self.add_group_but.setStyleSheet("background-color: lightblue")

        self.add_dipole_but = QtGui.QToolButton(toolbar)
        self.add_dipole_but.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.add_dipole_but.setText("add_dipole")
        self.add_dipole_but.setIcon(QtGui.QIcon('icons/share.svg'))
        self.drawing_page.label_right\
                         .add_dipole_mode\
                         .value_changed\
                         .connect(lambda: self.set_but_color(self.drawing_page.label_right.add_dipole_mode.value,
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
                         .connect(lambda: self.set_but_color(self.drawing_page.label_right.surface_mode.value,
                                                             self.surface_but))
        if self.drawing_page.label_right.surface_mode.value :
            self.surface_but.setStyleSheet("background-color: lightblue")
            
        
        #self.about_but = QtGui.QPushButton("About")
        
        helper_grid = QtGui.QAction('helper_grid',  toolbar)
        helper_grid.setIcon(QtGui.QIcon('icons/internet.svg'))
    
        vertical_line_widget = QtGui.QWidget()
        vertical_line_widget.setFixedWidth(2)
        #horizontalLineWidget.setSizePolicy(QtCore.QSizePolicy::Expanding, QSizePolicy::Fixed);
        vertical_line_widget.setStyleSheet("background-color: black")

        toolbar.addWidget(self.zoom_in_but)
        toolbar.addWidget(self.zoom_out_but)
        toolbar.addWidget(self.large_grid_but)
        toolbar.addWidget(self.small_grid_but)
        toolbar.addWidget(self.group_visu_but)
        toolbar.addWidget(self.dipole_visu_but)
        toolbar.addAction(helper_grid)
        toolbar.addWidget(vertical_line_widget)
        toolbar.addWidget(self.calibration_but)
        toolbar.addWidget(self.add_group_but)
        toolbar.addWidget(self.add_dipole_but)
        toolbar.addWidget(self.surface_but)
        #toolbar.addWidget(self.about_but)
        
    
        #zoom_in.triggered.connect(lambda : self.drawing_page.label_right.zoom_in(1.1))
        #zoom_out.triggered.connect(lambda : self.drawing_page.label_right.zoom_in(1/1.1))
        self.zoom_in_but.clicked.connect(lambda : self.drawing_page.label_right.zoom_in(1.1))
        self.zoom_out_but.clicked.connect(lambda : self.drawing_page.label_right.zoom_in(1/1.1))
        self.large_grid_but.clicked.connect(self.set_large_grid)
        self.small_grid_but.clicked.connect(self.set_small_grid)
        self.group_visu_but.clicked.connect(self.set_group_visualisation)
        self.dipole_visu_but.clicked.connect(self.set_dipole_visualisation)
        self.calibration_but.clicked.connect(self.start_calibration)
        self.add_group_but.clicked.connect(self.add_group)
        self.add_dipole_but.clicked.connect(self.add_dipole)
        self.surface_but.clicked.connect(self.calculate_surface)
        
    def add_group(self):        
        self.drawing_page.label_right.add_group_mode.set_opposite_value()

    def slot_add_group(self):
        """
        This is triggered when clicking on the drawing and the add_group_mode is True
        It calls the add_group method of the drawing object.
        """
        if self.drawing_page.label_right.add_group_mode.value:       
            self.get_click_coordinates()
        
        self.drawing_lst[self.current_count].add_group(self.drawing_page.label_right.HGC_latitude,
                                                       self.drawing_page.label_right.HGC_longitude)
        self.set_group_widget()
        
        # set the focus to the last element 
        self.listWidget_groupBox.item(self.drawing_lst[self.current_count].group_count - 1).setSelected(True)
        self.listWidget_groupBox.setFocus()
        
        self.set_group_toolbox()
        self.update_group_toolbox(self.drawing_lst[self.current_count].group_count - 1)
        self.drawing_page.label_right.set_img()

    def add_dipole(self):
        
        self.drawing_page.label_right.add_dipole_mode.set_opposite_value()

    def slot_surface(self):
        """
        triggered when item selection changed and surface mode is true.
        """
        if self.drawing_page.label_right.surface_mode.value:
            self.calculate_surface(self.listWidget_groupBox.currentRow())
        
    def calculate_surface(self, n):
        self.drawing_page.label_right.surface_mode.set_opposite_value()

        if self.drawing_page.label_right.surface_mode.value:
            self.drawing_page.widget_middle_up.setMaximumWidth(350)
            #self.drawing_page.widget_middle_up.setMinimumHeight(580)
        
            self.update_surface_qlabel(n)

        elif self.drawing_page.label_right.surface_mode.value == False:
            self.drawing_page.widget_middle_up.setMaximumWidth(10)
            #self.drawing_page.widget_middle_up.setMinimumHeight(580)


    def update_surface_qlabel(self, n):
        print("update surface qlabel number:", n)
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
        
        #self.drawing_page.label_middle_up = qlabel_drawing.QLabelSurfaceThreshold()
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
        

        self.drawing_page.label_right.large_grid_overlay.value = large_grid_tmp
        self.drawing_page.label_right.small_grid_overlay.value = small_grid_tmp
        self.drawing_page.label_right.group_visu.value = group_tmp
        self.drawing_page.label_right.dipole_visu.value = dipole_tmp

        self.drawing_page.label_right.set_img()
        
    def start_calibration(self):
        """
        Contains two parts:
        1. put the drawing on the center and click on the center -> signal
        2. put the drawing on the north and click on the norht -> signal
        """
        print("start calibration",
              self.drawing_page.label_right.calibration_mode.value)
        self.drawing_page.label_right.calibration_mode.value = True
        self.center_done = False
        self.north_done = False
        print("start calibration",
              self.drawing_page.label_right.calibration_mode.value,
              self.center_done, self.north_done)
        
        self.drawing_page.label_right.group_visu.value = False
        self.drawing_page.label_right.dipole_visu.value = False
        self.drawing_page.label_right.large_grid_overlay.value = False
        self.drawing_page.label_right.small_grid_overlay.value = False

        self.drawing_page.label_right.zoom_in(5.)
        
        
        height = self.drawing_page.label_right.drawing_height + self.vertical_scroll_bar.pageStep()
        width = self.drawing_page.label_right.drawing_width + self.horizontal_scroll_bar.pageStep()
        self.vertical_scroll_bar.setMaximum(height)
        self.horizontal_scroll_bar.setMaximum(width)

        #maybe a tuple instead of the list would be a better choice..
        self.approximate_center = [height/2., width/2.]
        self.set_zoom_center()
        
    def set_zoom_center(self):
        self.vertical_scroll_bar.setValue(self.approximate_center[0])
        self.horizontal_scroll_bar.setValue(self.approximate_center[1])
    
        
    def set_zoom_north(self):
        approximate_north = [0, self.approximate_center[1]]
        self.vertical_scroll_bar.setValue(approximate_north[0])
        self.horizontal_scroll_bar.setValue(approximate_north[1])

    def unzoom(self):
        self.drawing_page.label_right.zoom_in(1/5.)
        
    def slot_calibrate(self):
        """
        This is triggered when clicking on the drawing and the calibration_mode is True
        """
        if (self.drawing_page.label_right.calibration_mode.value == True and
            self.center_done == True and
            self.north_done == False):
            
            self.north_done = True
            self.get_click_coordinates()
            self.drawing_lst[self.current_count].calibrated_north_x = self.drawing_page.label_right.x_drawing
            self.drawing_lst[self.current_count].calibrated_north_y = self.drawing_page.label_right.y_drawing
            
            self.unzoom()
            self.drawing_page.label_right.large_grid_overlay.value = True
            self.drawing_page.label_right.group_visu.value = True
            self.drawing_page.label_right.set_img()
            self.drawing_page.label_right.calibration_mode.value = False
            
        elif (self.drawing_page.label_right.calibration_mode.value == True and
              self.center_done == False and
              self.north_done == False):
            
            self.get_click_coordinates()
            print("after the click", self.drawing_page.label_right.x_drawing, self.drawing_page.label_right.y_drawing)
            self.drawing_lst[self.current_count].calibrated_center_x = self.drawing_page.label_right.x_drawing
            self.drawing_lst[self.current_count].calibrated_center_y = self.drawing_page.label_right.y_drawing
            self.center_done = True
            self.set_zoom_north()
        
        """ elif self.drawing_page.label_right.calibration_mode.value == False and self.center_done == True and self.north_done == True:
        print("false, true, true")    
        self.unzoom()
        self.drawing_page.label_right.calibration_mode.value = True
        return
        """ 
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

        title_left_down = QtGui.QLabel("Group information")
        title_left_down.setAlignment(QtCore.Qt.AlignCenter)
        title_left_down.setContentsMargins(0, 5, 0, 5)
        self.drawing_page.widget_left_down_layout.addWidget(title_left_down)
        
        group_count = self.drawing_lst[self.current_count].group_count
                                         
        self.listWidget_groupBox = QtGui.QListWidget(self)
        self.listWidget_groupBox.setStyleSheet("QListView::item:selected {background : rgb(77, 185, 88);}");
        
        self.groupBoxLineList = []
        for i in range(group_count):
            self.grid_position = [0, 0]
            groupBoxLine = group_box.GroupBox()
            colorised = False
            if ((self.drawing_lst[self.current_count].group_lst[i].surface == 0) or
                (self.drawing_lst[self.current_count].group_lst[i].surface == None)):

                colorised = True
            if ((self.drawing_lst[self.current_count].group_lst[i].zurich.upper() in ["B","C","D","E","F","G"]) and
                (self.drawing_lst[self.current_count].group_lst[i].g_spot == 0)):
                colorised = True

            groupBoxLine.set_title("Group " + str(self.drawing_lst[self.current_count].group_lst[i].number),
                                   self.grid_position,colorised)           
            groupBoxLine.set_spot_count(self.drawing_lst[self.current_count].group_lst[i].spots,
                                        self.grid_position)
            groupBoxLine.set_zurich_combox_box(self.drawing_lst[self.current_count].group_lst[i].zurich,
                                         self.grid_position)
            groupBoxLine.set_mcIntosh_combo_box(self.drawing_lst[self.current_count].group_lst[i].McIntosh,
                                           self.drawing_lst[self.current_count].group_lst[i].zurich,
                                           self.grid_position)

            groupBoxLine.set_confirm_spots(self.grid_position)

            groupBoxLine.set_delete_group_button(self.grid_position)
            
            if self.drawing_lst[self.current_count].group_lst[i].zurich == "X":
                groupBoxLine.get_zurich().setStyleSheet("background-color: orange")

            #groupBoxLine.get_confirm_spots().setShortcut(QtGui.QKeySequence("Ctrl+s"))
            #print(groupBoxLine.get_zurich().currentIndex())
            groupBoxLine.get_zurich().currentIndexChanged.\
                connect(lambda: self.modify_drawing_zurich(self.listWidget_groupBox.currentRow(),False))
            groupBoxLine.get_McIntosh().currentIndexChanged.\
                connect(lambda: self.modify_drawing_mcIntosh(self.listWidget_groupBox.currentRow(),False))
            groupBoxLine.get_confirm_spots().clicked.\
                connect(lambda: self.modify_drawing_spots(self.listWidget_groupBox.currentRow(),False))
            
            
            self.groupBoxLineList.append(groupBoxLine)

            item = QtGui.QListWidgetItem(self.listWidget_groupBox)
            item.setSizeHint(groupBoxLine.sizeHint())
            self.listWidget_groupBox.setItemWidget(item, groupBoxLine)
            
        self.drawing_page.widget_left_down_layout.addWidget(self.listWidget_groupBox)

        # not sure it is still needed??
        # self.listWidget_group_toolbox.set_empty()
        #self.listWidget_group_toolbox.set_welcome()

        # first element of the list widget initially highlighted and other disabled
        # first element surface updated
        if self.listWidget_groupBox.count()>0:
            self.listWidget_groupBox.item(0).setSelected(True)
            
        self.update_surface_qlabel(0)    
        self.listWidget_groupBox.setFocus()
        
        

        for i in range(1,self.listWidget_groupBox.count()):
            self.groupBoxLineList[i].get_spots().setEnabled(False)
            self.groupBoxLineList[i].get_zurich().setEnabled(False)
            self.groupBoxLineList[i].get_McIntosh().setEnabled(False)

        # Signals related to the change of item in the group box
        self.listWidget_groupBox\
            .itemSelectionChanged\
            .connect(lambda: self.update_group_toolbox(self.listWidget_groupBox.currentRow()))
        self.listWidget_groupBox\
            .itemSelectionChanged\
            .connect(lambda: self.update_group_visu(self.listWidget_groupBox.currentRow()))
        self.listWidget_groupBox\
            .itemSelectionChanged.connect(self.disable_other_groupBoxLine)
        self.listWidget_groupBox\
            .itemSelectionChanged\
            .connect(lambda: self.update_surface_qlabel(self.listWidget_groupBox.currentRow()))
        
    def set_group_toolbox(self):
        " Set the group toolbox at the bottom of the left column."
        
        widget_separator = QtGui.QWidget()
        #Couleur #F2F1F0 est la couleur du background lightgray
        widget_separator.setStyleSheet("background-color: #F2F1F0")
        widget_separator.setMinimumHeight(10)
        widget_separator.setMaximumHeight(10)
        self.drawing_page.widget_left_down_layout.addWidget(widget_separator)
        self.group_toolbox = group_box.GroupBox()
        self.drawing_page.widget_left_down_layout.addWidget(self.group_toolbox)
        if self.listWidget_groupBox.count()>0:
            self.update_group_toolbox(0)
        
    def update_group_toolbox(self, n):
        self.grid_position = [0, 0]
        self.group_toolbox.set_empty()
        self.group_toolbox.set_title("Group " + str(self.drawing_lst[self.current_count].group_lst[n].number),
                                       self.grid_position,0)
        self.group_toolbox.set_spot_count(self.drawing_lst[self.current_count].group_lst[n].spots,
                                            self.grid_position)
        self.group_toolbox.set_zurich_combox_box(self.drawing_lst[self.current_count].group_lst[n].zurich,
                                              self.grid_position)
        self.group_toolbox.set_mcIntosh_combo_box(self.drawing_lst[self.current_count].group_lst[n].McIntosh,
                                                self.drawing_lst[self.current_count].group_lst[n].zurich,
                                                self.grid_position)
        self.group_toolbox.set_confirm_spots(self.grid_position)
        self.group_toolbox.set_latitude(self.drawing_lst[self.current_count].group_lst[n].latitude,
                                          self.grid_position)
    
        self.group_toolbox.set_longitude(self.drawing_lst[self.current_count].group_lst[n].longitude,
                                           self.grid_position)
        
        self.group_toolbox.set_surface(self.drawing_lst[self.current_count].group_lst[n].surface,
                                         self.grid_position)
        self.group_toolbox.set_arrows_buttons()
        
        if self.drawing_lst[self.current_count].group_lst[n].zurich.upper()  in ["B","C","D","E","F","G"]:
            self.group_toolbox.set_larger_spot(self.drawing_lst[self.current_count].group_lst[n].g_spot,
                                                 self.grid_position)
        else:
            self.group_toolbox.set_larger_spot(-1, self.grid_position)
            
        self.group_toolbox.set_add_surface_button()
        
        self.group_toolbox.get_confirm_spots().clicked.connect(lambda: self.modify_drawing_spots(self.listWidget_groupBox.currentRow(),True))
        self.group_toolbox.get_zurich().currentIndexChanged.connect(lambda: self.modify_drawing_zurich(self.listWidget_groupBox.currentRow(),True))
        self.group_toolbox.get_McIntosh().currentIndexChanged.connect(lambda: self.modify_drawing_mcIntosh(self.listWidget_groupBox.currentRow(),True))

        position_step = 0.1 * math.pi/180 
        up, down, left, right = self.group_toolbox.get_arrows()
        up.clicked.connect(lambda: self.update_HGC_position('latitude', position_step))
        down.clicked.connect(lambda: self.update_HGC_position('latitude', -position_step))
        left.clicked.connect(lambda: self.update_HGC_position('longitude', position_step))
        right.clicked.connect(lambda: self.update_HGC_position('longitude', -position_step))
        
        self.group_toolbox.get_confirm_spots().setShortcut(QtGui.QKeySequence("Enter"))

    def update_HGC_position(self, coordinate, value):
        print("update the position")

        if coordinate=='longitude':
            self.drawing_lst[self.current_count].group_lst[self.listWidget_groupBox.currentRow()].longitude += value
            self.group_toolbox.update_longitude(self.drawing_lst[self.current_count].group_lst[self.listWidget_groupBox.currentRow()].longitude)

        elif coordinate=='latitude':
            self.drawing_lst[self.current_count].group_lst[self.listWidget_groupBox.currentRow()].latitude += value
            self.group_toolbox.update_latitude(self.drawing_lst[self.current_count].group_lst[self.listWidget_groupBox.currentRow()].latitude)

        self.drawing_page.label_right.set_img()

        
    def disable_other_groupBoxLine(self):
        for i in range(self.listWidget_groupBox.count()):
            if (i != self.listWidget_groupBox.currentRow()):
                self.groupBoxLineList[i].get_spots().setEnabled(False)
                self.groupBoxLineList[i].get_zurich().setEnabled(False)
                self.groupBoxLineList[i].get_McIntosh().setEnabled(False)
            else:
                self.groupBoxLineList[i].get_zurich().setEnabled(True)
                self.groupBoxLineList[i].get_McIntosh().setEnabled(True)
                self.groupBoxLineList[i].get_spots().setEnabled(True)
                

    def modify_drawing_spots(self,n, is_toolbox):
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
            
        self.groupBoxLineList[n].update_zurich(self.drawing_lst[self.current_count].group_lst[n].zurich)
        self.group_toolbox.update_zurich(self.drawing_lst[self.current_count].group_lst[n].zurich)
        
        if new_zurich_type == "X":
            self.groupBoxLineList[n].get_zurich().setStyleSheet("background-color: orange")
            self.group_toolbox.get_zurich().setStyleSheet("background-color: orange")
        else:
            self.groupBoxLineList[n].get_zurich().setStyleSheet("background-color: white")
            self.group_toolbox.get_zurich().setStyleSheet("background-color: white")

    def modify_drawing_mcIntosh(self, n, is_toolbox):
        old_mcIntosh_type = self.drawing_lst[self.current_count]\
                                .group_lst[self.listWidget_groupBox.currentRow()]\
                                .McIntosh
        if is_toolbox:
            new_mcIntosh_type = str(self.group_toolbox.get_McIntosh().currentText())
        else:
            new_mcIntosh_type = str(self.groupBoxLineList[n].get_McIntosh().currentText())

        if new_mcIntosh_type!=old_mcIntosh_type:
            self.drawing_lst[self.current_count]\
                .group_lst[self.listWidget_groupBox.currentRow()]\
                .McIntosh = new_mcIntosh_type
        
        self.groupBoxLineList[n].update_McIntosh(self.drawing_lst[self.current_count].group_lst[n].McIntosh)
        self.group_toolbox.update_McIntosh(self.drawing_lst[self.current_count].group_lst[n].McIntosh)
    
        
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
        self.drawing_operator.setEnabled(False)
        self.drawing_operator.setStyleSheet("background-color: white; color:black")
        
        self.drawing_observer = QtGui.QLineEdit(self)
        self.drawing_observer.setMaximumWidth(self.column_maximum_width)
        self.drawing_observer.setEnabled(False)
        self.drawing_observer.setStyleSheet("background-color: white; color:black")
        
        self.drawing_date = QtGui.QDateEdit()
        self.drawing_date.setMaximumWidth(self.column_maximum_width)
        self.drawing_date.setDisplayFormat("dd/MM/yyyy")
        today = QtCore.QDate.currentDate()
        self.drawing_date.setDate(today)
        self.drawing_date.setEnabled(False)
        self.drawing_date.setStyleSheet("background-color: white; color:black")
        
        self.drawing_time = QtGui.QLineEdit("00:00",self)
        self.drawing_time.setMaximumWidth(self.column_maximum_width)
        self.drawing_time.setInputMask("99:99")
        self.drawing_time.setEnabled(False)
        self.drawing_time.setStyleSheet("background-color: white; color:black")
        
        #self.drawing_time.setStyleSheet("background-color: red")
        
        self.drawing_quality = QtGui.QSpinBox(self)
        self.drawing_quality.setMaximumWidth(self.column_maximum_width)
        self.drawing_quality.setMinimum(1)
        self.drawing_quality.setMaximum(5)
        self.drawing_quality.setValue(3)
        self.drawing_quality.setEnabled(False)
        self.drawing_quality.setStyleSheet("background-color: white; color:black")
        
        self.drawing_type = QtGui.QComboBox(self)
        self.drawing_type.setMaximumWidth(self.column_maximum_width)
        self.drawing_type.setEnabled(False)
        self.drawing_type.setStyleSheet("background-color: white; color:black")
        self.drawing_type.addItem('USET')
        self.drawing_type.addItem('USET77')
        self.drawing_type.addItem('USET41')
        

        self.form_layout1.addRow('Operator:', self.drawing_operator)
        self.form_layout1.addRow('Observer:', self.drawing_observer)
        self.form_layout1.addRow('Date:', self.drawing_date)
        self.form_layout1.addRow('Time:', self.drawing_time)
        self.form_layout1.addRow('Quality:', self.drawing_quality)
        self.form_layout1.addRow('Type:', self.drawing_type)
        #self.form_layout.addWidget(self.but_scan)
        #self.form_layout.addWidget(self.but_analyse)
        #self.drawing_time.textChanged.connect(self.check_valid_datetime)


        widget_form = QtGui.QWidget()
        widget_form.setMaximumWidth(self.column_maximum_width)
        widget_form.setLayout(self.form_layout1)
        #self.widget_left_up_layout.addWidget(title)
        self.drawing_page.widget_left_up_layout.addWidget(widget_form)

    def add_surface(self):
        
        qlabel_title = QtGui.QLabel("Surface calculation")
        qlabel_title.setAlignment(QtCore.Qt.AlignCenter)
        qlabel_title.setContentsMargins(0, 5, 0, 5)
        
        self.drawing_page.widget_middle_up_layout.setSpacing(10)
        qlabel_polygon = QtGui.QLabel("Selection tools:")
        selection_layout = QtGui.QHBoxLayout()
        
        self.draw_polygon_but = QtGui.QToolButton()
        self.draw_polygon_but.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.draw_polygon_but.setText("Select")
        self.draw_polygon_but.setIcon(QtGui.QIcon('icons/Darrio_Ferrando/polygon.svg'))
        
        self.crop_but = QtGui.QToolButton()
        self.crop_but.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.crop_but.setText("Crop")
        self.crop_but.setDisabled(True)
        
        self.zoom_in_but = QtGui.QToolButton()
        self.zoom_in_but.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.zoom_in_but.setText("zoom in")
        self.zoom_in_but.setIcon(QtGui.QIcon('icons/zoom-in.svg'))

        self.zoom_out_but = QtGui.QToolButton()
        self.zoom_out_but.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.zoom_out_but.setText("zoom out")
        self.zoom_out_but.setIcon(QtGui.QIcon('icons/search.svg'))

        self.reset_but = QtGui.QToolButton()
        self.reset_but.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.reset_but.setText("Reset")

        selection_layout.addWidget(self.draw_polygon_but)
        selection_layout.addWidget(self.crop_but)
        selection_layout.addWidget(self.zoom_in_but)
        selection_layout.addWidget(self.zoom_out_but)
        selection_layout.addWidget(self.reset_but)
        
        qlabel_threshold = QtGui.QLabel("Threshold:")
        self.threshold_but = QtGui.QToolButton()
        self.threshold_but.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.threshold_but.setText("threshold")
        
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
        pixel_number_linedit = QtGui.QLineEdit()
        surface_linedit = QtGui.QLineEdit()

        form_layout.addRow("Pixel Number:", pixel_number_linedit)
        form_layout.addRow("Surface:", surface_linedit)
        
        paint_layout.addWidget(self.pencil_but)
        paint_layout.addWidget(self.bucket_fill_but)
        paint_layout.addWidget(self.rubber_but)

        save_but = QtGui.QToolButton()
        save_but.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        save_but.setText("Save")
        
        calculate_but = QtGui.QToolButton()
        calculate_but.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        calculate_but.setText("Calculate")
        

        self.drawing_page.widget_middle_up_layout.addWidget(qlabel_title)
        self.drawing_page.widget_middle_up_layout.addWidget(qlabel_polygon)
        self.drawing_page.widget_middle_up_layout.addLayout(selection_layout)
        
        self.drawing_page.widget_middle_up_layout.addWidget(qlabel_threshold)
        self.drawing_page.widget_middle_up_layout.addWidget(self.threshold_but)
        # add line with default value (coming from gradient)
        self.drawing_page.widget_middle_up_layout.addWidget(self.qlabel_paint_tool)
        self.drawing_page.widget_middle_up_layout.addLayout(paint_layout)
        
        # surface :  value
        # save
        # next group
        self.drawing_page.widget_middle_up_layout.addWidget(self.drawing_page.label_middle_up)
        self.drawing_page.widget_middle_up_layout.addWidget(calculate_but)
        self.drawing_page.widget_middle_up_layout.addLayout(form_layout)
        self.drawing_page.widget_middle_up_layout.addWidget(save_but)
        
        
        self.draw_polygon_but.clicked.connect(self.draw_polygon)
        self.crop_but.clicked.connect(self.crop_method)
        self.reset_but.clicked.connect(self.reset)
                                   
        threshold_value = 225 # to be determined by a more clever way or a gradient
        self.threshold_but\
            .clicked.connect(lambda: self.threshold(threshold_value))

        self.pencil_but.clicked.connect(self.draw_pencil)
        self.bucket_fill_but.clicked.connect(self.draw_bucket)

    def crop_method(self):
        self.drawing_page.label_middle_up.crop()
        self.draw_polygon_but.setDisabled(True)
        
    def threshold(self, value):
        self.drawing_page.label_middle_up.threshold = True
        self.drawing_page.label_middle_up.polygon = False
        self.drawing_page.label_middle_up.crop_done = False
        self.drawing_page.label_middle_up.bucket = False

        self.threshold_but.setDisabled(True)
        #self.drawing_page.label_middle_up.mode_threshold.set_opposite_value()
        self.drawing_page.label_middle_up.set_img()

        if self.drawing_page.label_middle_up.crop_done :
            self.draw_polygon_but.setDisabled(True)
            self.crop_but.setDisabled(True)
            
        self.pencil_but.setEnabled(True)
        self.bucket_fill_but.setEnabled(True)
        self.rubber_but.setEnabled(True)
            
    def draw_pencil(self):
        self.drawing_page.label_middle_up.pencil = True
        self.drawing_page.label_middle_up.threshold = False
        self.drawing_page.label_middle_up.polygon = False
        self.drawing_page.label_middle_up.crop_done = False
        self.drawing_page.label_middle_up.bucket = False
    
    def draw_bucket(self):
        self.drawing_page.label_middle_up.bucket = True
        self.drawing_page.label_middle_up.threshold = False
        self.drawing_page.label_middle_up.polygon = False
        self.drawing_page.label_middle_up.crop_done = False
        self.drawing_page.label_middle_up.pencil = False
        
    def draw_polygon(self):
        print("draw polygon function")
        self.drawing_page.label_middle_up.polygon = True
        self.drawing_page.label_middle_up.threshold = False
        self.drawing_page.label_middle_up.crop_done = False
        self.drawing_page.label_middle_up.pencil = False
        self.drawing_page.label_middle_up.bucket = False
        self.crop_but.setEnabled(True)
        
        # no function here but the click on the image
        # will call set_img in the qlabel
        
        #if not self.drawing_page.label_middle_up.mode_draw_polygon.value:
        #    self.drawing_page.label_middle_up.pointsList = []

    def reset(self):
        
        self.drawing_page.label_middle_up.threshold = False
        self.drawing_page.label_middle_up.polygon = False
        self.drawing_page.label_middle_up.crop_done = False
        self.drawing_page.label_middle_up.pencil = False
        self.drawing_page.label_middle_up.bucket = False
        
        self.threshold_but.setEnabled(True)
        self.draw_polygon_but.setEnabled(True)
        self.crop_but.setEnabled(True)
        self.drawing_page.label_middle_up.reset_img()
        self.pencil_but.setDisabled(True)
        self.bucket_fill_but.setDisabled(True)
        self.rubber_but.setDisabled(True)
        self.drawing_page.label_middle_up.crop_done = False
        
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

        self.goto_drawing_button.clicked.connect(lambda: self.update_counter(int(self.goto_drawing_linedit.text())-1))
        self.goto_drawing_button.clicked.connect(lambda: self.drawing_page.label_right.set_img())

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
        self.drawing_date.setDate(QtCore.QDate(self.drawing_lst[ self.current_count].datetime.year,
                                               self.drawing_lst[ self.current_count].datetime.month,
                                               self.drawing_lst[ self.current_count].datetime.day))
        self.drawing_time.setText(str(self.drawing_lst[ self.current_count].datetime.strftime('%H')) +
                                  ":" +
                                  str(self.drawing_lst[ self.current_count].datetime.strftime('%M')))
        
        self.drawing_quality.setValue(int(self.drawing_lst[self.current_count].quality))

        index_drawing_type = self.drawing_type\
                                 .findText(self.drawing_lst[self.current_count].drawing_type)
        self.drawing_type.setCurrentIndex(index_drawing_type)

        

        print(self.drawing_lst[self.current_count].changed)
        
        if self.drawing_lst[self.current_count].changed:
            self.but_save.setStyleSheet("background-color: rgb(255, 165, 84)")
        else:
            self.but_save.setStyleSheet("background-color: lightgray")
     
    def set_path_to_qlabel(self):
        
        filename = ("usd" +
                    str(self.drawing_lst[self.current_count].datetime.year) +
                    str(self.drawing_lst[self.current_count].datetime.strftime('%m')) +
                    str(self.drawing_lst[self.current_count].datetime.strftime('%d')) +
                    str(self.drawing_lst[self.current_count].datetime.strftime('%H')) +
                    str(self.drawing_lst[self.current_count].datetime.strftime('%M')) +
                    ".jpg")
        
        directory = os.path.join("/media/archdrawings/",
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
        self.drawing_page.label_right.set_img()
        self.set_group_widget()
        self.set_group_toolbox()
        
        #self.drawing_page.label_right.show()
    
