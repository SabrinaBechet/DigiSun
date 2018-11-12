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
import analyse_mode_bool
import matplotlib.path as mpltPath
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon

#sys.setrecursionlimit(100000) # check where it is exactly used...

class GroupSurfaceWidget(QtGui.QWidget):

    def __init__(self):
         super(GroupSurfaceWidget, self).__init__()
         self.layout = QtGui.QVBoxLayout()
         self.layout.setSpacing(15)
         self.setLayout(self.layout)

         self.scroll = QtGui.QScrollArea()
         self.scroll\
             .setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
         self.scroll\
             .setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
         self.scroll.setWidgetResizable(True)
         
         self.qlabel_group_surface = QLabelGroupSurface()
         self.qlabel_group_surface.setAlignment(QtCore.Qt.AlignTop and QtCore.Qt.AlignRight)
         #self.qlabel_group_surface.setMaximumSize(600,600)
         self.scroll.setWidget(self.qlabel_group_surface)#self.widget_left_up)
         
         qlabel_title = QtGui.QLabel("Surface calculation")
         qlabel_title.setAlignment(QtCore.Qt.AlignCenter)
         qlabel_title.setContentsMargins(0, 5, 0, 5)
         
         threshold_slider = QtGui.QSlider(QtCore.Qt.Horizontal)
         threshold_slider.setRange(0,256)
         threshold_slider.setTickPosition(QtGui.QSlider.TicksBelow)
         threshold_slider.setValue(225)
         threshold_slider.valueChanged.connect(
             lambda: self.update_img_threshold_value(threshold_slider.value()))
         self.threshold_linedit = QtGui.QLineEdit(str(threshold_slider.value()))

         threshold_layout = QtGui.QFormLayout()
         threshold_layout.addRow("Threshold selection:",
                            self.threshold_linedit)

         qlabel_general = QtGui.QLabel("General tools:")
         
         zoom_in_but =QtGui.QToolButton()
         zoom_in_but.setIcon(QtGui.QIcon('icons/Smashicons/zoom-in.svg'))
         zoom_in_but.setMinimumWidth(self.width()/4.)
         zoom_in_but.clicked.connect(
             lambda: self.qlabel_group_surface.zoom_in(2.))

         zoom_out_but = QtGui.QToolButton()
         zoom_out_but.setIcon(QtGui.QIcon('icons/Smashicons/search.svg'))
         zoom_out_but.setMinimumWidth(self.width()/4.)
         zoom_out_but.clicked.connect(
             lambda: self.qlabel_group_surface.zoom_in(1/2.))

         reset_but = QtGui.QToolButton()
         reset_but.setText("reset")
         reset_but.setMinimumWidth(self.width()/4.)
         reset_but.clicked.connect(
             lambda: self.update_img_threshold_value(threshold_slider.value()))
         
         draw_polygon_but = QtGui.QToolButton()
         draw_polygon_but.setIcon(QtGui.QIcon('icons/Darrio_Ferrando/polygon.svg'))
         draw_polygon_but.setMinimumWidth(self.width()/4.)
         draw_polygon_but.clicked.connect( self.qlabel_group_surface.draw_polygon)
         
         qlabel_polygon = QtGui.QLabel("Polygon selection:")
         cut_polygon_but = QtGui.QToolButton()
         cut_polygon_but.setText("cut")
         cut_polygon_but.setMinimumWidth(self.width()/4.)
         cut_polygon_but.clicked.connect(
             lambda : self.cut_polygon(threshold_slider.value()))

         qlabel_paint = QtGui.QLabel("paint tools:")
         pencil_but = QtGui.QToolButton()
         pencil_but.setIcon(QtGui.QIcon('icons/Freepik/black_brush-stroke_32.png'))
         pencil_but.setMinimumWidth(self.width()/4.)
         pencil_but.clicked.connect(lambda: self.draw_pencil(0))

         bucket_white_fill_but = QtGui.QToolButton()
         bucket_white_fill_but.setIcon(QtGui.QIcon('icons/Darrio_Ferrando/bucket.svg'))
         bucket_white_fill_but.setMinimumWidth(self.width()/4.)
         bucket_white_fill_but.clicked.connect(
             lambda : self.qlabel_group_surface.set_bucket_fill(self.current_array,
                                                                0,
                                                                255))
         
         erase_but = QtGui.QToolButton()
         erase_but.setIcon(QtGui.QIcon('icons/Freepik/white_brush-stroke_32.png'))
         erase_but.setMinimumWidth(self.width()/4.)
         erase_but.clicked.connect(lambda: self.draw_pencil(255))

         layout_general = QtGui.QGridLayout()
         layout_general.addWidget(qlabel_general, 0, 0)
         layout_general.addWidget(zoom_in_but, 1, 0)
         layout_general.addWidget(zoom_out_but, 1, 1)
         layout_general.addWidget(reset_but, 1, 2)
         layout_general.addWidget(qlabel_polygon, 2, 0)
         layout_general.addWidget(draw_polygon_but, 3, 0)
         layout_general.addWidget(cut_polygon_but, 3, 1)
         layout_general.addWidget(qlabel_paint, 4, 0)
         layout_general.addWidget(pencil_but, 5, 0)
         layout_general.addWidget(erase_but, 5, 1)
         layout_general.addWidget(bucket_white_fill_but, 5, 2)
         
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
        #thresh_value , selection_array_thresh = cv2.threshold(self.selection_array,
        #                                                      value,
        #                                                      256,
        #                                                      cv2.THRESH_BINARY_INV)
        cut_array = self.qlabel_group_surface.cut_polygon(self.current_array)#selection_array_thresh)
        self.set_img(cut_array)
         
    def update_img_threshold_value(self, value):
        self.qlabel_group_surface.polygon.value = False
        self.qlabel_group_surface.pencil.value = False
        self.qlabel_group_surface.bucket.value = False
        
        new_selection_thresh = self.threshold(value)
        self.threshold_linedit.setText(str(value))
        self.set_img(new_selection_thresh)
        self.qlabel_group_surface.pointsList = []

    def set_array(self, np_array, value=225):
        self.selection_array = np_array
        self.set_img(self.threshold(value))
        self.qlabel_group_surface.pointsList = []

    def threshold(self, value=225):
        thresh_value , selection_array_thresh = cv2.threshold(self.selection_array,
                                                              value,
                                                              256,
                                                              cv2.THRESH_BINARY_INV)
            
        return selection_array_thresh
    
    def set_img(self, img):
        self.current_array = img
        self.qlabel_group_surface.set_original_img(img)
        nb_pixel = self.count_pixel(img)
        self.pixel_number_linedit.setText(str(nb_pixel))

    def count_pixel(self, img):
        return np.count_nonzero(img) 


        
class QLabelGroupSurface(QtGui.QLabel):

    array_changed = QtCore.pyqtSignal()
    
    def __init__(self):
        super(QLabelGroupSurface, self).__init__()
       
        self.original_pixmap = QtGui.QPixmap() # used for the reset
        #self.threshold_pixmap = QtGui.QPixmap()
        self.first_pixamp_polygon = QtGui.QPixmap() # used for the polygon drawing
        self.pixmap_before_threshold = QtGui.QPixmap()
        
        #self.setMaximumWidth(500)
        self.width_scale = 600
        self.height_scale = 600
        self.scaling_factor = 1
        self.pointsList = []
        
        # self.is_drawing = False
        #self.to_fill = False
        #self.threshold_value = 225
        
        self.polygon = analyse_mode_bool.analyseModeBool(False)
        self.crop_done = analyse_mode_bool.analyseModeBool(False)
        self.pencil = analyse_mode_bool.analyseModeBool(False)
        self.bucket = analyse_mode_bool.analyseModeBool(False)
    
    def zoom_in(self, scaling_factor):
        self.width_scale *=  scaling_factor
        self.height_scale *=  scaling_factor
        
        self.scaling_factor *=scaling_factor
        print("the scaling factor is", self.scaling_factor)
        #self.set_img()

        bis = self.original_pixmap.scaled(int(self.width_scale),
                                          int(self.height_scale),
                                          QtCore.Qt.KeepAspectRatio)
        
        
        self.setPixmap(bis)#original_pixmap)
    
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

        polygon_points =  [(int(math.floor(a.y()/(2.* self.scaling_factor ))),
                            int(math.floor(a.x()/(2. * self.scaling_factor)))) for a in self.pointsList]
        print(polygon_points)

        #path = mpltPath.Path(polygon_points)

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
        
        """x = self.position.x()
        y = self.position.y()
        image = self.pixmap().toImage()
        array_image = self.convertQImageToMat(image)
        array_image = self.iter_fill(x, y, array_image)
        newPixmap = self.np2qpixmap(array_image)
        self.setPixmap(newPixmap)
        """

    def bucket_fill(self, position_x, position_y):

        print("enter in the bucket fill", position_x, position_y, self.array.shape[1], self.array.shape[0])
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

            
        
    """def iter_fill(self,x_start,y_start,array):
        stack = [(x_start,y_start)]
        #C1, C2 and C3 are the colors in RGB that the pixel need to be in
        #If the pen is white, then the pixels are turned black (0,0,0),
        #otherwise they are turned red (0,0,255)
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

    def check_color(self,x,y,array,c1,c2,c3):
        return(array[y][x][0] == c1 and array[y][x][1] == c2 and array[y][x][2] == c3)

    """
    def mousePressEvent(self, QMouseEvent):
        position =  QMouseEvent.pos()
        
        if self.polygon.value :
            print("mouse press event: ", position)
            self.draw_polygon(position)

        elif self.pencil.value:
            self.array[int(math.floor(position.y()/(2.* self.scaling_factor ))),
                       int(math.floor(position.x()/(2.* self.scaling_factor )))] = self.new_value
            self.array_changed.emit()

        elif self.bucket.value:
            self.bucket_fill(int(math.floor(position.y()/(2.* self.scaling_factor ))),
                             int(math.floor(position.x()/(2.* self.scaling_factor ))))
            self.array_changed.emit()
        
            
    def mouseMoveEvent(self, QMouseEvent):
        if self.pencil.value:
            print("mouse move event")
            position =  QMouseEvent.pos()
            self.array[int(math.floor(position.y()/(2.* self.scaling_factor ))),
                       int(math.floor(position.x()/(2.* self.scaling_factor )))] = self.new_value
            self.array_changed.emit()
            
    def mouseReleaseEvent(self,QMouseEvent):
        
        if self.pencil.value:
            print("enter in the mouse release and painter end")
            position =  QMouseEvent.pos()
            self.array[int(math.floor(position.y()/(2.* self.scaling_factor ))),
                       int(math.floor(position.x()/(2.* self.scaling_factor )))] = self.new_value
            self.array_changed.emit()
            
