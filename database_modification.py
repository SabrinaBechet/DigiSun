# !/usr/bin/env python
# -*-coding:utf-8-*-

from PIL import Image

import pathlib
import os
import pymysql
import math
from matplotlib import pyplot as plt
import database, coordinates

def play_with_database(table, field, date_min, date_max):
    db = pymysql.connect(host='soldb.oma.be',
                         user='usetdevadmin',
                         passwd='usetdevadmin',
                         db='uset_dev')
    cursor = db.cursor()

    cursor.execute('SELECT ' + field + ' from ' + table +
                   ' where DateTime> %s and DateTime< %s',((date_min, date_max)))

    db.commit()
    result = cursor.fetchall()
    print(result[0][0])
    return result


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
        




if __name__=='__main__':

    archdrawing_path = '/media/archdrawings'
    
    """path_drawing, nb_drawing_year  = get_list_drawings(archdrawing_path)
    print("nb de dessins au total: ", len(path_drawing))
    print(nb_drawing_year)
    plt.bar(nb_drawing_year.keys(), nb_drawing_year.values() )
    plt.grid()
    plt.show()
    """

    """get_height_from_image_lst(archdrawing_path)

    """
    db = database.database()
    
    datetime_group = db.get_field_time_interval("groups", "Datetime", "1940-03-01 00:00", "2018-05-31 23:00")
    datetime_group_set = set(datetime_group)

    x_check = []
    longitude_check = []
    latitude_check = []
    angle_P_check = []
    angle_B_check = []
    angle_L_check = []

    angle_scan_check = []
    angle_scan_from_database = []

    x_center_check = []
    radius_check  = []

    theta_check = []
    phi_check = []

    zurich_check = []
    gspot_check = []
    largest_spot_check = []
    
    for el in datetime_group_set:
        print(el)

        try:
            calibrated = db.get_field_datetime("drawings", "Calibrated", el)[0]
    
            if calibrated >0 :
                
                longitude = db.get_field_datetime("groups", "Dipole1Long", el)
                latitude = db.get_field_datetime("groups", "Dipole1Lat", el)
                x_center = db.get_field_datetime("calibrations", "CenterX", el)[0]
                y_center = db.get_field_datetime("calibrations", "CenterY", el)[0]
                x_north = db.get_field_datetime("calibrations", "NorthX", el)[0]
                y_north = db.get_field_datetime("calibrations", "NorthY", el)[0]
                angle_P = db.get_field_datetime("drawings", "AngleP", el)[0]
                angle_B0 = db.get_field_datetime("drawings", "AngleB", el)[0]
                angle_L0 = db.get_field_datetime("drawings", "AngleL", el)[0]
                angle_calib  = db.get_field_datetime("drawings", "AngleScan", el)[0]
                height = get_height_from_image_lst(archdrawing_path, el)
                radius_database = db.get_field_datetime("calibrations", "Radius", el)[0]
                g_spot = db.get_field_datetime("groups", "GSpot", el)
                zurich = db.get_field_datetime("groups", "Zurich", el)

                
                #print(el, longitude, x_center,  angle_P, angle_B0, angle_L0, height, calibrated)
                
                center = coordinates.Cartesian(x_center, y_center)
                north = coordinates.Cartesian(x_north, y_north)
                angle_calibration = center.angle_from_y_axis(north)
                radius = center.distance(north)
                
                
                for group_el in range(len(longitude)):
                    largest_spot = None
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

                    if g_spot[group_el] in [1, 4, 7]:
                        largest_spot = 'L'
                        db.write_field_datetime('groups', 'Largest_spot', largest_spot, el, group_el)
                    elif g_spot[group_el] in [2, 5, 8]:
                        largest_spot = 'T'
                        db.write_field_datetime('groups', 'Largest_spot', largest_spot, el, group_el)
                    elif g_spot[group_el] in [3, 6, 9]:
                        largest_spot = 'E'
                        db.write_field_datetime('groups', 'Largest_spot', largest_spot, el, group_el)
                        
                    #largest_spot_check.append(largest_spot)
                    #db.write_field_datetime('groups', 'Largest_spot', largest_spot, el, group_el)
                    #db.write_field_datetime('groups', 'PosY', "{:.0f}".format(y_upper), el, group_el)
                    
                    # check qu'on retrouve bien les bonnes lat et longitude en faisant le calcul inverse
                    long2, lat2 = coordinates.heliographic_from_drawing(x_center, height - y_center,
                                                                        x_north, height - y_north,
                                                                        x_upper,
                                                                        height - y_upper,
                                                                        angle_P, angle_B0, angle_L0)
                    
                    """print("***check")
                    print("longitude:", longitude_group, long2)
                    print("latitude:", latitude_group, lat2)
                    """
                    """
                    print(longitude_group, latitude_group, x_center, x_north,
                          x_upper, x_upper - int(x_upper), radius, radius_database, int(radius_database),
                          angle_calibration, (radius - int(radius)))
                    """
                    #if (angle_calibration<0.000001) and (radius - int(radius)<0.00001):
                    x_check.append(x_upper - int(x_upper))
                    longitude_check.append(longitude_group * 180/math.pi)
                    latitude_check.append(latitude_group * 180/math.pi)
                    angle_P_check.append(angle_P)
                    angle_B_check.append(angle_B0)
                    angle_L_check.append(angle_L0)
                    angle_scan_check.append(angle_calibration)
                    zurich_check.append(zurich)
                    gspot_check.append(g_spot)

                    #print(group_el, zurich[group_el], g_spot[group_el], largest_spot)
                    
                    #theta_check.append(theta)
                    
                    x_center_check.append(x_center)
                    radius_check.append(radius - int(radius))
                    
                    theta_check.append(theta)
                    phi_check.append(phi)
                    
                    # inserver dans la base de donne dans la bonne colonne
                
        except IndexError:
            print("there is an index error for the date: {} ".format(el))
                
        
    #plt.hist(x_check, 100, (0,1))
    """largest_spot_count = []
    largest_spot_name = [0, 1, 2, 3]
    largest_spot_count.append(largest_spot_check.count('L'))
    largest_spot_count.append(largest_spot_check.count('E'))
    largest_spot_count.append(largest_spot_check.count('T'))
    largest_spot_count.append(largest_spot_check.count(None))
    
    
    plt.plot(largest_spot_name, largest_spot_count)
    x_not_just = [x for x in x_check if (x > 0.1 and x < 0.9)]
    print("tot", len(x_check), len(x_not_just))
    #plt.scatter(x_check, latitude_check)
    plt.grid()
    plt.show()
    """
    
