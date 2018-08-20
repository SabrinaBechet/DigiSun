# !/usr/bin/env python
# -*-coding:utf-8-*-
import os
from PyQt4 import QtGui, QtCore
from PIL import Image
from PIL.ImageQt import ImageQt
import database, drawing
from datetime import date, time, datetime, timedelta
import coordinates
import numpy as np
import math

"""
The classes defined here contains only information related to the GUI of the drawing analyse.
Keep the analyse itself somwhere else!
"""

class GroupBox(QtGui.QWidget):
    """
    Represent the boxe associated to a group
    """
    def __init__(self):
        super(GroupBox, self).__init__()
        layout = QtGui.QVBoxLayout()
        self.grid_layout = QtGui.QGridLayout()
        #self.grid_layout.setSpacing(0)
        #self.grid_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.grid_layout)

    
    def set_title(self, title, grid_position):
        self.title_label = QtGui.QLabel(title)
        #self.title_label.setMaximumWidth(50)
        self.grid_layout.addWidget(self.title_label,
                                   grid_position[0],
                                   grid_position[1],)
        grid_position[1]+=1

    def set_spot_count(self, spot_count, grid_position):
        self.spot_number_linedit = QtGui.QLineEdit(str(spot_count),self)
        self.spot_number_linedit.setMaximumWidth(60)
        self.grid_layout.addWidget(self.spot_number_linedit,
                                   grid_position[0],
                                   grid_position[1])
        grid_position[1]+=1

    def set_zurich_type(self, zurich_type, grid_position):
        self.zurich_type = QtGui.QComboBox(self)
        self.zurich_type.setStyleSheet("color:black")
        self.zurich_type.setMaximumWidth(50)
        self.zurich_type.addItem("A")
        self.zurich_type.addItem("B")
        self.zurich_type.addItem("C")
        self.zurich_type.addItem("D")
        self.zurich_type.addItem("E")
        self.zurich_type.addItem("F")
        self.zurich_type.addItem("G")
        self.zurich_type.addItem("H")
        self.zurich_type.addItem("J")
        self.grid_layout.addWidget(self.zurich_type,
                                   grid_position[0],
                                   grid_position[1])
        grid_position[1]+=1
        index = self.zurich_type.findText(zurich_type)
        self.zurich_type.setCurrentIndex(index)

    def set_mcIntosh_type(self, mcIntosh_type, zurich_type, grid_position):
        self.McIntosh_type = QtGui.QComboBox(self)
        self.McIntosh_type.setStyleSheet("color: black")
        self.McIntosh_type.setMaximumWidth(70)
        if zurich_type=='A':
            self.McIntosh_type.addItem("Axx")
        elif zurich_type=='B':
            self.McIntosh_type.addItem("Bxo")
            self.McIntosh_type.addItem("Bxi")
            self.McIntosh_type.addItem("Bxc")
        elif zurich_type=='C':
            self.McIntosh_type.addItem("Cro")
            self.McIntosh_type.addItem("Cri")
            self.McIntosh_type.addItem("Crc")
            self.McIntosh_type.addItem("Cso")
            self.McIntosh_type.addItem("Csi")
            self.McIntosh_type.addItem("Csc")
            self.McIntosh_type.addItem("Cao")
            self.McIntosh_type.addItem("Cai")
            self.McIntosh_type.addItem("Cac")
            self.McIntosh_type.addItem("Cho")
            self.McIntosh_type.addItem("Chi")
            self.McIntosh_type.addItem("Chc")
            self.McIntosh_type.addItem("Cko")
            self.McIntosh_type.addItem("Cki")
            self.McIntosh_type.addItem("Ckc")
        elif zurich_type=='D':
            self.McIntosh_type.addItem("Dro")
            self.McIntosh_type.addItem("Dri")
            self.McIntosh_type.addItem("Drc")
            self.McIntosh_type.addItem("Dso")
            self.McIntosh_type.addItem("Dsi")
            self.McIntosh_type.addItem("Dsc")
            self.McIntosh_type.addItem("Dao")
            self.McIntosh_type.addItem("Dai")
            self.McIntosh_type.addItem("Dac")
            self.McIntosh_type.addItem("Dho")
            self.McIntosh_type.addItem("Dhi")
            self.McIntosh_type.addItem("Dhc")
            self.McIntosh_type.addItem("Dko")
            self.McIntosh_type.addItem("Dki")
            self.McIntosh_type.addItem("Dkc")
        elif zurich_type=='E':
            self.McIntosh_type.addItem("Ero")
            self.McIntosh_type.addItem("Eri")
            self.McIntosh_type.addItem("Erc")
            self.McIntosh_type.addItem("Eso")
            self.McIntosh_type.addItem("Esi")
            self.McIntosh_type.addItem("Esc")
            self.McIntosh_type.addItem("Eao")
            self.McIntosh_type.addItem("Eai")
            self.McIntosh_type.addItem("Eac")
            self.McIntosh_type.addItem("Eho")
            self.McIntosh_type.addItem("Ehi")
            self.McIntosh_type.addItem("Ehc")
            self.McIntosh_type.addItem("Eko")
            self.McIntosh_type.addItem("Eki")
            self.McIntosh_type.addItem("Ekc")
        elif zurich_type=='F':
            self.McIntosh_type.addItem("Fro")
            self.McIntosh_type.addItem("Fri")
            self.McIntosh_type.addItem("Frc")
            self.McIntosh_type.addItem("Fso")
            self.McIntosh_type.addItem("Fsi")
            self.McIntosh_type.addItem("Fsc")
            self.McIntosh_type.addItem("Fao")
            self.McIntosh_type.addItem("Fai")
            self.McIntosh_type.addItem("Fac")
            self.McIntosh_type.addItem("Fho")
            self.McIntosh_type.addItem("Fhi")
            self.McIntosh_type.addItem("Fhc")
            self.McIntosh_type.addItem("Fko")
            self.McIntosh_type.addItem("Fki")
            self.McIntosh_type.addItem("Fkc")    
        elif zurich_type=='H':
            self.McIntosh_type.addItem("Hhx")
            self.McIntosh_type.addItem("Hkx")
        elif zurich_type=='J':
            self.McIntosh_type.addItem("Hsx")
            self.McIntosh_type.addItem("Hax")   
        
        self.grid_layout.addWidget(self.McIntosh_type,
                                   grid_position[0],
                                   grid_position[1])
        grid_position[1]+=1 
        index = self.McIntosh_type.findText(mcIntosh_type)
        self.McIntosh_type.setCurrentIndex(index)
        
    def set_longitude(self, longitude, grid_position):
        grid_position[0] +=1
        self.longitude_label = QtGui.QLabel("Longitude")
        #self.longitude_label.setMaximumWidth(50)
        self.longitude_linedit = QtGui.QLineEdit(self)
        self.longitude_linedit.setText('{0:.2f}'.format(longitude))
        self.longitude_linedit.setMaximumWidth(60)
        self.grid_layout.addWidget(self.longitude_label, grid_position[0], 0)
        self.grid_layout.addWidget(self.longitude_linedit, grid_position[0], 1)

    def set_latitude(self, latitude, grid_position):
        grid_position[0]+=1
        
        self.latitude_label = QtGui.QLabel("Latitude")
        #self.latitude_label.setMaximumWidth(50)
        self.latitude_linedit = QtGui.QLineEdit(self)
        self.latitude_linedit.setText('{0:.2f}'.format(latitude))
        self.latitude_linedit.setMaximumWidth(60)
        self.grid_layout.addWidget(self.latitude_label, grid_position[0], 0)
        self.grid_layout.addWidget(self.latitude_linedit, grid_position[0], 1)

    def set_larger_spot(self, larger_spot, grid_position):
        grid_position[0]+=1
        self.larger_spot_label = QtGui.QLabel("Larger spot")
        #self.larger_spot_label.setMaximumWidth(50)
        self.larger_spot_linedit = QtGui.QLineEdit(self)
        self.larger_spot_linedit.setMaximumWidth(60)
        self.grid_layout.addWidget(self.larger_spot_label, grid_position[0], 0)
        self.grid_layout.addWidget(self.larger_spot_linedit, grid_position[0], 1)
        
        if larger_spot is None:
            self.larger_spot_linedit.setStyleSheet("background-color: rgb(255, 165, 84)")
        elif larger_spot in [1, 4, 7]:
            self.larger_spot_linedit.setText("leading")
        elif larger_spot in [2, 5, 8]:
            self.larger_spot_linedit.setText("trailing")
        elif larger_spot in [3, 6, 9]:
            self.larger_spot_linedit.setText("egal")
        elif larger_spot==0:
            self.larger_spot_linedit.setStyleSheet("background-color: rgb(255, 165, 84)")
            
    def set_surface(self, surface, grid_position):
        grid_position[0]+=1
        self.surface_label = QtGui.QLabel("Surface")
        #self.surface_label.setMaximumWidth(50)
        self.surface_linedit = QtGui.QLineEdit(self)
        self.surface_linedit.setMaximumWidth(60)
        self.grid_layout.addWidget(self.surface_label, grid_position[0], 0)
        self.grid_layout.addWidget(self.surface_linedit, grid_position[0], 1)
        
        if surface is None:
            surface = 0.
        self.surface_linedit.setText('{0:.2f}'.format(surface))
        if surface==0.:
            self.surface_linedit.setStyleSheet("background-color: rgb(255, 165, 84)")
    
    def set_empty(self):
        #Empty the layout
        for i in reversed(range(self.grid_layout.count())): 
            self.grid_layout.itemAt(i).widget().setParent(None)
        
        
    def set_welcome(self):
        label = QtGui.QLabel("Click on a group to see more informations")
        self.grid_layout.addWidget(label)

            
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
            # note: a column with the cartesian coord of group should be recorded in the db!      
            for i in range(self.current_drawing.group_count):
                radius = 25
                if self.current_drawing.group_lst[i].zurich.upper() in ["C","D","E","F","G"]:
                    radius = 40 
                painter.setPen(pen_border)
                
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
        self.widget_left_up.setMinimumWidth(300)
        self.widget_left_up.setMaximumHeight(300)
        self.widget_left_up.setStyleSheet("background-color:darkred;")   
        self.widget_left_up_layout = QtGui.QVBoxLayout()
        self.widget_left_up_layout.setContentsMargins(0, 0, 0, 0) # this line
        self.widget_left_up_layout.setSpacing(0)
        self.widget_left_up_layout.setAlignment(QtCore.Qt.AlignTop)
        self.widget_left_up.setLayout(self.widget_left_up_layout)

        self.widget_left_middle = QtGui.QWidget()
        self.widget_left_middle.setMinimumWidth(300)
        self.widget_left_middle.setMaximumHeight(200)
        self.widget_left_middle.setStyleSheet("background-color:green;")   
        self.widget_left_middle_layout = QtGui.QVBoxLayout()
        self.widget_left_middle_layout.setContentsMargins(0, 0, 0, 0) # this line
        self.widget_left_middle_layout.setSpacing(0)
        self.widget_left_middle_layout.setAlignment(QtCore.Qt.AlignTop)
        self.widget_left_middle.setLayout(self.widget_left_middle_layout)
        
        self.widget_left_down = QtGui.QWidget()
        self.widget_left_down.setMaximumWidth(300)
        self.widget_left_down.setStyleSheet("background-color:lightblue;")   
        self.widget_left_down_layout = QtGui.QVBoxLayout()
        self.widget_left_down_layout.setContentsMargins(0, 0, 0, 0) # this line
        self.widget_left_down_layout.setSpacing(0)
        self.widget_left_down_layout.setAlignment(QtCore.Qt.AlignTop and QtCore.Qt.AlignRight)
        self.widget_left_down.setLayout(self.widget_left_down_layout)
        

        
 
        self.widget_right = QtGui.QWidget()
        self.widget_right.setStyleSheet("background-color:gray;")
        self.widget_right_layout = QtGui.QVBoxLayout()
        self.widget_right_layout.setContentsMargins(0, 0, 0, 0) # this line
        self.widget_right_layout.setSpacing(0)
        self.widget_right.setLayout(self.widget_right_layout)
        self.label_right = QLabelDrawing()
        self.widget_right.layout().addWidget(self.label_right)
  
        scroll = QtGui.QScrollArea()
        scroll.setWidget(self.label_right)
        
        scroll.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        scroll.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        scroll.setWidgetResizable(True)        
        self.widget_right_layout.addWidget(scroll)
        
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
        
        toolbar.addAction(zoom_in)
        toolbar.addAction(zoom_out)
        toolbar.addAction(large_grid)
        toolbar.addAction(small_grid)
        toolbar.addAction(helper_grid)
        toolbar.addAction(sunspot_view)
        toolbar.addAction(dipole_view)
        
        zoom_in.triggered.connect(lambda : self.drawing_page.label_right.zoom_in(1.1))
        zoom_out.triggered.connect(lambda : self.drawing_page.label_right.zoom_in(1/1.1))
        
        large_grid.triggered.connect(self.set_large_grid)
        small_grid.triggered.connect(self.set_small_grid)
        sunspot_view.triggered.connect(self.set_group_visualisation)
        dipole_view.triggered.connect(self.set_dipole_visualisation)

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
        
        current_datetime = self.drawing_lst[self.current_count].datetime
        current_datetime_minus_1sec = self.drawing_lst[self.current_count]\
                                          .datetime - timedelta(seconds=1)
        
        current_datetime_plus_1sec = self.drawing_lst[self.current_count]\
                                         .datetime + timedelta(seconds=1)
        
        group_count = self.drawing_lst[self.current_count].group_count
                                         
        self.myQListWidget = QtGui.QListWidget(self)
        self.myQListWidget.setStyleSheet("QListView::item:selected {background : rgb(77, 185, 88);}");
        
        self.grid_position = [0, 0]
        
        for i in range(group_count):
            groupBoxLine = GroupBox()
            
            groupBoxLine.set_title("Group " + str(self.drawing_lst[self.current_count].group_lst[i].number),
                                       self.grid_position)
            
            groupBoxLine.set_spot_count(self.drawing_lst[self.current_count].group_lst[i].spots,
                                            self.grid_position)
            
            groupBoxLine.set_zurich_type(self.drawing_lst[self.current_count].group_lst[i].zurich,
                                             self.grid_position)
            
            groupBoxLine.set_mcIntosh_type(self.drawing_lst[self.current_count].group_lst[i].McIntosh,
                                                self.drawing_lst[self.current_count].group_lst[i].zurich,
                                                self.grid_position)
            
            
            
            myQListWidgetItem = QtGui.QListWidgetItem(self.myQListWidget)
            myQListWidgetItem.setSizeHint(groupBoxLine.sizeHint())
            
            
            self.myQListWidget.addItem(myQListWidgetItem)
            self.myQListWidget.setItemWidget(myQListWidgetItem,groupBoxLine)
            
      
        self.drawing_page.widget_left_down_layout.addWidget(self.myQListWidget)
        
        
        myQCustomQWidget = GroupBox()
        myQCustomQWidget.set_empty()
        myQCustomQWidget.set_welcome()

        self.drawing_page.widget_left_down_layout.addWidget(myQCustomQWidget)
        
    

        self.myQListWidget.itemPressed.connect(lambda: self.update_left_down_box(myQCustomQWidget,self.myQListWidget.currentRow()))
        

    def update_left_down_box(self,myQCustomQWidget,n):

        myQCustomQWidget.set_empty()
        myQCustomQWidget.set_title("Group " + str(self.drawing_lst[self.current_count].group_lst[n].number),
                                       self.grid_position)
        myQCustomQWidget.set_spot_count(self.drawing_lst[self.current_count].group_lst[n].spots,
                                            self.grid_position)
        myQCustomQWidget.set_zurich_type(self.drawing_lst[self.current_count].group_lst[n].zurich,
                                             self.grid_position)
        myQCustomQWidget.set_mcIntosh_type(self.drawing_lst[self.current_count].group_lst[n].McIntosh,
                                                self.drawing_lst[self.current_count].group_lst[n].zurich,
                                                self.grid_position)
        myQCustomQWidget.set_latitude(self.drawing_lst[self.current_count].group_lst[n].latitude,
                                          self.grid_position)
        myQCustomQWidget.set_longitude(self.drawing_lst[self.current_count].group_lst[n].longitude,
                                           self.grid_position)
        myQCustomQWidget.set_surface(self.drawing_lst[self.current_count].group_lst[n].surface,
                                         self.grid_position)
        if self.drawing_lst[self.current_count].group_lst[n].zurich.upper()  in ["B","C","D","E","F","G"]:
            myQCustomQWidget.set_larger_spot(self.drawing_lst[self.current_count].group_lst[n].g_spot,
                                                 self.grid_position)
        



        
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
        self.show_drawing()
        self.set_group_widget()
        #print("current count:", self.current_count)
       
    def set_drawing_lst(self, drawing_lst):
        """
        Get the list of drawings from bulk analysis page.
        Set the counter to 0.
        """
        #print("*********set  a new list")
        self.drawing_lst = drawing_lst
        self.len_drawing_lst = len(drawing_lst)
        #print(self.len_drawing_lst)
        self.current_count = 0
        if len(drawing_lst)>1:
            self.but_next.setEnabled(True)
            self.but_previous.setEnabled(True)
        else:
            self.but_next.setDisabled(True)
            self.but_previous.setDisabled(True)
        self.set_drawing_lineEdit()

        #print("counter:", self.current_count)
        
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
        
        #print("show drawing", self.current_count)
        self.set_path_to_qlabel()
        self.drawing_page.label_right.current_drawing = self.drawing_lst[self.current_count]
        self.drawing_page.label_right.set_img()
        #self.drawing_page.label_right.show()
        
