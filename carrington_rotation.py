
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
    print("days to remove: ", (360 - sun.angle_L0())/13.19)

    date_close_zero_meridian = drawing_time - timedelta(days = day_to_substract)
                                        
    #drawing_time.day = drawing_time.day - 
    #date_close_zero_meridian = drawing_time - (360 - sun.angle_L0())/13.19
    
    sun_zero_meridian = SunEphemeris.SunEphemeris(date_close_zero_meridian)
    angle_date_close_zero_meridian = sun_zero_meridian.angle_L0()

    carrington_rotation_number = (sun_zero_meridian.julian_day - 2398167.329)/27.2753

    if angle_date_close_zero_meridian> 180:
        carrington_rotation_number_round = int(carrington_rotation_number) + 1
    else:
        carrington_rotation_number_round = int(carrington_rotation_number) + 2
        
    print("date close zero meridian: ", date_close_zero_meridian)
    print("angle : ", angle_date_close_zero_meridian)
    print("carrington rotation number: ", carrington_rotation_number)
    print("carrington rotation number round: ", carrington_rotation_number_round)

    
