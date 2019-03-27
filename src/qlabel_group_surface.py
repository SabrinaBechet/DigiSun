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

import sys
import math
import numpy as np
import analyse_mode_bool
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
from PyQt4 import QtGui, QtCore
from PIL import Image, ImageQt

__author__ = "Mael Panouillot, Sabrina Bechet"

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
        self.scroll.setWidget(self.qlabel_group_surface)

        self.radius = 0
        self.start_x = 0
        self.start_y = 0
        self.center_x = 0
        self.center_y = 0

        qlabel_title = QtGui.QLabel("Area calculation")
        qlabel_title.setAlignment(QtCore.Qt.AlignCenter)
        qlabel_title.setContentsMargins(0, 5, 0, 5)

        threshold_slider = QtGui.QSlider(QtCore.Qt.Horizontal)
        threshold_slider.setRange(0, 256)
        threshold_slider.setTickPosition(QtGui.QSlider.TicksBelow)

        self.default_threshold = 225
        threshold_slider.setValue(self.default_threshold)
        threshold_slider.valueChanged.connect(
            lambda: self.update_img_threshold_value(threshold_slider.value()))
        self.threshold_linedit = QtGui.QLineEdit(str(self.default_threshold))
        self.threshold_linedit.setDisabled(True)
        self.threshold_linedit.setStyleSheet(
            "background-color: lightgray; color:black")

        threshold_layout = QtGui.QFormLayout()
        threshold_layout.addRow("Threshold selection:",
                                self.threshold_linedit)
       
        qlabel_general = QtGui.QLabel("General tools:")

        button_size = 50
        
        zoom_in_but = QtGui.QToolButton()
        zoom_in_but.setToolTip("zoom in")
        zoom_in_but.setIcon(QtGui.QIcon('../icons/Smashicons/zoom-in.png'))
        zoom_in_but.clicked.connect(
            lambda: self.qlabel_group_surface.zoom_in(2.))
        zoom_in_but.setMinimumWidth(button_size)
        zoom_in_but.setShortcut(QtGui.QKeySequence("Ctrl++"))
        
        zoom_out_but = QtGui.QToolButton()
        zoom_out_but.setToolTip("zoom out'")
        zoom_out_but.setIcon(QtGui.QIcon('../icons/Smashicons/zoom-out.png'))
        zoom_out_but.clicked.connect(
            lambda: self.qlabel_group_surface.zoom_in(1/2.))
        zoom_out_but.setMinimumWidth(button_size)
        zoom_out_but.setShortcut(QtGui.QKeySequence("Ctrl+-"))

        reset_but = QtGui.QToolButton()
        reset_but.setToolTip("reset'")
        reset_but.setIcon(QtGui.QIcon('../icons/Pixel_perfect/settings.png'))
        reset_but.clicked.connect(
            lambda: self.update_img_threshold_value(threshold_slider.value()))
        reset_but.setMinimumWidth(button_size)
        reset_but.setShortcut(QtGui.QKeySequence("Ctrl+z"))
        
        bigger_frame_but = QtGui.QToolButton()
        bigger_frame_but.setToolTip("expand frame")
        bigger_frame_but.setIcon(
            QtGui.QIcon('../icons/Freepik/thin-expand-arrows.png'))
        bigger_frame_but.clicked.connect(
            lambda: self.bigger_frame.emit())
        bigger_frame_but.setMinimumWidth(button_size)
        bigger_frame_but.setShortcut(QtGui.QKeySequence("Ctrl+e"))

        smaller_frame_but = QtGui.QToolButton()
        smaller_frame_but.setToolTip("reduce frame")
        smaller_frame_but.setIcon(
            QtGui.QIcon('../icons/Freepik/exit-full-screen-arrows.png'))
        smaller_frame_but.clicked.connect(
            lambda: self.smaller_frame.emit())
        smaller_frame_but.setMinimumWidth(button_size)
        smaller_frame_but.setShortcut(QtGui.QKeySequence("Ctrl+r"))

        draw_polygon_but = QtGui.QToolButton()
        draw_polygon_but.setToolTip("draw polygon")
        draw_polygon_but.setIcon(
            QtGui.QIcon('../icons/Darrio_Ferrando/polygon.png'))
        draw_polygon_but.clicked.connect(
            lambda: self.set_opposite_value(
                self.qlabel_group_surface.polygon_mode))
        draw_polygon_but.clicked.connect(
            self.qlabel_group_surface.draw_polygon)
        draw_polygon_but.setMinimumWidth(button_size)
        draw_polygon_but.setShortcut(QtGui.QKeySequence("Ctrl+d"))
        
        cut_polygon_but = QtGui.QToolButton()
        cut_polygon_but.setToolTip("cut polygon")
        cut_polygon_but.setIcon(
            QtGui.QIcon('../icons/Freepik/crop.png'))
        cut_polygon_but.clicked.connect(
            lambda: self.cut_polygon(threshold_slider.value()))
        cut_polygon_but.setMinimumWidth(button_size)
        cut_polygon_but.setShortcut(QtGui.QKeySequence("Ctrl+c"))

        draw_1pixel_black_but = QtGui.QToolButton()
        draw_1pixel_black_but.setToolTip("draw black pixel")
        draw_1pixel_black_but.setIcon(
            QtGui.QIcon('../icons/Freepik/1pix_black_square.png'))
        draw_1pixel_black_but.clicked.connect(
            lambda: self.set_opposite_value(
                self.qlabel_group_surface.black_pencil_mode))
        draw_1pixel_black_but.clicked.connect(lambda: self.draw_pencil(0))
        draw_1pixel_black_but.setMinimumWidth(button_size)
        draw_1pixel_black_but.setShortcut(QtGui.QKeySequence("Ctrl+x"))

        draw_1pixel_white_but = QtGui.QToolButton()
        draw_1pixel_white_but.setToolTip("draw white pixel")
        draw_1pixel_white_but.setIcon(
            QtGui.QIcon('../icons/Freepik/1pix_white_square.png'))
        draw_1pixel_white_but.clicked.connect(
            lambda: self.set_opposite_value(
                self.qlabel_group_surface.white_pencil_mode))
        draw_1pixel_white_but.clicked.connect(lambda: self.draw_pencil(255))
        draw_1pixel_white_but.setMinimumWidth(button_size)
        draw_1pixel_white_but.setShortcut(QtGui.QKeySequence("Ctrl+w"))

        bucket_white_fill_but = QtGui.QToolButton()
        bucket_white_fill_but.setToolTip("white bucket fill")
        bucket_white_fill_but.setIcon(
            QtGui.QIcon('../icons/Freepik/white-bucket.png'))
        bucket_white_fill_but.clicked.connect(
            lambda: self.set_opposite_value(
                self.qlabel_group_surface.white_bucket_mode))
        bucket_white_fill_but.clicked.connect(
            lambda: self.qlabel_group_surface.set_bucket_fill(
                self.current_array,
                0,
                255))
        bucket_white_fill_but.setMinimumWidth(button_size)
        bucket_white_fill_but.setShortcut(QtGui.QKeySequence("alt+w"))
        
        bucket_black_fill_but = QtGui.QToolButton()
        bucket_black_fill_but.setToolTip("black bucket fill" )
        bucket_black_fill_but.setIcon(
            QtGui.QIcon('../icons/Freepik/black-bucket.png'))
        bucket_black_fill_but.clicked.connect(
            lambda: self.set_opposite_value(
                self.qlabel_group_surface.black_bucket_mode))
        bucket_black_fill_but.clicked.connect(
            lambda: self.qlabel_group_surface.set_bucket_fill(
                self.current_array,
                255,
                0))
        bucket_black_fill_but.setMinimumWidth(button_size)
        bucket_black_fill_but.setShortcut(QtGui.QKeySequence("alt+x"))

        save_but = QtGui.QPushButton("sa&ve area")
        save_but.setToolTip("\'Ctrl+v\'")
        save_but.setShortcut(QtGui.QKeySequence("Ctrl+v"))
        save_but.clicked.connect(self.fill_surface_info)
        
        
        pixel_slider = QtGui.QSlider(QtCore.Qt.Horizontal)
        pixel_slider.setRange(0, 2)
        pixel_slider.setTickInterval(1)
        pixel_slider.setTickPosition(QtGui.QSlider.TicksBelow)

        self.pixel_linedit = QtGui.QLineEdit(str(1))
        self.pixel_linedit.setDisabled(True)
        self.pixel_linedit.setStyleSheet(
            "background-color: lightgray; color:black")

        pencil_size_layout = QtGui.QFormLayout()
        pencil_size_layout.addRow("Pencil size (pixel):",
                                   self.pixel_linedit)
        
        pixel_slider.valueChanged.connect(
            lambda: self.qlabel_group_surface.update_pixel_size(
                pixel_slider.value()))
        pixel_slider.valueChanged.connect(
            lambda: self.pixel_linedit.setText(str((pixel_slider.value() * 2) + 1)))
    
        self.qlabel_group_surface.polygon_mode.value_changed.connect(
            lambda: self.set_button_color(
                self.qlabel_group_surface.polygon_mode.value,
                draw_polygon_but))
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
        layout_general.addWidget(reset_but, 1, 2)
        layout_general.addWidget(bigger_frame_but, 1, 3)
        layout_general.addWidget(smaller_frame_but, 1, 4)
        layout_general.addWidget(draw_polygon_but, 1, 5)
        layout_general.addWidget(cut_polygon_but, 1, 6)
        layout_general.addWidget(bucket_white_fill_but, 2, 0)
        layout_general.addWidget(bucket_black_fill_but, 2, 1)
        layout_general.addWidget(draw_1pixel_white_but, 2, 2)
        layout_general.addWidget(draw_1pixel_black_but, 2, 3)
        layout_general.addWidget(save_but, 2, 4, 1, -1)

        layout_general.addLayout(pencil_size_layout, 3, 0, 1, 4)
        layout_general.addWidget(pixel_slider, 3, 4, 1, 3)
        

        form_layout = QtGui.QFormLayout()
        self.pixel_number_linedit = QtGui.QLineEdit()
        self.projected_surface_linedit = QtGui.QLineEdit()
        self.deprojected_surface_linedit = QtGui.QLineEdit()

        form_layout.addRow("Pixel Number:",
                           self.pixel_number_linedit)
        form_layout.addRow("Projected area (msd):",
                           self.projected_surface_linedit)
        form_layout.addRow("Deprojected area (msh):",
                           self.deprojected_surface_linedit)

        

        self.layout.addWidget(qlabel_title)
        self.layout.addLayout(threshold_layout)
        self.layout.addWidget(threshold_slider)
        self.layout.addLayout(layout_general)
        #self.layout.addLayout(pencil_size_layout)
        #self.layout.addWidget(pixel_slider)

        self.layout.addWidget(self.scroll)
        self.layout.addLayout(form_layout)
        #self.layout.addWidget(save_but)

        self.qlabel_group_surface.array_changed.connect(
            lambda: self.set_img(self.qlabel_group_surface.array))

    def set_opposite_value(self, mode):
        if mode.value:
            mode.value = False
        else:
            mode.value = True

    def set_button_color(self, mode_bool, but):
        if mode_bool is True:
            but.setStyleSheet("background-color: lightblue")
        elif mode_bool is False:
            but.setStyleSheet("background-color: lightgray")

    def draw_pencil(self, new_value):
        self.qlabel_group_surface.set_pencil_array(
            self.current_array, new_value)

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
        #self.qlabel_group_surface.zoom_in(2.)
        self.qlabel_group_surface.polygon_mode.value = False
        self.qlabel_group_surface.white_pencil_mode.value = False
        self.qlabel_group_surface.black_pencil_mode.value = False
        self.qlabel_group_surface.white_bucket_mode.value = False
        self.qlabel_group_surface.black_bucket_mode.value = False
        self.selection_array = np_array
        self.set_img(self.threshold(self.default_threshold))
        self.qlabel_group_surface.pointsList = []

    def threshold(self, value):
        selection_array_thresh =  np.copy(self.selection_array)
        selection_array_thresh[np.where(selection_array_thresh>value)] = 0
        selection_array_thresh[np.where(selection_array_thresh>0)] = 255

        return selection_array_thresh

    def set_img(self, img):
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

    def count_pixel(self, img):
        return np.count_nonzero(img)

    def fill_surface_info(self):
        self.drawing.group_lst[self.index].set_surface(self.nb_pixel,
                                                       self.projected_area,
                                                       self.deprojected_area)
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

            deprojected_area_sum = 0
            for i in range(len(pos_x)):
                distance_from_center = math.sqrt(
                    (pos_x[i] - self.center_x)**2 +
                    (pos_y[i] - self.center_y)**2)

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
            return nb_pixel * math.pow(10, 6)/(math.pi * self.radius**2)
        else:
            return 0

    def update_frame_surface(self, radius, step=0):
        """
        change the size of the frame around the surface selection.
        """
        div_factor = self.radius_division_factor
        div_factor_tmp = div_factor + step * 100

        if div_factor_tmp:
            frame_size_tmp = math.floor(radius / div_factor_tmp) * 100
            if frame_size_tmp > 0:
                frame_size = frame_size_tmp
                self.radius_division_factor = div_factor_tmp

        else:
            frame_size = math.floor(radius / self.radius_division_factor) * 100

        return frame_size


class QLabelGroupSurface(QtGui.QLabel):

    array_changed = QtCore.pyqtSignal()

    def __init__(self):
        super(QLabelGroupSurface, self).__init__()

        # used for the reset
        self.original_pixmap = QtGui.QPixmap()
        # used for the polygon drawing
        self.first_pixamp_polygon = QtGui.QPixmap()

        self.width_scale = 300
        self.height_scale = 300
        self.scaling_factor = 1
        self.pointsList = []

        self.polygon_mode = analyse_mode_bool.analyseModeBool(False)
        self.white_pencil_mode = analyse_mode_bool.analyseModeBool(False)
        self.black_pencil_mode = analyse_mode_bool.analyseModeBool(False)
        self.white_bucket_mode = analyse_mode_bool.analyseModeBool(False)
        self.black_bucket_mode = analyse_mode_bool.analyseModeBool(False)

        self.max_count = 0
        self.pixel_size = 0

    def zoom_in(self, scaling_factor):
        self.width_scale *= scaling_factor
        self.height_scale *= scaling_factor
        self.scaling_factor *= scaling_factor
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
        im8 = Image.fromarray(np_img)
        imQt = QtGui.QImage(ImageQt.ImageQt(im8))

        return QtGui.QPixmap.fromImage(imQt)

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
                painter.drawLine(self.pointsList[i-1], self.pointsList[i])

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
                                          self.height_scale)),
                           int(math.floor(a.x() * array.shape[0] /
                                          self.width_scale)))
                          for a in self.pointsList]

        polygon = Polygon(polygon_points)
        count = 0
        for index, value in np.ndenumerate(array):
            if value > 0:
                count += 1
                if polygon.contains(Point(index)) is False:
                    array[index] = 0

        return array

    def set_pencil_array(self, array, new_value):
        self.polygon_mode.value = False
        if new_value == 0:
            self.white_pencil_mode.value = False
        else:
            self.black_pencil_mode.value = False
        self.white_bucket_mode.value = False
        self.black_bucket_mode.value = False

        self.array = array
        self.new_value = new_value

    def set_bucket_fill(self, array, old_value, new_value):
        self.polygon_mode.value = False
        self.white_pencil_mode.value = False
        self.black_pencil_mode.value = False
        if new_value == 0:
            self.white_bucket_mode.value = False
        else:
            self.black_bucket_mode.value = False

        self.array = array
        self.new_value = new_value
        self.old_value = old_value

    def bucket_fill(self, position_x, position_y, count=0):
        try:
            self.max_count = max(self.max_count, count)
            if self.array[position_x, position_y] == self.new_value:
                return
            self.array[position_x, position_y] = self.new_value
            if position_x > 0:
                self.bucket_fill(position_x - 1, position_y, count+1)
            if position_x < self.array.shape[1] - 1:
                self.bucket_fill(position_x + 1, position_y, count+1)
            if position_y > 0:
                self.bucket_fill(position_x, position_y - 1, count+1)
            if position_y < self.array.shape[0] - 1:
                self.bucket_fill(position_x, position_y + 1, count+1)

        except RuntimeError:
            print("Time too long, check that the border is closed!")

    def update_pixel_size(self, pixel_size):
        self.pixel_size = pixel_size
            
    def mousePressEvent(self, QMouseEvent):
        position = QMouseEvent.pos()
        if (self.white_pencil_mode.value or self.black_pencil_mode.value or
                self.white_bucket_mode.value or self.black_bucket_mode.value):
            pos_y_scaled = int(math.floor(position.y() * self.array.shape[1] /
                                          self.height_scale))
            pos_x_scaled = int(math.floor(position.x() * self.array.shape[0] /
                                          self.width_scale))
            y_min = pos_y_scaled - self.pixel_size
            y_max = pos_y_scaled + self.pixel_size + 1
            x_min = pos_x_scaled - self.pixel_size
            x_max = pos_x_scaled + self.pixel_size + 1

        if self.polygon_mode.value:
            self.draw_polygon(position)

        elif self.white_pencil_mode.value or self.black_pencil_mode.value:
            self.array[y_min:y_max, x_min:x_max] = self.new_value
            self.array_changed.emit()

        elif self.white_bucket_mode.value or self.black_bucket_mode.value:
            self.bucket_fill(pos_y_scaled, pos_x_scaled)
            self.array_changed.emit()

    def mouseMoveEvent(self, QMouseEvent):
        if self.white_pencil_mode.value or self.black_pencil_mode.value:
            position = QMouseEvent.pos()
            pos_y_scaled = int(math.floor(position.y() * self.array.shape[1] /
                                          self.height_scale))
            pos_x_scaled = int(math.floor(position.x() * self.array.shape[0] /
                                          self.width_scale))
            y_min = pos_y_scaled - self.pixel_size
            y_max = pos_y_scaled + self.pixel_size + 1
            x_min = pos_x_scaled - self.pixel_size
            x_max = pos_x_scaled + self.pixel_size + 1

            self.array[y_min:y_max, x_min:x_max] = self.new_value
            self.array_changed.emit()

    def mouseReleaseEvent(self, QMouseEvent):
        if self.white_pencil_mode.value or self.black_pencil_mode.value:
            position = QMouseEvent.pos()
            pos_y_scaled = int(math.floor(position.y() * self.array.shape[1] /
                                          self.height_scale))
            pos_x_scaled = int(math.floor(position.x() * self.array.shape[0] /
                                          self.width_scale))
            y_min = pos_y_scaled - self.pixel_size
            y_max = pos_y_scaled + self.pixel_size + 1
            x_min = pos_x_scaled - self.pixel_size
            x_max = pos_x_scaled + self.pixel_size + 1

            self.array[y_min:y_max, x_min:x_max] = self.new_value
            self.array_changed.emit()
