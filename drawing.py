# !/usr/bin/env python
#coding: utf-8

from datetime import date, time, datetime
import coordinates
from PyQt4 import QtCore
import math

class Group(QtCore.QObject):
    """
    Note: It is important to change the value before emitting the signal
    Otherwhise might play with old value due to signal emitted!!
    """
    
    value_changed = QtCore.pyqtSignal()
    
    def __init__(self, param=None):
        super(Group, self).__init__()

        try:
            (self._id_,
             self._datetime,
             self._number,
             self._latitude,
             self._longitude,
             self._Lcm,
             self._CenterToLimb_angle,
             self._quadrant,
             self._McIntosh,
             self._zurich,
             self._spots,
             self._dipole1_lat,
             self._dipole1_long,
             self._dipole2_lat,
             self._dipole2_long,
             self._surface,
             self._raw_surface_px,
             self._raw_surface_msd,
             self._g_spot,
             self._posX,
             self._posY,
             self._dipole1_posX,
             self._dipoel1_posY,
             self._dipole2_posX,
             self._dipole2_posY,
             self._largest_spot) = param

        except ValueError:
            print("problem to set the groups parameters from the database")

        except TypeError:
            print("no value for the initialisation of the groups")
            self._id_ = 0
            self._datetime = datetime(2000,01,01,00,00)
            self._number = 0
            self._latitude = None
            self._longitude = None
            self._Lcm = None
            self._CenterToLimb_angle = None
            self._quadrant = None
            self._McIntosh = 'Xxx'
            self._zurich  = 'X'
            self._spots = 0
            self._dipole1_lat = None
            self._dipole1_long = None
            self._dipole2_lat = None
            self._dipole2_long = None
            self._surface = None
            self._raw_surface_px = None
            self._raw_surface_msd = None
            self._g_spot = None
            self._posX = None
            self._posY = None
            self._dipole1_posX = None
            self._dipole_posY = None
            self._dipole2_posX = None
            self._dipole2_posY = None
            self._largest_spot = None
            
        self.changed = False

    def __repr__(self):
        return "Group {}".format(self._number)

    @property    
    def number(self):
        return self._number   
    @number.setter
    def number(self, value):
        print("here we are changing the value of group number to ", value)
        self._number = value
        self.changed = True
        self.value_changed.emit()
        
    @property    
    def longitude(self):
        return self._longitude
    @longitude.setter
    def longitude(self, value):
        """
        the longitude of the group can only be changed via 
        the "change_group_position" function
        """
        print("here we  CAN NOT change the value of longitude to ", value,
              " or ", value*180/math.pi , " degree ")

    @property    
    def latitude(self):
        return self._latitude
    @latitude.setter
    def latitude(self, value):
        """
        the latitude of the group can only be changed via 
        the "change_group_position" function
        """
        print("here we CAN NOT change the value of latitude to ", value,
              " or ", value*180/math.pi , " degree ")
        
    @property    
    def posX(self):
        return self._posX
    @posX.setter
    def posX(self, value):
        """
        the posX of the group can only be changed via 
        the "change_group_position" function
        """
   
    @property    
    def posY(self):
        return self._posY 
    @posY.setter
    def posY(self, value):
        """
        the posX of the group can only be changed via 
        the "change_group_position" function
        """
        print("here we CAN NOT change the value of pos Y to ", value)

    @property    
    def Lcm(self):
        return self._Lcm
    @Lcm.setter
    def Lcm(self, value):
        """
        the Lcm of the group can only be changed via 
        the "change_group_position" function
        """
        print("here we CAN NOT change the value of Lcm to ", value)

    @property    
    def CenterToLimb_angle(self):
        return self._CenterToLimb_angle
    @CenterToLimb_angle.setter
    def CenterToLimb_angle(self, value):
        """
        the Center to limb angle of the group can only be changed via 
        the "change_group_position" function
        """
        print("here we CAN NOT change the value of CenterToLimb angle to ", value)
        
    @property    
    def quadrant(self):
        return self._quadrant
    @quadrant.setter
    def quadrant(self, value):
        """
        the quadrant of the group can only be changed via 
        the "change_group_position" function
        """
        print("here we CAN NOT change the value of quadrant to ", value)
       
    @property    
    def surface(self):
        return self._surface
    @surface.setter
    def surface(self, value):
        print("here we CAN NOT change the value of surface to ", value)
        #self._surface = value
        #self.changed = True
        #self.value_changed.emit()

        
    @property    
    def McIntosh(self):
        #print("here we are reading the value of mcIntosh of a group ")
        return self._McIntosh
    
    @McIntosh.setter
    def McIntosh(self, value):
        print("here we are changing the value of mcIntosh to ", value)
        self._McIntosh = value
        self.changed = True
        self.value_changed.emit()

    @property    
    def zurich(self):
        #print("here we are reading the value of zurich of a group ")
        return self._zurich
    
    @zurich.setter
    def zurich(self, value):
        print("here we are changing the value of zurich to ", value)
        self._zurich = value
        self.changed = True
        self.value_changed.emit()
        

    @property    
    def spots(self):
        """ the number of spots in the group"""
        #print("here we are reading the value of spots of a group ")
        return self._spots
    @spots.setter
    def spots(self, value):
        print("here we are changing the value of spots to ", value)
        self._spots = value
        self.changed = True
        self.value_changed.emit()

    @property    
    def dipole1_lat(self):
        return self._dipole1_lat
    @dipole1_lat.setter
    def dipole1_lat(self, value):
        print("here we CAN NOT change the value of dipole1_lat to ", value)
        #self._dipole1_lat = value
        #self.changed = True
        #self.value_changed.emit()
        
    @property    
    def dipole1_long(self):
        return self._dipole1_long
    @dipole1_long.setter
    def dipole1_long(self, value):
        print("here we CAN NOT change the value of dipole1_long to ", value)
        #self._dipole1_long = value
        #self.changed = True
        #self.value_changed.emit()
        
    @property    
    def dipole2_lat(self):
        return self._dipole2_lat
    @dipole2_lat.setter
    def dipole2_lat(self, value):
        print("here we CAN NOT change the value of dipole2_lat to ", value)
        #self._dipole2_lat = value
        #self.changed = True
        #self.value_changed.emit()
        
    @property    
    def dipole2_long(self):
        return self._dipole2_long
    @dipole2_long.setter
    def dipole2_long(self, value):
        print("here we CAN NOT change the value of dipole2_long to ", value)
        #self._dipole2_long = value
        #self.changed = True
        #self.value_changed.emit()
        
    @property    
    def dipole1_posX(self):
        return self._dipole1_posX
    @dipole1_posX.setter
    def dipole1_posX(self, value):
        print("here we CAN NOT change the value of dipole1_posX to ", value)
        #self._dipole1_posX = value
        #self.changed = True
        #self.value_changed.emit()
   
    @property    
    def dipole1_posY(self):
        return self._dipole1_posY
    @dipole1_posY.setter
    def dipole1_posY(self, value):
        print("here we CAN NOT change the value of dipole1_posY to ", value)
        #self._dipole1_posY = value
        #self.changed = True
        #self.value_changed.emit()

    @property    
    def dipole2_posX(self):
        return self._dipole2_posX
    @dipole2_posX.setter
    def dipole2_posX(self, value):
        print("here we CAN NOT change the value of dipole2_posX to ", value)
        #self._dipole2_posX = value
        #self.changed = True
        #self.value_changed.emit()

    @property    
    def dipole2_posY(self):
        return self._dipole2_posY
    @dipole2_posY.setter
    def dipole2_posY(self, value):
        print("here we CAN NOT change the value of dipole2_posY to ", value)
        #self._dipole2_posY = value
        #self.changed = True
        #self.value_changed.emit()
       
    @property    
    def g_spot(self):
        return self._g_spot
    @g_spot.setter
    def g_spot(self, value):
        print("here we CAN NOT change the value of g_spot to ", value)
        
    @property    
    def largest_spot(self):
        return self._largest_spot
    @largest_spot.setter
    def largest_spot(self, value):
        """
        TO DO: here check that is the value is either L, T or E
        """
        print("here we are changing the value of the largest spot to ", value)
        self._largest_spot = value         
        self.changed = True
        self.value_changed.emit()

        
    def set_dipole_position(self, dipole_points, dipole_angles):
        """
        Add the dipole to the database by clicking on the drawing
        """
        print("set the dipole position")
        if len(dipole_points)==4:
            self._dipole1_posX = dipole_points[0]
            self._dipole1_posY = dipole_points[1]
            self._dipole2_posX = dipole_points[2]
            self._dipole2_posY = dipole_points[3]
            self._dipole1_lat = dipole_angles[0]
            self._dipole1_long = dipole_angles[1]
            self._dipole2_lat = dipole_angles[2]
            self._dipole2_long = dipole_angles[3]
        
            self.changed = True
            self.value_changed.emit()

    def update_g_spot(self):
        """
        Update the g_spot in two situations:
        - the McIntosh type change
        - the largest spot change
        """
        group_compactness = self._McIntosh[2]
        self._g_spot = 0
        if self.largest_spot=='L' and group_compactness=='o':
            self._g_spot = 1
        elif self.largest_spot=='T' and group_compactness=='o':
            self._g_spot = 2
        elif self.largest_spot=='E' and group_compactness=='o':
            self._g_spot = 3
        elif self.largest_spot=='L' and group_compactness=='i':
            self._g_spot = 4
        elif self.largest_spot=='T' and group_compactness=='i':
            self._g_spot = 5
        elif self.largest_spot=='E' and group_compactness=='i':
            self._g_spot = 6
        elif self.largest_spot=='L' and group_compactness=='c':
            self._g_spot = 7
        elif self.largest_spot=='T' and group_compactness=='c':
            self._g_spot = 8
        elif self.largest_spot=='E' and group_compactness=='c':
            self._g_spot = 9
        #print("g spot has been updated to ", self.g_spot)   
        self.changed = True
        self.value_changed.emit()

    def set_surface(self, pixel_nb, proj_area, deproj_area):

        self._raw_surface_px = pixel_nb
        self._surface = deproj_area
        self._raw_surface_msd = proj_area
        
        self.changed = True
        self.value_changed.emit()
        
       
class Drawing(QtCore.QObject):
    """
    It represents all the information extracted from the drawing
    and stored in the database.
    All the attribute are 'private' 
    (in the python convention with the underscore
    before the name).
    """

    value_changed = QtCore.pyqtSignal()
                   
    def __init__(self, param = None):

        super(Drawing, self).__init__()  
        try:
            (self._id_drawing,
             self._datetime,
             self._drawing_type,
             self._quality,
             self._observer,
             self._carington_rotation,
             self._julian_date,
             self._calibrated,
             self._analyzed,
             self._group_count,
             self._spot_count,
             self._wolf,
             self._angle_P,
             self._angle_B,
             self._angle_L,
             self._path,
             self._operator,
             self._last_update_time) = param

        except ValueError:
            print("problem to set the drawing parameters from the database")

        except TypeError:
            print("no value for the initialisation of the drawing")
            self._id_drawing = 0
            self._datetime = datetime(2000,01,01,00,00)
            self._drawing_type = None
            self._quality = None
            self._observer = None
            self._carington_rotation = 0
            self._julian_date = 0.0
            self._calibrated = 0
            self._analyzed = 0
            self._group_count = 0
            self._spot_count = 0
            self._wolf = 0
            self._angle_P = 0
            self._angle_B = 0
            self._angle_L = 0
            self._path = None
            self._operator = None
            self._last_update_time = None
            
        self._group_lst = []
        
        self.changed = False

    def set_drawing_type(self, param):
        """
        Set the drawing type parameters from a list of value from the database.
        """
        try:
            (self._id_drawing_type,
             self._name,
             self._prefix,
             self._p_oriented,
             self._height,
             self._widht,
             self._pt1_name,
             self._pt2_name,
             self._pt1_fraction_width,
             self._pt1_fraction_height,
             self._pt2_fraction_width,
             self._pt2_fraction_height) = param

        except ValueError:
            print("problem to set the drawing_type from the database")
         
    def set_calibration(self, param):
        """
        Set the calibration parameters from a list of value from the database.
        """
        self._calibrated_center = coordinates.Cartesian(0,0)
        self._calibrated_north = coordinates.Cartesian(0,0)
        
        try:
            (self._id_calibration,
             self._datetime_calibration,
             self._drawing_type_calibration,
             self._calibrated_north.x,
             self._calibrated_north.y,
             self._calibrated_center.x,
             self._calibrated_center.y,
             self._calibrated_radius,
             self._calibrated_angle_scan) = param
            
        except ValueError:
            print("problem to set the calibraiton from the database")

            
    def set_group(self, param):
        """
        Set a new group from a list of value from the database.
        """
        group_tmp = Group(param)
        group_tmp.value_changed.connect(self.get_group_signal)
        self._group_lst.append(group_tmp)
        
    def radius(self, pt1, pt2):
        return math.sqrt((pt1.x - pt2.x)**2 + (pt1.y - pt2.y)**2)
        
    def calibrate(self, point1_x, point1_y, point2_x, point2_y):
        """
        Calcualte the calibrated center and calibrated north from 
        - the input points
        - pt name (drawing type information)
        """
        if self.pt1_name == 'Center'  and self.pt2_name == 'North':
            self.calibrated_center = coordinates.Cartesian(point1_x, point1_y)
            self.calibrated_north = coordinates.Cartesian(point2_x, point2_y)
            self.calibrated_radius = self.calibrated_center.distance(
                self.calibrated_north)

        elif self.pt1_name == 'South'  and self.pt2_name == 'North':
            self.calibrated_center = coordinates.Cartesian(
                (point1_x + point2_x)/2,
                (point1_y + point2_y)/2)
            self.calibrated_north = coordinates.Cartesian(point2_x, point2_y)
            self.calibrated_radius = self.calibrated_center.distance(
                self.calibrated_north)   
            
        self.calibrated_angle_scan = self.calibrated_center.angle_from_y_axis(
            self.calibrated_north)
        self.calibrated = 1
       
    def get_group_signal(self):
        print("get group signal")
        self.changed = True
        self.value_changed.emit()
        

    def __repr__(self):
        return 'Drawing :  date({}), group_count({})'.format(
            self._datetime, self._group_count)

    @property    
    def datetime(self):
        #print("here we are reading the value of datetime ")
        return self._datetime
    
    @property    
    def drawing_type(self):
        #print("here we are reading the value of drawing_type ")
        return self._drawing_type
    
    @drawing_type.setter
    def drawing_type(self, value):
        print("here we are changing the value of drawing_type to ", value)
        self._drawing_type = value
        self.changed = True
        self.value_changed.emit()
        
        
    @property    
    def quality(self):
        #print("here we are reading the value of quality ")
        return self._quality
    
    @quality.setter
    def quality(self, value):
        print("here we are changing the value of quality to ", value)
        self._quality = value
        self.changed = True
        self.value_changed.emit()
        
    @property    
    def observer(self):
        #print("here we are reading the value of observer ")
        return self._observer

    @observer.setter    
    def observer(self, value):
        print("here we are changing the value of observer to ", value)
        self._observer = value
        self.changed = True
        self.value_changed.emit()
        
    @property    
    def carington_rotation(self):
        #print("here we are reading the value of observer ")
        return self._carington_rotation

    @carington_rotation.setter    
    def carington_rotation(self, value):
        print("here we are changing the value of carington rotation to ", value)
        self._carington_rotation = value
        self.changed = True
        self.value_changed.emit()
               
    @property    
    def calibrated(self):
        return self._calibrated
    
    @calibrated.setter
    def calibrated(self, value):
        print("here we are changing the value of calibrated to ", value)
        self._calibrated = value
        self.changed = True
        self.value_changed.emit()

    @property    
    def analyzed(self):
        return self._analyzed
    
    @analyzed.setter
    def analyzed(self, value):
        print("here we are changing the value of analyzed to ", value)
        self._analyzed = value
        self.changed = True
        self.value_changed.emit()

    @property    
    def group_count(self):
        return self._group_count
    
    @group_count.setter
    def group_count(self, value):
        """ 
        change only via the update_group_number" function
        """
        print("here we CAN NOT change the value of group_count to ", value)
        #self._group_count = value
        #self.changed = True
        #self.value_changed.emit()

    @property    
    def wolf(self):
        return self._wolf
    
    @wolf.setter
    def wolf(self, value):
        """
        Wolf is only changed via add/delete a group or 
        change the spots number of a group
        """
        print("here we CAN NOT change the value of wolf to ", value)
        #self._wolf = value
        #self.changed = True
        #self.value_changed.emit()
            
    @property
    def angle_P(self):
        #print("here we are reading the value of angle P")
        return self._angle_P

    @angle_P.setter
    def angle_P(self, value):
        print("here we are changing the value of angle_P to ", value)
        self._angle_P = value
        self.changed = True
        self.value_changed.emit()
        

    @property
    def angle_B(self):
        #print("here we are reading the value of angle B")
        return self._angle_B

    @angle_B.setter
    def angle_B(self, value):
        print("here we are changing the value of angle_B to ", value)
        self._angle_B = value
        self.changed = True
        self.value_changed.emit()
        

    @property
    def angle_L(self):
        #print("here we are reading the value of angle L")
        return self._angle_L

    @angle_L.setter
    def angle_L(self, value):
        print("here we are changing the value of angle_L to ", value)
        self._angle_L = value
        self.changed = True
        self.value_changed.emit()
        
        
    @property    
    def operator(self):
        #print("here we are reading the value of operator")
        return self._operator
    
    @operator.setter
    def operator(self, value):
        print("here we are changing the value of operator to ", value)
        self._operator = value
        self.changed = True
        self.value_changed.emit()
  
    @property
    def group_lst(self):
        #print("here we are reading the value of group_lst")
        return self._group_lst

    @group_lst.setter
    def group_lst(self, value):
        print("here we are changing the value of group_lst to ", value)
        self._group_lst = value
        self.changed = True
        self.value_changed.emit()
        

    @property
    def calibrated_center(self):
        ##rint("here we are reading the value of calibrated center")
        return self._calibrated_center

    @calibrated_center.setter
    def calibrated_center(self, value):
        print("here we are changing the value of calibrated center to ",
              value.x, value.y)
        self._calibrated_center = coordinates.Cartesian(value.x, value.y)
        self.changed = True
        self.value_changed.emit()
        
    @property
    def calibrated_center_x(self):
        ##rint("here we are reading the value of calibrated center")
        return self._calibrated_center.x

    @calibrated_center_x.setter
    def calibrated_center_x(self, value):
        print("here we are changing the value of calibrated center x to ", value)
        self._calibrated_center.x = value
        self.changed = True
        self.value_changed.emit()
        
    @property
    def calibrated_center_y(self):
        ##rint("here we are reading the value of calibrated center")
        return self._calibrated_center.y

    @calibrated_center_y.setter
    def calibrated_center_y(self, value):
        print("here we are changing the value of calibrated center y to ", value)
        self._calibrated_center.y = value
        self.changed = True
        self.value_changed.emit()
        
    @property
    def calibrated_north(self):
        #print("here we are reading the value of calibrated north")
        return self._calibrated_north

    @calibrated_north.setter
    def calibrated_north(self, value):
        print("here we are changing the value of calibrated north to ",
              value.x, value.y)
        self._calibrated_north = coordinates.Cartesian(value.x, value.y)
        self.changed = True
        self.value_changed.emit()
        
    @property
    def calibrated_north_x(self):
        ##rint("here we are reading the value of calibrated north")
        return self._calibrated_north.x

    @calibrated_north_x.setter
    def calibrated_north_x(self, value):
        print("here we are changing the value of calibrated north x to ", value)
        self._calibrated_north.x = value
        self.changed = True
        self.value_changed.emit()
        
    @property
    def calibrated_north_y(self):
        ##rint("here we are reading the value of calibrated north")
        return self._calibrated_north.y

    @calibrated_north_y.setter
    def calibrated_north_y(self, value):
        print("here we are changing the value of calibrated north y to ", value)
        self._calibrated_north.y = value
        self.changed = True
        self.value_changed.emit()
        
    @property
    def calibrated_radius(self):
        #print("here we are reading the value of calibrated radius")
        return self._calibrated_radius

    @calibrated_radius.setter
    def calibrated_radius(self, value):
        print("here we are changing the value of calibrated radius to ", value)
        self._calibrated_radius = value
        self.changed = True
        self.value_changed.emit()

    @property
    def calibrated_angle_scan(self):
        #print("here we are reading the value of calibrated radius")
        return self._calibrated_angle_scan

    @calibrated_angle_scan.setter
    def calibrated_angle_scan(self, value):
        print("here we are changing the value of calibrated angle scan to ",
              value)
        self._calibrated_angle_scan = value
        self.changed = True
        self.value_changed.emit()

    @property    
    def pt1_fraction_width(self):
        #print("here we are reading the value of drawing_type ")
        return self._pt1_fraction_width
    
    @pt1_fraction_width.setter
    def pt1_fraction_width(self, value):
        print("here we are changing the value of fraction width to ", value)
        print("this is not authorized!!")
        #self._pt1_fraction_width = value
        #self.changed = True
        #self.value_changed.emit()

    @property    
    def pt1_fraction_height(self):
        #print("here we are reading the value of drawing_type ")
        return self._pt1_fraction_height
    
    @pt1_fraction_height.setter
    def pt1_fraction_height(self, value):
        print("here we are changing the value of fraction height to ", value)
        print("this is not authorized!!")
        #self._pt1_fraction_height = value
        #self.changed = True
        #self.value_changed.emit()

    @property    
    def pt2_fraction_width(self):
        #print("here we are reading the value of drawing_type ")
        return self._pt2_fraction_width
    
    @pt2_fraction_width.setter
    def pt2_fraction_width(self, value):
        print("here we are changing the value of fraction width to ", value)
        print("this is not authorized!!")
        #self._pt2_fraction_width = value
        #self.changed = True
        #self.value_changed.emit()

    @property    
    def pt2_fraction_height(self):
        #print("here we are reading the value of drawing_type ")
        return self._pt2_fraction_height
    
    @pt2_fraction_height.setter
    def pt2_fraction_height(self, value):
        print("here we are changing the value of fraction height to ", value)
        print("this is not authorized!!")
        #self._pt2_fraction_height = value
        #self.changed = True
        #self.value_changed.emit()  

    @property    
    def pt1_name(self):
        #print("here we are reading the value of drawing_type ")
        return self._pt1_name

    @pt1_name.setter
    def pt1_name(self, value):
        print("here we are changing the value of point1 name to ", value)
        print("this is not authorized!!")
        #self._pt2_fraction_height = value
        #self.changed = True
        #self.value_changed.emit()

    @property    
    def pt2_name(self):
        #print("here we are reading the value of drawing_type ")
        return self._pt2_name

    @pt2_name.setter
    def pt2_name(self, value):
        print("here we are changing the value of point2 name to ", value)
        print("this is not authorized!!")

    @property
    def last_update_time(self):
        return self._last_update_time

    @last_update_time.setter
    def last_update_time(self, value):
        print("here we are changing the value of last update time to ", value)
        self._last_update_time = value
        self.changed = True
        self.value_changed.emit()
        
    def change_group_position(self, group_number, latitude, longitude, posX, posY):
        """
        Update the position of the group and all the quantities related to it.
        - the HGC latitude of the group
        - the HGC longitude of the group
        - the raw position of the group on the drawing
        - the the central merdian distance (LCM)
        - the center to limb angle
        - the quadrant
        """
        print("update the position of the group!!!")
        
        self._group_lst[group_number]._latitude = latitude
        self._group_lst[group_number]._longitude = longitude
        self._group_lst[group_number]._posX = posX
        self._group_lst[group_number]._posY = posY

        print("latitude : {} ".format(self._group_lst[group_number]._latitude))
        print("longitude : {} ".format(self._group_lst[group_number]._longitude))
        print("posX : {} ".format(self._group_lst[group_number]._posX))
        print("posY : {} ".format(self._group_lst[group_number]._posY))
        
        self._group_lst[group_number]._Lcm = self._angle_L - longitude * 180/math.pi
        distance_from_center = math.sqrt((posX - self.calibrated_center.x )**2 +
                                         (posY - self.calibrated_center.y )**2)
        
        self._group_lst[group_number]._CenterToLimb_angle = (math.asin(distance_from_center *
                                             1./self.calibrated_radius) * 180. /math.pi)

        if posX > self.calibrated_center.x and posY > self.calibrated_center.y:
            self._group_lst[group_number]._quadrant = "NE"
        elif posX > self.calibrated_center.x and posY < self.calibrated_center.y:
            self._group_lst[group_number]._quadrant = "SE"
        elif posX < self.calibrated_center.x and posY > self.calibrated_center.y:
            self._group_lst[group_number]._quadrant = "NW"
        elif posX < self.calibrated_center.x and posY < self.calibrated_center.y:
            self._group_lst[group_number]._quadrant = "SW"   
        
        self.changed = True
        self.value_changed.emit()

        
    def update_spot_number(self, group_number, sunspot_number):
        """
        Change the sunspot number -> update:
        - groups.spots
        - drawings.spot_count
        - drawings.wolf
        """
        #print("update the sunspot_number!", sunspot_number)
        self._group_lst[group_number]._spots = sunspot_number
        total_sunspots = 0
        for group in self._group_lst:
            total_sunspots +=  group._spots
        self._spot_count = total_sunspots
        self._wolf = self._group_count * 10 + self._spot_count
        self.changed = True
        self.value_changed.emit()

    def update_group_number(self, group_number):
        self._group_count = group_number
        total_sunspots = 0
        for group in self._group_lst:
            total_sunspots +=  group._spots

            self._wolf = self._group_count * 10 + self._spot_count
        self.changed = True
        self.value_changed.emit()
        
    def add_group(self, latitude, longitude, posX, posY):
        """
        By clicking on the drawing, one add to the database:
        - group_count + 1 -> update the wolf number
        - group position and all the quantities related to it.
        """

        self.update_group_number(self.group_count + 1)
        group_tmp = Group()
        group_tmp.number = self.group_count - 1
        self._group_lst.append(group_tmp)
                               
        self.change_group_position(self.group_count - 1, latitude, longitude,
                                   posX, posY)

    def delete_group(self, group_index):
        """
        Delete a group among the list of groups
        """
        self.update_spot_number(group_index, 0)
        self.update_group_number(self.group_count - 1)
        self._group_lst.pop(group_index)
        
        for i in range(group_index, len(self._group_lst)):
            self._group_lst[i].number = i
            
