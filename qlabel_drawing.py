# !/usr/bin/env python
# -*-coding:utf-8-*-
from PyQt4 import QtGui, QtCore
from PIL import Image
from PIL.ImageQt import ImageQt
import numpy as np
import math
import coordinates
import cv2
import numpy as np
import time
import sys

sys.setrecursionlimit(100000)

def radian_between_zero_pi(radian):

        #if radian > 0 and radian < math.pi:
        norm_radian = radian
        if radian > 2*math.pi:
            norm_radian = radian % 2*math.pi
        elif radian<0:
            norm_radian = math.pi - math.fabs(norm_radian)
            
        return norm_radian
    
class analyseModeBool(QtCore.QObject):
    """
    This represents the mode of the analysis.
    
    There are 5 viewing modes wich are overlays:
    - large grid
    - small grid
    - helper grid
    - group visualisation
    - dipole visualisation
    
    There a 4 action modes:
    - calibrate 
    - add group
    - add dipole
      * input parameter: group number! works only for a given group
    - calculate the surface
      * input parameter: group number! works only for a given group
    """

    value_changed = QtCore.pyqtSignal()
    
    def __init__(self, input_value='False'):
        super(analyseModeBool, self).__init__()
        self._value = input_value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, input_value):
        #print("**the value of the mode has changed to ", input_value)
        self._value = input_value
        self.value_changed.emit()
        
    def set_opposite_value(self):
        if self._value==True:
            self._value=False
            self.value_changed.emit()
        else:
            self._value=True
            self.value_changed.emit()

class QLabelSurfaceThreshold(QtGui.QLabel):

    mouse_pressed = QtCore.pyqtSignal()
    
    def __init__(self):
        super(QLabelSurfaceThreshold, self).__init__()
        self.setFrameShape(QtGui.QFrame.Panel)
        self.setFrameShadow(QtGui.QFrame.Plain)
        self.setLineWidth(3)
        
        self.original_pixmap = QtGui.QPixmap() # used for the reset
        self.threshold_pixmap = QtGui.QPixmap()
        self.first_pixamp_polygon = QtGui.QPixmap() # used for the polygon drawing

        self.width_scale = 300
        self.height_scale = 300

        self.pointsList  =[]
        
        self.is_drawing = False
        self.to_fill = False

        """self.mode_draw_polygon = analyseModeBool(False)
        self.mode_threshold = analyseModeBool(False)
        self.mode_pencil = analyseModeBool(False)
        self.mode_bucket_fill = analyseModeBool(False)
        self.mode_rubber = analyseModeBool(False)
        self.first_view = analyseModeBool(True)
        """

        self.threshold = False
        self.polygon = False
        self.crop_done = False
        self.pencil = False
        self.bucket = False
        
        
        self.painter = QtGui.QPainter()
        self.pen = QtGui.QPen(QtCore.Qt.red)
        self.pen.setWidth(5)
        
    def convertQImageToMat(self, incomingImage):
        '''  Converts a QImage into an opencv MAT format  '''

        incomingImage = incomingImage.convertToFormat(4)
        width = incomingImage.width()
        height = incomingImage.height()

        ptr = incomingImage.bits()
        ptr.setsize(incomingImage.byteCount())
        arr = np.array(ptr).reshape(height, width, 4)  #  Copies the data
        return arr

    def np2qpixmap(self, np_img):
        frame = cv2.cvtColor(np_img, cv2.COLOR_BGR2RGB)
        img = QtGui.QImage(frame, frame.shape[1], frame.shape[0], QtGui.QImage.Format_RGB888)
        return QtGui.QPixmap.fromImage(img)


    def set_threshold_img(self, threshold_value):

        print("enter the threshold function")
        qimage = self.pixmap().toImage()
        pixel_matrix = self.convertQImageToMat(qimage)
        print(type(pixel_matrix), pixel_matrix.size)
        pixMat_int8 = ((pixel_matrix * 255.) / pixel_matrix.max()).astype(np.uint8)
        thresh_value , pixel_matrix_thresh = cv2.threshold(pixMat_int8, threshold_value, 256, cv2.THRESH_BINARY_INV)
        self.threshold_pixmap = self.np2qpixmap(pixel_matrix_thresh).copy()
        self.setPixmap(self.threshold_pixmap)
        print("exit the threshold function")
        self.threshold = False
        
    def reset_img(self):
        """
        Reset the img to its origin pixmap
        """
        self.pointsList = []
        self.setPixmap(self.original_pixmap)
        
    
    def draw_polygon(self):
        self.pointsList.append(self.position)
        
        print("enter the draw polygon", len(self.pointsList))
        
        
        if len(self.pointsList) == 1:
            print("set the pixmap polygon", len(self.pointsList))
            self.first_pixamp_polygon = self.pixmap().copy()

        self.setPixmap(self.first_pixamp_polygon)    
        self.painter.begin(self.pixmap())
            
        
        pen_polygon = QtGui.QPen(QtCore.Qt.cyan)
        pen_polygon.setWidth(3)
        self.painter.setPen(pen_polygon)
        if len(self.pointsList) == 1:
            self.painter.drawPoint(self.pointsList[-1])
            
        else:
            for i in range(len(self.pointsList)):
                self.painter.drawLine(self.pointsList[i-1],self.pointsList[i])
        self.painter.end()

        self.update()
        
        #self.setPixmap(self.pixmap())

    def draw_pencil(self):
        self.painter.begin(self.pixmap())
        self.painter.setPen(self.pen)
        self.painter.setBrush(QtCore.Qt.cyan)
        self.painter.drawPoint(self.position)
            
    def set_img(self):
        """
        Set the image in the surface calculation widget.
        It the input pixamp is None, then use the previous pixmap in memory (self.pixmap())

        If draw_polygon : select a region around the interesting group (for an ulterior crop)
        If pencil : begin the painter for the drawing line (and rubber if color is white)
        - allow to select a region for a later crop
        """
        print("**** set img", self.threshold, self.polygon, self.pencil, self.bucket)
        
        #if pixmap is not None:
        #    self.setPixmap(pixmap)
        # check if pixmap is None and self.pixmap is emppty -> message!!

        #mode de depart quand on lance image pour la premiere fois
        #if not self.mode_draw_polygon.value and not self.mode_threshold.value:
        #    self.original_pixmap = pixmap.copy()
            
        """self.painter.begin(self.pixmap())
        pen_polygon = QtGui.QPen(QtCore.Qt.red)
        pen_polygon.setWidth(10000)
        self.painter.setPen(pen_polygon)
        self.painter.end()
        """
        #if self.first_view:

        
        if self.threshold :
            self.set_threshold_img(225)
            
        if self.polygon :
            self.draw_polygon()

        if self.pencil:
             self.draw_pencil()

        if self.bucket:
             self.bucket_fill()   
        
       
        self.show()
        #self.first_view.value = False
        
    def bucket_fill(self):
        x = self.position.x()
        y = self.position.y()
        image = self.pixmap().toImage()
        array_image = self.convertQImageToMat(image)
        array_image = self.iter_fill(x,y,array_image)
        newPixmap = self.np2qpixmap(array_image)
        self.setPixmap(newPixmap)


    def iter_fill(self,x_start,y_start,array):
        stack = [(x_start,y_start)]
        #C1, C2 and C3 are the colors in RGB that the pixel need to be in
        #If the pen is white, then the pixels are turned black (0,0,0), otherwise they are turned red (0,0,255)
        if self.pen.color() == QtCore.Qt.black:
            c1 = 0
            c2 = 0
            c3 = 0
        else:
            c1 = 0
            c2 = 0
            c3 = 255
        while stack:
            x, y, stack = stack[0][0], stack[0][1], stack[1:]
            if not self.check_color(x,y,array,c1,c2,c3):
                array[y][x][0] = c1
                array[y][x][1] = c2
                array[y][x][2] = c3
                if x > 0:
                    stack.append((x - 1, y))
                if x < (len(array[y])-1):
                    stack.append((x + 1, y))
                if y > 0:
                    stack.append((x, y - 1))
                if y < (len(array)-1):
                    stack.append((x, y + 1))
        return array

    def modify_rubber_color(self):
        if(self.pen.color() == QtCore.Qt.red):
            self.pen.setColor(QtCore.Qt.black)
        else:
            self.pen.setColor(QtCore.Qt.red)


    def check_color(self,x,y,array,c1,c2,c3):
        return(array[y][x][0] == c1 and array[y][x][1] == c2 and array[y][x][2] == c3)


    def mousePressEvent(self,QMouseEvent):
        self.position = QMouseEvent.pos()
        if self.polygon or self.pencil or self.bucket :
            self.set_img()
            
    def mouseMoveEvent(self,QMouseEvent):
            
        if self.pencil:
            self.painter.drawPoint(QMouseEvent.pos())
            self.setPixmap(self.pixmap())
    
    def mouseReleaseEvent(self,QMouseEvent):
        
        if self.pencil:
            print("enter in the mouse release and painter end")
            self.painter.end()
        
    def crop(self):
        left = None
        right = None
        up = None
        down = None
        for i in range(len(self.pointsList)):
            if left == None or self.pointsList[i].x() < left:
                left = self.pointsList[i].x()
            if right == None or self.pointsList[i].x() > right:
                right = self.pointsList[i].x()
            if up == None or self.pointsList[i].y() < up:
                up = self.pointsList[i].y()
            if down == None or self.pointsList[i].y() > down:
                down = self.pointsList[i].y()
                
        new_pixmap = self.pixmap().copy(left,up,right-left,down-up)
        new_pixmap = new_pixmap.scaled(300, 300, QtCore.Qt.KeepAspectRatio)
    
        self.setPixmap(new_pixmap)
        self.crop_done = True
    
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

       # overlay mode
       self.large_grid_overlay = analyseModeBool(True)
       self.small_grid_overlay = analyseModeBool(False)
       self.group_visu = analyseModeBool(True)
       self.dipole_visu = analyseModeBool(False)
       
       #action mode
       self.calibration_mode = analyseModeBool(False)
       self.add_group_mode = analyseModeBool(False)
       self.add_dipole_mode = analyseModeBool(False)
       self.surface_mode = analyseModeBool(False)

       self.group_visu_index = 0

    def set_img(self):
            
        img = Image.open(self.file_path)

        self.drawing_width = img.size[0]
        self.drawing_height = img.size[1]
        print("!img size: ", img.size)
        
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

        if self.large_grid_overlay.value or self.small_grid_overlay.value:
                
            painter.setPen(QtGui.QPen(QtCore.Qt.red))    
            painter.setPen(pen_border)
            painter.drawEllipse(QtCore.QPointF(self.current_drawing.calibrated_center.x,
                                               self.current_drawing.calibrated_center.y),
                                self.current_drawing.calibrated_radius,
                                self.current_drawing.calibrated_radius)
                       
            if self.large_grid_overlay.value:
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
            
        if self.group_visu.value :
            #print(self.group_visu_index)
            # note: a column with the cartesian coord of group should be recorded in the db!
            pen_selected = QtGui.QPen(QtCore.Qt.green)
            pen_selected.setWidth(5)
            
            for i in range(self.current_drawing.group_count):
                radius = 10
                #if self.current_drawing.group_lst[i].zurich.upper() in ["C","D","E","F","G"]:
                #    radius = 40
                    
                painter.setPen(pen_border)
                
                if self.group_visu_index==i:
                    painter.setPen(pen_selected)
                    
                x, y, x_up, y_up = self.get_cartesian_coordinate_from_HGC(self.current_drawing.group_lst[i].longitude,
                                                              self.current_drawing.group_lst[i].latitude)


               
                print("draw group ", x, y)
                painter.drawEllipse(QtCore.QPointF(x, y), radius, radius)
                
        if self.dipole_visu.value :
            # note: a column with the cartesian coord of group should be recorded in the db!      
            for i in range(self.current_drawing.group_count):

                pen_point = QtGui.QPen(QtCore.Qt.red)
                pen_point.setWidth(10)
                pen_line = QtGui.QPen(QtCore.Qt.red)
                pen_line.setWidth(5)
               
                dip1_x, dip1_y, tst, tst2 = self.get_cartesian_coordinate_from_HGC(self.current_drawing.group_lst[i].dipole1_long,
                                                                        self.current_drawing.group_lst[i].dipole1_lat)
                dip2_x, dip2_y, tst, tst2 = self.get_cartesian_coordinate_from_HGC(self.current_drawing.group_lst[i].dipole2_long,
                                                                        self.current_drawing.group_lst[i].dipole2_lat)
                painter.setPen(pen_point)
                painter.drawPoints(QtCore.QPointF(dip1_x,dip1_y), QtCore.QPointF(dip2_x,dip2_y) )
                painter.setPen(pen_line)
                painter.drawLine(dip1_x, dip1_y, dip2_x, dip2_y)

                
        painter.end()
        self.setPixmap(self.drawing_pixMap.scaled(int(self.width_scale),
                                                  int(self.height_scale),
                                                  QtCore.Qt.KeepAspectRatio))
        

        #self.show()

    
    
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
                                                                   self.drawing_height - self.current_drawing.calibrated_center.y,
                                                                   self.current_drawing.calibrated_north.x,
                                                                   self.drawing_height - self.current_drawing.calibrated_north.y,
                                                                   longitude,
                                                                   latitude,
                                                                   self.current_drawing.angle_P,
                                                                   self.current_drawing.angle_B,
                                                                   self.current_drawing.angle_L)


       
        
        (x_upper_left_origin2,
         y_upper_left_origin2,
         z_upper_left_origin2) = coordinates.cartesian_from_drawing_method2(self.current_drawing.calibrated_center.x,
                                                                   self.drawing_height - self.current_drawing.calibrated_center.y,
                                                                   self.current_drawing.calibrated_north.x,
                                                                   self.drawing_height - self.current_drawing.calibrated_north.y,
                                                                   longitude,
                                                                   latitude,
                                                                   self.current_drawing.angle_P,
                                                                   self.current_drawing.angle_B,
                                                                   self.current_drawing.angle_L)
        
        """print("THE check")
        print(self.current_drawing.calibrated_center.x + x_upper_left_origin,
              self.current_drawing.calibrated_center.y - y_upper_left_origin,
              z_upper_left_origin)
        print(self.current_drawing.calibrated_center.x + x_upper_left_origin2,
              self.current_drawing.calibrated_center.y - y_upper_left_origin2,
              z_upper_left_origin2) 
        """
        x_centered_lower_left_origin = self.current_drawing.calibrated_center.x + x_upper_left_origin
        y_centered_lower_left_origin = self.current_drawing.calibrated_center.y - y_upper_left_origin

        x_centered_upper_left_origin = self.current_drawing.calibrated_center.x + x_upper_left_origin
        y_centered_upper_left_origin = self.current_drawing.calibrated_center.y + y_upper_left_origin

        lon, lat = coordinates.heliographic_from_drawing(self.current_drawing.calibrated_center.x,
                                                         self.drawing_height - self.current_drawing.calibrated_center.y,
                                                         self.current_drawing.calibrated_north.x,
                                                         self.drawing_height - self.current_drawing.calibrated_north.y,
                                                         x_centered_lower_left_origin,
                                                         self.drawing_height - y_centered_lower_left_origin,
                                                         self.current_drawing.angle_P,
                                                         self.current_drawing.angle_B,
                                                         self.current_drawing.angle_L)


        """print("**check")
        print(self.current_drawing.calibrated_center.x,
              self.drawing_height - self.current_drawing.calibrated_center.y,
              self.current_drawing.calibrated_north.x,
              self.drawing_height - self.current_drawing.calibrated_north.y,
              x_centered_lower_left_origin,
              self.drawing_height - y_centered_lower_left_origin,
              self.current_drawing.angle_P,
              self.current_drawing.angle_B,
              self.current_drawing.angle_L)
        
        print("***************")
        print("long, lat", radian_between_zero_pi(longitude), latitude)
        print("x, y", x_centered_lower_left_origin, y_centered_lower_left_origin)
        print("long, lat", radian_between_zero_pi(lon), lat)
        """
        return x_centered_lower_left_origin, y_centered_lower_left_origin,   x_centered_upper_left_origin, y_centered_upper_left_origin

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
        print("drawing coord lower left origin:", x_drawing, self.drawing_height - y_drawing)
        print("drawing coord of the center:",
              self.current_drawing.calibrated_center.x,
              self.current_drawing.calibrated_center.y)
        
        #print("**radius", self.radius)
        #print("pixmap coord centered: ", x_pixmap_centered, y_pixmap_centered)
        #print("x center pixmap", x_center_pixmap)
        
        #print("P, B, L", (self.angle_P, self.angle_B, self.angle_L))
        
        center_x_lower_left_origin = self.current_drawing.calibrated_center.x
        center_y_lower_left_origin = self.drawing_height - self.current_drawing.calibrated_center.y
        north_x_lower_left_origin = self.current_drawing.calibrated_north.x
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

        
        self.HGC_longitude = longitude
        self.HGC_latitude = latitude
        print("longitude: ", longitude)
        print("latitude: ", latitude)
        
        if self.calibration_mode.value or self.add_group_mode.value:
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
    
