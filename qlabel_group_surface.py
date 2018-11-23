# !/usr/bin/env python
# -*-coding:utf-8-*-
from PyQt4 import QtGui, QtCore
#from PIL import Image
from PIL.ImageQt import ImageQt
import numpy as np
import math
import coordinates
import cv2
import numpy as np
import time
import sys
import analyse_mode_bool
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon

sys.setrecursionlimit(10000) 

class GroupSurfaceWidget(QtGui.QWidget):

    bigger_frame = QtCore.pyqtSignal()
    smaller_frame = QtCore.pyqtSignal()
    surface_saved = QtCore.pyqtSignal()
    
    def __init__(self):
        super(GroupSurfaceWidget, self).__init__()
        self.layout = QtGui.QVBoxLayout()
        self.layout.setSpacing(15)
        self.setLayout(self.layout)
        
        self.radius_division_factor = 400
        
        self.scroll = QtGui.QScrollArea()
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
        
        qlabel_title = QtGui.QLabel("Surface calculation")
        qlabel_title.setAlignment(QtCore.Qt.AlignCenter)
        qlabel_title.setContentsMargins(0, 5, 0, 5)
        
        threshold_slider = QtGui.QSlider(QtCore.Qt.Horizontal)
        threshold_slider.setRange(0,256)
        threshold_slider.setTickPosition(QtGui.QSlider.TicksBelow)
        
        self.default_threshold = 225
        threshold_slider.setValue(self.default_threshold)
        threshold_slider.valueChanged.connect(
            lambda: self.update_img_threshold_value(threshold_slider.value()))
        self.threshold_linedit = QtGui.QLineEdit(str(self.default_threshold))
        
        threshold_layout = QtGui.QFormLayout()
        threshold_layout.addRow("Threshold selection:",
                                self.threshold_linedit)
        
        qlabel_general = QtGui.QLabel("General tools:")
        
        zoom_in_but =QtGui.QToolButton()
        zoom_in_but.setIcon(QtGui.QIcon('icons/Smashicons/zoom-in.svg'))
        zoom_in_but.clicked.connect(
            lambda: self.qlabel_group_surface.zoom_in(2.))
        
        zoom_out_but = QtGui.QToolButton()
        zoom_out_but.setIcon(QtGui.QIcon('icons/Smashicons/search.svg'))
        zoom_out_but.clicked.connect(
            lambda: self.qlabel_group_surface.zoom_in(1/2.))
        
        reset_but = QtGui.QToolButton()
        reset_but.setText("reset")
        reset_but.setIcon(QtGui.QIcon('icons/Pixel_perfect/settings.svg'))
        reset_but.clicked.connect(
            lambda: self.update_img_threshold_value(threshold_slider.value()))
        
        undo_but = QtGui.QToolButton()
        undo_but.setIcon(QtGui.QIcon('icons/Eleonor_Wang/undo.svg'))
        
        bigger_frame_but =QtGui.QToolButton()
        bigger_frame_but.setIcon(
            QtGui.QIcon('icons/Linh_Pham/mine_bigger_frame.png'))
        bigger_frame_but.clicked.connect(
            lambda: self.bigger_frame.emit())
  
        smaller_frame_but =QtGui.QToolButton()
        smaller_frame_but.setIcon(
            QtGui.QIcon('icons/Linh_Pham/mine_smaller_frame.png'))
        smaller_frame_but.clicked.connect(
            lambda: self.smaller_frame.emit())
        
        draw_polygon_but = QtGui.QToolButton()
        draw_polygon_but.setIcon(
            QtGui.QIcon('icons/Darrio_Ferrando/polygon.svg'))
        draw_polygon_but.clicked.connect(
            lambda : self.set_opposite_value(
                self.qlabel_group_surface.polygon_mode))
        draw_polygon_but.clicked.connect(
            self.qlabel_group_surface.draw_polygon)
        
        cut_polygon_but = QtGui.QToolButton()
        cut_polygon_but.setIcon(
            QtGui.QIcon('icons/Freepik/crop.svg'))
        cut_polygon_but.clicked.connect(
            lambda : self.cut_polygon(threshold_slider.value()))
        
        draw_1pixel_black_but = QtGui.QToolButton()
        draw_1pixel_black_but.setIcon(
            QtGui.QIcon('icons/Freepik/1pix_black_square.svg'))
        draw_1pixel_black_but.clicked.connect(
            lambda : self.set_opposite_value(
                self.qlabel_group_surface.black_pencil_mode))
        draw_1pixel_black_but.clicked.connect(lambda: self.draw_pencil(0))

        draw_1pixel_white_but = QtGui.QToolButton()
        draw_1pixel_white_but.setIcon(
            QtGui.QIcon('icons/Freepik/1pix_white_square.svg'))
        draw_1pixel_white_but.clicked.connect(
            lambda : self.set_opposite_value(
                self.qlabel_group_surface.white_pencil_mode))
        draw_1pixel_white_but.clicked.connect(lambda: self.draw_pencil(255))
        
        bucket_white_fill_but = QtGui.QToolButton()
        bucket_white_fill_but.setIcon(
            QtGui.QIcon('icons/Freepik/white-bucket.svg'))
        bucket_white_fill_but.clicked.connect(
            lambda : self.set_opposite_value(
                self.qlabel_group_surface.white_bucket_mode))
        bucket_white_fill_but.clicked.connect(
            lambda : self.qlabel_group_surface.set_bucket_fill(self.current_array,
                                                               0,
                                                               255))
        bucket_black_fill_but = QtGui.QToolButton()
        bucket_black_fill_but.setIcon(
            QtGui.QIcon('icons/Freepik/black-bucket.svg'))
        bucket_black_fill_but.clicked.connect(
            lambda : self.set_opposite_value(
                self.qlabel_group_surface.black_bucket_mode))
        bucket_black_fill_but.clicked.connect(
            lambda : self.qlabel_group_surface.set_bucket_fill(self.current_array,
                                                               255,
                                                               0))
        
        
        """cross_but = QtGui.QToolButton()
        cross_but.setMinimumWidth(self.width()/6.)
        cross_but.clicked.connect(lambda: self.draw_pencil(255))
        
        pixel_slider = QtGui.QSlider(QtCore.Qt.Horizontal)
        pixel_slider.setRange(1,5)
        pixel_slider.setTickPosition(QtGui.QSlider.TicksBelow)
        pixel_slider.setValue(1)
        """
        
        self.qlabel_group_surface.polygon_mode.value_changed.connect(
            lambda: self.set_button_color(
                self.qlabel_group_surface.polygon_mode.value,
                draw_polygon_but ))
        if self.qlabel_group_surface.polygon_mode.value:
            draw_polygon_but.setStyleSheet("background-color: lightblue")
            
        self.qlabel_group_surface.white_pencil_mode.value_changed.connect(
            lambda: self.set_button_color(
                self.qlabel_group_surface.white_pencil_mode.value,
                draw_1pixel_white_but))
        if self.qlabel_group_surface.white_pencil_mode.value:
            draw_1pixel_white_but.setStyleSheet("background-color: lightblue")
            
        self.qlabel_group_surface.black_pencil_mode.value_changed.connect(
            lambda: self.set_button_color(
                self.qlabel_group_surface.black_pencil_mode.value,
                draw_1pixel_black_but))
        if self.qlabel_group_surface.black_pencil_mode.value:
            draw_1pixel_black_but.setStyleSheet("background-color: lightblue")
            
        self.qlabel_group_surface.white_bucket_mode.value_changed.connect(
            lambda: self.set_button_color(
                self.qlabel_group_surface.white_bucket_mode.value,
                bucket_white_fill_but))
        if self.qlabel_group_surface.white_bucket_mode.value:
            bucket_white_fill_but.setStyleSheet("background-color: lightblue")
            
        self.qlabel_group_surface.black_bucket_mode.value_changed.connect(
            lambda: self.set_button_color(
                self.qlabel_group_surface.black_bucket_mode.value,
                bucket_black_fill_but))
        if self.qlabel_group_surface.black_bucket_mode.value:
            bucket_black_fill_but.setStyleSheet("background-color: lightblue")
             
        layout_general = QtGui.QGridLayout()
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
        form_layout = QtGui.QFormLayout()
        self.pixel_number_linedit = QtGui.QLineEdit()
        self.projected_surface_linedit = QtGui.QLineEdit()
        self.deprojected_surface_linedit = QtGui.QLineEdit()
        
        form_layout.addRow("Pixel Number:",
                           self.pixel_number_linedit)
        form_layout.addRow("Projected surface (msd):",
                           self.projected_surface_linedit)
        form_layout.addRow("Deprojected surface (msh):",
                           self.deprojected_surface_linedit)
        
        save_but = QtGui.QPushButton("save")

        save_but.clicked.connect(self.fill_surface_info)
        
        self.layout.addWidget(qlabel_title)
        self.layout.addLayout(threshold_layout)
        self.layout.addWidget(threshold_slider)
        self.layout.addLayout(layout_general)
        
        self.layout.addWidget(self.scroll)
        self.layout.addLayout(form_layout)
        self.layout.addWidget(save_but)
        
        self.qlabel_group_surface.array_changed.connect(
            lambda: self.set_img(self.qlabel_group_surface.array))

    def set_opposite_value(self, mode):
        if mode.value:
            mode.value = False
        else:
            mode.value = True
        
    def set_button_color(self, mode_bool, but):
        if mode_bool==True:
            but.setStyleSheet("background-color: lightblue")
        elif mode_bool==False:
            but.setStyleSheet("background-color: lightgray")    
         
    def draw_pencil(self, new_value):
        self.qlabel_group_surface.set_pencil_array(self.current_array, new_value)
        
         
    def cut_polygon(self, value):
        cut_array = self.qlabel_group_surface.cut_polygon(self.current_array)
        self.set_img(cut_array)
         
    def update_img_threshold_value(self, value):
        self.qlabel_group_surface.polygon_mode.value = False
        self.qlabel_group_surface.white_pencil_mode.value = False
        self.qlabel_group_surface.black_pencil_mode.value = False
        self.qlabel_group_surface.white_bucket_mode.value = False
        self.qlabel_group_surface.black_bucket_mode.value = False

        self.default_threshold = value
        new_selection_thresh = self.threshold(value)
        self.threshold_linedit.setText(str(value))
        self.set_img(new_selection_thresh)
        self.qlabel_group_surface.pointsList = []

    def set_array(self, np_array):
        print("new array ")
        self.qlabel_group_surface.polygon_mode.value = False
        self.qlabel_group_surface.white_pencil_mode.value = False
        self.qlabel_group_surface.black_pencil_mode.value = False
        self.qlabel_group_surface.white_bucket_mode.value = False
        self.qlabel_group_surface.black_bucket_mode.value = False
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
        #print("set img")
        self.current_array = img
        self.qlabel_group_surface.set_original_img(img)
        self.nb_pixel = self.count_pixel(img)
        self.projected_area = self.projected_area_calculation(self.nb_pixel)
        self.deprojected_area = self.deprojected_area_calculation(img)
        self.pixel_number_linedit.setText(str(self.nb_pixel))
        self.projected_surface_linedit.setText(
            '{0:.2f}'.format(self.projected_area))
        self.deprojected_surface_linedit.setText(
            '{0:.2f}'.format(self.deprojected_area))

        #print(self.nb_pixel, self.projected_area, self.deprojected_area )
        
    def count_pixel(self, img):
        return np.count_nonzero(img)

    def fill_surface_info(self):
        self.drawing.group_lst[self.index].surface = self.deprojected_area
        self.drawing.group_lst[self.index].raw_surface_px = self.nb_pixel
        self.drawing.group_lst[self.index].raw_surface_msd = self.projected_area
        print("fill surface info")
        print("deproj area ", self.deprojected_area, type(self.deprojected_area))
        print("pixel ", self.nb_pixel, type(self.nb_pixel))
    
        self.surface_saved.emit()

        
    def set_group_info(self, drawing, index, start_x, start_y):
        self.drawing = drawing
        self.radius = drawing.calibrated_radius
        self.start_x = start_x
        self.start_y = start_y
        self.center_x = drawing.calibrated_center.x
        self.center_y = drawing.calibrated_center.y
        self.index = index

    def deprojected_area_calculation(self, img):
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
        #print("the div factor is ", div_factor_tmp)
        
        if div_factor_tmp:
            frame_size_tmp = math.floor(radius / div_factor_tmp) * 100
            if frame_size_tmp > 0:
                frame_size = frame_size_tmp
                self.radius_division_factor = div_factor_tmp
            
        else:
            frame_size = math.floor(radius / self.radius_division_factor) * 100

        #print("the frame is now: ", frame_size)
        return frame_size
        
class QLabelGroupSurface(QtGui.QLabel):

    array_changed = QtCore.pyqtSignal()
    
    
    def __init__(self):
        super(QLabelGroupSurface, self).__init__()
       
        self.original_pixmap = QtGui.QPixmap() # used for the reset
        self.first_pixamp_polygon = QtGui.QPixmap() # used for the polygon drawing
        
        self.width_scale = 600
        self.height_scale = 600
        self.scaling_factor = 1
        self.pointsList = []
           
        self.polygon_mode = analyse_mode_bool.analyseModeBool(False)
        self.white_pencil_mode = analyse_mode_bool.analyseModeBool(False)
        self.black_pencil_mode = analyse_mode_bool.analyseModeBool(False)
        self.white_bucket_mode = analyse_mode_bool.analyseModeBool(False)
        self.black_bucket_mode = analyse_mode_bool.analyseModeBool(False)

        self.max_count = 0
        
    def zoom_in(self, scaling_factor):
        self.width_scale *=  scaling_factor
        self.height_scale *=  scaling_factor
        self.scaling_factor *=scaling_factor
        bis = self.original_pixmap.scaled(int(self.width_scale),
                                          int(self.height_scale),
                                          QtCore.Qt.KeepAspectRatio)
        self.setPixmap(bis)
        
    def set_original_img(self, np_array):
        self.original_pixmap = self.np2qpixmap(np_array).copy()
        self.pointsList = []
        bis = self.original_pixmap.scaled(int(self.width_scale),
                                          int(self.height_scale),
                                          QtCore.Qt.KeepAspectRatio)
        self.setPixmap(bis)
      
    def np2qpixmap(self, np_img):
        """convert np array into pixmap"""
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
        self.white_pencil_mode.value = False
        self.black_pencil_mode.value = False
        self.white_bucket_mode.value = False
        self.black_bucket_mode.value = False
    
        painter = QtGui.QPainter()
        pen = QtGui.QPen(QtCore.Qt.red)
        pen.setWidth(5)
        
        if position:
            self.pointsList.append(position)
            
        if len(self.pointsList) == 0:
            self.first_pixamp_polygon = self.pixmap().copy()
            
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
        self.polygon_mode.value = False
        self.white_pencil_mode.value = False
        self.black_pencil_mode.value = False
        self.white_bucket_mode.value = False
        self.black_bucket_mode.value = False
        
        polygon_points = [(int(math.floor(a.y() * array.shape[1] /
                                          self.height_scale )),
                           int(math.floor(a.x() * array.shape[0] /
                                          self.width_scale )))
                          for a in self.pointsList]
        
        polygon = Polygon(polygon_points)
        count = 0
        for index, value in np.ndenumerate(array):
            if value>0 :
                count+=1
                if polygon.contains(Point(index)) == False:
                    array[index] = 0


        #print("total number of white pixels: ", count)
        return array
        
    def set_pencil_array(self, array, new_value):

        print("set the pencil array")
        
        self.polygon_mode.value = False
        if new_value ==0 :
            self.white_pencil_mode.value = False
            #self.black_pencil_mode.value = True    
        else:
            #self.white_pencil_mode.value = True
            self.black_pencil_mode.value = False
        self.white_bucket_mode.value = False
        self.black_bucket_mode.value = False
        
        self.array = array
        self.new_value = new_value
    
    def set_bucket_fill(self, array, old_value, new_value):

        self.polygon_mode.value = False
        self.white_pencil_mode.value = False
        self.black_pencil_mode.value = False
        if new_value ==0 :
            self.white_bucket_mode.value =  False
            #self.black_bucket_mode.value =  True
        else:
            #self.white_bucket_mode.value =  True
            self.black_bucket_mode.value =  False
   
        self.array = array
        self.new_value = new_value
        self.old_value = old_value
        
    def bucket_fill(self, position_x, position_y, count=0):

        try:
            self.max_count = max(self.max_count, count)
            print(self.max_count)
            if self.array[position_x, position_y] == self.new_value:
                return
            
            self.array[position_x, position_y] = self.new_value
            if position_x > 0:
                self.bucket_fill(position_x - 1, position_y, count+1)
            if position_x < self.array.shape[1] - 1 :
                self.bucket_fill(position_x + 1, position_y, count+1)
            if position_y > 0 :
                self.bucket_fill(position_x , position_y - 1, count+1)
            if position_y < self.array.shape[0] - 1 :
                self.bucket_fill(position_x , position_y + 1, count+1)

        except RuntimeError :
            print("Time too long, check that the border is closed!")
                
    def mousePressEvent(self, QMouseEvent):
        position =  QMouseEvent.pos()

        if (self.white_pencil_mode.value or self.black_pencil_mode.value or 
            self.white_bucket_mode.value or self.black_bucket_mode.value):
            pos_y_scaled = int(math.floor(position.y() * self.array.shape[1] /
                                          self.height_scale ))
            pos_x_scaled = int(math.floor(position.x() * self.array.shape[0] /
                                      self.width_scale ))

        if self.polygon_mode.value:
            self.draw_polygon(position)

        elif self.white_pencil_mode.value or self.black_pencil_mode.value:
            self.array[pos_y_scaled, pos_x_scaled] = self.new_value
            self.array_changed.emit()

        elif self.white_bucket_mode.value or self.black_bucket_mode.value:
            self.bucket_fill(pos_y_scaled, pos_x_scaled)
            self.array_changed.emit()
               
    def mouseMoveEvent(self, QMouseEvent):
        if self.white_pencil_mode.value or self.black_pencil_mode.value:
            #print("mouse move event")
            position =  QMouseEvent.pos()
            pos_y_scaled = int(math.floor(position.y() * self.array.shape[1] /
                                          self.height_scale ))
            pos_x_scaled = int(math.floor(position.x() * self.array.shape[0] /
                                          self.width_scale ))
            
            self.array[pos_y_scaled, pos_x_scaled] = self.new_value
            self.array_changed.emit()
            
    def mouseReleaseEvent(self,QMouseEvent):
        if self.white_pencil_mode.value or self.black_pencil_mode.value:
            #print("enter in the mouse release and painter end")
            position =  QMouseEvent.pos()
            pos_y_scaled = int(math.floor(position.y() * self.array.shape[1] /
                                          self.height_scale ))
            pos_x_scaled = int(math.floor(position.x() * self.array.shape[0] /
                                          self.width_scale ))
            
            self.array[pos_y_scaled, pos_x_scaled]= self.new_value
            self.array_changed.emit()
            
