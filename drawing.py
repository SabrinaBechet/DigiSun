from datetime import date, time, datetime
import database, coordinates
from PyQt4 import QtCore

import math

"""
to do:
- method the print the drawing information in a nice way.
"""

class Group(QtCore.QObject):
    """
    It contains all the information of a group extracted from the drawing.
    The attributes are:
    - id = id in the mysql database
    - datetime =  datetime of the drawing
    - drawing_type = type of drawing
    - number =  number of the sunspot among all the group of the drawing
    - longitude of the barycenter of the group
    - latitude of the barycenter of the group
    - Lcm ??
    - alpha_angle ??
    - quandrant ??
    - McIntosh = classification of the group
    - Zurich = classification of the group
    - Spots = number of spots
    - Dipole1Lat
    - Dipole1Long
    - Dipole2Lat
    - Dipole2Long
    - DipoleDefined
    - Surface
    - RawSurface_px
    - rawSurface_msd
    - GSpot

    Note: It is important to change the value before emitting the signal
    Otherwhise might play with old signal due to signal emitted!!
    """
    
    value_changed = QtCore.pyqtSignal()
    
    def __init__(self):
        super(Group, self).__init__()
        
        self._id_ = 0
        self._datetime = datetime(2000,01,01,00,00)
        self._drawing_type = 'None'
        self._number = 0
        self._longitude = 0
        self._latitude = 0
        self._pos_X = 0
        self._pos_Y = 0 
        self._Lcm = 0
        self._CenterToLimb_angle = 0
        self._L0 = 0
        self._quadrant = 0
        self._McIntosh = 'Xxx'
        self._zurich = 'X'
        self._spots = 0
        self._dipole1_lat = 0
        self._dipole1_long = 0
        self._dipole2_lat = 0
        self._dipole2_long = 0
        self._dipole_defined = 0
        self._surface = 0
        self._raw_surface_px = 0
        self._raw_surface_msd = 0
        self._g_spot = 0

        self.changed = False


    def __repr__(self):
        return "Group {}".format(self._number)
        
    @property    
    def number(self):
        #print("here we are reading the value of number of a group ")
        return self._number
    
    @number.setter
    def number(self, value):
        print("here we are changing the value of group number to ", value)
        self._number = value
        self.changed = True
        self.value_changed.emit()
        
    @property    
    def longitude(self):
        #print("here we are reading the value of longitude of a group ")
        return self._longitude
    
    @longitude.setter
    def longitude(self, value):
        print("here we are changing the value of longitude to ", value,
              " or ", value*180/math.pi , " degree ")
        self._longitude = value
        self.changed = True
        self.value_changed.emit()

    @property    
    def latitude(self):
        #print("here we are reading the value of latitude of a group ")
        return self._latitude
    
    @latitude.setter
    def latitude(self, value):
        print("here we are changing the value of latitude to ", value,
              " or ", value*180/math.pi , " degree ")
        self._latitude = value
        self.changed = True
        self.value_changed.emit()

    @property    
    def pos_X(self):
        #print("here we are reading the value of longitude of a group ")
        return self._pos_X
    
    @pos_X.setter
    def pos_X(self, value):
        print("here we are changing the value of pos X to ", value)
        self._pos_X = value
        self.changed = True
        self.value_changed.emit()

    @property    
    def pos_Y(self):
        #print("here we are reading the value of longitude of a group ")
        return self._pos_Y
    
    @pos_Y.setter
    def pos_Y(self, value):
        print("here we are changing the value of pos Y to ", value)
        self._pos_Y = value
        self.changed = True
        self.value_changed.emit()

    @property    
    def Lcm(self):
        #print("here we are reading the value of longitude of a group ")
        return self._Lcm
    
    @Lcm.setter
    def Lcm(self, value):
        print("here we are changing the value of Lcm to ", value)
        self._Lcm = value
        self.changed = True
        self.value_changed.emit()

    @property    
    def CenterToLimb_angle(self):
        #print("here we are reading the value of longitude of a group ")
        return self._CenterToLimb_angle
    
    @Lcm.setter
    def CenterToLimb_angle(self, value):
        print("here we are changing the value of CenterToLimb angle to ", value)
        self._CenterToLimb_angle = value
        self.changed = True
        self.value_changed.emit()

    @property    
    def quadrant(self):
        #print("here we are reading the value of longitude of a group ")
        return self._quadrant
    
    @quadrant.setter
    def quadrant(self, value):
        print("here we are changing the value of quadrant to ", value)
        self._quadrant = value
        self.changed = True
        self.value_changed.emit()
        
    @property    
    def surface(self):
        #print("here we are reading the value of surface of a group ")
        return self._surface
    
    @surface.setter
    def surface(self, value):
        print("here we are changing the value of surface to ", value)
        self._surface = value
        self.changed = True
        self.value_changed.emit()

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
        #print("here we are reading the value of spots of a group ")
        return self._dipole1_lat
    
    @dipole1_lat.setter
    def dipole1_lat(self, value):
        print("here we are changing the value of dipole1_lat to ", value)
        self._dipole1_lat = value
        self.changed = True
        self.value_changed.emit()
        

    @property    
    def dipole1_long(self):
        #print("here we are reading the value of spots of a group ")
        return self._dipole1_long
    
    @dipole1_long.setter
    def dipole1_long(self, value):
        print("here we are changing the value of dipole1_lat to ", value)
        self._dipole1_long = value
        self.changed = True
        self.value_changed.emit()
        

    @property    
    def dipole2_lat(self):
        #print("here we are reading the value of spots of a group ")
        return self._dipole2_lat
    
    @dipole2_lat.setter
    def dipole2_lat(self, value):
        print("here we are changing the value of dipole2_lat to ", value)
        self._dipole2_lat = value
        self.changed = True
        self.value_changed.emit()
        

    @property    
    def dipole2_long(self):
        #print("here we are reading the value of spots of a group ")
        return self._dipole2_long
    
    @dipole2_long.setter
    def dipole2_long(self, value):
        print("here we are changing the value of dipole2_lat to ", value)
        self._dipole2_long = value
        self.changed = True
        self.value_changed.emit()
        
           
    @property    
    def g_spot(self):
        #print("here we are reading the value of g_spot of a group ")
        return self._g_spot
    
    @g_spot.setter
    def g_spot(self, value):
        print("here we are changing the value of g_spot to ", value)
        self._g_spot = value         
        self.changed = True
        self.value_changed.emit()
        
        
    def fill_from_database(self, datetime, group_number):
        """
        A drawing can be identified uniquely with its datetime.
        Then all the attribute of the drawing can be filled from the database
        """
        self._datetime = datetime
        
        db = database.database()

        (self._id_,
         self._datetime,
         self._drawing_type,
         self._number,
         self._latitude,
         self._longitude,
         self._Lcm,
         self._CenterToLimb_angle,
         self._L0,
         self._quadrant,
         self._McIntosh,
         self._zurich,
         self._spots,
         self._dipole1_lat,
         self._dipole1_long,
         self._dipole2_lat,
         self._dipole2_long,
         self._dipole_defined,
         self._surface,
         self._raw_surface_px,
         self._raw_surface_msd,
         self._g_spot,
         self._pos_X,
         self._pos_Y) = db.get_all_datetime_group_number("groups", datetime, group_number)[0]

    
class Drawing(QtCore.QObject):
    """
    It represents all the information extracted from the drawing
    and stored in the database.
    All the attribute are 'private' (in the python convention with the underscore
    before the name).
    """

    value_changed = QtCore.pyqtSignal()
    
    def __init__(self):

        #print("initialize a drawing..")
        super(Drawing, self).__init__()
        self._id_drawnig= 0 
        self._datetime = datetime(2000,01,01,00,00)
        self._drawing_type = 'None'
        self._quality = 'None'
        self._observer = 'None'
        self._carington_rotation = 0
        self._julian_date = 0.0
        self._calibrated = 0
        self._analyzed = 0
        self._group_count = 0
        self._spot_count = 0
        self._wolf = 0
        self._angle_B = 0.0
        self._angle_L = 0.0
        self._angle_P = 0.0
        self._angle_scan = 0
        self._path = 'None'
        self._operator = 'None'
        self._last_update_time = datetime.now()
       
        self._calibrated_center = coordinates.Cartesian(0,0)
        self._calibrated_north = coordinates.Cartesian(0,0)
        self._calibrated_radius = 0
        self._calibrated_angle_scan = 0

        self._prefix = 'None'
        self._p_oriented = 0
        self._height = 0
        self._widht = 0
        self._pt1_name = 'None'
        self._pt1_fraction_width = 0
        self._pt1_fraction_height = 0
        self._pt2_name = 'None'
        self._pt2_fraction_width = 0
        self._pt2_fraction_height = 0
        
        self._group_lst = []

        self.changed = False


    def radius(self, pt1, pt2):

        return math.sqrt((pt1.x - pt2.x)**2 + (pt1.y - pt2.y)**2)
        
    def calibrate(self, point1_x, point1_y, point2_x, point2_y):
        if self.pt1_name == 'Center'  and self.pt2_name == 'North':
            self.calibrated_center = coordinates.Cartesian(point1_x, point1_y)
            self.calibrated_north = coordinates.Cartesian(point2_x, point2_y)
            self.calibrated_radius = self.calibrated_center.distance(self.calibrated_north)

        elif self.pt1_name == 'South'  and self.pt2_name == 'North':
            self.calibrated_center = coordinates.Cartesian((point1_x + point2_x)/2, (point1_y + point2_y)/2)
            self.calibrated_north = coordinates.Cartesian(point2_x, point2_y)
            self.calibrated_radius = self.calibrated_center.distance(self.calibrated_north)   
            
        self.calibrated_angle_scan = self.calibrated_center.angle_from_y_axis(self.calibrated_north)
        self.calibrated = 1
       
            
        
    def get_group_signal(self):
        print("get group signal")
        self.value_changed.emit()
        self.changed = True

    def __repr__(self):
        return 'Drawing :  date({}), group_count({})'.format(
            self._datetime, self._group_count)
            
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
        print("here we are changing the value of group_count to ", value)
        self._group_count = value
        self.changed = True
        self.value_changed.emit()

    @property    
    def wolf(self):
        return self._wolf
    
    @wolf.setter
    def wolf(self, value):
        print("here we are changing the value of wolf to ", value)
        self._wolf = value
        self.changed = True
        self.value_changed.emit()
            
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
        print("here we are changing the value of calibrated center to ", value.x, value.y)
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
        print("here we are changing the value of calibrated north to ", value.x, value.y)
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
        print("here we are changing the value of calibrated angle scan to ", value)
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
        #self._pt2_fraction_height = value
        #self.changed = True
        #self.value_changed.emit() 

    
             
    def fill_from_database(self, datetime):
        """
        A drawing can be identified uniquely with its datetime.
        Then all the attribute of the drawing can be filled from the database
        """
        self.datetime = datetime
        print("fill from database", datetime)

        
        db = database.database()

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
             self._angle_scan, 
             self._path, 
             self._operator, 
             self._last_update_time) = db.get_all_datetime("drawings", datetime)[0]

            
        except IndexError:
            print("empty set for the drawing table..")
            
        print(self._datetime, self._calibrated, self._analyzed)

        try:
            (self._id_calibration,
             self._datetime_calibration,
             self._drawing_type_calibration,
             self._calibrated_north.x,
             self._calibrated_north.y,
             self._calibrated_center.x,
             self._calibrated_center.y,
             self._calibrated_radius,
             self._calibrated_angle_scan) = db.get_all_datetime("calibrations", datetime)[0]

        except IndexError:
            print("empty set for the calibration table")
            self._calibrated = 0

            
        try:
            (self._id_type_of_drawing,
             self._name,
             self._prefix,
             self._p_oriented,
             self._width,
             self._height,
             self._pt1_name,
             self._pt2_name,
             self._pt1_fraction_width,
             self._pt1_fraction_height,
             self._pt2_fraction_width,
             self._pt2_fraction_height) = db.get_drawing_information("drawing_type", self.drawing_type)[0]
            
        except IndexError:
            print("empty set for the drawing_type table..")

            
        for group_number in range(self._group_count):
            group_tmp = Group()
            group_tmp.fill_from_database(self._datetime, group_number)
            group_tmp.value_changed.connect(self.get_group_signal)
            self._group_lst.append(group_tmp)
            #print(group_number, self.group_lst[group_number].longitude, self.group_lst[group_number].latitude)

    def add_group(self, latitude, longitude, posX, posY):

        self.group_count +=1
        group_tmp = Group()
        group_tmp.number = self.group_count - 1
        group_tmp.latitude = latitude
        group_tmp.longitude = longitude
        group_tmp.pos_X = posX
        group_tmp.pos_Y = posY
        
        group_tmp.Lcm = self._angle_L - longitude * 180/math.pi
        
        radius_from_center = math.sqrt((posX - self.calibrated_center.x )**2 +
                                       (posY - self.calibrated_center.y )**2)
        
        group_tmp.CenterToLimb_angle = (math.asin(radius_from_center *
                                                  1./self.calibrated_radius) *
                                        180. /math.pi)

        print("calibrated value: ", self.calibrated_center.x, self.calibrated_center.y)
        print("pos :", posX, posY)
        
        if posX > self.calibrated_center.x and posY > self.calibrated_center.y:
            group_tmp.quadrant = "NE"
        elif posX > self.calibrated_center.x and posY < self.calibrated_center.y:
            group_tmp.quadrant = "SE"
        elif posX < self.calibrated_center.x and posY > self.calibrated_center.y:
            group_tmp.quadrant = "NW"
        elif posX < self.calibrated_center.x and posY < self.calibrated_center.y:
            group_tmp.quadrant = "SW"   
        
        #cmd = self._angle_L - longitude * 180/math.pi
        #print("central meridian distance: ", cmd)
        self._group_lst.append(group_tmp)
        self.changed = True
        self.value_changed.emit()


    def delete_group(self, group_index):
        """
        Delete a group among the list of groups
        """
        self.group_count -= 1
        self._group_lst.pop(group_index)
        for i in range(group_index, len(self._group_lst)):
            self._group_lst[i].number = i
            
