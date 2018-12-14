# !/usr/bin/env python
# -*-coding:utf-8-*-

import pathlib
import os
import pymysql
import math
from matplotlib import pyplot as plt
import database, coordinates


"""
List of function to plot the information stored in the database
"""

def draw_angle_scan():
    """
    Read the value of AngleScan in the drawings table and 
    write it in the calibrations table.
    """

    db = database.database()
    
    angle_scan_drawing = db.get_field_time_interval("drawings",
                                                "AngleScan",
                                                "1940-03-01 00:00",
                                                "2018-05-31 23:00")
    angle_scan_drawing = [x*180/math.pi for x in angle_scan_drawing]
    angle_scan_drawing = [x for x in angle_scan_drawing if x!=0]
    

    print("value max: {}".format(max(angle_scan_drawing)))
    print("value min: {}".format(min(angle_scan_drawing)))
   
    plt.hist(angle_scan_drawing, bins=100, range=(-10,10))
    #print(angle_scan_drawing)
    plt.xlabel("angle scan (degree)")
    plt.grid()
    plt.show()
            

            
if __name__=='__main__':

    archdrawing_path = '/media/archdrawings'
    
    draw_angle_scan()
   
    
