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

sys.setrecursionlimit(100000) # check where it is exactly used...

class QLabelGroupSurface(QtGui.QLabel):

    mouse_pressed = QtCore.pyqtSignal()
    
    def __init__(self):
        super(QLabelGroupSurface, self).__init__()
        self.setFrameShape(QtGui.QFrame.Panel)
        self.setFrameShadow(QtGui.QFrame.Plain)
        self.setLineWidth(3)
        
        self.original_pixmap = QtGui.QPixmap() # used for the reset
        #self.threshold_pixmap = QtGui.QPixmap()
        self.first_pixamp_polygon = QtGui.QPixmap() # used for the polygon drawing
        self.pixmap_before_threshold = QtGui.QPixmap()
        
        self.setMaximumWidth(300)
        self.width_scale = 300
        self.height_scale = 300

        self.pointsList = []
        
        self.is_drawing = False
        self.to_fill = False

        self.threshold_value = 225

        """self.mode_draw_polygon = analyseModeBool(False)
        self.mode_threshold = analyseModeBool(False)
        self.mode_pencil = analyseModeBool(False)
        self.mode_bucket_fill = analyseModeBool(False)
        self.mode_rubber = analyseModeBool(False)
        self.first_view = analyseModeBool(True)
        """

        self.threshold = analyse_mode_bool.analyseModeBool(False)
        self.threshold_done = analyse_mode_bool.analyseModeBool(False)
        
        self.polygon = analyse_mode_bool.analyseModeBool(False)
        self.crop_done = analyse_mode_bool.analyseModeBool(False)
        self.pencil = analyse_mode_bool.analyseModeBool(False)
        self.bucket = analyse_mode_bool.analyseModeBool(False)

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

        if not self.threshold_done.value:
            self.pixmap_before_threshold = self.pixmap().copy()
        
        qimage = self.pixmap_before_threshold.toImage()
        pixel_matrix = self.convertQImageToMat(qimage)
        #print(type(pixel_matrix), pixel_matrix.size)

        pixMat_int8 = ((pixel_matrix * 255.) / pixel_matrix.max()).astype(np.uint8)
        thresh_value , pixel_matrix_thresh = cv2.threshold(pixMat_int8, threshold_value, 256, cv2.THRESH_BINARY_INV)
        threshold_pixmap = self.np2qpixmap(pixel_matrix_thresh).copy()

        self.setPixmap(threshold_pixmap)

        self.threshold_done.value = True
        
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
        print("**** set img",
              self.threshold.value,
              self.polygon.value,
              self.pencil.value,
              self.bucket.value,
              self.crop_done.value,
              self.threshold_done.value)
        
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

        
        if self.threshold.value :
            print("threshold!!", self.threshold_value)
            self.set_threshold_img(self.threshold_value)
            
        if self.polygon.value :
            self.draw_polygon()

        if self.pencil.value:
             self.draw_pencil()

        if self.bucket.value:
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
        if self.polygon.value or self.pencil.value or self.bucket.value :
            self.set_img()
            self.setPixmap(self.pixmap())
            
    def mouseMoveEvent(self,QMouseEvent):
            
        if self.pencil.value:
            self.painter.drawPoint(QMouseEvent.pos())
            self.setPixmap(self.pixmap())
    
    def mouseReleaseEvent(self,QMouseEvent):
        
        if self.pencil.value:
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
        self.crop_done.value = True

    def calculate_area(self):
        image = self.pixmap().toImage()
        array_image = self.convertQImageToMat(image)
        count = self.count_pixel(array_image)
        return count

    def count_pixel(self,array):
        count = 0
        for y in range(len(array)):
            for x in range(len(array)):
                if(array[y][x][0] == 0 and array[y][x][1] == 0 and array[y][x][2] == 255):
                    count += 1
        return count
    
    
