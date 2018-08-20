import math
import matplotlib.pyplot as plt
import matplotlib as mpl

import numpy as np

def from_spherical_to_cartesian(r, theta, phi):

    x = r * math.sin(theta*3.14/180) * math.cos(phi*3.14/180)
    y = r * math.sin(theta*3.14/180) * math.sin(phi*3.14/180)
    z = r * math.cos(theta*3.14/180)

    return x, y, z

def plot_latitude(radius, angleP, angleB):

    radius = radius
    x_border = []
    y_border = []
    for theta in range(0, int(2 * math.pi * 100), 1):
        
        x_border.append(radius * math.cos(theta/100.))
        y_border.append(radius * math.sin(theta/100.))
        
    x_center = 0
    y_center = 0
    
    alpha = angleB * math.pi/180.
    theta_rot = angleP * math.pi/180.
    
    a_lst = []
    b_lst = []
    center_x_lst = []
    center_y_lst = []
    latitude_lst = []

    longitude = np.linspace(0, math.pi,100)
        
    for latitude in range(0,180, 5):
        #x, y, z = from_spherical_to_cartesian(radius, longitude, latitude)
        
        center_x_lst.append(x_center )
        center_y_lst.append(y_center + radius * math.sin(latitude*math.pi*2/180.) * math.cos(alpha))
        minor_radius = radius * math.cos(latitude*2*math.pi/180.) * math.sin(alpha)
        major_radius = radius * math.cos(latitude*2*math.pi/180.)
        a_lst.append(minor_radius)
        b_lst.append(major_radius)
        latitude_lst.append(latitude*math.pi*2/180)
        
        
    for i in range(0,len(center_x_lst)):
        x_ellipse = b_lst[i] * np.cos(longitude) * np.cos(theta_rot) - a_lst[i] * np.sin(longitude) * np.sin(theta_rot)
        y_ellipse = a_lst[i] * np.sin(longitude) * np.cos(theta_rot) + b_lst[i] * np.cos(longitude) * np.sin(theta_rot)
        
        new_center_x = center_x_lst[i] * np.cos(theta_rot) - center_y_lst[i] * np.sin(theta_rot)
        new_center_y = center_x_lst[i] * np.sin(theta_rot) + center_y_lst[i] * np.cos(theta_rot)
    
        plt.plot(new_center_x + x_ellipse, new_center_y + y_ellipse)
        

    plt.scatter(x_border, y_border, s=1)
    plt.grid()
    #plt.scatter(x_parallel, y_parallel, s=1)
    plt.show()


if __name__ =='__main__':
    plot_latitude(5, 0, 20)
