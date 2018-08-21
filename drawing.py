from datetime import date, time, datetime
import database, coordinates

"""
to do:
- method the print the drawing information in a nice way.
"""

class Group():
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

        self.id_ = 0
        self.datetime = datetime(2000,01,01,00,00)
        self.drawing_type = 'None'
        self.number = 0
        self.longitude = 0
        self.latitude = 0
        self.Lcm = 0
        self.alpha_angle = 0
        self.L0 = 0
        self.quadrant = 0
        self.McIntosh = 'Xxx'
        self.zurich = 'X'
        self.spots = 0

    def fill_from_database(self, datetime, group_number):
        """
        A drawing can be identified uniquely with its datetime.
        Then all the attribute of the drawing can be filled from the database
        """
        self.datetime = datetime
        
        db = database.database()

        (self.id_,
         self.datetime,
         self.drawing_type,
         self.number,
         self.latitude,
         self.longitude,
         self.Lcm,
         self.alpha_angle,
         self.L0,
         self.quadrant,
         self.McIntosh,
         self.zurich,
         self.spots,
         self.dipole1_lat,
         self.dipole1_long,
         self.dipole2_lat,
         self.dipole2_long,
         self.dipole_defined,
         self.surface,
         self.raw_surface_px,
         self.raw_surface_msd,
         self.g_spot) = db.get_all_datetime_group_number("groups", datetime, group_number)[0]
        

class Drawing():
    """
    It represents all the information extracted from the drawing
    and stored in the database.
    """
    def __init__(self):

        #print("initialize a drawing..")

        self.id_drawnig= 0 
        self.datetime = datetime(2000,01,01,00,00)
        self.drawing_type = 'None'
        self.quality = 'None'
        self.observer = 'None'
        self.carington_rotation = 0
        self.julian_date = 0.0
        self.calibrated = 0
        self.analyzed = 0
        self.group_count = 0
        self.spot_count = 0
        self.wolf = 0
        self.angle_B = 0.0
        self.angle_L = 0.0
        self.angle_P = 0.0
        self.angle_scan = 0
        self.path = 'None'
        self.operator = 'None'
        self.last_update_time = datetime.now()
       
        self.calibrated_center = coordinates.Cartesian(0,0)
        self.calibrated_north = coordinates.Cartesian(0,0)
        self.calibrated_radius = 0

        self.group_lst = []

    
    """def is_different(self, drawing_to_compare):

        if (self.datetime == drawing_to_compare.datetime and
            self.drawing_type == drawing_to_compare.drawing_type and
            self.quality == drawing_to_compare.quality and
            self.observer == drawing_to_compare.observer and
            self.carington
    """    
    def fill_from_database(self, datetime):
        """
        A drawing can be identified uniquely with its datetime.
        Then all the attribute of the drawing can be filled from the database
        """
        self.datetime = datetime
        
        db = database.database()
        
        (self.id_drawing,
         self.datetime,
         self.drawing_type, 
         self.quality, 
         self.observer, 
         self.carington_rotation,
         self.julian_date, 
         self.calibrated, 
         self.analyzed, 
         self.group_count, 
         self.spot_count, 
         self.wolf, 
         self.angle_P, 
         self.angle_B, 
         self.angle_L, 
         self.angle_scan, 
         self.path, 
         self.operator, 
         self.last_update_time) = db.get_all_datetime("drawings", datetime)[0]
        
        
        (self.id_calibration,
         self.datetime_calibration,
         self.drawing_type_calibration,
         self.calibrated_north.x,
         self.calibrated_north.y,
         self.calibrated_center.x,
         self.calibrated_center.y,
         self.calibrated_radius) = db.get_all_datetime("calibrations", datetime)[0]

        
        for group_number in range(self.group_count):
            group_tmp = Group()
            group_tmp.fill_from_database(self.datetime, group_number)
            self.group_lst.append(group_tmp)
            #print(group_number, self.group_lst[group_number].longitude, self.group_lst[group_number].latitude)
        
