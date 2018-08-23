from datetime import date, time, datetime
import database, coordinates

"""
to do:
- method the print the drawing information in a nice way.
"""

class Group(object):
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
    """
    def __init__(self):

        self._id_ = 0
        self._datetime = datetime(2000,01,01,00,00)
        self._drawing_type = 'None'
        self._number = 0
        self._longitude = 0
        self._latitude = 0
        self._Lcm = 0
        self._alpha_angle = 0
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

    @property    
    def number(self):
        #print("here we are reading the value of number of a group ")
        return self._number
    
    @number.setter
    def number(self, value):
        print("here we are changing the value of number to ", value)
        self._number = value

    @property    
    def longitude(self):
        #print("here we are reading the value of longitude of a group ")
        return self._longitude
    
    @longitude.setter
    def longitude(self, value):
        print("here we are changing the value of longitude to ", value)
        self._longitude = value

    @property    
    def latitude(self):
        #print("here we are reading the value of latitude of a group ")
        return self._latitude
    
    @latitude.setter
    def latitude(self, value):
        print("here we are changing the value of latitude to ", value)
        self._latitude = value    
        
    @property    
    def surface(self):
        #print("here we are reading the value of surface of a group ")
        return self._surface
    
    @surface.setter
    def surface(self, value):
        print("here we are changing the value of surface to ", value)
        self._surface = value

    @property    
    def McIntosh(self):
        #print("here we are reading the value of mcIntosh of a group ")
        return self._McIntosh
    
    @McIntosh.setter
    def McIntosh(self, value):
        print("here we are changing the value of mcIntosh to ", value)
        self._McIntosh = value    

    @property    
    def zurich(self):
        #print("here we are reading the value of zurich of a group ")
        return self._zurich
    
    @zurich.setter
    def zurich(self, value):
        print("here we are changing the value of zurich to ", value)
        self._zurich = value

    @property    
    def spots(self):
        """ the number of spots in the group"""
        #print("here we are reading the value of spots of a group ")
        return self._spots
    
    @spots.setter
    def spots(self, value):
        print("here we are changing the value of spots to ", value)
        self._spots = value

    @property    
    def g_spot(self):
        #print("here we are reading the value of g_spot of a group ")
        return self._g_spot
    
    @g_spot.setter
    def g_spot(self, value):
        print("here we are changing the value of g_spot to ", value)
        self._g_spot = value         
        
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
         self._alpha_angle,
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
         self._g_spot) = db.get_all_datetime_group_number("groups", datetime, group_number)[0]
        

class Drawing(object):
    """
    It represents all the information extracted from the drawing
    and stored in the database.
    All the attribute are 'private' (in the python way with the underscore
    before the name).
    """
    def __init__(self):

        #print("initialize a drawing..")

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

        self._group_lst = []

    @property    
    def drawing_type(self):
        #print("here we are reading the value of drawing_type ")
        return self._drawing_type
    
    @drawing_type.setter
    def drawing_type(self, value):
        print("here we are changing the value of drawing_type to ", value)
        self._drawing_type = value
        
    @property    
    def quality(self):
        #print("here we are reading the value of quality ")
        return self._quality
    
    @quality.setter
    def quality(self, value):
        print("here we are changing the value of quality to ", value)
        self._quality = value
        
    @property    
    def observer(self):
        #print("here we are reading the value of observer ")
        return self._observer

    @property
    def angle_P(self):
        #print("here we are reading the value of angle P")
        return self._angle_P

    @angle_P.setter
    def angle_P(self, value):
        self._angle_P = value

    @property
    def angle_B(self):
        #print("here we are reading the value of angle B")
        return self._angle_B

    @angle_B.setter
    def angle_B(self, value):
        self._angle_B = value   

    @property
    def angle_L(self):
        #print("here we are reading the value of angle L")
        return self._angle_L

    @angle_L.setter
    def angle_L(self, value):
        self._angle_L = value   
    
    @observer.setter
    def observer(self, value):
        #print("here we are changing the value of observer to ", value)
        self._observer = value

    @property    
    def operator(self):
        #print("here we are reading the value of operator")
        return self._operator
    
    @operator.setter
    def operator(self, value):
        print("here we are changing the value of operator to ", value)
        self._operator = value    
        
    @property    
    def calibrated(self):
        return self._calibrated
    
    @calibrated.setter
    def calibrated(self, value):
        #print("here we are changing the value of calibrated to ", value)
        self._calibrated = value

    @property    
    def group_count(self):
        return self._group_count
    
    @group_count.setter
    def group_count(self, value):
        print("here we are changing the value of group_count to ", value)
        self._group_count = value
        
    @property
    def group_lst(self):
        #print("here we are reading the value of group_lst")
        return self._group_lst

    @group_lst.setter
    def group_lst(self, value):
        self._group_lst = value

    @property
    def calibrated_center(self):
        #print("here we are reading the value of calibrated center")
        return self._calibrated_center

    @calibrated_center.setter
    def calibrated_center(self, value):
        self._calibrated_center = value

    @property
    def calibrated_north(self):
        #print("here we are reading the value of calibrated north")
        return self._calibrated_north

    @calibrated_north.setter
    def calibrated_north(self, value):
        self._calibrated_north = value    

    @property
    def calibrated_radius(self):
        #print("here we are reading the value of calibrated radius")
        return self._calibrated_radius

    @calibrated_radius.setter
    def calibrated_radius(self, value):
        self._calibrated_radius = value
        
    def fill_from_database(self, datetime):
        """
        A drawing can be identified uniquely with its datetime.
        Then all the attribute of the drawing can be filled from the database
        """
        self.datetime = datetime
        
        db = database.database()
        
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
        
        
        (self._id_calibration,
         self._datetime_calibration,
         self._drawing_type_calibration,
         self._calibrated_north.x,
         self._calibrated_north.y,
         self._calibrated_center.x,
         self._calibrated_center.y,
         self._calibrated_radius) = db.get_all_datetime("calibrations", datetime)[0]

        
        for group_number in range(self._group_count):
            group_tmp = Group()
            group_tmp.fill_from_database(self._datetime, group_number)
            self._group_lst.append(group_tmp)
            #print(group_number, self.group_lst[group_number].longitude, self.group_lst[group_number].latitude)
        
