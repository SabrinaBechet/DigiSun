# !/usr/bin/env python
# -*- coding:utf-8-*-
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

import math


class Coordinates():

    def __init__(self):
        pass


class Spherical(Coordinates):
    """
    The angles are in radian
    """

    def __init__(self, radius, theta, phi):
        Coordinates.__init__(self)
        self.theta = theta
        self.phi = phi
        self.radius = radius

    def convert_to_cartesian(self):
        x = self.radius * math.sin(self.phi) * math.sin(self.theta)
        y = self.radius * math.cos(self.phi)
        z = self.radius * math.sin(self.phi) * math.cos(self.theta)

        return x, y, z


class Cartesian(Coordinates):
    """
    Contains cartesian coordinates with the following reference:
    x = right-east
    y = up-north
    z = toward earth
    All the angle are *IN RADIAN*
    """

    def __init__(self, x, y, z=0):
        # super().__init__()
        Coordinates.__init__(self)
        self.x = x
        self.y = y
        self.z = z

    def translate(self, delta_x=0, delta_y=0, delta_z=0):

        self.x += delta_x
        self.y += delta_y
        self.z += delta_z

    def rotate_around_x(self, theta):
        """
        Rotate counterclockwise around the x-axis of *theta radian*.
        """
        y_rot = (self.y * math.cos(theta) -
                 self.z * math.sin(theta))
        z_rot = (self.y * math.sin(theta) +
                 self.z * math.cos(theta))
        self.y = y_rot
        self.z = z_rot

    def rotate_around_y(self, theta):
        """
        Rotate counterclockwise around the y-axis of *theta radian*.
        """
        x_rot = (self.x * math.cos(theta) +
                 self.z * math.sin(theta))
        z_rot = (-self.x * math.sin(theta) +
                 self.z * math.cos(theta))
        self.x = x_rot
        self.z = z_rot

    def rotate_around_z(self, theta):
        """
        Rotate counterclockwise around the z-axis of *theta radian*.
        """
        x_rot = (self.x * math.cos(theta) -
                 self.y * math.sin(theta))
        y_rot = (self.x * math.sin(theta) +
                 self.y * math.cos(theta))
        self.x = x_rot
        self.y = y_rot

    def distance(self, pointB):
        """
        Return the distance between the point A and B
        """
        return math.sqrt((self.x - pointB.x) ** 2 +
                         (self.y - pointB.y) ** 2 +
                         (self.z - pointB.z) ** 2)

    def angle_from_x_axis(self, pointB):
        """
        Return the angle *in radian* between the x-axis and
        vector formed with the point B
        """
        return math.atan((self.y - pointB.y)/float(self.x - pointB.x))

    def angle_from_y_axis(self, pointB):
        """
        Return the angle *in radian* between the x-axis and
        vector formed with the point B
        """
        return math.atan((self.x - pointB.x)/float(self.y - pointB.y))

    def normalize(self, value):
        if value > 0:
            self.x *= value
            self.y *= value
            self.z *= value
        else:
            print("the value must be greater than 0!")

    def set_axis_z(self):
        try:
            self.z = math.sqrt(1 - self.x**2 - self.y**2)
        except ValueError:
            print("click outside of the solar disk!")

    def convert_to_spherical(self):
        """
        Return the spherical coordinate theta and phi *in radian*
        """
        radius = 1
        theta = math.atan2(self.x, self.z)
        phi = math.acos(self.y/radius)

        return theta, phi


def cartesian_from_HGC_upper_left_origin(x_center, y_center, x_north,
                                         y_north, HGC_long, HGC_lat,
                                         angle_P, angle_B0, angle_L0, height):
    """
    get the cartesian coordinate suitable for Qpainter (origin upper left)
    from the given heliographic latitude/longitude (for group or dipole).
    NB: starting from the center(!!)
    x_lower_left_origin = x_upper_left_origin while
    y_lower_left_origin = - y_upper_left_origin
    """
    (x_lower_left_origin,
     y_lower_left_origin,
     z_lower_left_origin) = cartesian_from_drawing(x_center,
                                                   height - y_center,
                                                   x_north,
                                                   height - y_north,
                                                   HGC_long,
                                                   HGC_lat,
                                                   angle_P,
                                                   angle_B0,
                                                   angle_L0)

    x_centered_upper_left_origin = x_center + x_lower_left_origin
    y_centered_upper_left_origin = y_center - y_lower_left_origin

    return x_centered_upper_left_origin, y_centered_upper_left_origin, 0


def cartesian_from_drawing(x_center, y_center, x_north,
                           y_north, HGC_long, HGC_lat,
                           angle_P, angle_B0, angle_L0):
    """
    Given a heliographic longitude and latitude in radian,
    returns the corresponding x, y, z positions on the drawing with
    center in lower left corner
    """
    center = Cartesian(x_center, y_center)
    north = Cartesian(x_north, y_north)
    angle_calibration = center.angle_from_y_axis(north)
    # angle_calibration_degree = angle_calibration * 180/math.pi
    radius = center.distance(north)

    theta = (angle_L0 * math.pi/180.) - HGC_long
    phi = math.pi/2 - HGC_lat

    sun_spherical = Spherical(1, theta, phi)
    x, y, z = sun_spherical.convert_to_cartesian()

    sun_cartesian = Cartesian(x, y, z)

    sun_cartesian.rotate_around_x(angle_B0 * math.pi/180.)
    sun_cartesian.rotate_around_z(-angle_P * math.pi/180. - angle_calibration)

    drawing = Cartesian(sun_cartesian.x,
                        sun_cartesian.y,
                        sun_cartesian.z)

    # drawing.rotate_around_z(-angle_calibration)
    drawing.normalize(radius)

    return drawing.x, drawing.y, drawing.z


def cartesian_from_drawing_method2(x_center, y_center, x_north,
                                   y_north, HGC_long, HGC_lat,
                                   angle_P, angle_B0, angle_L0):

    """
    Given a heliographic longitude and latitude *in radian*,
    returns the corresponding x, y, z positions on the drawing with
    center in the lower left corner
    """
    center = Cartesian(x_center, y_center)
    north = Cartesian(x_north, y_north)
    angle_calibration = center.angle_from_y_axis(north)
    radius = center.distance(north)

    theta = (angle_L0 * math.pi/180) - HGC_long
    phi = math.pi/2 - HGC_lat

    sun_spherical = Spherical(1, -HGC_long, phi)
    x, y, z = sun_spherical.convert_to_cartesian()

    sun_cartesian = Cartesian(x, y, z)
    sun_cartesian.rotate_around_y(angle_L0 * math.pi/180.)
    sun_cartesian.rotate_around_x(angle_B0 * math.pi/180.)
    sun_cartesian.rotate_around_z(-angle_P * math.pi/180.)

    drawing = Cartesian(sun_cartesian.x,
                        sun_cartesian.y,
                        sun_cartesian.z)
    drawing.rotate_around_z(-angle_calibration)
    drawing.normalize(radius)

    return drawing.x, drawing.y, drawing.z


def heliographic_from_drawing(x_center, y_center, x_north,
                              y_north, x_drawing, y_drawing,
                              angle_P, angle_B0, angle_L0):
    """
    Given a position on the drawing,
    returns the corresponding heliographic longitude and latitude.
    """
    center = Cartesian(x_center, y_center)
    north = Cartesian(x_north, y_north)
    angle_calibration = center.angle_from_y_axis(north)
    radius = center.distance(north)
    drawing = Cartesian(x_drawing, y_drawing)

    disk_trigo = Cartesian(drawing.x, drawing.y)
    disk_trigo.translate(-center.x, -center.y)
    disk_trigo.normalize(1./radius)
    disk_trigo.set_axis_z()
    disk_trigo.rotate_around_z(angle_calibration)

    sun = Cartesian(disk_trigo.x, disk_trigo.y, disk_trigo.z)
    sun.rotate_around_z(angle_P * math.pi/180.)
    sun.rotate_around_x(-angle_B0 * math.pi/180.)
    sun.rotate_around_y(-angle_L0 * math.pi/180.)

    theta, phi = sun.convert_to_spherical()

    HGC_longitude = - theta
    HGC_latitude = math.pi/2 - phi

    return HGC_longitude, HGC_latitude
