# !/usr/bin/env python
# -*-coding:utf-8-*-
import os
from PyQt4 import QtGui, QtCore

import qlabel_drawing 

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

        left_column_maximum_width = 380

        self.scroll_widget_left_up = QtGui.QScrollArea()
        self.scroll_widget_left_up\
            .setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.scroll_widget_left_up\
            .setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.scroll_widget_left_up .setWidgetResizable(True)
        self.widget_left_up = QtGui.QWidget()
        #self.widget_left_up.setMinimumWidth(left_column_maximum_width)
        #self.widget_left_up.setMaximumHeight(self.width()/2.)#500)
        self.widget_left_up.setStyleSheet("background-color:lightgray;")
        self.scroll_widget_left_up.setWidget(self.widget_left_up)
        
        self.widget_left_up_layout = QtGui.QVBoxLayout()
        self.widget_left_up_layout.setContentsMargins(0, 0, 0, 0) 
        self.widget_left_up_layout.setSpacing(0)
        self.widget_left_up_layout.setAlignment(QtCore.Qt.AlignTop)
        self.widget_left_up.setLayout(self.widget_left_up_layout)
        

        self.widget_left_middle = QtGui.QWidget()
        #self.widget_left_middle.setMinimumWidth(left_column_maximum_width)
        #self.widget_left_middle.setMinimumHeight(self.height()/3.)
        self.widget_left_middle.setMaximumHeight(self.height()/3.)
        self.widget_left_middle.setStyleSheet("background-color:lightgray;")   
        self.widget_left_middle_layout = QtGui.QVBoxLayout()
        self.widget_left_middle_layout.setContentsMargins(0, 0, 0, 0) 
        self.widget_left_middle_layout.setSpacing(0)
        self.widget_left_middle_layout.setAlignment(QtCore.Qt.AlignTop)
        self.widget_left_middle.setLayout(self.widget_left_middle_layout)
        self.widget_left_middle_layout.setMargin(10)
        
        self.widget_left_down = QtGui.QWidget()
        self.widget_left_down.setMaximumWidth(left_column_maximum_width)
        self.widget_left_down.setMinimumHeight(self.height()/3.)
        self.widget_left_down.setStyleSheet("background-color:lightblue;")   
        self.widget_left_down_layout = QtGui.QVBoxLayout()
        self.widget_left_down_layout.setContentsMargins(0, 0, 0, 0) 
        self.widget_left_down_layout.setSpacing(0)
        self.widget_left_down_layout.setAlignment(QtCore.Qt.AlignTop and
                                                  QtCore.Qt.AlignRight)
        self.widget_left_down.setLayout(self.widget_left_down_layout)
        
        self.widget_left_down_bis = QtGui.QWidget()
        self.widget_left_down_bis.setMaximumWidth(left_column_maximum_width)
        self.widget_left_down_bis.setMaximumHeight(200)
        self.widget_left_down_bis.setStyleSheet("background-color:lightblue;")   
        self.widget_left_down_bis_layout = QtGui.QVBoxLayout()
        self.widget_left_down_bis_layout.setContentsMargins(0, 0, 0, 0) 
        self.widget_left_down_bis_layout.setSpacing(0)
        self.widget_left_down_bis_layout.setAlignment(QtCore.Qt.AlignTop and
                                                      QtCore.Qt.AlignRight)
        self.widget_left_down_bis.setLayout(self.widget_left_down_bis_layout)
        
        self.widget_middle_up = QtGui.QWidget()
        self.widget_middle_up.setMaximumWidth(left_column_maximum_width)
        # trick to keep the surface panel closed by default
        self.widget_middle_up.setMaximumWidth(10)
        #self.widget_middle_up.setMinimumHeight(200)
        self.widget_middle_up.setStyleSheet("background-color:lightgray;")
        self.widget_middle_up_layout = QtGui.QVBoxLayout()
        self.widget_middle_up_layout.setContentsMargins(0, 0, 0, 0) 
        self.widget_middle_up_layout.setSpacing(10)
        self.widget_middle_up_layout.setAlignment(QtCore.Qt.AlignTop)
        self.widget_middle_up.setLayout(self.widget_middle_up_layout)
        #self.label_middle_up = qlabel_group_surface.QLabelGroupSurface()
        
        self.widget_right = QtGui.QWidget()
        self.widget_right.setStyleSheet("background-color:gray;")
        self.widget_right_layout = QtGui.QVBoxLayout()
        self.widget_right_layout.setContentsMargins(0, 0, 0, 0) 
        self.widget_right_layout.setSpacing(0)
        self.widget_right.setLayout(self.widget_right_layout)
        """self.label_right = qlabel_drawing.QLabelDrawing()

        self.scroll = QtGui.QScrollArea()
        self.scroll.setWidget(self.label_right)
        
        self.scroll.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.scroll.setWidgetResizable(True)
 
        self.widget_right_layout.addWidget(self.scroll)
        """
        splitter_down = QtGui.QSplitter(QtCore.Qt.Vertical, self)
        self.layout().addWidget(splitter_down)
        splitter_down.addWidget(self.widget_left_down)
        splitter_down.addWidget(self.widget_left_down_bis)
        
        splitter_middle_down = QtGui.QSplitter(QtCore.Qt.Vertical, self)
        self.layout().addWidget(splitter_middle_down)
        #splitter_middle_down.addWidget(self.widget_left_up)
        splitter_middle_down.addWidget(self.scroll_widget_left_up)
        splitter_middle_down.addWidget(self.widget_left_middle)
        splitter_middle_down.addWidget(splitter_down)
              
        splitter_main = QtGui.QSplitter(QtCore.Qt.Horizontal, self)
        self.layout().addWidget(splitter_main)
        splitter_main.addWidget(splitter_middle_down)
        splitter_main.addWidget(self.widget_middle_up)
        splitter_main.addWidget(self.widget_right)
    
