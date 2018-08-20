# !/usr/bin/env python
# -*- coding:utf-8-*-

import os
import math
import coordinates
import unittest


class test_heliographic_coordinates(unittest.TestCase):
    """
    These test are based on measures taken on drawings and 
    estimations of the group position in cm. The error on this
    position can be up to mm so a precision of 0.1 only is asked 
    for this test.
    This test is done for each quadrant of the solar disk (drawing).
    """
    def test_upper_left_quadrant(self):

        x_center, y_center = 0, 0
        x_north, y_north = 0, 12.5
        x_drawing, y_drawing = -6.9, 4.9
        angle_P = 17
        angle_B = 1.209
        angle_L  = 68.20

        longitude_drawing = 1.908
        latitude_drawing = 0.229
        
        lon, lat = coordinates.heliographic_from_drawing(x_center,
                                                         y_center,
                                                         x_north,
                                                         y_north,
                                                         x_drawing,
                                                         y_drawing,
                                                         angle_P,
                                                         angle_B,
                                                         angle_L)

        self.assertLessEqual(math.fabs(lon - longitude_drawing),0.1)
        self.assertLessEqual(math.fabs(lat - latitude_drawing),0.1)

    def test_upper_right_quadrant(self):

        x_center, y_center = 0, 0
        x_north, y_north = 0, 12.5
        x_drawing, y_drawing = -0.3, 2.6
        angle_P = 18.02
        angle_B = 1.56
        angle_L  = 105.54

        longitude_drawing = 1.884
        latitude_drawing = 0.228
        
        lon, lat = coordinates.heliographic_from_drawing(x_center,
                                                         y_center,
                                                         x_north,
                                                         y_north,
                                                         x_drawing,
                                                         y_drawing,
                                                         angle_P,
                                                         angle_B,
                                                         angle_L)
                
        self.assertLessEqual(math.fabs(lon - longitude_drawing),0.1)
        self.assertLessEqual(math.fabs(lat - latitude_drawing),0.1)

    def test_lower_right_quadrant(self):

        x_center, y_center = 0, 0
        x_north, y_north = 0, 12.5
        x_drawing, y_drawing = 4.2, -4
        angle_P = 20.35
        angle_B = 2.43
        angle_L  = 199.59

        longitude_drawing = 3.05
        latitude_drawing = -0.144
        
        lon, lat = coordinates.heliographic_from_drawing(x_center,
                                                         y_center,
                                                         x_north,
                                                         y_north,
                                                         x_drawing,
                                                         y_drawing,
                                                         angle_P,
                                                         angle_B,
                                                         angle_L)
        
        self.assertLessEqual(math.fabs(lon - longitude_drawing),0.1)
        self.assertLessEqual(math.fabs(lat - latitude_drawing),0.1)

    def test_lower_left_quadrant(self):

        x_center, y_center = 0, 0
        x_north, y_north = 0, 12.5
        x_drawing, y_drawing = -1.2, -0.6
        angle_P = -16.16
        angle_B = -6.65
        angle_L  = 158.92

        longitude_drawing = 2.881
        latitude_drawing = -0.136
        
        lon, lat = coordinates.heliographic_from_drawing(x_center,
                                                         y_center,
                                                         x_north,
                                                         y_north,
                                                         x_drawing,
                                                         y_drawing,
                                                         angle_P,
                                                         angle_B,
                                                         angle_L)
        
        self.assertLessEqual(math.fabs(lon - longitude_drawing),0.1)
        self.assertLessEqual(math.fabs(lat - latitude_drawing),0.1)


class test_cartesian_coordinates(unittest.TestCase):
    """
    check the conversion from cartesian to spherical.
    """
    def test_upper_left_quadrant(self):

        x_center, y_center = 0, 0
        x_north, y_north = 0, 12.5
        x_drawing, y_drawing = -6.9, 4.9
        angle_P = 17
        angle_B = 1.209
        angle_L  = 68.20

        longitude_drawing = 1.908
        latitude_drawing = 0.229
        
        lon, lat = coordinates.heliographic_from_drawing(x_center,
                                                         y_center,
                                                         x_north,
                                                         y_north,
                                                         x_drawing,
                                                         y_drawing,
                                                         angle_P,
                                                         angle_B,
                                                         angle_L)
        x, y, z = coordinates.cartesian_from_drawing(x_center,
                                                     y_center,
                                                     x_north,
                                                     y_north,
                                                     lon,
                                                     lat,
                                                     angle_P,
                                                     angle_B,
                                                     angle_L)
        
        
        self.assertEqual(x, x_drawing)
        self.assertEqual(y, y_drawing)

        
        
if __name__=='__main__':
    unittest.main()
