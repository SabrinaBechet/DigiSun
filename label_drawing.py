# !/usr/bin/env python
# -*-coding:utf-8-*-
import os, sys
from PyQt4 import QtGui, QtCore
from PIL import Image
from PIL.ImageQt import ImageQt
import database, drawing
from datetime import date, time, datetime

class QLabelDrawing(QtGui.QLabel):
   
    def __init__(self):
       super(QLabelDrawing, self).__init__()
       
       my_font = QtGui.QFont("Comic Sans MS", 20)
       self.setText('No drawings corresponding to this entry')
       self.setFont(my_font)
       self.setAlignment(QtCore.Qt.AlignCenter)
       self.setContentsMargins(0, 0, 0, 0)
       self.setMinimumWidth(300)
       self.width_scale = 1000
       self.height_scale = 1000
       #self.drawing_pixMap = QtGui.QPixmap()
       #self.setPixmap( self.drawing_pixMap)

      
       print(self.pixmap())

    def set_img(self):

        directory = "/home/sabrinabct/Projets/DigiSun_2018/archdrawing"
        filename = "usd201807010625.jpg"
        img = Image.open(os.path.join(directory, filename))
        qim = ImageQt(img) #convert PIL image to a PIL.ImageQt object
        drawing_pixMap = QtGui.QPixmap.fromImage(qim)
        self.setPixmap(drawing_pixMap.scaled(int(self.width_scale),
                                             int(self.height_scale),
                                             QtCore.Qt.KeepAspectRatio))
        
    def show_img(self):

        #self.setPixmap(self.drawing_pixMap.scaled(int(self.width_scale),
        #                                          int(self.height_scale),
        #                                          QtCore.Qt.KeepAspectRatio))
        self.show()
        
    def zoom_in(self, scaling_factor):
       
        print("zoom in")
       
        

        self.width_scale *=  scaling_factor
        print("zoom in 2")
        self.height_scale *=  scaling_factor
        print("zoom in 3", self.width_scale, self.height_scale)

        self.set_img()
        
        """img = self.pixmap()
        tst = img.scaled(int(self.width_scale),
                         int(self.height_scale),
                         QtCore.Qt.KeepAspectRatio)
        self.setPixmap(tst)
        """
        #self.resize(self.width_scale, self.height_scale)
        #self.show_img()

    """def resizeEvent(self, evt):
        self.setPixmap(self.drawing_pixMap.scaled(int(self.width_scale),
                                                  int(self.height_scale),
                                                  QtCore.Qt.KeepAspectRatio))
    """  
class MaFenetre(QtGui.QWidget):

    def __init__(self):
        super(MaFenetre, self).__init__()
        layout = QtGui.QVBoxLayout()
        label = QLabelDrawing()
        layout.addWidget(label)
        but_zoom_in = QtGui.QPushButton("zoom in", self)
        but_zoom_out = QtGui.QPushButton("zoom out", self)
        
        label.set_img()
        label.show_img()

        layout.addWidget(but_zoom_in)
        layout.addWidget(but_zoom_out)
        
        self.setLayout(layout)
        but_zoom_in.clicked.connect(lambda : label.zoom_in(1.1))
        but_zoom_out.clicked.connect(lambda : label.zoom_in(1/1.1))

       
app = QtGui.QApplication(sys.argv)
fenetre = MaFenetre()

fenetre.show()
app.exec_()
