
import math


def group_frame(zurich, hgc_lon, hgc_lat, leading_long, leading_lat, trailing_long, trailing_lat):
    
    if zurich in ['A', 'J', 'H']:
        if zurich in ['A', 'J']:
            step = 1.5
        elif zurich in ['H']:
            step = 3
        
        long_min = hgc_lon * 180/math.pi - step
        long_max = hgc_lon * 180/math.pi + step
        lat_min = hgc_lat * 180/math.pi - step
        lat_max = hgc_lat * 180/math.pi + step

            
    elif zurich in ['B', 'C', 'D','E','F','G']:

        step_long = 3
        step_lat = 1.5
            
        long_min = leading_long * 180/math.pi - step_long
        long_max = trailing_long * 180/math.pi + step_long

        lat_min = leading_lat * 180/math.pi - step_lat
        lat_max = trailing_lat * 180/math.pi + step_lat
        

    return long_min, long_max, lat_min, lat_max
