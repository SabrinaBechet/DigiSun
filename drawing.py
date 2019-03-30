# !/usr/bin/env python
# coding: utf-8

"""
The Drawing object represent a given drawing.
The Group object represent a group with all its physical/positinal features.
Both information are stored in the database in the table drawings/groups respectively.
"""


from datetime import datetime
import math
import coordinates
import database
import carrington_rotation
import sun_ephemeris
from PyQt4 import QtCore


class Group(QtCore.QObject):
    """
    Note: It is important to change the value before emitting the signal
    Otherwhise might play with old value due to signal emitted!!
    """
    value_changed = QtCore.pyqtSignal()

    def __init__(self, param=None):
        super(Group, self).__init__()

        dict_group_database = {'id' : 0,
                               'DateTime': datetime(2000, 1, 1, 00, 00),
                               'DigiSunNumber': 0,
                               'Latitude': None,
                               'Longitude': None,
                               'Lcm': None,
                               'CenterToLimbAngle': None,
                               'Quadrant': None,
                               'McIntosh': 'Xxx',
                               'Zurich': 'X',
                               'Spots': 0,
                               'Dipole1Lat': None,
                               'Dipole1Long': None,
                               'Dipole2Lat': None,
                               'Dipole2Long': None,
                               'DeprojArea_msh': None,
                               'RawArea_px': None,
                               'ProjArea_msd': None,
                               'GSpot': None,
                               'PosX' : None,
                               'PosY' : None,
                               'Dipole1PosX': None,
                               'Dipole1PosY': None,
                               'Dipole2PosX': None,
                               'Dipole2PosY': None,
                               'LargestSpot': None,
                               'GroupNumber' : None,
                               'GroupExtra1' : '',
                               'GroupExtra2' : '',
                               'GroupExtra3' : ''}

        if param:
            for keys, values in dict_group_database.items():
                try:
                    dict_group_database[keys] = param[keys]
                except KeyError:
                    pass
                    #print("The following information is missing: {} ".format(keys) +
                    #      " It will be set to {} ".format(values))
                    
                
        self._id_ = dict_group_database['id']
        self._datetime = dict_group_database['DateTime']
        self._number = dict_group_database['DigiSunNumber']
        self._latitude = dict_group_database['Latitude']
        self._longitude = dict_group_database['Longitude']
        self._Lcm = dict_group_database['Lcm']
        self._CenterToLimb_angle = dict_group_database['CenterToLimbAngle']
        self._quadrant = dict_group_database['Quadrant']
        self._McIntosh = dict_group_database['McIntosh']
        self._zurich = dict_group_database['Zurich']
        self._spots = dict_group_database['Spots']
        self._dipole1_lat = dict_group_database['Dipole1Lat']
        self._dipole1_long = dict_group_database['Dipole1Long']
        self._dipole2_lat = dict_group_database['Dipole2Lat']
        self._dipole2_long = dict_group_database['Dipole2Long']
        self._surface = dict_group_database['DeprojArea_msh']
        self._raw_surface_px = dict_group_database['RawArea_px']
        self._raw_surface_msd = dict_group_database['ProjArea_msd']
        self._g_spot = dict_group_database['GSpot']
        self._posX = dict_group_database['PosX']
        self._posY = dict_group_database['PosY']
        self._dipole1_posX = dict_group_database['Dipole1PosX']
        self._dipole1_posY = dict_group_database['Dipole1PosY']
        self._dipole2_posX = dict_group_database['Dipole2PosX']
        self._dipole2_posY = dict_group_database['Dipole2PosY']
        self._largest_spot = dict_group_database['LargestSpot']
        self._group_number = dict_group_database['GroupNumber']
        self._group_extra1 = dict_group_database['GroupExtra1']
        self._group_extra2 = dict_group_database['GroupExtra2']
        self._group_extra3 = dict_group_database['GroupExtra3']

        self.changed = False

    def __repr__(self):
        return "Group {}".format(self._number)

    @property
    def number(self):
        return self._number

    @number.setter
    def number(self, value):
        # print("here we are changing the value of group number to ", value)
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
              " or ", value * 180/math.pi, " degree ")

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
              " or ", value * 180/math.pi, " degree ")

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
        print("here we CAN NOT change the value of CenterToLimb angle to ",
              value)

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

    @property
    def McIntosh(self):
        return self._McIntosh

    @McIntosh.setter
    def McIntosh(self, value):
        # print("here we are changing the value of mcIntosh to ", value)
        self._McIntosh = value
        self.changed = True
        self.value_changed.emit()

    @property
    def zurich(self):
        return self._zurich

    @zurich.setter
    def zurich(self, value):
        # print("here we are changing the value of zurich to ", value)
        self._zurich = value
        self.changed = True
        self.value_changed.emit()

    @property
    def spots(self):
        """ the number of spots in the group"""
        return self._spots

    @spots.setter
    def spots(self, value):
        # print("here we are changing the value of spots to ", value)
        self._spots = value
        self.changed = True
        self.value_changed.emit()

    @property
    def dipole1_lat(self):
        return self._dipole1_lat

    @dipole1_lat.setter
    def dipole1_lat(self, value):
        print("here we CAN NOT change the value of dipole1_lat to ", value)

    @property
    def dipole1_long(self):
        return self._dipole1_long

    @dipole1_long.setter
    def dipole1_long(self, value):
        print("here we CAN NOT change the value of dipole1_long to ", value)

    @property
    def dipole2_lat(self):
        return self._dipole2_lat

    @dipole2_lat.setter
    def dipole2_lat(self, value):
        print("here we CAN NOT change the value of dipole2_lat to ", value)

    @property
    def dipole2_long(self):
        return self._dipole2_long

    @dipole2_long.setter
    def dipole2_long(self, value):
        print("here we CAN NOT change the value of dipole2_long to ", value)

    @property
    def dipole1_posX(self):
        return self._dipole1_posX

    @dipole1_posX.setter
    def dipole1_posX(self, value):
        print("here we CAN NOT change the value of dipole1_posX to ", value)

    @property
    def dipole1_posY(self):
        return self._dipole1_posY

    @dipole1_posY.setter
    def dipole1_posY(self, value):
        print("here we CAN NOT change the value of dipole1_posY to ", value)

    @property
    def dipole2_posX(self):
        return self._dipole2_posX

    @dipole2_posX.setter
    def dipole2_posX(self, value):
        print("here we CAN NOT change the value of dipole2_posX to ", value)

    @property
    def dipole2_posY(self):
        return self._dipole2_posY

    @dipole2_posY.setter
    def dipole2_posY(self, value):
        print("here we CAN NOT change the value of dipole2_posY to ", value)

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
        #print("here we are changing the value of the largest spot to ", value)
        self._largest_spot = value
        self.changed = True
        self.value_changed.emit()

    @property
    def group_number(self):
        return self._group_number

    @group_number.setter
    def group_number(self, value):
        print("here we are changing the value of group number to ", value)
        self._group_number = value
        self.changed = True
        self.value_changed.emit()

    @property
    def group_extra1(self):
        return self._group_extra1

    @group_extra1.setter
    def group_extra1(self, value):
        print("here we are changing the value of group extra 1 to ", value)
        self._group_extra1 = value
        self.changed = True
        self.value_changed.emit()

    @property
    def group_extra2(self):
        return self._group_extra2

    @group_extra2.setter
    def group_extra2(self, value):
        print("here we are changing the value of group extra 2 to ", value)
        self._group_extra2 = value
        self.changed = True
        self.value_changed.emit()

    @property
    def group_extra3(self):
        return self._group_extra3

    @group_extra3.setter
    def group_extra3(self, value):
        print("here we are changing the value of group extra 3 to ", value)
        self._group_extra3 = value
        self.changed = True
        self.value_changed.emit()

    def set_dipole_position(self, dipole_points, dipole_angles):
        """
        Add the dipole to the database by clicking on the drawing
        """
        # print("set the dipole position..", len(dipole_points))
        
        if len(dipole_points) == 4:
            self._dipole1_posX = dipole_points[0]
            self._dipole1_posY = dipole_points[1]
            self._dipole2_posX = dipole_points[2]
            self._dipole2_posY = dipole_points[3]
            self._dipole1_lat = round(dipole_angles[0], 6)
            self._dipole1_long = round(dipole_angles[1], 6)
            self._dipole2_lat = round(dipole_angles[2], 6)
            self._dipole2_long = round(dipole_angles[3], 6)

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
        if self.largest_spot == 'L' and group_compactness == 'o':
            self._g_spot = 1
        elif self.largest_spot == 'T' and group_compactness == 'o':
            self._g_spot = 2
        elif self.largest_spot == 'E' and group_compactness == 'o':
            self._g_spot = 3
        elif self.largest_spot == 'L' and group_compactness == 'i':
            self._g_spot = 4
        elif self.largest_spot == 'T' and group_compactness == 'i':
            self._g_spot = 5
        elif self.largest_spot == 'E' and group_compactness == 'i':
            self._g_spot = 6
        elif self.largest_spot == 'L' and group_compactness == 'c':
            self._g_spot = 7
        elif self.largest_spot == 'T' and group_compactness == 'c':
            self._g_spot = 8
        elif self.largest_spot == 'E' and group_compactness == 'c':
            self._g_spot = 9
        self.changed = True
        self.value_changed.emit()

    def set_surface(self, pixel_nb, proj_area, deproj_area):

        #print("here we are changing the value of the surface")
        self._raw_surface_px = pixel_nb
        self._surface = round(deproj_area, 2)
        self._raw_surface_msd = round(proj_area, 2)

        self.changed = True
        self.value_changed.emit()

    def save_group_info(self):
        
        db = database.database()
        
        db.write_group_info(self._datetime,
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
                            self._dipole1_posY,
                            self._dipole2_posX,
                            self._dipole2_posY,
                            self._largest_spot,
                            self._group_number,
                            self._group_extra1,
                            self._group_extra2,
                            self._group_extra3)


class Drawing(QtCore.QObject):
    """
    It represents all the information extracted from the drawing
    and stored in the database.  All the attribute are 'private'
    (in the python convention with the underscore
    before the name).
    """

    value_changed = QtCore.pyqtSignal()
    info_saved = QtCore.pyqtSignal()

    def __init__(self, param=None):

        super(Drawing, self).__init__()
        
        dict_drawing_database ={'id':0,
                                'DateTime': datetime(2000, 1, 1, 00, 00),
                                'TypeOfDrawing':'',
                                'Quality':'',
                                'Observer':None,
                                'CarringtonRotation':0,
                                'JulianDate':0.0,
                                'Calibrated':0,
                                'Analyzed':0,
                                'GroupCount':0,
                                'SpotCount':0,
                                'Wolf':0,
                                'AngleP':0,
                                'AngleB':0,
                                'AngleL':0,
                                'Filename':'',
                                'Operator':None,
                                'LastUpdateTime':None,
                                'AllAreaDone':0,
                                'DrawingExtra1':'',
                                'DrawingExtra2':'',
                                'DrawingExtra3':''}

        if param:
            for keys, values in dict_drawing_database.items():
                try:
                    dict_drawing_database[keys] = param[keys]
                except KeyError:
                    pass
                    # print("The following information is missing: {} ".format(keys) +
                    #      " It will be set to {} ".format(values))
                              
        self._id_drawing = dict_drawing_database['id']
        self._datetime = dict_drawing_database['DateTime']
        self._drawing_type = dict_drawing_database['TypeOfDrawing']
        self._quality = dict_drawing_database['Quality']
        self._observer = dict_drawing_database['Observer']
        self._carrington_rotation = dict_drawing_database['CarringtonRotation']
        self._julian_date = dict_drawing_database['JulianDate']
        self._calibrated = dict_drawing_database['Calibrated']
        self._analyzed = dict_drawing_database['Analyzed']
        self._group_count = dict_drawing_database['GroupCount']
        self._spot_count = dict_drawing_database['SpotCount']
        self._wolf = dict_drawing_database['Wolf']
        self._angle_P = dict_drawing_database['AngleP']
        self._angle_B = dict_drawing_database['AngleB']
        self._angle_L = dict_drawing_database['AngleL']
        self._path = dict_drawing_database['Filename']
        self._operator = dict_drawing_database['Operator']
        self._last_update_time = dict_drawing_database['LastUpdateTime']
        self._area_done = dict_drawing_database['AllAreaDone']
        self._drawing_extra1 = dict_drawing_database['DrawingExtra1']
        self._drawing_extra2 = dict_drawing_database['DrawingExtra2']
        self._drawing_extra3 = dict_drawing_database['DrawingExtra3']
        
        
        self._group_lst = []
        self.changed = False

    def __repr__(self):
        return 'Drawing :  date({}), group_count({})'.format(
            self._datetime, self._group_count)
    
    def fill_from_daily_scan(self, drawing_datetime, operator, observer,
                             drawing_type, drawing_quality, drawing_name):

        self._datetime = drawing_datetime
        self._observer = observer
        self._operator = operator
        self._drawing_type = drawing_type
        self._quality = drawing_quality
        self._last_update_time = datetime.now()
        self._path = drawing_name

        # calcualte quantities related to datetime...
        sun = sun_ephemeris.SunEphemeris(drawing_datetime)
        self._julian_date = sun.julian_day
        self._carrington_rotation = int(carrington_rotation.carrington_rotation(
            drawing_datetime))
        self.angle_P = round(sun.angle_P(), 6)
        self.angle_B = round(sun.angle_B0(), 6)
        self.angle_L = round(sun.angle_L0(), 6)

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
            print("!!!!!!!!!!!!!!problem to set the drawing_type "
                  "from the database!!!!!!!!!!")

    def set_calibration(self, param):
        """
        Set the calibration parameters from a list of value from the database.
        """
        self._calibrated_center = coordinates.Cartesian(0, 0)
        self._calibrated_north = coordinates.Cartesian(0, 0)

        try:
            (self._id_calibration,
             self._datetime_calibration,
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
        if self.pt1_name == 'Center' and self.pt2_name == 'North':
            self.calibrated_center = coordinates.Cartesian(point1_x, point1_y)
            self.calibrated_north = coordinates.Cartesian(point2_x, point2_y)
            self.calibrated_radius = self.calibrated_center.distance(
                self.calibrated_north)

        elif self.pt1_name == 'South' and self.pt2_name == 'North':
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
        self.changed = True
        self.value_changed.emit()

    @property
    def datetime(self):
        return self._datetime

    @property
    def drawing_type(self):
        return self._drawing_type

    @drawing_type.setter
    def drawing_type(self, value):
        # print("here we are changing the value of drawing_type to ", value)
        self._drawing_type = value
        self.changed = True
        self.value_changed.emit()

    @property
    def quality(self):
        return self._quality

    @quality.setter
    def quality(self, value):
        # print("here we are changing the value of quality to ", value)
        self._quality = value
        self.changed = True
        self.value_changed.emit()

    @property
    def observer(self):
        return self._observer

    @observer.setter
    def observer(self, value):
        # print("here we are changing the value of observer to ", value)
        self._observer = value
        self.changed = True
        self.value_changed.emit()

    @property
    def carrington_rotation(self):
        return self._carrington_rotation

    @carrington_rotation.setter
    def carrington_rotation(self, value):
        # print("here we are changing the value of carrington rotation to ",
        #      value)
        self._carrington_rotation = value
        self.changed = True
        self.value_changed.emit()

    @property
    def julian_date(self):
        return self._julian_date

    @property
    def calibrated(self):
        return self._calibrated

    @calibrated.setter
    def calibrated(self, value):
        # print("here we are changing the value of calibrated to ", value)
        self._calibrated = value
        self.changed = True
        self.value_changed.emit()

    @property
    def analyzed(self):
        return self._analyzed

    @analyzed.setter
    def analyzed(self, value):
        # print("here we are changing the value of analyzed to ", value)
        self._analyzed = value
        self.changed = True
        self.value_changed.emit()

    @property
    def spot_count(self):
        return self._spot_count

    @property
    def group_count(self):
        return self._group_count

    @group_count.setter
    def group_count(self, value):
        """
        change only via the update_group_number" function
        """
        print("here we CAN NOT change the value of group_count to ", value)

    @property
    def wolf(self):
        return self._wolf

    @wolf.setter
    def wolf(self, value):
        """
        Wolf is only changed via add/delete a group or
        change the spots number of a group
        """
        # print("here we CAN NOT change the value of wolf to ", value)

    @property
    def angle_P(self):
        return self._angle_P

    @angle_P.setter
    def angle_P(self, value):
        print("here we are changing the value of angle_P to ", value)
        self._angle_P = value
        self.changed = True
        self.value_changed.emit()

    @property
    def angle_B(self):
        return self._angle_B

    @angle_B.setter
    def angle_B(self, value):
        # print("here we are changing the value of angle_B to ", value)
        self._angle_B = value
        self.changed = True
        self.value_changed.emit()

    @property
    def angle_L(self):
        return self._angle_L

    @angle_L.setter
    def angle_L(self, value):
        print("here we are changing the value of angle_L to ", value)
        self._angle_L = value
        self.changed = True
        self.value_changed.emit()

    @property
    def path(self):
        return self._path

    @property
    def operator(self):
        return self._operator

    @operator.setter
    def operator(self, value):
        # print("here we are changing the value of operator to ", value)
        self._operator = value
        self.changed = True
        self.value_changed.emit()

    @property
    def group_lst(self):
        return self._group_lst

    @group_lst.setter
    def group_lst(self, value):
        # print("here we are changing the value of group_lst to ", value)
        self._group_lst = value
        self.changed = True
        self.value_changed.emit()

    @property
    def calibrated_center(self):
        return self._calibrated_center

    @calibrated_center.setter
    def calibrated_center(self, value):
        # print("here we are changing the value of calibrated center to ",
        #      value.x, value.y)
        self._calibrated_center = coordinates.Cartesian(value.x, value.y)
        self.changed = True
        self.value_changed.emit()

    @property
    def calibrated_center_x(self):
        return self._calibrated_center.x

    @calibrated_center_x.setter
    def calibrated_center_x(self, value):
        # print("here we are changing the value of calibrated center x to ",
        #      value)
        self._calibrated_center.x = value
        self.changed = True
        self.value_changed.emit()

    @property
    def calibrated_center_y(self):
        return self._calibrated_center.y

    @calibrated_center_y.setter
    def calibrated_center_y(self, value):
        # print("here we are changing the value of calibrated center y to ",
        #      value)
        self._calibrated_center.y = value
        self.changed = True
        self.value_changed.emit()

    @property
    def calibrated_north(self):
        return self._calibrated_north

    @calibrated_north.setter
    def calibrated_north(self, value):
        # print("here we are changing the value of calibrated north to ",
        #      value.x, value.y)
        self._calibrated_north = coordinates.Cartesian(value.x, value.y)
        self.changed = True
        self.value_changed.emit()

    @property
    def calibrated_north_x(self):
        return self._calibrated_north.x

    @calibrated_north_x.setter
    def calibrated_north_x(self, value):
        # print("here we are changing the value of calibrated north x to ",
        #      value)
        self._calibrated_north.x = value
        self.changed = True
        self.value_changed.emit()

    @property
    def calibrated_north_y(self):
        return self._calibrated_north.y

    @calibrated_north_y.setter
    def calibrated_north_y(self, value):
        # print("here we are changing the value of calibrated north y to ",
        #      value)
        self._calibrated_north.y = value
        self.changed = True
        self.value_changed.emit()

    @property
    def calibrated_radius(self):
        return self._calibrated_radius

    @calibrated_radius.setter
    def calibrated_radius(self, value):
        # print("here we are changing the value of calibrated radius to ",
        #      value)
        self._calibrated_radius = value
        self.changed = True
        self.value_changed.emit()

    @property
    def calibrated_angle_scan(self):
        return self._calibrated_angle_scan

    @calibrated_angle_scan.setter
    def calibrated_angle_scan(self, value):
        # print("here we are changing the value of calibrated angle scan to ",
        #      value)
        self._calibrated_angle_scan = value
        self.changed = True
        self.value_changed.emit()

    @property
    def pt1_fraction_width(self):
        return self._pt1_fraction_width

    @pt1_fraction_width.setter
    def pt1_fraction_width(self, value):
        print("here we are changing the value of fraction width to ", value)
        print("this is not authorized!!")

    @property
    def pt1_fraction_height(self):
        return self._pt1_fraction_height

    @pt1_fraction_height.setter
    def pt1_fraction_height(self, value):
        print("here we are changing the value of fraction height to ", value)
        print("this is not authorized!!")

    @property
    def pt2_fraction_width(self):
        return self._pt2_fraction_width

    @pt2_fraction_width.setter
    def pt2_fraction_width(self, value):
        print("here we are changing the value of fraction width to ", value)
        print("this is not authorized!!")

    @property
    def pt2_fraction_height(self):
        return self._pt2_fraction_height

    @pt2_fraction_height.setter
    def pt2_fraction_height(self, value):
        print("here we are changing the value of fraction height to ", value)
        print("this is not authorized!!")

    @property
    def pt1_name(self):
        return self._pt1_name

    @pt1_name.setter
    def pt1_name(self, value):
        print("here we are changing the value of point1 name to ", value)
        print("this is not authorized!!")

    @property
    def pt2_name(self):
        return self._pt2_name

    @pt2_name.setter
    def pt2_name(self, value):
        print("here we are changing the value of point2 name to ", value)
        print("this is not authorized!!")

    @property
    def p_oriented(self):
        return self._p_oriented

    @p_oriented.setter
    def p_oriented(self, value):
        print("here we are changing the value of p_oriented name to ", value)
        print("this is not authorized!!")

    @property
    def last_update_time(self):
        return self._last_update_time

    @last_update_time.setter
    def last_update_time(self, value):
        # print("here we are changing the value of last update time to ", value)
        self._last_update_time = value
        self.changed = True
        self.value_changed.emit()

    def change_group_position(self, group_number, latitude, longitude,
                              posX, posY):
        """
        Update the position of the group and all the quantities related to it.
        - the HGC latitude of the group
        - the HGC longitude of the group
        - the raw position of the group on the drawing
        - the the central merdian distance (LCM)
        - the center to limb angle
        - the quadrant
        """
        # print("update the position of the group!!!")

        self._group_lst[group_number]._latitude = round(latitude, 6)
        self._group_lst[group_number]._longitude = round(longitude, 6)
        self._group_lst[group_number]._posX = posX
        self._group_lst[group_number]._posY = posY
   
        self._group_lst[group_number]._Lcm = round(self._angle_L -
                                                   longitude * 180/math.pi, 4)
        distance_from_center = math.sqrt((posX - self.calibrated_center.x)**2 +
                                         (posY - self.calibrated_center.y)**2)

        self._group_lst[group_number]._CenterToLimb_angle = round(
            (math.asin(distance_from_center * 1./self.calibrated_radius) *
             180./math.pi), 4)

        if posX > self.calibrated_center.x and posY > self.calibrated_center.y:
            self._group_lst[group_number]._quadrant = "NE"
        elif (posX > self.calibrated_center.x and
              posY < self.calibrated_center.y):
            self._group_lst[group_number]._quadrant = "SE"
        elif (posX < self.calibrated_center.x and
              posY > self.calibrated_center.y):
            self._group_lst[group_number]._quadrant = "NW"
        elif (posX < self.calibrated_center.x and
              posY < self.calibrated_center.y):
            self._group_lst[group_number]._quadrant = "SW"

        self.changed = True
        self.value_changed.emit()

    def update_spot_number(self, group_number, sunspot_number):
        """
        Put the number of spots of the group[group_number] equal to
        sunspot number.
        Then recalculates the total sunspot number and the wolf number.
        """
        # print("update the sunspot_number!", sunspot_number)
        self._group_lst[group_number]._spots = sunspot_number
        total_sunspots = 0
        for group in self._group_lst:
            total_sunspots += group._spots
        self._spot_count = total_sunspots
        self._wolf = self._group_count * 10 + self._spot_count
        self.changed = True
        self.value_changed.emit()

    def update_group_number(self, group_number):
        self._group_count = group_number
        total_sunspots = 0
        for group in self._group_lst:
            total_sunspots += group._spots
            self._wolf = self._group_count * 10 + self._spot_count
        self.changed = True
        self.value_changed.emit()

    def add_group(self, latitude, longitude, posX, posY):
        """
        By clicking on the drawing, one add to the database:
        - group_count + 1 -> update the wolf number
        - group position and all the quantities related to it.
        - connect the signal emitted by a group to a signal emitted 
          by the drawing (for instance value changed).
        """
        self.update_group_number(self.group_count + 1)
        group_tmp = Group()
        group_tmp.value_changed.connect(self.get_group_signal)
        
        group_tmp._datetime = self.datetime
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

        db = database.database()
        db.delete_group_info(self._datetime, group_index)

        for i in range(group_index, len(self._group_lst)):
            self._group_lst[i].number = i

        self._last_update_time = datetime.now()
        self.save_info()
        
    def save_info(self):
        # print("save the info of the drawing!")
        
        db = database.database()
        db.write_drawing_info(self._drawing_type,
                              self._quality,
                              self._observer.upper(),
                              self._carrington_rotation,
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
                              self._operator.upper(),
                              self._last_update_time,
                              self._datetime)

        self._datetime_calibration = self._datetime
        db.write_calibration_info(self._calibrated_north.x,
                                  self._calibrated_north.y,
                                  self._calibrated_center.x,
                                  self._calibrated_center.y,
                                  self._calibrated_radius,
                                  self._calibrated_angle_scan,
                                  self._datetime_calibration)

        """for el in self.index_to_delete:
            db.delete_group_info(self._datetime, el)
            print("*********************extra group deleted!!", el)
        """            
        for el in self._group_lst:
            # print("save group info ", el)
            el.save_group_info()

        self.info_saved.emit()
