# !/usr/bin/env python
# -*-coding:utf-8-*-
from PyQt4 import QtGui, QtCore
from PIL import Image
from PIL.ImageQt import ImageQt
import numpy as np
import math
import coordinates

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

    """
    A signal (specifically an unbound signal) is an attribute of a class that is a sub-class of QObject. 
    When a signal is referenced as an attribute of an instance of the class then PyQt5 automatically 
    binds the instance to the signal in order to create a bound signal.
    """
    drawing_clicked = QtCore.pyqtSignal()
    
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

       # viewing mode
       self.large_grid_overlay = True
       self.small_grid_overlay = False
       self.group_visu = True
       self.dipole_visu = False

       #action mode
       self.calibration_mode = False
       self.add_group_mode = False
       self.add_dipole_mode = False
        
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

        self.x_drawing = x_drawing
        self.y_drawing = y_drawing
        
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
        
        if self.calibration_mode:
            print("*******emit signal!!")
            self.drawing_clicked.emit()
        
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
    
