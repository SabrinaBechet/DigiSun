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

import math


def group_frame(zurich, radius, posx, posy, center_x, center_y):
    distance_from_center = math.sqrt((posx - center_x)**2 +
                                     (posy - center_y)**2)

    if posx==0.0 and posy==0.0:
        print('hey the positions are nul!')
        return int(radius/6.)
    
    if distance_from_center < radius:
        center_to_limb = (math.asin(distance_from_center *
                                    1./radius))
    """
    print("distance from center: {} ".format(distance_from_center))
    print("center to limb angle: {}".format(center_to_limb * 180/math.pi))
    print("cos correction: {}".format(math.cos(float(center_to_limb))))
    """
    if zurich in ['A', 'J']:
        step = (radius/30.) * (math.cos(float(center_to_limb)))
    elif zurich in ['H']:
        step = (radius/18.) * (math.cos(float(center_to_limb)))
    elif zurich in ['B', 'C', 'D']:
        step = (radius/9.) * (math.cos(float(center_to_limb)))
    elif zurich in ['E']:
        step = (radius/6.) * (math.cos(float(center_to_limb)))
    elif zurich in ['F', 'G', 'X']:
        step = (radius/4.) * (math.cos(float(center_to_limb)))

    return int(step * 2)
