
from datetime import datetime, timedelta
import SunEphemeris

def carrington_rotation(drawing_time):
    """
    A rotation starts when the heliographic prime meridian (L0)
    crosses the subterrestrial point of the solar disc.
    The first Carrington rotation started on 1853 Nov 9
    (JD 2398167.329), later points can be calculated using the 
    synodic period rsyn = 27.2753 days. 
    (ref: Heliospheric Coordinate systems, Franz & Harper 2002)
    """

    sun = SunEphemeris.SunEphemeris(drawing_time)

    day_to_substract = (360 - sun.angle_L0())/13.19
    date_close_zero_meridian = drawing_time - timedelta(days = day_to_substract)
                                        
    sun_zero_meridian = SunEphemeris.SunEphemeris(date_close_zero_meridian)
    angle_date_close_zero_meridian = sun_zero_meridian.angle_L0()

    angle_date_close_zero_meridian_tmp = angle_date_close_zero_meridian
    date_close_zero_meridian_tmp = date_close_zero_meridian
    day_to_substract_tmp = 1000


    # approximate the time of the rotation with 3 decimal precision
    while (abs(day_to_substract_tmp)>0.001):
        angle_close_zero_meridian_tmp = 360 - angle_date_close_zero_meridian_tmp
        if angle_close_zero_meridian_tmp > 180:
            angle_close_zero_meridian_tmp = angle_close_zero_meridian_tmp - 360

        day_to_substract_tmp = (angle_close_zero_meridian_tmp)/13.19

        date_close_zero_meridian_tmp = date_close_zero_meridian_tmp - timedelta(days = day_to_substract_tmp)
        sun_zero_meridian_tmp = SunEphemeris.SunEphemeris(date_close_zero_meridian_tmp)
        angle_date_close_zero_meridian_tmp = sun_zero_meridian_tmp.angle_L0()
        

   
    
    carrington_rotation_number = int((sun.julian_day - 2398167.329)/27.2753) + 1
    carrington_rotation_number2 = round((sun_zero_meridian_tmp.julian_day - 2398167.329)/27.2753) + 1

    #print(carrington_rotation_number, carrington_rotation_number2)
    
   
    
    return carrington_rotation_number2
