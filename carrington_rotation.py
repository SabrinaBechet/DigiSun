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

from datetime import timedelta
import sun_ephemeris


def carrington_rotation(drawing_time, file_path = 'VSOP87D.ear'):
    """
    A rotation starts when the heliographic prime meridian (L0)
    crosses the subterrestrial point of the solar disc.
    The first Carrington rotation started on 1853 Nov 9
    (JD 2398167.329), later points can be calculated using the
    synodic period rsyn = 27.2753 days.
    (ref: Heliospheric Coordinate systems, Franz & Harper 2002)
    """

    sun = sun_ephemeris.SunEphemeris(drawing_time, file_path)

    day_to_substract = (360 - sun.angle_L0())/13.19
    date_close_zero_meridian = drawing_time - timedelta(days=day_to_substract)

    sun_zero_meridian = sun_ephemeris.SunEphemeris(date_close_zero_meridian,
                                                   file_path)
    angle_date_close_zero_meridian = sun_zero_meridian.angle_L0()

    angle_date_close_zero_meridian_tmp = angle_date_close_zero_meridian
    date_close_zero_meridian_tmp = date_close_zero_meridian
    day_to_substract_tmp = 1000

    # approximate the time of the rotation with 3 decimal precision
    while (abs(day_to_substract_tmp) > 0.001):
        angle_close_zero_meridian_tmp = (360 -
                                         angle_date_close_zero_meridian_tmp)
        if angle_close_zero_meridian_tmp > 180:
            angle_close_zero_meridian_tmp = angle_close_zero_meridian_tmp - 360

        day_to_substract_tmp = (angle_close_zero_meridian_tmp)/13.19

        date_close_zero_meridian_tmp = (date_close_zero_meridian_tmp -
                                        timedelta(days=day_to_substract_tmp))
        sun_zero_meridian_tmp = sun_ephemeris.SunEphemeris(
            date_close_zero_meridian_tmp,
            file_path)
        angle_date_close_zero_meridian_tmp = sun_zero_meridian_tmp.angle_L0()

    # carrington_rotation_number = int((sun.julian_day -
    #                                  2398167.329)/27.2753) + 1
    carrington_rotation_number = round((sun_zero_meridian_tmp.julian_day -
                                        2398167.329)/27.2753) + 1

    return carrington_rotation_number
