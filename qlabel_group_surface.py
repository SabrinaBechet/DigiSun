# !/usr/bin/env python
# -*-coding:utf-8-*-
from PyQt5 import QtGui, QtCore, QtWidgets
from PIL import Image
from PIL.ImageQt import ImageQt
import numpy as np
import math
import coordinates
import cv2
import numpy as np
import time
import sys
import analyse_mode_bool
#import matplotlib.path as mpltPath
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon

sys.setrecursionlimit(100000) # check where it is exactly used...

class GroupSurfaceWidget(QtWidgets.QWidget):

    bigger_frame = QtCore.pyqtSignal()
    smaller_frame = QtCore.pyqtSignal()
    
    def __init__(self):
         super(GroupSurfaceWidget, self).__init__()
         self.layout = QtWidgets.QVBoxLayout()
         self.layout.setSpacing(15)
         self.setLayout(self.layout)

         self.radius_division_factor = 400

         self.scroll = QtWidgets.QScrollArea()
         self.scroll\
             .setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
         self.scroll\
             .setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
         self.scroll.setWidgetResizable(True)
         
         self.qlabel_group_surface = QLabelGroupSurface()
         self.qlabel_group_surface.setAlignment(QtCore.Qt.AlignTop and
                                                QtCore.Qt.AlignLeft)
         #self.qlabel_group_surface.setMinimumSize(300,300)
         self.scroll.setWidget(self.qlabel_group_surface)

         self.radius = 0
         self.start_x = 0
         self.start_y = 0
         self.center_x = 0
         self.center_y = 0
         
         qlabel_title = QtWidgets.QLabel("Surface calculation")
         qlabel_title.setAlignment(QtCore.Qt.AlignCenter)
         qlabel_title.setContentsMargins(0, 5, 0, 5)
         
         threshold_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
         threshold_slider.setRange(0,256)
         threshold_slider.setTickPosition(QtWidgets.QSlider.TicksBelow)
        
         self.default_threshold = 225
         threshold_slider.setValue(self.default_threshold)
         threshold_slider.valueChanged.connect(
             lambda: self.update_img_threshold_value(threshold_slider.value()))
         self.threshold_linedit = QtWidgets.QLineEdit(str(self.default_threshold))

         threshold_layout = QtWidgets.QFormLayout()
         threshold_layout.addRow("Threshold selection:",
                            self.threshold_linedit)
         
         qlabel_general = QtWidgets.QLabel("General tools:")
         
         zoom_in_but =QtWidgets.QToolButton()
         zoom_in_but.setIcon(QtGui.QIcon('icons/Smashicons/zoom-in.svg'))
         zoom_in_but.clicked.connect(
             lambda: self.qlabel_group_surface.zoom_in(2.))

         zoom_out_but = QtWidgets.QToolButton()
         zoom_out_but.setIcon(QtGui.QIcon('icons/Smashicons/search.svg'))
         zoom_out_but.clicked.connect(
             lambda: self.qlabel_group_surface.zoom_in(1/2.))

         reset_but = QtWidgets.QToolButton()
         reset_but.setText("reset")
         reset_but.setIcon(QtGui.QIcon('icons/Pixel_perfect/settings.svg'))
         reset_but.clicked.connect(
             lambda: self.update_img_threshold_value(threshold_slider.value()))

         undo_but = QtWidgets.QToolButton()
         undo_but.setIcon(QtGui.QIcon('icons/Eleonor_Wang/undo.svg'))
         
         bigger_frame_but =QtWidgets.QToolButton()
         bigger_frame_but.setIcon(
             QtGui.QIcon('icons/Linh_Pham/mine_bigger_frame.png'))
         bigger_frame_but.clicked.connect(
             lambda: self.bigger_frame.emit())
  
         smaller_frame_but =QtWidgets.QToolButton()
         smaller_frame_but.setIcon(
             QtGui.QIcon('icons/Linh_Pham/mine_smaller_frame.png'))
         smaller_frame_but.clicked.connect(
             lambda: self.smaller_frame.emit())
  
         draw_polygon_but = QtWidgets.QToolButton()
         draw_polygon_but.setIcon(
             QtGui.QIcon('icons/Darrio_Ferrando/polygon.svg'))
         draw_polygon_but.clicked.connect(
             self.qlabel_group_surface.draw_polygon)
         
         cut_polygon_but = QtWidgets.QToolButton()
         cut_polygon_but.setIcon(
             QtGui.QIcon('icons/Freepik/crop.svg'))
         cut_polygon_but.clicked.connect(
             lambda : self.cut_polygon(threshold_slider.value()))

         draw_1pixel_black_but = QtWidgets.QToolButton()
         draw_1pixel_black_but.setIcon(
             QtGui.QIcon('icons/Freepik/1pix_black_square.svg'))
         draw_1pixel_black_but.clicked.connect(lambda: self.draw_pencil(0))

         draw_1pixel_white_but = QtWidgets.QToolButton()
         draw_1pixel_white_but.setIcon(
             QtGui.QIcon('icons/Freepik/1pix_white_square.svg'))
         draw_1pixel_white_but.clicked.connect(lambda: self.draw_pencil(255))
         
         bucket_white_fill_but = QtWidgets.QToolButton()
         bucket_white_fill_but.setIcon(
             QtGui.QIcon('icons/Freepik/white-bucket.svg'))
         bucket_white_fill_but.clicked.connect(
             lambda : self.qlabel_group_surface.set_bucket_fill(self.current_array,
                                                                0,
                                                                255))
         bucket_black_fill_but = QtWidgets.QToolButton()
         bucket_black_fill_but.setIcon(
             QtGui.QIcon('icons/Freepik/black-bucket.svg'))
         bucket_black_fill_but.clicked.connect(
             lambda : self.qlabel_group_surface.set_bucket_fill(self.current_array,
                                                                255,
                                                                0))
         

         """cross_but = QtWidgets.QToolButton()
         cross_but.setMinimumWidth(self.width()/6.)
         cross_but.clicked.connect(lambda: self.draw_pencil(255))

         pixel_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
         pixel_slider.setRange(1,5)
         pixel_slider.setTickPosition(QtWidgets.QSlider.TicksBelow)
         pixel_slider.setValue(1)
         """
         
         layout_general = QtWidgets.QGridLayout()
         layout_general.addWidget(qlabel_general, 0, 0, 1, -1)
         layout_general.addWidget(zoom_in_but, 1, 0)
         layout_general.addWidget(zoom_out_but, 1, 1)
         layout_general.addWidget(undo_but, 1, 2)
         layout_general.addWidget(reset_but, 1, 3)
         layout_general.addWidget(bigger_frame_but, 1, 4)
         layout_general.addWidget(smaller_frame_but, 1, 5)
         layout_general.addWidget(draw_polygon_but, 1, 6)
         layout_general.addWidget(cut_polygon_but, 1, 7)
         layout_general.addWidget(bucket_white_fill_but, 2, 0)
         layout_general.addWidget(bucket_black_fill_but, 2, 1)
         layout_general.addWidget(draw_1pixel_white_but, 2, 2)
         layout_general.addWidget(draw_1pixel_black_but, 2, 3)
         
         """layout_general.addWidget(cross_but, 7, 0)
         layout_general.addWidget(pixel_slider, 7, 1)
         """
         form_layout = QtWidgets.QFormLayout()
         self.pixel_number_linedit = QtWidgets.QLineEdit()
         self.projected_surface_linedit = QtWidgets.QLineEdit()
         self.deprojected_surface_linedit = QtWidgets.QLineEdit()
         
         form_layout.addRow("Pixel Number:",
                            self.pixel_number_linedit)
         form_layout.addRow("Projected surface (msd):",
                            self.projected_surface_linedit)
         form_layout.addRow("Deprojected surface (msh):",
                            self.deprojected_surface_linedit)

         save_but = QtWidgets.QPushButton("save")
         
         self.layout.addWidget(qlabel_title)
         self.layout.addLayout(threshold_layout)
         self.layout.addWidget(threshold_slider)
         self.layout.addLayout(layout_general)
         
         self.layout.addWidget(self.scroll)
         self.layout.addLayout(form_layout)
         self.layout.addWidget(save_but)
         
         self.qlabel_group_surface.array_changed.connect(
             lambda: self.set_img(self.qlabel_group_surface.array))

         
    def draw_pencil(self, new_value):
        self.qlabel_group_surface.set_pencil_array(self.current_array, new_value)
        
         
    def cut_polygon(self, value):
        cut_array = self.qlabel_group_surface.cut_polygon(self.current_array)
        self.set_img(cut_array)
         
    def update_img_threshold_value(self, value):
        self.qlabel_group_surface.polygon.value = False
        self.qlabel_group_surface.pencil.value = False
        self.qlabel_group_surface.bucket.value = False

        self.default_threshold = value
        new_selection_thresh = self.threshold(value)
        self.threshold_linedit.setText(str(value))
        self.set_img(new_selection_thresh)
        self.qlabel_group_surface.pointsList = []

    def set_array(self, np_array):
        self.selection_array = np_array
        self.set_img(self.threshold(self.default_threshold))
        self.qlabel_group_surface.pointsList = []

    def threshold(self, value):
        #print("do the threshold for a value of ", value)
        thresh_value , selection_array_thresh = cv2.threshold(self.selection_array,
                                                              value,
                                                              256,
                                                              cv2.THRESH_BINARY_INV)
            
        return selection_array_thresh
    
    def set_img(self, img):
        self.current_array = img
        self.qlabel_group_surface.set_original_img(img)
        nb_pixel = self.count_pixel(img)
        projected_area = self.projected_area_calculation(nb_pixel)
        deprojected_area = self.deprojected_area_calculation(img)
        self.pixel_number_linedit.setText(str(nb_pixel))
        self.projected_surface_linedit.setText('{0:.2f}'.format(projected_area))
        self.deprojected_surface_linedit.setText('{0:.2f}'.format(deprojected_area))
        
    def count_pixel(self, img):
        return np.count_nonzero(img)

    def set_info(self, radius, start_x, start_y, center_x, center_y):
        print("set info")
        print(radius, start_x, start_y, center_x, center_y)
        self.radius = radius
        self.start_x = start_x
        self.start_y = start_y
        self.center_x = center_x
        self.center_y = center_y

    def deprojected_area_calculation(self, img):
        print("**** check the deprojected area calculation")
        print("start value ", self.start_x, self.start_y)
        if self.radius:
            index_x, index_y = img.nonzero()
            pos_x = [x + self.start_x for x in index_x]
            pos_y = [x + self.start_y for x in index_y]

            print(len(index_x), len(pos_x))
            
            deprojected_area_sum = 0
            for i in range(len(pos_x)):
                distance_from_center =  math.sqrt((pos_x[i] - self.center_x )**2 +
                                                  (pos_y[i] - self.center_y )**2)
                #print(i, pos_x[i], self.center_x, pos_y[i], self.center_y,
                #distance_from_center)
                #print(i, pos_x[i] - self.center_x , pos_y[i] - self.center_y)
                #print(i, self.radius, distance_from_center, pos_x[i], pos_y[i])
                if distance_from_center < self.radius:
                    center_to_limb_angle = (math.asin(distance_from_center *
                                                      1./self.radius))
                    
                    deprojected_area_sum += 1./math.cos(center_to_limb_angle)
                    
            return (deprojected_area_sum * math.pow(10, 6) /
                    (2 * math.pi * self.radius**2))
                
        else:
            return 0
            
    def projected_area_calculation(self, nb_pixel):
        if self.radius:
            return nb_pixel * math.pow(10,6)/(math.pi * self.radius**2)
        else:
            return 0

    def update_frame_surface(self, radius, step=0):
        """
        change the size of the frame around the surface selection.
        """
        div_factor = self.radius_division_factor
        div_factor_tmp =  div_factor + step * 100
        print("the div factor is ", div_factor_tmp)
        
        if div_factor_tmp:
            frame_size_tmp = math.floor(radius / div_factor_tmp) * 100
            if frame_size_tmp > 0:
                frame_size = frame_size_tmp
                self.radius_division_factor = div_factor_tmp
            
            
        else:
            frame_size = math.floor(radius / self.radius_division_factor) * 100

        print("the frame is now: ", frame_size)
        return frame_size
        
class QLabelGroupSurface(QtWidgets.QLabel):

    array_changed = QtCore.pyqtSignal()
    
    def __init__(self):
        super(QLabelGroupSurface, self).__init__()
       
        self.original_pixmap = QtGui.QPixmap() # used for the reset
        self.first_pixamp_polygon = QtGui.QPixmap() # used for the polygon drawing
        
        self.width_scale = 600
        self.height_scale = 600
        self.scaling_factor = 1
        self.pointsList = []
           
        self.polygon = analyse_mode_bool.analyseModeBool(False)
        self.crop_done = analyse_mode_bool.analyseModeBool(False)
        self.pencil = analyse_mode_bool.analyseModeBool(False)
        self.bucket = analyse_mode_bool.analyseModeBool(False)
    
    def zoom_in(self, scaling_factor):
        self.width_scale *=  scaling_factor
        self.height_scale *=  scaling_factor
        
        self.scaling_factor *=scaling_factor
        print("the scaling factor is", self.scaling_factor)
       
        bis = self.original_pixmap.scaled(int(self.width_scale),
                                          int(self.height_scale),
                                          QtCore.Qt.KeepAspectRatio)
        self.setPixmap(bis)
        
        
        
    
    def set_original_img(self, np_array):
        #print("set the original image")
        self.original_pixmap = self.np2qpixmap(np_array).copy()
        self.pointsList = []
        #self.original_pixmap = pixmap
        #self.setPixmap(original_pixmap)
        bis = self.original_pixmap.scaled(int(self.width_scale),
                                          int(self.height_scale),
                                          QtCore.Qt.KeepAspectRatio)
        
        
        self.setPixmap(bis)#original_pixmap)
    def convertQImageToMat(self, incomingImage):
        """
        convert QImage to np array
        """
        '''  Converts a QImage into an opencv MAT format  '''

        incomingImage = incomingImage.convertToFormat(3)
        width = incomingImage.width()
        height = incomingImage.height()

        print("convert to mat ", width, height)
        
        ptr = incomingImage.bits()
        ptr.setsize(incomingImage.byteCount())
        arr = np.array(ptr).reshape(height, width, 1)  #  Copies the data
        return arr
        
    def np2qpixmap(self, np_img):
        """
        convert np array into pixmap
        """
        #print("np2qimage")
        #print(type(np_img), np_img.shape)
        #frame = cv2.cvtColor(np_img, cv2.COLOR_BGR2RGB)
        frame = cv2.cvtColor(np_img,cv2.COLOR_GRAY2RGB)
        img = QtGui.QImage(frame,
                           frame.shape[1],
                           frame.shape[0],
                           QtGui.QImage.Format_RGB888)
        return QtGui.QPixmap.fromImage(img)

    
    def draw_polygon(self, position=None):
        """
        Method that has a *graphic* role. it shows the polygon on screen and 
        records the list of points.
        """
        self.polygon.value = True
        self.pencil.value = False

        painter = QtGui.QPainter()
        pen = QtGui.QPen(QtCore.Qt.red)
        pen.setWidth(5)
        
        if position:
            self.pointsList.append(position)
        
        #print("enter the draw polygon", len(self.pointsList))
        
        if len(self.pointsList) == 0:
            #print("set the pixmap polygon", len(self.pointsList))
            self.first_pixamp_polygon = self.pixmap().copy()

        #self.setPixmap(self.first_pixamp_polygon)
        bis = self.first_pixamp_polygon.scaled(int(self.width_scale),
                                               int(self.height_scale),
                                               QtCore.Qt.KeepAspectRatio)
        
        self.setPixmap(bis)
        painter.begin(self.pixmap())
        pen_polygon = QtGui.QPen(QtCore.Qt.cyan)
        pen_polygon.setWidth(3)
        painter.setPen(pen_polygon)
        if len(self.pointsList) == 1:
            painter.drawPoint(self.pointsList[-1])
            
        else:
            for i in range(len(self.pointsList)):
                painter.drawLine(self.pointsList[i-1],self.pointsList[i])
        painter.end()

    def cut_polygon(self, array):
        """
        Change the matrix of pixel and return a new array.
        """
        self.polygon.value = False
        print("polygon")
        print(self.pointsList)
        polygon_points =  [(int(math.floor(a.y() * array.shape[1] / self.height_scale )),
                            int(math.floor(a.x() * array.shape[0] / self.width_scale )))
                           for a in self.pointsList]
        
        print(polygon_points)
        polygon = Polygon(polygon_points)
        print(array.shape)
        count=0
        
        for index, value in np.ndenumerate(array):
            if value>0 :
                count+=1
                if polygon.contains(Point(index)) == False:
                    array[index] = 0


        print("total number of white pixels: ", count)
        return array
        
    def set_pencil_array(self, array, new_value):
        print("set pencil array")
        print(new_value)
        print(array.max())
        self.polygon.value = False
        self.pencil.value = True
        
        self.array = array
        self.new_value = new_value
    
    def set_bucket_fill(self, array, old_value, new_value):

        self.array = array
        self.new_value = new_value
        self.old_value = old_value
        self.polygon.value = False
        self.pencil.value = False
        self.bucket.value = True
        
    def bucket_fill(self, position_x, position_y):

        print("enter in the bucket fill", position_x,
              position_y, self.array.shape[1], self.array.shape[0])
        
        print("new value: ", self.new_value)
        print("old value: ", self.old_value)
        print("current value: ",self.array[position_x, position_y])
        
        if self.array[position_x, position_y] == self.new_value:
            print("already done", position_x, position_y)
            return
        
        self.array[position_x, position_y] = self.new_value

        if position_x > 0:
            print("go to the right", position_x, position_y)
            self.bucket_fill(position_x - 1, position_y)
        if position_x < self.array.shape[1] - 1 :
            print("go to the left", position_x, position_y)
            self.bucket_fill(position_x + 1, position_y)
        if position_y > 0 :
            print("go up", position_x, position_y)
            self.bucket_fill(position_x , position_y - 1)
        if position_y < self.array.shape[0] - 1 :
            print("do down", position_x, position_y)
            self.bucket_fill(position_x , position_y + 1)

  
    def mousePressEvent(self, QMouseEvent):
        position =  QMouseEvent.pos()

        if (self.pencil.value or
            self.bucket.value):
            pos_y_scaled = int(math.floor(position.y() * self.array.shape[1] /
                                      self.height_scale ))
            pos_x_scaled = int(math.floor(position.x() * self.array.shape[0] /
                                      self.width_scale ))

            print("mouse press event: ", position, pos_x_scaled, pos_y_scaled)
        if self.polygon.value :
            self.draw_polygon(position)

        elif self.pencil.value:
            self.array[pos_y_scaled, pos_x_scaled] = self.new_value
            self.array_changed.emit()

        elif self.bucket.value:
            self.bucket_fill(pos_y_scaled, pos_x_scaled)
            self.array_changed.emit()
               
    def mouseMoveEvent(self, QMouseEvent):
        if self.pencil.value:
            print("mouse move event")
            position =  QMouseEvent.pos()
            pos_y_scaled = int(math.floor(position.y() * self.array.shape[1] /
                                          self.height_scale ))
            pos_x_scaled = int(math.floor(position.x() * self.array.shape[0] /
                                          self.width_scale ))
            
            self.array[pos_y_scaled, pos_x_scaled] = self.new_value
            self.array_changed.emit()
            
    def mouseReleaseEvent(self,QMouseEvent):
        
        if self.pencil.value:
            print("enter in the mouse release and painter end")
            position =  QMouseEvent.pos()
            pos_y_scaled = int(math.floor(position.y() * self.array.shape[1] /
                                          self.height_scale ))
            pos_x_scaled = int(math.floor(position.x() * self.array.shape[0] /
                                          self.width_scale ))
            
            self.array[pos_y_scaled, pos_x_scaled]= self.new_value
            self.array_changed.emit()
            
