# !/usr/bin/env python
# -*-coding:utf-8-*-
import time
import numpy as np
import math
import coordinates
import analyse_mode_bool
from PyQt4 import QtGui, QtCore
from PIL import Image
from PIL.ImageQt import ImageQt


def rgb2gray(rgb):
    return np.dot(rgb[..., :3], [0.299, 0.587, 0.114])


class QLabelDrawing(QtGui.QLabel):
    """
    Class to show the drawing,
    display the grid, groups, dipoles,..
    and interact with it
    It contains:
    - text (in case no pixmap)
    - drawing_pixMap : the pixamp with no scaling
    - width_scale : the width of the image to show (depending on the zoom)
    - height_scale : the height of the image to show (depending on the zoom)

    note: properties make functions look like attribute
    """

    """
    A signal (specifically an unbound signal) is an attribute of a class
    that is a sub-class of QObject.
    When a signal is referenced as an attribute of an instance of the class
    then PyQt5 automatically
    binds the instance to the signal in order to create a bound signal.
    """
    drawing_clicked = QtCore.pyqtSignal()
    center_clicked = QtCore.pyqtSignal()
    north_clicked = QtCore.pyqtSignal()
    group_added = QtCore.pyqtSignal()
    dipole_added = QtCore.pyqtSignal()

    def __init__(self):

        super(QLabelDrawing, self).__init__()

        self.setAlignment(QtCore.Qt.AlignCenter)

        self.width_scale = 1000
        self.height_scale = 1000

        # overlay mode
        self.quick_zoom = analyse_mode_bool.analyseModeBool(False)
        self.large_grid_overlay = analyse_mode_bool.analyseModeBool(True)
        self.small_grid_overlay = analyse_mode_bool.analyseModeBool(False)
        self.grid_draw_point = False
        self.grid_interpolate_point = True
        self.group_visu = analyse_mode_bool.analyseModeBool(True)
        self.dipole_visu = analyse_mode_bool.analyseModeBool(False)

        # helper mode
        self.helper_grid = analyse_mode_bool.analyseModeBool(False)
        self.helper_grid_position_clicked = False

        # action mode
        # only one action mode at the time!
        self.calibration_mode = analyse_mode_bool.analyseModeBool(False)
        self.center_done = False
        self.north_done = False
        self.add_group_mode = analyse_mode_bool.analyseModeBool(False)
        self.add_dipole_mode = analyse_mode_bool.analyseModeBool(False)
        self.surface_mode = analyse_mode_bool.analyseModeBool(False)

        self.group_visu_index = 0

        self.scaling_factor = 1
        self.dipole_points = []
        self.dipole_angles = []

        self.frame_size = 0

    def set_msg_no_entry(self):
        my_font = QtGui.QFont("Comic Sans MS", 20)
        self.setText('No drawings corresponding to this entry')
        self.setFont(my_font)

        self.setContentsMargins(0, 0, 0, 0)

    def get_img_array(self):
        """
        open an image specified with file_path and
        return its corresponding numpy array
        """
        try:
            img = Image.open(self.file_path)
            im_arr = np.asarray(img)
            try:
                if im_arr.shape[2] == 3:
                    im_arr = rgb2gray(im_arr)
            except IndexError:
                print("the original file is in L format..")

            return im_arr

        except IOError:
            print("this file does not exist")
            return

    def set_img(self):
        try:
            img = Image.open(self.file_path)
            self.drawing_width = img.size[0]
            self.drawing_height = img.size[1]
            qim = ImageQt(img)  # convert PIL image to a PIL.ImageQt object
            self.drawing_pixMap = QtGui.QPixmap.fromImage(qim)

        except IOError:
            print("did not find the image!")
            return

        self.img_mean_dimension = (self.drawing_width +
                                   self.drawing_height)/2.

        self.pen_width = int(self.drawing_height *
                             1000/(700.*self.height_scale))

        painter = QtGui.QPainter()
        painter.begin(self.drawing_pixMap)

        if (self.helper_grid_position_clicked and
                self.current_drawing.calibrated):
            pen_helper_grid = QtGui.QPen(QtCore.Qt.gray)
            pen_helper_grid.setWidth(self.pen_width)
            pen_helper_grid.setStyle(QtCore.Qt.DotLine)
            painter.setPen(pen_helper_grid)

            grid_interval = [-7.5, -5, -1.25, 1.25, 5,  7.5]

            for interval in grid_interval:
                x_lst_0_180, y_lst_0_180 = self.get_line_on_sphere(
                    self.HGC_longitude * 180/math.pi + 90 - interval,
                    self.current_drawing.calibrated_radius,
                    "longitude",
                    self.HGC_latitude * 180/math.pi + 90 - 7.5,
                    self.HGC_latitude * 180/math.pi + 90 + 8.1,
                    0.1)
                if len(x_lst_0_180) > 0:
                    path_0_180 = self.set_drawing_path_small_step(x_lst_0_180,
                                                                  y_lst_0_180)
                    painter.drawPath(path_0_180)
                point = QtCore.QPointF(
                    self.current_drawing.calibrated_center.x +
                    x_lst_0_180[0] - 5,
                    self.current_drawing.calibrated_center.y +
                    y_lst_0_180[0] + 20)
                font = QtGui.QFont()
                font.setPixelSize(self.img_mean_dimension/200.)
                painter.setFont(font)
                painter.drawText(point, str(interval))
                """for i in range(len(x_lst_0_180)):
                painter.drawPoint(
                self.current_drawing.calibrated_center.x + x_lst_0_180[i],
                self.current_drawing.calibrated_center.y + y_lst_0_180[i])
                """

            for interval in grid_interval:
                x_lst_0_180, y_lst_0_180 = self.get_line_on_sphere(
                    self.HGC_latitude * 180/math.pi + 90 - interval,
                    self.current_drawing.calibrated_radius,
                    "latitude",
                    self.HGC_longitude * 180/math.pi + 90 - 7.5,
                    self.HGC_longitude * 180/math.pi + 90 + 8.1,
                    0.1)
                if len(x_lst_0_180) > 0:
                    path_0_180 = self.set_drawing_path_small_step(x_lst_0_180,
                                                                  y_lst_0_180)
                    painter.drawPath(path_0_180)
                """
                for i in range(len(x_lst_0_180)):
                    painter.drawPoint(
                self.current_drawing.calibrated_center.x + x_lst_0_180[i],
                self.current_drawing.calibrated_center.y + y_lst_0_180[i])
                """
            self.helper_grid_position_clicked = False

        if ((self.large_grid_overlay.value or
             self.small_grid_overlay.value) and
                self.current_drawing.calibrated):
            pen_border = QtGui.QPen(QtCore.Qt.blue)
            pen_border.setWidth(self.pen_width)
            pen_border.setStyle(QtCore.Qt.SolidLine)
            pen_special_line = QtGui.QPen(QtCore.Qt.magenta)
            pen_special_line.setWidth(self.pen_width)
            pen_grid = QtGui.QPen()
            pen_grid.setColor(QtGui.QColor(22, 206, 255))
            pen_grid.setWidth(self.pen_width)
            pen_grid.setStyle(QtCore.Qt.SolidLine)
            large_pen = QtGui.QPen(QtCore.Qt.red)
            large_pen.setWidth(5)
            large_pen.setStyle(QtCore.Qt.SolidLine)

            painter.setPen(pen_border)
            painter.drawEllipse(
                QtCore.QPointF(self.current_drawing.calibrated_center.x,
                               self.current_drawing.calibrated_center.y),
                self.current_drawing.calibrated_radius,
                self.current_drawing.calibrated_radius)

            if self.large_grid_overlay.value:
                angle_array_longitude_range = np.arange(0, 190, 30)
                angle_array_latitude_range = np.arange(-180, 190, 30)
            else:
                angle_array_longitude_range = np.arange(0, 190, 10)
                angle_array_latitude_range = np.arange(-180, 190, 10)

            for longitude in angle_array_longitude_range:
                if longitude == 90:
                    if (self.current_drawing.angle_L < 90 or
                            self.current_drawing.angle_L > 270):
                        pen_special_line.setStyle(QtCore.Qt.SolidLine)
                        painter.setPen(pen_special_line)
                    else:
                        pen_special_line.setStyle(QtCore.Qt.DotLine)
                        painter.setPen(pen_special_line)
                else:
                    painter.setPen(pen_grid)

                x_lst_0_180, y_lst_0_180 = self.get_line_on_sphere(
                    longitude,
                    self.current_drawing.calibrated_radius,
                    "longitude",
                    0,
                    180)

                x_lst_minus180_0, y_lst_minus180_0 = self.get_line_on_sphere(
                    longitude,
                    self.current_drawing.calibrated_radius,
                    "longitude",
                    -180,
                    0)

                if self.grid_interpolate_point:
                    start_interpol = time.clock()
                    if len(x_lst_0_180) > 0:
                        path_0_180 = self.set_drawing_path(x_lst_0_180,
                                                           y_lst_0_180)
                        painter.drawPath(path_0_180)

                    if len(x_lst_minus180_0) > 0:
                        path_minus180_0 = self.set_drawing_path(
                            x_lst_minus180_0,
                            y_lst_minus180_0)
                        painter.drawPath(path_minus180_0)

                    end_interpol = time.clock()
                    # print("********time for interpolation for longitude",
                    # end_interpol - start_interpol)

                if self.grid_draw_point:
                    start_draw_point = time.clock()
                    for i in range(len(x_lst_0_180)):
                        painter.drawPoint(
                            self.current_drawing.calibrated_center.x +
                            x_lst_0_180[i],
                            self.current_drawing.calibrated_center.y +
                            y_lst_0_180[i])
                    for i in range(len(x_lst_minus180_0)):
                            painter.drawPoint(
                                self.current_drawing.calibrated_center.x +
                                x_lst_minus180_0[i],
                                self.current_drawing.calibrated_center.y +
                                y_lst_minus180_0[i])
                    end_draw_point = time.clock()
                    # print("********time for draw point ",
                    # end_draw_point - start_draw_point)

            for latitude in angle_array_latitude_range:
                if latitude == 90 or latitude == -90:
                    pen_special_line.setStyle(QtCore.Qt.SolidLine)
                    painter.setPen(pen_special_line)
                else:
                    painter.setPen(pen_grid)

                (x_lst_0_90, y_lst_0_90) = self.get_line_on_sphere(
                    latitude,
                    self.current_drawing.calibrated_radius,
                    "latitude",
                    0,
                    90)

                (x_lst_minus90_0, y_lst_minus90_0) = self.get_line_on_sphere(
                    latitude,
                    self.current_drawing.calibrated_radius,
                    "latitude",
                    -90,
                    0)

                if self.grid_interpolate_point:
                    start_interpol = time.clock()
                    if len(x_lst_0_90) > 0:
                        path_0_90 = self.set_drawing_path(x_lst_0_90,
                                                          y_lst_0_90)
                        painter.drawPath(path_0_90)

                    if len(x_lst_minus90_0) > 0:
                        path_minus90_0 = self.set_drawing_path(x_lst_minus90_0,
                                                               y_lst_minus90_0)
                        painter.drawPath(path_minus90_0)

                    end_interpol = time.clock()
                    # print("********time for interpolation for latitude",
                    # end_interpol - start_interpol)

                if self.grid_draw_point:
                    for i in range(len(x_lst_0_90)):
                        painter.drawPoint(
                            self.current_drawing.calibrated_center.x +
                            x_lst_0_90[i],
                            self.current_drawing.calibrated_center.y +
                            y_lst_0_90[i])

                    for i in range(len(x_lst_minus90_0)):
                        painter.drawPoint(
                            self.current_drawing.calibrated_center.x +
                            x_lst_minus90_0[i],
                            self.current_drawing.calibrated_center.y +
                            y_lst_minus90_0[i])

            painter.setPen(large_pen)
            painter.drawPoint(self.current_drawing.calibrated_center.x,
                              self.current_drawing.calibrated_center.y)
            painter.drawPoint(self.current_drawing.calibrated_north.x,
                              self.current_drawing.calibrated_north.y)

        if ((self.group_visu.value or self.surface_mode.value) and
                self.current_drawing.calibrated):
            pen_border = QtGui.QPen(QtCore.Qt.blue)
            pen_border.setWidth(self.pen_width)
            pen_border.setStyle(QtCore.Qt.DotLine)
            pen_selected = QtGui.QPen(QtCore.Qt.DotLine)
            pen_selected.setWidth(self.pen_width * 1.5)
            pen_selected.setColor(QtGui.QColor(77, 185, 88))
            large_pen = QtGui.QPen(QtCore.Qt.blue)
            large_pen.setWidth(self.pen_width * 2)
            large_pen.setStyle(QtCore.Qt.SolidLine)

            for i in range(self.current_drawing.group_count):
                if (self.current_drawing.group_lst[i].longitude and
                        self.current_drawing.group_lst[i].latitude):
                    radius = self.drawing_height / 50.
                    painter.setPen(pen_border)

                    if self.group_visu_index == i:
                        painter.setPen(pen_selected)
                        radius = self.drawing_height / 50.
                        pen_selected.setColor(QtGui.QColor(77, 185, 88))
                    else:
                        large_pen.setColor(QtCore.Qt.blue)
                        pen_selected.setColor(QtGui.QColor("transparent"))

                    # here we could directly take x, y from the database
                    # posX = self.current_drawing.group_lst[i].posX
                    # posY = self.current_drawing.group_lst[i].posY
                    # but...
                    # we calculate the x, y and uses it as a visual check that
                    # the calcualtion is correct
                    x, y, z = coordinates.cartesian_from_HGC_upper_left_origin(
                        self.current_drawing.calibrated_center.x,
                        self.current_drawing.calibrated_center.y,
                        self.current_drawing.calibrated_north.x,
                        self.current_drawing.calibrated_north.y,
                        self.current_drawing.group_lst[i].longitude,
                        self.current_drawing.group_lst[i].latitude,
                        self.current_drawing.angle_P,
                        self.current_drawing.angle_B,
                        self.current_drawing.angle_L,
                        self.drawing_height)

                    if self.surface_mode.value:
                        painter.setPen(pen_selected)
                        x_min = int(x - self.frame_size/2)
                        y_min = int(y - self.frame_size/2)
                        painter.drawRect(
                            x_min, y_min, self.frame_size, self.frame_size)
                    else:
                        pen_point = QtGui.QPen(QtCore.Qt.blue)
                        pen_point.setStyle(QtCore.Qt.SolidLine)
                        pen_point.setWidth(50000 / (self.height_scale))
                        painter.setPen(large_pen)
                        painter.drawPoint(QtCore.QPointF(x, y))

                        painter.setPen(pen_selected)
                        painter.drawEllipse(
                            QtCore.QPointF(x, y), radius, radius)

        if (self.dipole_visu.value and self.current_drawing.calibrated):
            pen_point = QtGui.QPen(QtCore.Qt.blue)
            pen_point.setWidth(self.pen_width * 2)
            pen_line = QtGui.QPen(QtCore.Qt.blue)
            pen_line.setWidth(self.pen_width/2.)
            pen_point_selected = QtGui.QPen()
            pen_point_selected.setWidth(self.pen_width * 2)
            pen_point_selected.setColor(QtGui.QColor(77, 185, 88))
            pen_line_selected = QtGui.QPen()
            pen_line_selected.setWidth(self.pen_width / 2.)
            pen_line_selected.setColor(QtGui.QColor(77, 185, 88))

            for i in range(self.current_drawing.group_count):
                zurich_type = self.current_drawing.group_lst[i].zurich.upper()
                if (zurich_type in ["B", "C", "D", "E", "F", "G", "X"] and
                        self.current_drawing.group_lst[i].dipole1_long):
                    # here we calculate x, y from the HGC coordinates as a test
                    (dip1_x,
                     dip1_y,
                     dip1_z) = coordinates\
                         .cartesian_from_HGC_upper_left_origin(
                             self.current_drawing.calibrated_center.x,
                             self.current_drawing.calibrated_center.y,
                             self.current_drawing.calibrated_north.x,
                             self.current_drawing.calibrated_north.y,
                             self.current_drawing.group_lst[i].dipole1_long,
                             self.current_drawing.group_lst[i].dipole1_lat,
                             self.current_drawing.angle_P,
                             self.current_drawing.angle_B,
                             self.current_drawing.angle_L,
                             self.drawing_height)

                    # here we calculate x, y from the HGC coordinates as a test
                    (dip2_x,
                     dip2_y,
                     dip2_z) = coordinates\
                        .cartesian_from_HGC_upper_left_origin(
                             self.current_drawing.calibrated_center.x,
                             self.current_drawing.calibrated_center.y,
                             self.current_drawing.calibrated_north.x,
                             self.current_drawing.calibrated_north.y,
                             self.current_drawing.group_lst[i].dipole2_long,
                             self.current_drawing.group_lst[i].dipole2_lat,
                             self.current_drawing.angle_P,
                             self.current_drawing.angle_B,
                             self.current_drawing.angle_L,
                             self.drawing_height)

                    painter.setPen(pen_point)
                    if self.group_visu_index == i:
                        painter.setPen(pen_point_selected)
                    painter.drawPoints(QtCore.QPointF(dip1_x, dip1_y),
                                       QtCore.QPointF(dip2_x, dip2_y))
                    painter.setPen(pen_line)
                    if self.group_visu_index == i:
                        painter.setPen(pen_line_selected)
                    painter.drawLine(dip1_x, dip1_y, dip2_x, dip2_y)

        if (self.add_dipole_mode.value and self.current_drawing.calibrated):
            pen_point = QtGui.QPen(QtCore.Qt.blue)
            pen_point.setWidth(self.pen_width * 2)
            pen_line = QtGui.QPen(QtCore.Qt.blue)
            pen_line.setWidth(self.pen_width/2.)
            pen_point_selected = QtGui.QPen()
            pen_point_selected.setWidth(self.pen_width * 2)
            pen_point_selected.setColor(QtGui.QColor(77, 185, 88))
            pen_line_selected = QtGui.QPen()
            pen_line_selected.setWidth(self.pen_width / 2.)
            pen_line_selected.setColor(QtGui.QColor(77, 185, 88))

            if len(self.dipole_points) == 2:
                painter.drawPoint(
                    QtCore.QPointF(self.dipole_points[0],
                                   self.dipole_points[1]))

            elif len(self.dipole_points) == 4:
                painter.drawPoint(
                    QtCore.QPointF(self.dipole_points[0],
                                   self.dipole_points[1]))
                painter.drawPoint(
                    QtCore.QPointF(self.dipole_points[2],
                                   self.dipole_points[3]))
                painter.drawLine(self.dipole_points[0], self.dipole_points[1],
                                 self.dipole_points[2], self.dipole_points[3])
                self.dipole_points = []
                self.dipole_angles = []
            else:
                print("problem with the number of points")
                print(len(self.dipole_points))
                self.dipole_points = []
                self.dipole_angles = []

        painter.end()
        pixmap = self.drawing_pixMap.scaled(int(self.width_scale),
                                            int(self.height_scale),
                                            QtCore.Qt.KeepAspectRatio)

        self.setPixmap(pixmap)

    def set_drawing_path_small_step(self, x_lst, y_lst):
        """ Join a list of points by step of 1.
        Input : the list of poits
        Output : the path
        """
        start_point = QtCore.QPointF(
            self.current_drawing.calibrated_center.x + x_lst[0],
            self.current_drawing.calibrated_center.y + y_lst[0])
        path = QtGui.QPainterPath(start_point)

        for i in range(1, len(x_lst)-1, 1):
            start_point = QtCore.QPointF(
                self.current_drawing.calibrated_center.x + x_lst[i-1],
                self.current_drawing.calibrated_center.y + y_lst[i-1])
            middle_point = QtCore.QPointF(
                self.current_drawing.calibrated_center.x + x_lst[i],
                self.current_drawing.calibrated_center.y + y_lst[i])
            end_point = QtCore.QPointF(
                self.current_drawing.calibrated_center.x + x_lst[i+1],
                self.current_drawing.calibrated_center.y + y_lst[i+1])
            path.cubicTo(start_point, middle_point, end_point)

        return path

    def set_drawing_path(self, x_lst, y_lst):
        """ Join a list of points by step of 1 for the beginning and the end.
        Larger step in the middle. This is used for the grid
        Input : the list of poits
        Output : the path
        """
        start_point = QtCore.QPointF(
            self.current_drawing.calibrated_center.x + x_lst[0],
            self.current_drawing.calibrated_center.y + y_lst[0])
        path = QtGui.QPainterPath(start_point)

        if len(x_lst) < 10:
            for i in range(1, len(x_lst)-1, 1):
                start_point = QtCore.QPointF(
                    self.current_drawing.calibrated_center.x + x_lst[i-1],
                    self.current_drawing.calibrated_center.y + y_lst[i-1])
                middle_point = QtCore.QPointF(
                    self.current_drawing.calibrated_center.x + x_lst[i],
                    self.current_drawing.calibrated_center.y + y_lst[i])
                end_point = QtCore.QPointF(
                    self.current_drawing.calibrated_center.x + x_lst[i+1],
                    self.current_drawing.calibrated_center.y + y_lst[i+1])
                path.cubicTo(start_point, middle_point, end_point)

        if len(x_lst) > 10:
            for i in range(1, 10, 1):
                start_point = QtCore.QPointF(
                    self.current_drawing.calibrated_center.x + x_lst[i-1],
                    self.current_drawing.calibrated_center.y + y_lst[i-1])
                middle_point = QtCore.QPointF(
                    self.current_drawing.calibrated_center.x + x_lst[i],
                    self.current_drawing.calibrated_center.y + y_lst[i])
                end_point = QtCore.QPointF(
                    self.current_drawing.calibrated_center.x + x_lst[i+1],
                    self.current_drawing.calibrated_center.y + y_lst[i+1])
                path.cubicTo(start_point, middle_point, end_point)

        if len(x_lst) > 20:
            for i in range(15, len(x_lst) - 20, 10):
                start_point = QtCore.QPointF(
                    self.current_drawing.calibrated_center.x + x_lst[i-5],
                    self.current_drawing.calibrated_center.y + y_lst[i-5])
                middle_point = QtCore.QPointF(
                    self.current_drawing.calibrated_center.x + x_lst[i],
                    self.current_drawing.calibrated_center.y + y_lst[i])
                end_point = QtCore.QPointF(
                    self.current_drawing.calibrated_center.x + x_lst[i+5],
                    self.current_drawing.calibrated_center.y + y_lst[i+5])
                path.cubicTo(start_point, middle_point, end_point)

            for i in range(len(x_lst)-19, len(x_lst)-1, 1):
                start_point = QtCore.QPointF(
                    self.current_drawing.calibrated_center.x + x_lst[i-1],
                    self.current_drawing.calibrated_center.y + y_lst[i-1])
                middle_point = QtCore.QPointF(
                    self.current_drawing.calibrated_center.x + x_lst[i],
                    self.current_drawing.calibrated_center.y + y_lst[i])
                end_point = QtCore.QPointF(
                    self.current_drawing.calibrated_center.x + x_lst[i+1],
                    self.current_drawing.calibrated_center.y + y_lst[i+1])
                path.cubicTo(start_point, middle_point, end_point)

        return path

    def get_spherical_coord_latitude(self, longitude, radius,
                                     range_min, range_max, step=1):
        spherical_coord_lst = []
        scale = 100  # to have a range integer,even for decimal value (ex 1.25)
        for latitude in range(int(range_min * scale),
                              int(range_max * scale),
                              int(step * scale)):
            spherical_coord = coordinates.Spherical(radius,
                                                    math.pi/2 -
                                                    latitude/scale *
                                                    math.pi/180.,
                                                    longitude * math.pi/180.)
            spherical_coord_lst.append(spherical_coord)
        return spherical_coord_lst

    def get_spherical_coord_longitude(self, latitude, radius,
                                      range_min, range_max, step=1):
        spherical_coord_lst = []
        scale = 100  # to have a range integer,even for decimal value (ex 1.25)
        for longitude in range(int(range_min * scale),
                               int(range_max * scale),
                               int(step * scale)):
            spherical_coord = coordinates.Spherical(radius,
                                                    math.pi/2 - latitude *
                                                    math.pi/180.,
                                                    longitude/scale *
                                                    math.pi/180.)
            spherical_coord_lst.append(spherical_coord)
        return spherical_coord_lst

    def get_line_on_sphere(self, angle, radius,
                           line_type, range_min, range_max, step=1):
        """
        get the list of x and y position along a
        given line on a sphere (longitude or latitude) for the other line
        (respectively latitude or longitude) of the angle given
        by the first parameter.
        Input:
        - angle of the line
        - radius of the circle
        - range min of the line
        - rangel max of the line
        - step in angle (degrees)
        """
        x_array = np.array([])
        y_array = np.array([])
        if line_type == 'latitude':
            spherical_coord_lst = self.get_spherical_coord_latitude(angle,
                                                                    radius,
                                                                    range_min,
                                                                    range_max,
                                                                    step)
        elif line_type == 'longitude':
            spherical_coord_lst = self.get_spherical_coord_longitude(angle,
                                                                     radius,
                                                                     range_min,
                                                                     range_max,
                                                                     step)

        center = coordinates.Cartesian(
            self.current_drawing.calibrated_center.x,
            self.current_drawing.calibrated_center.y)
        north = coordinates.Cartesian(
            self.current_drawing.calibrated_north.x,
            self.current_drawing.calibrated_north.y)

        # angle given in radian
        angle_calibration = center.angle_from_y_axis(north)

        for spherical_coord in spherical_coord_lst:
            x, y, z = spherical_coord.convert_to_cartesian()
            cart_coord = coordinates.Cartesian(x, y, z)

            cart_coord.rotate_around_y(
                self.current_drawing.angle_L * math.pi/180.)
            cart_coord.rotate_around_x(
                -self.current_drawing.angle_B * math.pi/180.)
            cart_coord.rotate_around_z(
                self.current_drawing.angle_P * math.pi/180. -
                angle_calibration)

            if cart_coord.z > 0:
                x_array = np.append(x_array, [cart_coord.x])
                y_array = np.append(y_array, [cart_coord.y])

        return x_array, y_array

    def zoom_in(self, scaling_factor):
        self.width_scale *= scaling_factor
        self.height_scale *= scaling_factor
        self.scaling_factor *= scaling_factor
        self.set_img()

    def mousePressEvent(self, QMouseEvent):
        """ Associate a  mousePress event to a signal that depends on
        the mode activated.
        """
        x_click = QMouseEvent.x()
        y_click = QMouseEvent.y()
        pixmap_x_min, pixmap_y_min = self.get_pixmap_coordinate_range()

        init_width = 1000  # without any zoom
        init_height = 1000  # without any zoom
        pixmap_width = init_width / self.width_scale  # =1 without any zoom
        pixmap_height = init_height / self.height_scale  # =1 without any zoom

        # change of coordinate system: qlabel -> pixmap
        x_pixmap = round((x_click - pixmap_x_min) * pixmap_width)
        y_pixmap = round((y_click - pixmap_y_min) * pixmap_height)

        # change of coordinate system: qlabel -> drawing
        x_drawing = round((x_click - pixmap_x_min) * self.drawing_width /
                          self.pixmap().width())
        y_drawing = round((y_click - pixmap_y_min) * self.drawing_height /
                          self.pixmap().height())

        """
        x_center_drawing = ((self.current_drawing.calibrated_center.x -
                             pixmap_x_min) * self.drawing_width /
                            self.pixmap().width())

        y_center_drawing = ((self.current_drawing.calibrated_center.y -
                             pixmap_y_min) * self.drawing_height /
                            self.pixmap().height())
        """

        if (not self.add_group_mode.value and
                not self.add_dipole_mode.value and
                not self.calibration_mode.value):
            for el in self.current_drawing.group_lst:
                if ((x_drawing >= el.posX -
                     self.current_drawing.calibrated_radius/30) and
                    (x_drawing <= el.posX +
                     self.current_drawing.calibrated_radius/30) and
                    (y_drawing >= el.posY -
                     self.current_drawing.calibrated_radius/30) and
                    (y_drawing <= el.posY +
                     self.current_drawing.calibrated_radius/30)):
                    self.selected_element = self.current_drawing\
                                                .group_lst.index(el)
                    # print("**** drawing clicked signal!!")
                    self.drawing_clicked.emit()

        # print("click coordinate: ", x_click, y_click)
        # print("pixmap coord: ", x_pixmap, y_pixmap)
        # print("drawing coord:", x_drawing, y_drawing)
        # print("drawing coord lower left origin:",
        #      x_drawing, self.drawing_height - y_drawing)
        # print("drawing coord of the center:",
        #      self.current_drawing.calibrated_center.x,
        #      self.current_drawing.calibrated_center.y)

        if (self.add_group_mode.value or
                self.add_dipole_mode.value or
                self.helper_grid.value):
            center_x_lower_left_origin = self.current_drawing\
                                             .calibrated_center.x
            center_y_lower_left_origin = (self.drawing_height -
                                          self.current_drawing
                                          .calibrated_center.y)
            north_x_lower_left_origin = self.current_drawing\
                                            .calibrated_north.x
            north_y_lower_left_origin = (self.drawing_height -
                                         self.current_drawing
                                         .calibrated_north.y)
            drawing_x_lower_left_origin = x_drawing
            drawing_y_lower_left_origin = self.drawing_height - y_drawing
            (longitude,
             latitude) = coordinates.heliographic_from_drawing(
                 center_x_lower_left_origin,
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
            if self.HGC_longitude < 0:
                self.HGC_longitude = 2 * math.pi + self.HGC_longitude

        if (self.calibration_mode.value and self.center_done and
                not self.north_done):
            self.north_done = True
            calib_pt2_x = x_drawing
            calib_pt2_y = y_drawing
            self.current_drawing.calibrate(self.calib_pt1_x,
                                           self.calib_pt1_y,
                                           calib_pt2_x,
                                           calib_pt2_y)

            self.zoom_in(1/5.)
            self.large_grid_overlay.value = True
            self.group_visu.value = True
            self.set_img()
            self.calibration_mode.value = False
            QtGui.QApplication.restoreOverrideCursor()
            self.north_clicked.emit()

        elif (self.calibration_mode.value and not self.center_done and
              not self.north_done):

            self.current_drawing.calibrated = 0
            self.calib_pt1_x = x_drawing
            self.calib_pt1_y = y_drawing
            self.center_done = True
            self.center_clicked.emit()

        if (self.current_drawing.calibrated and self.helper_grid.value):
            self.helper_grid_center_x = x_drawing
            self.helper_grid_center_y = y_drawing
            self.helper_grid_position_clicked = True
            self.set_img()

        if (self.add_group_mode.value and self.current_drawing.calibrated):
            self.current_drawing.add_group(self.HGC_latitude,
                                           self.HGC_longitude,
                                           x_drawing,
                                           y_drawing)
            self.group_added.emit()

        if (self.add_dipole_mode.value and self.current_drawing.calibrated):

            print("click on the drawing to add a dipole")
            print(len(self.dipole_points), len(self.dipole_angles))

            if (self.current_drawing.group_lst[self.group_visu_index]
                    .zurich.upper() in ["B", "C", "D", "E", "F", "G", "X"]):
                self.dipole_points.append(x_drawing)
                self.dipole_points.append(y_drawing)
                self.dipole_angles.append(self.HGC_latitude)
                self.dipole_angles.append(self.HGC_longitude)
                self.current_drawing\
                    .group_lst[self.group_visu_index]\
                    .set_dipole_position(self.dipole_points,
                                         self.dipole_angles)
                self.set_img()
                self.dipole_added.emit()

    def get_pixmap_coordinate_range(self):
        """
        get the pixmap minimum and maximum coordinate values
        in qlabel referential.
        """
        qlabel_width = self.width()
        qlabel_height = self.height()
        qlabel_x_center = qlabel_width/2.
        qlabel_y_center = qlabel_height/2.
        pixmap_x_min = math.floor(qlabel_x_center -
                                  self.pixmap().width()/2.)
        pixmap_x_max = math.floor(qlabel_x_center +
                                  self.pixmap().width()/2.)
        pixmap_y_min = math.floor(qlabel_y_center -
                                  self.pixmap().height()/2.)
        pixmap_y_max = math.floor(qlabel_y_center +
                                  self.pixmap().height()/2.)

        return pixmap_x_min, pixmap_y_min
