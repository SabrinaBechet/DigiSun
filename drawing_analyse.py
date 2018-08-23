# !/usr/bin/env python
# -*-coding:utf-8-*-
import os
from PyQt4 import QtGui, QtCore
from PIL import Image
from PIL.ImageQt import ImageQt
import database, drawing, group_box
from datetime import date, time, datetime, timedelta
import coordinates
import numpy as np
import math

"""
The classes defined here contains only information related to the GUI of the drawing analyse.
Keep the analyse itself somwhere else!
- QLabelDrawing : represent the drawing
- DrawingViewPage : the template of the DrawingViewPage
- DrawingAnalysePage: the page itself with all the widgets
"""

class QLabelDrawing(QtGui.QLabel):
    """
    Class to show the drawing, 
    display the grid, groups, dipoles, etc
    and interact with it
    It contains:
    - text (in case no pixmap)
    - drawing_pixMap : the pixamp with no scaling
    - width_scale : the width of the image to show (depending on the zoom)
    - height_scale : the height of the image to show (depending on the zoom)

    note: properties make functions look like attribute
    """
    def __init__(self):
       super(QLabelDrawing, self).__init__()
       my_font = QtGui.QFont("Comic Sans MS", 20)
       self.setText('No drawings corresponding to this entry')
       self.setFont(my_font)
       self.setAlignment(QtCore.Qt.AlignCenter)
       self.setContentsMargins(0, 0, 0, 0)
       #self.setMinimumWidth(300)
       self.width_scale = 1000
       self.height_scale = 1000
 
       self.large_grid_overlay = True
       self.small_grid_overlay = False
       self.group_visu = True
       self.dipole_visu = False

       self.group_visu_index = 0
       
    def set_img(self):
        
        img = Image.open(self.file_path)
        qim = ImageQt(img) #convert PIL image to a PIL.ImageQt object
        self.drawing_pixMap = QtGui.QPixmap.fromImage(qim)

        pen_grid = QtGui.QPen(QtCore.Qt.blue)
        pen_grid.setWidth(3)
        pen_grid.setStyle(QtCore.Qt.DotLine)
        
        pen_border = QtGui.QPen(QtCore.Qt.blue)
        # the width should depend on the dpi/size of the drawing
        pen_border.setWidth(3)
        pen_border.setStyle(QtCore.Qt.SolidLine)
        
        pen_special_line =  QtGui.QPen(QtCore.Qt.magenta)
        pen_special_line.setWidth(5)
        pen_special_line.setStyle(QtCore.Qt.SolidLine)

        painter = QtGui.QPainter()
        painter.begin(self.drawing_pixMap)

        if self.large_grid_overlay or self.small_grid_overlay:
                
            painter.setPen(QtGui.QPen(QtCore.Qt.red))    
            painter.setPen(pen_border)
            painter.drawEllipse(QtCore.QPointF(self.current_drawing.calibrated_center.x,
                                               self.current_drawing.calibrated_center.y),
                                self.current_drawing.calibrated_radius,
                                self.current_drawing.calibrated_radius)
                       
            if self.large_grid_overlay:
                angle_array = np.arange(-180, 190, 30)
            else :
                angle_array = np.arange(-180, 190, 10)
                angle_array = np.append(angle_array, [270])
                           
            for latitude in angle_array:
                if latitude == 0 :
                    painter.setPen(pen_special_line)
                else:
                    painter.setPen(pen_grid)

                x_lst, y_lst = self.draw_line_on_sphere(latitude,
                                                        self.current_drawing.calibrated_radius,
                                                        "longitude")
                for i in range(len(x_lst)):
                    painter.drawPoint(self.current_drawing.calibrated_center.x + x_lst[i],
                                      self.current_drawing.calibrated_center.y + y_lst[i])

            for longitude in angle_array:
                if longitude == 0 :                
                    painter.setPen(pen_special_line)
                else:
                    painter.setPen(pen_grid)

                x_lst, y_lst = self.draw_line_on_sphere(longitude,
                                                        self.current_drawing.calibrated_radius,
                                                        "latitude")
                
                for i in range(len(x_lst)):
                    painter.drawPoint(self.current_drawing.calibrated_center.x + x_lst[i],
                                      self.current_drawing.calibrated_center.y + y_lst[i])    
            
        if self.group_visu :
            #print(self.group_visu_index)
            # note: a column with the cartesian coord of group should be recorded in the db!
            pen_selected = QtGui.QPen(QtCore.Qt.green)
            pen_selected.setWidth(3)
            
            for i in range(self.current_drawing.group_count):
                radius = 25
                if self.current_drawing.group_lst[i].zurich.upper() in ["C","D","E","F","G"]:
                    radius = 40
                    
                painter.setPen(pen_border)
                
                if self.group_visu_index==i:
                    painter.setPen(pen_selected)
                    
                x, y = self.get_cartesian_coordinate_from_HGC(self.current_drawing.group_lst[i].longitude,
                                                              self.current_drawing.group_lst[i].latitude)
                painter.drawEllipse(QtCore.QPointF(x, y), radius, radius)
                
        if self.dipole_visu :
            # note: a column with the cartesian coord of group should be recorded in the db!      
            for i in range(self.current_drawing.group_count):

                pen_point = QtGui.QPen(QtCore.Qt.red)
                pen_point.setWidth(10)
                pen_line = QtGui.QPen(QtCore.Qt.red)
                pen_line.setWidth(5)
               
                dip1_x, dip1_y = self.get_cartesian_coordinate_from_HGC(self.current_drawing.group_lst[i].dipole1_long,
                                                                        self.current_drawing.group_lst[i].dipole1_lat)
                dip2_x, dip2_y = self.get_cartesian_coordinate_from_HGC(self.current_drawing.group_lst[i].dipole2_long,
                                                                        self.current_drawing.group_lst[i].dipole2_lat)
                painter.setPen(pen_point)
                painter.drawPoints(QtCore.QPointF(dip1_x,dip1_y), QtCore.QPointF(dip2_x,dip2_y) )
                painter.setPen(pen_line)
                painter.drawLine(dip1_x, dip1_y, dip2_x, dip2_y)

                
        painter.end()
        self.setPixmap(self.drawing_pixMap.scaled(int(self.width_scale),
                                                  int(self.height_scale),
                                                  QtCore.Qt.KeepAspectRatio))
        self.drawing_width = img.size[0]
        self.drawing_height = img.size[1]
        print("img size: ", img.size)

        self.show()


    def get_cartesian_coordinate_from_HGC(self, longitude, latitude):
        """
        get the cartesian coordinate suitable for Qpainter (origin upper left)
        from the given heliographic latitude/longitude (for group or dipole).
        NB: starting from the center(!!)
        x_lower_left_origin = x_upper_left_origin while
        y_lower_left_origin = - y_upper_left_origin
        """
        (x_upper_left_origin,
         y_upper_left_origin,
         z_upper_left_origin) = coordinates.cartesian_from_drawing(self.current_drawing.calibrated_center.x,
                                                                   self.current_drawing.calibrated_center.y,
                                                                   self.current_drawing.calibrated_north.x,
                                                                   self.current_drawing.calibrated_north.y,
                                                                   longitude,
                                                                   latitude,
                                                                   self.current_drawing.angle_P,
                                                                   self.current_drawing.angle_B,
                                                                   self.current_drawing.angle_L)

        x_centered_lower_left_origin = self.current_drawing.calibrated_center.x + x_upper_left_origin
        y_centered_lower_left_origin = self.current_drawing.calibrated_center.y - y_upper_left_origin

        return x_centered_lower_left_origin, y_centered_lower_left_origin 

    def get_spherical_coord_latitude(self, longitude, radius):
        spherical_coord_lst = []
        for latitude in range(-180,180, 1):    
            spherical_coord =  coordinates.Spherical(radius,
                                                      math.pi/2 - latitude * math.pi/180.,
                                                      longitude * math.pi/180.)
            spherical_coord_lst.append(spherical_coord)
        return spherical_coord_lst

    def get_spherical_coord_longitude(self, latitude, radius):
        spherical_coord_lst = []
        for longitude in range(-180,180, 1):    
            spherical_coord =  coordinates.Spherical(radius,
                                                      math.pi/2 - latitude * math.pi/180.,
                                                      longitude * math.pi/180.)
            spherical_coord_lst.append(spherical_coord)
        return spherical_coord_lst
    
    def draw_line_on_sphere(self, angle, radius, line):
        x_arr = np.array([])
        y_arr = np.array([])

        if line=='latitude':
            spherical_coord_lst = self.get_spherical_coord_latitude(angle, radius)
        elif line=='longitude':
            spherical_coord_lst = self.get_spherical_coord_longitude(angle, radius)
            
        for spherical_coord in spherical_coord_lst:
            x, y, z = spherical_coord.convert_to_cartesian()
            cart_coord = coordinates.Cartesian(x, y, z)
            cart_coord.rotate_around_y(self.current_drawing.angle_L)
            cart_coord.rotate_around_z(self.current_drawing.angle_P)
            cart_coord.rotate_around_x(self.current_drawing.angle_B)
            
            if cart_coord.z>0:
                x_arr = np.append(x_arr, [cart_coord.x])
                y_arr = np.append(y_arr, [cart_coord.y])
             
        return x_arr, y_arr 

    def draw_longitude_line(self, latitude, radius):
        x_arr = np.array([])
        y_arr = np.array([])
        
        for longitude in range(-180, 180, 1):
            
            spherical_coord =  coordinates.Spherical(radius,
                                                     math.pi/2 - latitude * math.pi/180.,
                                                     longitude * math.pi/180.)
            
            x, y, z = spherical_coord.convert_to_cartesian()
            cart_coord = coordinates.Cartesian(x, y, z)
            cart_coord.rotate_around_y(self.current_drawing.angle_L)
            cart_coord.rotate_around_z(self.current_drawing.angle_P)
            cart_coord.rotate_around_x(self.current_drawing.angle_B)
            
            if cart_coord.z>0:
                x_arr = np.append(x_arr, [cart_coord.x])
                y_arr = np.append(y_arr, [cart_coord.y])
            
        return x_arr, y_arr 

    
    def zoom_in(self, scaling_factor):
       
        self.width_scale *=  scaling_factor
        self.height_scale *=  scaling_factor
        #print("zoom in", self.width_scale, self.height_scale)
        self.set_img()   

    def mousePressEvent(self, QMouseEvent):
        """ Associate a  mousePress event to a signal if the coordinate
        of the click position (QtGui.QMouseEvent.x, QtGui.QMouseEvent.y)
        corresponds to a line in the rectangle.
        """
        x_click = QMouseEvent.x()
        y_click = QMouseEvent.y()

        self.get_pixmap_coordinate_range()
        
        init_width = 1000 # without any zoom
        init_height = 1000 # without any zoom
        pixmap_width = init_width / self.width_scale # is 1 without any zoom
        pixmap_height = init_height / self.height_scale # is 1 without any zoom

        # change of coordinate system: qlabel -> pixmap
        x_pixmap = (x_click - self.pixmap_x_min) * pixmap_width 
        y_pixmap = (y_click - self.pixmap_y_min) * pixmap_height
 
        #change of coordinaet system: qlabel -> drawing
        x_drawing = (x_click - self.pixmap_x_min) * self.drawing_width / self.pixmap().width()
        y_drawing = (y_click - self.pixmap_y_min) * self.drawing_height / self.pixmap().height()
  
        x_center_drawing = ((self.current_drawing.calibrated_center.x -
                            self.pixmap_x_min) * self.drawing_width /
                            self.pixmap().width())
        y_center_drawing = ((self.current_drawing.calibrated_center.y -
                            self.pixmap_y_min) * self.drawing_height /
                            self.pixmap().height())
        
        print("click coordinate: ", x_click, y_click)
        print("pixmap coord: ", x_pixmap, y_pixmap)
        print("drawing coord:", x_drawing, y_drawing)
        print("drawing coord of the center:",
              self.current_drawing.calibrated_center.x,
              self.current_drawing.calibrated_center.y)
        
        #print("**radius", self.radius)
        #print("pixmap coord centered: ", x_pixmap_centered, y_pixmap_centered)
        #print("x center pixmap", x_center_pixmap)
        
        #print("P, B, L", (self.angle_P, self.angle_B, self.angle_L))

        center_x_lower_left_origin = self.current_drawing.calibrated_center.x
        center_y_lower_left_origin = self.drawing_height - self.current_drawing.calibrated_center.y
        north_x_lower_left_origin = self.current_drawing.calibrated_north.y
        north_y_lower_left_origin = self.drawing_height - self.current_drawing.calibrated_north.y
        drawing_x_lower_left_origin = x_drawing
        drawing_y_lower_left_origin = self.drawing_height - y_drawing
        longitude, latitude = coordinates.heliographic_from_drawing(center_x_lower_left_origin,
                                                                    center_y_lower_left_origin,
                                                                    north_x_lower_left_origin,
                                                                    north_y_lower_left_origin,
                                                                    drawing_x_lower_left_origin,
                                                                    drawing_y_lower_left_origin,
                                                                    self.current_drawing.angle_P,
                                                                    self.current_drawing.angle_B,
                                                                    self.current_drawing.angle_L)
        #print("longitude: ", longitude)
        #print("latitude: ", latitude)
        
    def get_pixmap_coordinate_range(self):
        """
        get the pixmap minimum and maximum coordinate values
        in qlabel referential.
        """
        qlabel_width = self.width()
        qlabel_height = self.height()
        self.qlabel_x_center = qlabel_width/2.
        self.qlabel_y_center = qlabel_height/2.
        
        self.pixmap_x_min = self.qlabel_x_center - self.pixmap().width()/2.
        self.pixmap_x_max = self.qlabel_x_center + self.pixmap().width()/2.
        self.pixmap_y_min = self.qlabel_y_center - self.pixmap().height()/2.
        self.pixmap_y_max = self.qlabel_y_center + self.pixmap().height()/2.

        #return self.pixmap_x_min, self.pixmap_x_max, self.pixmap_y_min, self.pixmap_y_max
    
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
        self.widget_left_up.setMinimumWidth(350)
        self.widget_left_up.setMaximumHeight(300)
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
        self.label_right = QLabelDrawing()
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
        add_group_action = QtGui.QAction('add group', toolbar)
        add_dipole_action = QtGui.QAction('add dipole', toolbar)
        surface_action = QtGui.QAction('surface', toolbar)
        
        toolbar.addAction(zoom_in)
        toolbar.addAction(zoom_out)
        toolbar.addAction(large_grid)
        toolbar.addAction(small_grid)
        toolbar.addAction(helper_grid)
        toolbar.addAction(sunspot_view)
        toolbar.addAction(dipole_view)

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

        calibrate_action.triggered.connect(self.calibrate)

    def calibrate(self):
        self.drawing_page.label_right.group_visu = False
        self.drawing_page.label_right.large_grid_overlay = False

        self.drawing_page.label_right.zoom_in(5.)
        vertical_scroll_bar = self.drawing_page.scroll.verticalScrollBar()
        horizontal_scroll_bar = self.drawing_page.scroll.horizontalScrollBar()
        height = self.drawing_page.label_right.drawing_height + vertical_scroll_bar.pageStep()
        width = self.drawing_page.label_right.drawing_width + horizontal_scroll_bar.pageStep()
        print(width/2., height/2.)
        vertical_scroll_bar.setMaximum(height)
        vertical_scroll_bar.setValue(height/2.)
        horizontal_scroll_bar.setMaximum(width)
        horizontal_scroll_bar.setValue(width/2.)
        
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

            groupBoxLine.set_delete_group_button(self.grid_position)
            


            #print(groupBoxLine.get_zurich().currentIndex())
            groupBoxLine.get_zurich().currentIndexChanged.connect(lambda : self.update_other_box(self.groupBoxLineList[self.listWidget_groupBox.currentRow()].get_zurich().currentIndex()))
            
            
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
        self.group_toolbox.get_zurich().setCurrentIndex(self.groupBoxLineList[n].get_zurich().currentIndex())
        self.group_toolbox.set_mcIntosh_type(self.drawing_lst[self.current_count].group_lst[n].McIntosh,
                                                self.drawing_lst[self.current_count].group_lst[n].zurich,
                                                self.grid_position)
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

        
        self.group_toolbox.get_zurich().currentIndexChanged.connect(lambda : self.update_other_box(self.group_toolbox.get_zurich().currentIndex()))

    
    def disable_other_lines(self):
        for i in range(self.listWidget_groupBox.count()):
            if (i != self.listWidget_groupBox.currentRow()):
                self.groupBoxLineList[i].get_spots().setEnabled(False)
                self.groupBoxLineList[i].get_zurich().setEnabled(False)
                self.groupBoxLineList[i].get_McIntosh().setEnabled(False)
            else:
                self.groupBoxLineList[i].get_spots().setEnabled(True)
                self.groupBoxLineList[i].get_zurich().setEnabled(True)
                self.groupBoxLineList[i].get_McIntosh().setEnabled(True)
        
    def update_groupBoxLineList(self,n):
        pass
    
    def modifyDrawing(self,n):
        pass
        
    def update_other_box(self,zurich):
        self.groupBoxLineList[self.listWidget_groupBox.currentRow()].get_zurich().setCurrentIndex(zurich)
        self.group_toolbox.get_zurich().setCurrentIndex(zurich)
        
        #self.listWidget_groupBox.currentItem().get_zurich().setCurrentText(1)
        """left_bottom_box = self.group_toolbox.findChild()
        index = self.group_toolbox.findText(zurich, QtCore.Qt.MatchFixedString)
        if index >= 0:
            listWidget_group_toolbox.setCurrentIndex(index)
            self.listWidget_groupBox.zurich_type.setCurrentIndex(index)"""
        
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
        #self.drawing_operator.setDisabled(True)
        self.drawing_observer = QtGui.QLineEdit(self)
        self.drawing_observer.setMaximumWidth(self.column_maximum_width)
        #self.drawing_observer.setDisabled(True)
        self.drawing_date = QtGui.QDateEdit()
        self.drawing_date.setMaximumWidth(self.column_maximum_width)
        self.drawing_date.setDisplayFormat("dd/MM/yyyy")
        today = QtCore.QDate.currentDate()
        self.drawing_date.setDate(today)
        #self.drawing_date.setDisabled(True)
        self.drawing_time = QtGui.QLineEdit("00:00",self)
        self.drawing_time.setMaximumWidth(self.column_maximum_width)
        self.drawing_time.setInputMask("99:99")
        #self.drawing_time.setDisabled(True)
        #self.drawing_time.setStyleSheet("background-color: red")
        
        self.drawing_quality = QtGui.QSpinBox(self)
        self.drawing_quality.setMaximumWidth(self.column_maximum_width)
        self.drawing_quality.setMinimum(1)
        self.drawing_quality.setMaximum(5)
        self.drawing_quality.setValue(3)
        #self.drawing_quality.setDisabled(True)
        self.drawing_type = QtGui.QComboBox(self)
        self.drawing_type.setMaximumWidth(self.column_maximum_width)
        self.drawing_type.setStyleSheet("color:black")
        self.drawing_type.addItem('USET')
        self.drawing_type.addItem('USET77')
        self.drawing_type.addItem('USET41')
        #self.drawing_type.setDisabled(True)

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
    
