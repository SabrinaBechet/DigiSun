# !/usr/bin/env python
# -*-coding:utf-8-*-
import os
from PyQt4 import QtGui, QtCore

import database, drawing, group_box, qlabel_drawing
from datetime import date, time, datetime, timedelta

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
        self.widget_left_down.setMinimumHeight(620)
        self.widget_left_down.setStyleSheet("background-color:lightblue;")   
        self.widget_left_down_layout = QtGui.QVBoxLayout()
        self.widget_left_down_layout.setContentsMargins(0, 0, 0, 0) 
        self.widget_left_down_layout.setSpacing(0)
        self.widget_left_down_layout.setAlignment(QtCore.Qt.AlignTop and QtCore.Qt.AlignRight)
        self.widget_left_down.setLayout(self.widget_left_down_layout)
        
        self.widget_right = QtGui.QWidget()
        self.widget_right.setStyleSheet("background-color:gray;")
        self.widget_right_layout = QtGui.QVBoxLayout()
        self.widget_right_layout.setContentsMargins(0, 0, 0, 0) 
        self.widget_right_layout.setSpacing(0)
        self.widget_right.setLayout(self.widget_right_layout)
        self.label_right = qlabel_drawing.QLabelDrawing()
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
        

        splitter_left = QtGui.QSplitter(QtCore.Qt.Vertical, self)
        self.layout().addWidget(splitter_left)
        splitter_left.addWidget(splitter_middle_down)
        splitter_left.addWidget(self.widget_left_down)
        
        splitter_main = QtGui.QSplitter(QtCore.Qt.Horizontal, self)
        self.layout().addWidget(splitter_main)
        splitter_main.addWidget(splitter_left)
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
        self.setCentralWidget(self.drawing_page)
        
        self.operator = operator

        self.column_maximum_width = 600
        self.add_drawing_information()
        self.add_current_session()
        self.drawing_lst = []
        self.set_toolbar()
        self.calibration_done = False
        self.drawing_page.label_right.drawing_clicked.connect(self.calibrate_signal)
        
        self.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)

    def set_toolbar(self):
        """Note : The QToolBar class inherit from QWidget.
        """

        toolbar = self.addToolBar("view")
        toolbar.setIconSize(QtCore.QSize(30, 30));

        # icons come from here: https://www.flaticon.com
        zoom_in = QtGui.QAction('zoom_in', toolbar)
        zoom_in.setIcon(QtGui.QIcon('icons/zoom-in.svg'))
        zoom_out = QtGui.QAction('zoom_out',  toolbar)
        zoom_out.setIcon(QtGui.QIcon('icons/search.svg'))
        large_grid = QtGui.QAction('large_grid',  toolbar)
        large_grid.setIcon(QtGui.QIcon('icons/internet.svg'))
        small_grid = QtGui.QAction('small_grid',  toolbar)
        small_grid.setIcon(QtGui.QIcon('icons/internet.svg'))
        helper_grid = QtGui.QAction('helper_grid',  toolbar)
        helper_grid.setIcon(QtGui.QIcon('icons/internet.svg'))
        sunspot_view = QtGui.QAction('sunspot_view',  toolbar)
        sunspot_view.setIcon(QtGui.QIcon('icons/share_1.svg'))
        dipole_view = QtGui.QAction('dipole_view',  toolbar)
        dipole_view.setIcon(QtGui.QIcon('icons/share.svg'))

        # mettre une barre pour separer les differents views/actions

        calibrate_action = QtGui.QAction('calibrate', toolbar)
        calibrate_action.setIcon(QtGui.QIcon('icons/target.svg'))
        add_group_action = QtGui.QAction('add group', toolbar)
        add_group_action.setIcon(QtGui.QIcon('icons/hospital.svg'))
        add_dipole_action = QtGui.QAction('add dipole', toolbar)
        add_dipole_action.setIcon(QtGui.QIcon('icons/weight.svg'))
        surface_action = QtGui.QAction('surface', toolbar)
        surface_action.setIcon(QtGui.QIcon('icons/layout.svg'))
        
        toolbar.addAction(zoom_in)
        toolbar.addAction(zoom_out)
        toolbar.addAction(large_grid)
        toolbar.addAction(small_grid)
        toolbar.addAction(helper_grid)
        toolbar.addAction(sunspot_view)
        toolbar.addAction(dipole_view)
        toolbar.insertSeparator(calibrate_action)
        toolbar.addAction(calibrate_action)
        toolbar.addAction(add_group_action)
        toolbar.addAction(add_dipole_action)
        toolbar.addAction(surface_action)
        
        zoom_in.triggered.connect(lambda : self.drawing_page.label_right.zoom_in(1.1))
        zoom_out.triggered.connect(lambda : self.drawing_page.label_right.zoom_in(1/1.1))
        
        large_grid.triggered.connect(self.set_large_grid)
        small_grid.triggered.connect(self.set_small_grid)
        sunspot_view.triggered.connect(self.set_group_visualisation)
        dipole_view.triggered.connect(self.set_dipole_visualisation)

        calibrate_action.triggered.connect(self.start_calibration)

    def start_calibration(self):
        """
        Contains two parts:
        1. put the drawing on the center and click on the center -> signal
        2. put the drawing on the north and click on the norht -> signal
        """
        print("start calibration", self.calibration_done)
        self.calibration_done = False
        self.center_done = False
        self.north_done = False
        print("start calibration", self.calibration_done, self.center_done, self.north_done)
        
        self.drawing_page.label_right.group_visu = False
        self.drawing_page.label_right.large_grid_overlay = False

        self.drawing_page.label_right.zoom_in(5.)
        
        self.vertical_scroll_bar = self.drawing_page.scroll.verticalScrollBar()
        self.horizontal_scroll_bar = self.drawing_page.scroll.horizontalScrollBar()
        height = self.drawing_page.label_right.drawing_height + self.vertical_scroll_bar.pageStep()
        width = self.drawing_page.label_right.drawing_width + self.horizontal_scroll_bar.pageStep()
        self.vertical_scroll_bar.setMaximum(height)
        self.horizontal_scroll_bar.setMaximum(width)

        #maybe a tuple instead of the list would be a better choice..
        self.approximate_center = [height/2., width/2.]
        self.set_zoom_center()
        

    def set_zoom_center(self):
        #print("first step calibrate center", self.calibration_done, self.center_done, self.north_done)
        self.vertical_scroll_bar.setValue(self.approximate_center[0])
        self.horizontal_scroll_bar.setValue(self.approximate_center[1])
        #self.drawing_page.label_right.drawing_clicked.connect(self.get_click_coordinates)
        
    def set_zoom_north(self):
        #print("second step calibrate north", self.calibration_done, self.center_done, self.north_done)
        approximate_north = [0, self.approximate_center[1]]
        self.vertical_scroll_bar.setValue(approximate_north[0])
        self.horizontal_scroll_bar.setValue(approximate_north[1])

    def unzoom(self):
        #print("enter in the dezoom", self.calibration_done, self.center_done, self.north_done)
        if self.calibration_done == False:
            self.drawing_page.label_right.zoom_in(1/5.)
        
    def calibrate_signal(self):
        print("** calibrate_signal", self.calibration_done, self.center_done, self.north_done)
        if self.calibration_done == False and self.center_done == True and self.north_done == False:
            print("false, true, false")
            self.north_done = True
            self.get_click_coordinates()
            self.unzoom()
            self.drawing_page.label_right.large_grid_overlay = True
            self.drawing_page.label_right.group_visu = True
            self.drawing_page.label_right.set_img()
            
        elif self.calibration_done == False and self.center_done == False and self.north_done == False:
            print("false, false, false")
            self.get_click_coordinates()
            self.center_done = True
            self.set_zoom_north()
        
        """ elif self.calibration_done == False and self.center_done == True and self.north_done == True:
        print("false, true, true")    
        self.unzoom()
        self.calibration_done = True
        return
        """ 
    def get_click_coordinates(self):
        print("get click coordinate")
        print(self.drawing_page.label_right.x_drawing)
        print(self.drawing_page.label_right.y_drawing)
        
    def set_group_visualisation(self):
        if self.drawing_page.label_right.group_visu==True:
            self.drawing_page.label_right.group_visu = False
            self.show_drawing()
        elif self.drawing_page.label_right.group_visu==False:
            self.drawing_page.label_right.group_visu = True
            self.show_drawing()

    def set_dipole_visualisation(self):
        if self.drawing_page.label_right.dipole_visu==True:
            self.drawing_page.label_right.dipole_visu = False
            self.show_drawing()
        elif self.drawing_page.label_right.dipole_visu==False:
            self.drawing_page.label_right.dipole_visu = True
            self.show_drawing()
        
    def set_large_grid(self):
        if self.drawing_page.label_right.large_grid_overlay==True:
            self.drawing_page.label_right.large_grid_overlay = False
            self.show_drawing()
        elif self.drawing_page.label_right.large_grid_overlay==False:
            self.drawing_page.label_right.large_grid_overlay = True
            self.drawing_page.label_right.small_grid_overlay = False
            self.show_drawing()

    def set_small_grid(self):
        if self.drawing_page.label_right.small_grid_overlay==True:
            self.drawing_page.label_right.small_grid_overlay = False
            self.show_drawing()
        elif self.drawing_page.label_right.small_grid_overlay==False:
            self.drawing_page.label_right.small_grid_overlay = True
            self.drawing_page.label_right.large_grid_overlay = False
            self.show_drawing()
            
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
            groupBoxLine.set_zurich_type(self.drawing_lst[self.current_count].group_lst[i].zurich,
                                         self.grid_position)
            groupBoxLine.set_mcIntosh_type(self.drawing_lst[self.current_count].group_lst[i].McIntosh,
                                           self.drawing_lst[self.current_count].group_lst[i].zurich,
                                           self.grid_position)

            groupBoxLine.set_confirm_spots(self.grid_position)

            groupBoxLine.set_delete_group_button(self.grid_position)
            

            


            #print(groupBoxLine.get_zurich().currentIndex())
            groupBoxLine.get_zurich().currentIndexChanged.connect(lambda: self.modifyDrawingZurich(self.listWidget_groupBox.currentRow(),False))
            groupBoxLine.get_McIntosh().currentIndexChanged.connect(lambda: self.modifyDrawingMcIntosh(self.listWidget_groupBox.currentRow(),False))
            groupBoxLine.get_confirm_spots().clicked.connect(lambda: self.modifyDrawingSpots(self.listWidget_groupBox.currentRow(),False))
            
            
            self.groupBoxLineList.append(groupBoxLine)

            item = QtGui.QListWidgetItem(self.listWidget_groupBox)
            item.setSizeHint(groupBoxLine.sizeHint())
            self.listWidget_groupBox.setItemWidget(item, groupBoxLine)
            
        self.drawing_page.widget_left_down_layout.addWidget(self.listWidget_groupBox)

        # not sure it is still needed??
        #self.listWidget_group_toolbox.set_empty()
        #self.listWidget_group_toolbox.set_welcome()

        # first element of the list widget initially highlighted and other disabled
        if self.listWidget_groupBox.count()>0:
            self.listWidget_groupBox.item(0).setSelected(True)
        self.listWidget_groupBox.setFocus()


        for i in range(1,self.listWidget_groupBox.count()):
            self.groupBoxLineList[i].get_spots().setEnabled(False)
            self.groupBoxLineList[i].get_zurich().setEnabled(False)
            self.groupBoxLineList[i].get_McIntosh().setEnabled(False)


        self.listWidget_groupBox\
            .itemSelectionChanged\
            .connect(lambda:self.update_group_toolbox(self.listWidget_groupBox.currentRow()))
        self.listWidget_groupBox\
            .itemSelectionChanged\
            .connect(lambda: self.update_group_visu(self.listWidget_groupBox.currentRow()))
        self.listWidget_groupBox.itemSelectionChanged.connect(lambda: self.disable_other_lines())
        
    def set_group_toolbox(self):
        " Set the group toolbox at the bottom of the left column."
        self.group_toolbox = group_box.GroupBox()
        self.drawing_page.widget_left_down_layout.addWidget(self.group_toolbox)
        if self.listWidget_groupBox.count()>0:
            self.update_group_toolbox(0)
        
         
    def update_group_toolbox(self,n):
        self.grid_position = [0, 0]
        self.group_toolbox.set_empty()
        self.group_toolbox.set_title("Group " + str(self.drawing_lst[self.current_count].group_lst[n].number),
                                       self.grid_position,0)
        self.group_toolbox.set_spot_count(self.drawing_lst[self.current_count].group_lst[n].spots,
                                            self.grid_position)
        self.group_toolbox.set_zurich_type(self.drawing_lst[self.current_count].group_lst[n].zurich,
                                              self.grid_position)
        self.group_toolbox.set_mcIntosh_type(self.drawing_lst[self.current_count].group_lst[n].McIntosh,
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
        



        self.group_toolbox.get_confirm_spots().clicked.connect(lambda: self.modifyDrawingSpots(self.listWidget_groupBox.currentRow(),True))
        self.group_toolbox.get_zurich().currentIndexChanged.connect(lambda: self.modifyDrawingZurich(self.listWidget_groupBox.currentRow(),True))
        self.group_toolbox.get_McIntosh().currentIndexChanged.connect(lambda: self.modifyDrawingMcIntosh(self.listWidget_groupBox.currentRow(),True))
        
        arrows_list = self.group_toolbox.get_arrows()
        arrows_list[0].clicked.connect(lambda: self.modify_longitude_latitude(False, True))
        arrows_list[1].clicked.connect(lambda: self.modify_longitude_latitude(False, False))
        arrows_list[2].clicked.connect(lambda: self.modify_longitude_latitude(True, True))
        arrows_list[3].clicked.connect(lambda: self.modify_longitude_latitude(True, False))
        
    
    def modify_longitude_latitude(self,longitude,positive):
        #Longitude is a boolean and is True if we need to modify the longitude (or false if we need to modify the latitude)
        #Positive is a boolean and is True if we need to +1 (or False if we need to -1)
        if positive:
            toAdd = 0.00174532925
        else:
            toAdd = -0.00174532925
        
        if longitude:
            self.drawing_lst[self.current_count].group_lst[self.listWidget_groupBox.currentRow()].longitude += toAdd
            self.group_toolbox.update_longitude(self.drawing_lst[self.current_count].group_lst[self.listWidget_groupBox.currentRow()].longitude)
        else:
            self.drawing_lst[self.current_count].group_lst[self.listWidget_groupBox.currentRow()].latitude += toAdd
            self.group_toolbox.update_latitude(self.drawing_lst[self.current_count].group_lst[self.listWidget_groupBox.currentRow()].latitude)
        
        self.drawing_page.label_right.set_img()


    def disable_other_lines(self):
        for i in range(self.listWidget_groupBox.count()):
            if (i != self.listWidget_groupBox.currentRow()):
                self.groupBoxLineList[i].get_spots().setEnabled(False)
                self.groupBoxLineList[i].get_zurich().setEnabled(False)
                self.groupBoxLineList[i].get_McIntosh().setEnabled(False)
            else:
                self.groupBoxLineList[i].get_zurich().setEnabled(True)
                self.groupBoxLineList[i].get_McIntosh().setEnabled(True)
                self.groupBoxLineList[i].get_spots().setEnabled(True)



    def modifyDrawingSpots(self,n,is_toolbox):
        print("SpotsSaved")
        if is_toolbox:
            self.drawing_lst[self.current_count].group_lst[self.listWidget_groupBox.currentRow()].spots = self.group_toolbox.get_spots().text()
        else:
            self.drawing_lst[self.current_count].group_lst[self.listWidget_groupBox.currentRow()].spots = self.groupBoxLineList[n].get_spots().text()
        self.groupBoxLineList[n].update_spots(self.drawing_lst[self.current_count].group_lst[n].spots)
        self.group_toolbox.update_spots(self.drawing_lst[self.current_count].group_lst[n].spots)

    def modifyDrawingZurich(self,n,is_toolbox):
        if is_toolbox:
            self.drawing_lst[self.current_count].group_lst[self.listWidget_groupBox.currentRow()].zurich = str(self.group_toolbox.get_zurich().currentText())
        else:
            self.drawing_lst[self.current_count].group_lst[self.listWidget_groupBox.currentRow()].zurich = str(self.groupBoxLineList[n].get_zurich().currentText())
        self.groupBoxLineList[n].update_zurich(self.drawing_lst[self.current_count].group_lst[n].zurich)
        self.group_toolbox.update_zurich(self.drawing_lst[self.current_count].group_lst[n].zurich)

    def modifyDrawingMcIntosh(self,n,is_toolbox):
        if is_toolbox:
            self.drawing_lst[self.current_count].group_lst[self.listWidget_groupBox.currentRow()].McIntosh = str(self.group_toolbox.get_McIntosh().currentText())
        else:
            self.drawing_lst[self.current_count].group_lst[self.listWidget_groupBox.currentRow()].McIntosh = str(self.groupBoxLineList[n].get_McIntosh().currentText())
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
        
    def add_current_session(self):
        
        form_layout2 = QtGui.QFormLayout()
        form_layout2.setSpacing(15)

        title_left_middle = QtGui.QLabel("Current session")
        title_left_middle.setAlignment(QtCore.Qt.AlignCenter)
        title_left_middle.setContentsMargins(0, 5, 0, 5)
        self.drawing_page.widget_left_middle_layout.addWidget(title_left_middle)
        
        self.current_operator = QtGui.QLineEdit(str(self.operator).upper(), self)
        self.current_operator.setMaximumWidth(self.column_maximum_width)
        
        self.but_previous = QtGui.QPushButton('previous', self)
        self.but_previous.setShortcut(QtGui.QKeySequence("Left"))
        self.but_next = QtGui.QPushButton('next', self)
        self.but_next.setShortcut(QtGui.QKeySequence("Right"))

        self.but_next.clicked.connect(lambda: self.update_counter(1))
        self.but_next.clicked.connect(self.show_drawing)
        self.but_previous.clicked.connect(lambda: self.update_counter(-1))
        self.but_previous.clicked.connect(self.show_drawing)

        layout_but = QtGui.QHBoxLayout()
        layout_but.addWidget(self.but_previous)
        layout_but.addWidget(self.but_next)

        self.but_save = QtGui.QPushButton('save', self)
        self.but_save.setMaximumWidth(self.column_maximum_width + 75)
        #self.but_save.clicked.connect(lambda: self.show_drawing())

        form_layout2.addRow("Current operator: ", self.current_operator)
        form_layout2.setLayout(1,
                               QtGui.QFormLayout.SpanningRole,
                               layout_but)
        
        form_layout2.setWidget(2,
                               QtGui.QFormLayout.SpanningRole,
                               self.but_save)

        
        self.drawing_page.widget_left_middle_layout.addLayout(form_layout2)

       
    def update_counter(self, value_to_add):
        self.current_count += value_to_add
        if self.current_count >= self.len_drawing_lst:
            self.current_count = self.len_drawing_lst-1
        elif self.current_count < 0:
            self.current_count = 0
        
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
       
       
    def set_drawing_lst(self, drawing_lst):
        """
        Get the list of drawings from bulk analysis page.
        Set the counter to 0.
        """
        self.drawing_lst = drawing_lst
        self.len_drawing_lst = len(drawing_lst)
        
        self.current_count = 0
        if len(drawing_lst)>1:
            self.but_next.setEnabled(True)
            self.but_previous.setEnabled(True)
        else:
            self.but_next.setDisabled(True)
            self.but_previous.setDisabled(True)
        self.set_drawing_lineEdit()
  
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

            
    def show_drawing(self):
        print("show drawing")
        self.set_path_to_qlabel()
        self.drawing_page.label_right.current_drawing = self.drawing_lst[self.current_count]
        self.drawing_page.label_right.group_visu_index = 0
        self.set_group_widget()
        self.set_group_toolbox()
        self.drawing_page.label_right.set_img()
        #self.drawing_page.label_right.show()
    
