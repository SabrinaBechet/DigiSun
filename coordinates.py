# !/usr/bin/env python
# -*- coding:utf-8-*-

import math
from matplotlib import pylab as plt

class Coordinates():

    def __init__(self):
        pass
        #print('coordinate')

class Spherical(Coordinates):

    def __init__(self, radius, theta, phi):
      Coordinates.__init__(self)
      " angle in radian"
      self.theta = theta 
      self.phi = phi
      self.radius = radius

    def convert_to_cartesian(self):
        x = self.radius * math.sin(self.phi) * math.sin(self.theta)
        y = self.radius * math.cos(self.phi)
        z = self.radius * math.sin(self.phi) * math.cos(self.theta)
        
        return x, y, z
        
class Cartesian(Coordinates):
    """
    Contains cartesian coordinates with the following reference:
    x = right-east
    y = up-north
    z = toward earth
    """
    
    def __init__(self, x, y, z=0):
        #super().__init__()
        Coordinates.__init__(self)
        self.x = x
        self.y = y
        self.z = z

    def translate(self, delta_x=0, delta_y=0, delta_z=0):

        self.x += delta_x
        self.y += delta_y
        self.z += delta_z

    def rotate_around_x(self, theta):
        """
        Rotate counterclockwise of theta degrees.
        """
        y_rot = (self.y * math.cos(theta * math.pi/180.) -
                 self.z * math.sin(theta * math.pi/180.))
        z_rot = (self.y * math.sin(theta * math.pi/180.) +
                 self.z * math.cos(theta * math.pi/180.))
        self.y = y_rot
        self.z = z_rot
        
    def rotate_around_y(self, theta):
        """
        Rotate counterclockwise of theta degrees.
        """
        x_rot = (self.x * math.cos(theta * math.pi/180.) +
                 self.z * math.sin(theta * math.pi/180.))
        z_rot = (-self.x * math.sin(theta * math.pi/180.) +
                 self.z * math.cos(theta * math.pi/180.))
        self.x = x_rot
        self.z = z_rot

    def rotate_around_z(self, theta):
        """
        Rotate counterclockwise of theta degrees.
        """
        x_rot = (self.x * math.cos(theta * math.pi/180.) -
                 self.y * math.sin(theta * math.pi/180.))
        y_rot = (self.x * math.sin(theta * math.pi/180.) +
                 self.y * math.cos(theta * math.pi/180.))
        self.x = x_rot
        self.y = y_rot
        
    def distance(self, pointB):
        """
        Return the distance between the point A and B
        """
        return math.sqrt((self.x - pointB.x)** 2 +
                         (self.y - pointB.y)** 2 +
                         (self.z - pointB.z)** 2)
    
    """def angle_from_x_axis(self, pointB):
        
        Return the angle in degree between the x-axis and vector formed with the point B
        
        return math.atan((self.y - pointB.y)/float(self.x - pointB.x)) * 180/math.pi
    
    def angle_from_y_axis(self, pointB):
        
        Return the angle in degree between the x-axis and vector formed with the point B
        
        return math.atan((self.x - pointB.x)/float(self.y - pointB.y)) * 180/math.pi
        """
    def normalize(self, value):
        if value>0:
            #print(self.x, self.y, self.z, value)
            self.x = self.x/value
            self.y = self.y/value
            self.z = self.z/value
        else:
            print("the value must be greater than 0!")

    def set_axis_z(self):
        self.z = math.sqrt(1 - self.x**2 - self.y**2)

    def convert_to_spherical(self):
        """
        Return the spherical coordinate theta and phi in radian
        """
        radius = 1
        theta = math.atan2(self.x, self.z) 
        phi = math.acos(self.y/radius) 

        return theta, phi

def cartesian_from_drawing(x_center, y_center, x_north,
                           y_north, HGC_long, HGC_lat,
                           angle_P, angle_B0, angle_L0):

    """
    Given a heliographic longitude and latitude, 
    returns the corresponding x, y, z positions on the drawing.
    """
    center = Cartesian(x_center, y_center)
    north = Cartesian(x_north, y_north)
    #angle_calibration = center.angle_from_y_axis(north)
    radius = center.distance(north)

    theta = (angle_L0 * math.pi/180) - HGC_long
    phi = math.pi/2 - HGC_lat

    print("theta:", theta)
    print("phi", phi)
    
    sun_spherical = Spherical(1, theta, phi)
    x, y, z = sun_spherical.convert_to_cartesian()

    sun_cartesian = Cartesian(x, y, z)
    sun_cartesian.rotate_around_x(angle_B0)
    sun_cartesian.rotate_around_z(-angle_P)

    print("x:", x)
    print("y:", y)
    print("z:", z)
    drawing = Cartesian(sun_cartesian.x,
                           sun_cartesian.y,
                           sun_cartesian.z)
    #drawing.rotate_around_z(-angle_calibration)
    drawing.normalize(1./radius)

    return drawing.x, drawing.y, drawing.z
    

def heliographic_from_drawing(x_center, y_center, x_north,
                              y_north, x_drawing, y_drawing,
                              angle_P, angle_B0, angle_L0):
    """
    Given a position on the drawing, 
    returns the corresponding heliographic longitude and latitude.
    """
    center = Cartesian(x_center, y_center)
    north = Cartesian(x_north, y_north)
    #angle_calibration = center.angle_from_y_axis(north)
    radius = center.distance(north)
    print("radius:", radius)
    drawing = Cartesian(x_drawing, y_drawing)
    
    disk_trigo = Cartesian(drawing.x, drawing.y)
    print("x:", disk_trigo.x)
    print("y:", disk_trigo.y)
    disk_trigo.translate(-center.x, -center.y)
    print("x:", disk_trigo.x)
    print("y:", disk_trigo.y)
    disk_trigo.normalize(radius)
    print("x:", disk_trigo.x)
    print("y:", disk_trigo.y)
    #print("z:", disk_trigo.z)
    disk_trigo.set_axis_z()
    print("z:", disk_trigo.z)
    disk_trigo.y = - disk_trigo.y
    #disk_trigo.rotate_around_z(angle_calibration)
        
    sun = Cartesian(disk_trigo.x, disk_trigo.y, disk_trigo.z)
    sun.rotate_around_z(angle_P)
    sun.rotate_around_x(-angle_B0)
    theta, phi = sun.convert_to_spherical()

    print("theta", theta)
    print("phi", phi)
    
    central_meridian_distance = theta
    HGC_longitude = (angle_L0 * math.pi/180) - central_meridian_distance
    HGC_latitude = math.pi/2 - phi
    
    return HGC_longitude, HGC_latitude



def check_accuracy():

    radius = 12.5
    error = 0.1
    angle_P = 0
    angle_B0 = 0
    angle_L0 = 0
    x_center = 0
    y_center = 0
    x_north = 0
    y_north = radius
    x_drawing = 0
    y_drawing = 0

    position = []
    diff_long_0_0_0 = []
    diff_lat_0_0_0 = []
    diff_long_26_0_0 = []
    diff_lat_26_0_0 = []
    diff_long_0_7_0 = []
    diff_lat_0_7_0 = []
    diff_long_0_0_180 = []
    diff_lat_0_0_180 = []
    
    for el in range(0,125,5):
        position.append(el/10.)
        long_tmp, lat_tmp = check_position_from_drawing(x_center, y_center, x_north,
                                                        y_north, x_drawing, el/10.,
                                                        angle_P, angle_B0, angle_L0) 
        long_0 = long_tmp * math.pi/180
        lat_0 = lat_tmp * math.pi/180.
        long_tmp, lat_tmp = check_position_from_drawing(x_center, y_center, x_north,
                                                        y_north, x_drawing, (el/10.) + error, 
                                                        angle_P, angle_B0, angle_L0) 
        
        long_1 = long_tmp * math.pi/180
        lat_1 = lat_tmp * math.pi/180.
        diff_long_0_0_0.append( abs(long_1 - long_0))
        diff_lat_0_0_0.append( abs(lat_1 - lat_0))

        long_tmp, lat_tmp = check_position_from_drawing(x_center, y_center, x_north,
                                                        y_north, x_drawing, el/10.,
                                                        26.31, angle_B0, angle_L0) 
        long_0 = long_tmp * math.pi/180
        lat_0 = lat_tmp * math.pi/180.
        long_tmp, lat_tmp = check_position_from_drawing(x_center, y_center, x_north,
                                                        y_north, x_drawing, (el/10.) + error, 
                                                        26.31, angle_B0, angle_L0)
        long_1 = long_tmp * math.pi/180
        lat_1 = lat_tmp * math.pi/180.
        
        diff_long_26_0_0.append( abs(long_1 - long_0))
        diff_lat_26_0_0.append( abs(lat_1 - lat_0))
        
        long_tmp, lat_tmp = check_position_from_drawing(x_center, y_center, x_north,
                                                        y_north, x_drawing, el/10., 
                                                        angle_P, 7.23, angle_L0) 
        long_0 = long_tmp * math.pi/180
        lat_0 = lat_tmp * math.pi/180.
        long_tmp, lat_tmp = check_position_from_drawing(x_center, y_center, x_north,
                                                        y_north, x_drawing, (el/10.) + error, 
                                                        angle_P, 7.23, angle_L0) 
        
        long_1 = long_tmp * math.pi/180
        lat_1 = lat_tmp * math.pi/180.
        diff_long_0_7_0.append( abs(long_1 - long_0))
        diff_lat_0_7_0.append( abs(lat_1 - lat_0))

        long_tmp, lat_tmp = check_position_from_drawing(x_center, y_center, x_north,
                                                        y_north, x_drawing, el/10., 
                                                        angle_P, angle_B0, 180) 
        long_0 = long_tmp * math.pi/180
        lat_0 = lat_tmp * math.pi/180.
        long_tmp, lat_tmp = check_position_from_drawing(x_center, y_center, x_north,
                                                        y_north, x_drawing, (el/10.) + error, 
                                                        angle_P, angle_B0, 180) 
        
        long_1 = long_tmp * math.pi/180
        lat_1 = lat_tmp * math.pi/180.
        diff_long_0_0_180.append( abs(long_1 - long_0))
        diff_lat_0_0_180.append( abs(lat_1 - lat_0))
        
    
    plt.plot(position, diff_lat_0_0_0,label='P=0, B0=0, L0=0')
    plt.plot(position, diff_lat_26_0_0,label='P=7, B0=0, L0=0')
    plt.plot(position, diff_lat_0_7_0,label='P=0, B0=7, L0=0')
    plt.plot(position, diff_lat_0_0_180,label='P=0, B0=0, L0=180')
    plt.xlabel('y position(cm)')
    plt.ylabel('latitude error(degree)')
    plt.legend(loc='upper left')
    plt.grid()
    plt.show()


if __name__=="__main__":
    check_accuracy()
