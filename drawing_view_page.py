# !/usr/bin/env python
# -*-coding:utf-8-*-
"""
DigiSun: a software to transform sunspot drawings into exploitable data. It allows to scan drawings, extract its information and store it in a database.
Copyright (C) 2019 Sabrina Bechet at Royal Observatory of Belgium (ROB)

This file is part of DigiSun.

DigiSun is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

DigiSun is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with DigiSun.  If not, see <https://www.gnu.org/licenses/>.
"""

from PyQt4 import QtGui, QtCore


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
        self.scroll_widget_left_up.setWidgetResizable(True)
        self.widget_left_up = QtGui.QWidget()
        self.scroll_widget_left_up.setMinimumWidth(left_column_maximum_width)
        #self.scroll_widget_left_up.setMaximumHeight(self.height()/2.)
        self.widget_left_up.setStyleSheet("background-color:lightgray;")
        self.scroll_widget_left_up.setWidget(self.widget_left_up)

        self.widget_left_up_layout = QtGui.QVBoxLayout()
        self.widget_left_up_layout.setContentsMargins(0, 0, 0, 0)
        self.widget_left_up_layout.setSpacing(0)
        self.widget_left_up_layout.setAlignment(QtCore.Qt.AlignTop)
        self.widget_left_up.setLayout(self.widget_left_up_layout)

        self.widget_left_middle = QtGui.QWidget()
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
        self.widget_left_down_bis.setMaximumHeight(250)
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
        self.widget_middle_up.setStyleSheet("background-color:lightgray;")
        self.widget_middle_up_layout = QtGui.QVBoxLayout()
        self.widget_middle_up_layout.setContentsMargins(0, 0, 0, 0)
        self.widget_middle_up_layout.setSpacing(10)
        self.widget_middle_up_layout.setAlignment(QtCore.Qt.AlignTop)
        self.widget_middle_up.setLayout(self.widget_middle_up_layout)

        self.widget_right = QtGui.QWidget()
        self.widget_right.setStyleSheet("background-color:gray;")
        self.widget_right_layout = QtGui.QVBoxLayout()
        self.widget_right_layout.setContentsMargins(0, 0, 0, 0)
        self.widget_right_layout.setSpacing(0)
        self.widget_right.setLayout(self.widget_right_layout)

        # for up and down
        vertical_splitter = QtGui.QSplitter(QtCore.Qt.Vertical, self)
        self.layout().addWidget(vertical_splitter)
        vertical_splitter.addWidget(self.scroll_widget_left_up)
        vertical_splitter.addWidget(self.widget_left_middle)
        vertical_splitter.addWidget(self.widget_left_down)
        vertical_splitter.addWidget(self.widget_left_down_bis)

        # for left and right
        horizontal_splitter = QtGui.QSplitter(QtCore.Qt.Horizontal, self)
        self.layout().addWidget(horizontal_splitter)
        horizontal_splitter.addWidget(vertical_splitter)
        horizontal_splitter.addWidget(self.widget_middle_up)
        horizontal_splitter.addWidget(self.widget_right)
