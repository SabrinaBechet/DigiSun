import math
import matplotlib.pyplot as plt
import matplotlib as mpl

import numpy as np
import coordinates


def sphere_border():

    radius = 4.
    x_border = []
    y_border = []
    for theta in range(0, int(2 * math.pi * 100), 1):
        
        x_border.append(radius * math.cos(theta/100.))
        y_border.append(radius * math.sin(theta/100.))

    return x_border, y_border

def draw_latitude(longitude, radius):
  
    #x_lst = []
    #z_lst = []

    x_arr = np.array([])
    y_arr = np.array([])
    
    for latitude in range(-180,180, 1):

        spherical_coord =  coordinates.Spherical(radius, longitude, latitude)
        P_angle = 20.
        B_angle = 7.
        
        x, y, z = spherical_coord.convert_to_cartesian()
        cart_coord = coordinates.Cartesian(x, y, z)
        cart_coord.rotate_around_y(P_angle)
        cart_coord.rotate_around_x(B_angle)
        
        if cart_coord.y>0:
            x_arr = np.append(x_arr, [cart_coord.x])
            y_arr = np.append(y_arr, [cart_coord.z])
        
    return x_arr, y_arr

def draw_longitude(latitude, radius):

    #x_lst = []
    #z_lst = []
    x_arr = np.array([])
    y_arr = np.array([])
    
    for longitude in range(-180,180, 1):

        spherical_coord =  coordinates.Spherical(radius, longitude, latitude)
        P_angle = 20.
        B_angle = 7.
        
        x, y, z = spherical_coord.convert_to_cartesian()
        cart_coord = coordinates.Cartesian(x, y, z)
        cart_coord.rotate_around_y(P_angle)
        cart_coord.rotate_around_x(B_angle)
        
        if cart_coord.y>0:
            x_arr = np.append(x_arr, [cart_coord.x])
            y_arr = np.append(y_arr, [cart_coord.z])
            #x_lst.append(cart_coord.x)
            #z_lst.append(cart_coord.z)
        
    return x_arr, y_arr


x_border, y_border = sphere_border()
plt.scatter(x_border, y_border, s=1)

for longitude in range(-180, 180, 5):
    x_lst, z_lst = draw_latitude(longitude, 4.)
    plt.scatter(x_lst, z_lst, s=1)

for latitude in range(-180, 180, 5):
    x_lst, z_lst = draw_longitude(latitude, 4.)
    plt.scatter(x_lst, z_lst, s=1)
   
    
plt.grid()
plt.show()
