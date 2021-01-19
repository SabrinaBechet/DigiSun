# !/usr/bin/env python
# -*-coding:utf-8-*-

import pathlib
import os
from datetime import datetime
import pymysql
import math
from matplotlib import pyplot as plt
import database
import coordinates

"""
Here are all the scripts used to change the database for 
the new version of DigiSun
"""

def get_height_from_image_lst(root_directory, datetime):
    el=datetime
    filename = 'usd{}{:02d}{:02d}{:02d}{:02d}'.format(el.year,
                                                      el.month,
                                                      el.day,
                                                      el.hour,
                                                      el.minute) + '.jpg'
    year_name = '{:02d}'.format(el.year)
    month_name = '{:02d}'.format(el.month)
    path = pathlib.PurePath(root_directory,
                            year_name,
                            month_name,
                            filename)
    
    with Image.open(str(path)) as img:
        width_group = img.size[0]
        height_group = img.size[1]
        
    return height_group
                                
def get_list_drawings(root_path):

    path_drawing = []
    nb_drawing_year = {}
    
    lst_year = os.listdir(root_path)
    lst_year = [x for x in lst_year if int(x) in range(1940,2019)]

    for year in lst_year:
        
        drawing_year = []
        path_year = pathlib.PurePath(root_path, year)
        lst_month = os.listdir(str(path_year))
        lst_month = [x for x in lst_month if x.isdigit() and int(x) in range(0,13)]
        for month in lst_month:
            drawing_month = []
            lst_day = os.listdir(str(pathlib.PurePath(path_year, month)))
            lst_day = [x for x in lst_day if x[-3:]=='jpg']
            for day in lst_day:
                path_drawing.append(day)
                drawing_year.append(day)
                drawing_month.append(day)
                
            #print("{}:{}".format(month, len(drawing_month)))
        drawing_year = [x[3:11] for x in drawing_year]
        drawing_year_set = set(drawing_year)
        #print("{}:{}".format(year, drawing_year))
        nb_drawing_year[int(year)]=(len(drawing_year_set))
                    
    return path_drawing, nb_drawing_year

def fill_largest_spot():
    db = database.database()
    
    datetime_group = db.get_field_time_interval("groups",
                                                "Datetime",
                                                "1940-03-01 00:00",
                                                "2018-05-31 23:00")
    datetime_group_set = set(datetime_group)

    for el in datetime_group_set:
        try:
            calibrated = db.get_field_datetime("drawings", "Calibrated", el)[0]
            
            if calibrated >0 :
                g_spot = db.get_field_datetime("groups", "GSpot", el)
                zurich = db.get_field_datetime("groups", "Zurich", el)
                
                for group_el in range(len(g_spot)):
                    largest_spot = None

                    if g_spot[group_el] in [1, 4, 7]:
                        largest_spot = 'L'
                        db.write_field_datetime_group('groups',
                                                      'Largest_spot',
                                                      largest_spot,
                                                      el,
                                                      group_el)
                    elif g_spot[group_el] in [2, 5, 8]:
                        largest_spot = 'T'
                        db.write_field_datetime_group('groups',
                                                      'Largest_spot',
                                                      largest_spot,
                                                      el,
                                                      group_el)
                    elif g_spot[group_el] in [3, 6, 9]:
                        largest_spot = 'E'
                        db.write_field_datetime_group('groups',
                                                      'Largest_spot',
                                                      largest_spot,
                                                      el,
                                                      group_el)
        except IndexError:
            print("there is an index error for the date: {} ".format(el))


def convert_last_update_time_datetime():
    
    db = database.database()
    datetime_drawing = db.get_field_time_interval("drawings",
                                                  "Datetime",
                                                  "2018-05-01 00:00",
                                                  "2018-05-31 23:00")
    for el_date in datetime_drawing:
        try:
            last_update_string = db.get_field_datetime("drawings", "LastUpdateTime", el_date)[0]
            
            if not isinstance(last_update_string, datetime):
                print(el_date, type(last_update_string))
                """db.write_field_datetime('drawings',
                                        'LastUpdateTime',
                                        None,
                                        el_date)
                """
            
            
        except IndexError:
            print("there is an index error for the date: {} ".format(el))

            
def move_angleScan_from_drawing_to_calibration():
    """
    Read the value of AngleScan in the drawings table and 
    write it in the calibrations table.
    """

    db = database.database()
    
    datetime_drawing = db.get_field_time_interval("drawings",
                                                "Datetime",
                                                "1940-03-01 00:00",
                                                "2018-05-31 23:00")
    for el_date in datetime_drawing:
        try:
            angle_scan = db.get_field_datetime("drawings", "AngleScan", el_date)[0] * 180/math.pi
            db.write_field_datetime('calibrations',
                                    'AngleScan',
                                    "{:0.4f}".format(angle_scan),
                                    el_date)
            
            #print(el_date, "{:0.4f}".format(angle_scan))
        except IndexError:
            print("there is an index error for the date: {} ".format(el))

    
def fill_all_posX_posY():
    """
    Read the values of longitude, latitude, calibration center and north
    calculate the posX and posY 
    fill it in the database
    """

    db = database.database()
    
    datetime_group = db.get_field_time_interval("groups",
                                                "Datetime",
                                                "1940-03-01 00:00",
                                                "2018-05-31 23:00")
    datetime_group_set = set(datetime_group)

    for el in datetime_group_set:

        try:
            calibrated = db.get_field_datetime("drawings", "Calibrated", el)[0]
            
            if calibrated >0 :
                
                longitude = db.get_field_datetime("groups", "Dipole2Long", el)
                latitude = db.get_field_datetime("groups", "Dipole2Lat", el)
                zurich = db.get_field_datetime("groups", "Zurich", el)
                x_center = db.get_field_datetime("calibrations", "CenterX", el)[0]
                y_center = db.get_field_datetime("calibrations", "CenterY", el)[0]
                x_north = db.get_field_datetime("calibrations", "NorthX", el)[0]
                y_north = db.get_field_datetime("calibrations", "NorthY", el)[0]
                angle_P = db.get_field_datetime("drawings", "AngleP", el)[0]
                angle_B0 = db.get_field_datetime("drawings", "AngleB", el)[0]
                angle_L0 = db.get_field_datetime("drawings", "AngleL", el)[0]
                
                
                height = get_height_from_image_lst(archdrawing_path, el)
                
                center = coordinates.Cartesian(x_center, y_center)
                north = coordinates.Cartesian(x_north, y_north)
                
                for group_el in range(len(longitude)):
                    if zurich[group_el] in ['B','C','D','E','F','G','X']:
                        longitude_group = longitude[group_el]
                        latitude_group = latitude[group_el]

                        theta = (angle_L0 * math.pi/180.) - longitude_group
                        phi = math.pi/2 - latitude_group

                        (x_upper,
                         y_upper,
                         z_upper) = coordinates.cartesian_from_HGC_upper_left_origin(
                             x_center, y_center,
                             x_north,  y_north,
                             longitude_group, latitude_group,
                             angle_P, angle_B0, angle_L0, height)

                        
                        db.write_field_datetime_group('groups',
                                                      'Dipole2_PosX',
                                                      "{:.0f}".format(x_upper),
                                                      el,
                                                      group_el)
                        db.write_field_datetime_group('groups',
                                                      'Dipole2_PosY',
                                                      "{:.0f}".format(y_upper),
                                                      el,
                                                      group_el)

                        """
                        # check qu'on retrouve bien les bonnes lat et
                        #longitude en faisant le calcul inverse
                        long2, lat2 = coordinates.heliographic_from_drawing(
                            x_center, height - y_center,
                            x_north, height - y_north,
                            x_upper,
                            height - y_upper,
                            angle_P, angle_B0, angle_L0)

                        print("***check")
                        print("longitude:", longitude_group, long2)
                        print("latitude:", latitude_group, lat2)
                        """
                        """
                        print(longitude_group, latitude_group, x_center, x_north,
                              x_upper, x_upper - int(x_upper), radius, 
                        radius_database, int(radius_database),
                        """
        except IndexError:
            print("there is an index error for the date: {} ".format(el))
            

if __name__=='__main__':

    archdrawing_path = '/media/archdrawings'
    
    
    #fill_all_posX_posY()
    #move_angleScan_from_drawing_to_calibration()
    convert_last_update_time_datetime()
