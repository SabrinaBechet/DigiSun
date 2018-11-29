
import math


def group_frame(zurich, radius, posx, posy, center_x, center_y):
    
    #print("check variable")
    #print(type(center_to_limb), center_to_limb)

    distance_from_center =  math.sqrt((posx - center_x )**2 +
                                      (posy - center_y )**2)
    
    if distance_from_center < radius:
        center_to_limb = (math.asin(distance_from_center *
                                          1./radius))
                    
    
    if zurich in ['A', 'J']:
        step = (radius/60.) *( math.cos(float(center_to_limb)))
    elif zurich in ['H']:
        step = (radius/30.) *( math.cos(float(center_to_limb)))
    elif zurich in ['B','C', 'D']:
        step = (radius/9.) *( math.cos(float(center_to_limb)))
    elif zurich in ['E']:
        step = (radius/6.) *( math.cos(float(center_to_limb)))
    elif zurich in ['F','G']:
        step = (radius/4.) *( math.cos(float(center_to_limb)))    

    return int(step*2)
