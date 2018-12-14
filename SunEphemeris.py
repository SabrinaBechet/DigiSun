from datetime import datetime
import ObserverTime
import math
#import re

class SunEphemeris():

    """ this object represent the coordinate and different parameter
    related to the sun. It depends only on the time of the observer.
    All the angles are expressed in degree.
    """    
    def __init__(self, obs_time):

        if isinstance(obs_time, datetime):
            self.obs_time = ObserverTime.ObserverTime(obs_time)
            self.julian_day = self.obs_time.julian_day()
            self.T_j2000 = self.obs_time.julian_century_j2000()
            self.T_j1900 = self.obs_time.julian_century_j1900()
            #self.carrington_rotation = self.obs_time.carrington_rotation()
            self.inclinaison_solar_equator = 7.25
            
        else:
            print("wrong time format! it should be in datetime format")

    def carrington_rotation(self):
        """
        A rotation starts when the heliographic prime meridian (L0)
        crosses the subterrestrial point of the solar disc.
        The first Carrington rotation started on 1853 Nov 9
        (JD 2398167.329), later points can be calculated using the 
        synodic period rsyn = 27.2753 days. 
        (ref: Heliospheric Coordinate systems, Franz & Harper 2002)
        """

        julian_date_close_zero_meridian = self.julian_day - (360 - self.angle_L0())/13.19

        #angle_close_zero_meridian = 
        
        print("julian date close zero meridian: ", julian_date_close_zero_meridian)

        
        
            
    def mean_anomaly(self):
        """The algo is from Jean Meeus - Astronomical Algorithms, 1991, pg 151.
        The result is an angle between 0 and 360 degrees.
        """
        return( 357.52910 + 35999.05030 * self.T_j2000 - 0.0001559 * self.T_j2000**2 -
                0.00000048 * self.T_j2000**3) % 360
    
    def mean_anomaly_earth(self):
        """The algo is from Jean Meeus - Astronomical Algorithms, 1991, pg 132.
        the result is an angle between 0 and 360 degrees.
        """
        return( 357.52772 + 35999.05034 * self.T_j2000 - 0.0001603 * self.T_j2000**2 -
                 (self.T_j2000**3)/300000.) % 360
    
    def equation_of_center(self):
        """
        It represents the angular difference between the actual position of a body in 
        its elliptical orbit and the position
        it would occupy if its motion were uniform in a circular orbit of the same period.
        The algo is from Jean Meeus - Astronomical Algorithms, 1991, pg 152.
        """
        return ( (1.914600 - 0.004817 * self.T_j2000 - 0.000014 * self.T_j2000**2) *
                 math.sin(self.mean_anomaly() * math.pi/180) +
                 (0.019993 - 0.000101 * self.T_j2000) * math.sin(2 * self.mean_anomaly() * math.pi/180) +
                 0.000290 * math.sin(3 * self.mean_anomaly() * math.pi/180))

    def mean_longitude(self):
        """   The ecliptic longitude at which an orbiting body could be found it its orbit were circular 
        and free of pertubations.
        The algo is from Jean Meeus - Astronomical Algorithms, 1991, pg 151.
        The result is an angle between 0 and 360 degrees.
        """
        return (280.46645 + 36000.76983 * self.T_j2000 + 0.0003032 * self.T_j2000**2 ) % 360

    def mean_longitude_moon(self):
        """
        The algo is from Jean Meeus - Astronomical Algorithms, 1991, pg 132.
        The result is an angle between 0 and 360 degrees.
        """
        return (218.3165 + 481267.8813 * self.T_j2000) % 360
    
    def true_longitude(self):
        """
        The true longitude is referred to the mean equinox of the date.
        The algo is from Jean Meeus - Astronomical Algorithms, 1991.
        """
        return self.mean_longitude() + self.equation_of_center() #+ self.planet_perturbations()

    def apparent_longitude(self):
        """
        The apparent longitude is referred to the true equinox of the date. 
        Then is necessary to correct the longitude for the nutation.
        The algo is from Jean Meeus - Astronomical Algorithms, 1991, pg 152.
        """
        return (self.true_longitude() - 0.00569 -
                0.00478 * math.sin(self.longitude_ascending_node_moon() * math.pi/180))
    
    def longitude_ascending_node_moon(self):
        """
        The orbit of the Moon is inclined at an angle of 5.145 degree to the ecliptic. 
        The ascending and descending nodes are when the Moon crosses the ecliptic plane.
        The algo is from Jean Meeus - Astronomical Algorithms, 1991, pg 132.
        """
        return (125.04452 -
                1934.136261 * self.T_j2000 +
                0.0020708 * self.T_j2000**2 +
                (self.T_j2000**3)/450000.) % 360

    def longitude_ascending_node_solar_equator(self):
        """
        The algo is from Jean Meeus - Astronomical Algorithms, 1991, page 178.
        """
        return (73.6667 + 1.3958333 * (self.obs_time.julian_ephemeris_day() - 2396758)/36525.)
    
    def mean_obliquity_ecliptic_j1900(self):
        """return the obliquity of the ecliptic in degree
        this is the obliquity free from short-term variation ("mean").
        """
        return (23.452294 - 0.0130125 * self.T_j1900 - 0.00000164 * self.T_j1900**2 +
                0.000000503 * self.T_j1900**3)
    
    def mean_obliquity_ecliptic(self):
        """return the obliquity of the ecliptic in degree
        this is the obliquity free from short-term variation ("mean") 
        The algo is from Jean Meeus - Astronomical Algorithms, 1991.
        """
        return (23.43929111 - 0.0130041 * self.T_j2000 - 0.00000016 * self.T_j2000**2 +
                0.000000503 * self.T_j2000**3)

    def nutation_obliquity_ecliptic(self):
        """
        The algo is from Jean Meeus - Astronomical Algorithms, 1991, p132.
        """
        return (0.002555 * math.cos(self.longitude_ascending_node_moon() * math.pi/180) +
                0.0001583 * math.cos(2 * self.mean_longitude() * math.pi/180) +
                0.00002777 * math.cos(2 * self.mean_longitude_moon() * math.pi/180) +
                0.00002499 * math.cos(2 * self.longitude_ascending_node_moon() * math.pi/180))

    def nutation_longitude_ecliptic(self):
        """
        The algo is from Jean Meeus - Astronomical Algorithms, 1991, p132.
        """
        return (- 0.0047777 * math.sin(self.longitude_ascending_node_moon() * math.pi/180) -
                0.0003666 * math.sin(2 * self.mean_longitude() * math.pi/180) -
                0.0000638 * math.sin(2 * self.mean_longitude_moon() * math.pi/180) +
                0.0000583 * math.sin(2 * self.longitude_ascending_node_moon() * math.pi/180))
    
    def true_obliquity_ecliptic(self):
        """return the obliquity of the ecliptic in degree. It includes the nutation.
        The algo is from Jean Meeus - Astronomical Algorithms, 1991."""
        return (self.mean_obliquity_ecliptic() + self.nutation_obliquity_ecliptic())

    def theta(self):
        """
        In the formula for theta, 25.38 is the Sun's sideral period of rotation in days. 
        This value has been fiwxed conventionnaly by Carrington. 
        It defines the zero meridian of the heliographic longitudes and 
        therefore must be treated as exact.
        The algo is from Jean Meeus - Astronomical Algorithms, 1991, pg 178.
        """
        return ((self.obs_time.julian_ephemeris_day() - 2398220) * 360 /25.38) % 360

    def VSOP87_one_term(self,a,b,c):
        return a * math.cos(b + c * self.obs_time.julian_millenia_j2000())

    def read_VSOP87(self):
        filename='/home/sabrinabct/Projets/DigiSun_2018/VSOP87D.ear'
        file = open(filename,'r')
        lines = file.readlines()
        
        coeff_a = []
        coeff_b = []
        coeff_c = []
        for line in lines:
            row = line[80:].split()
            
            coeff_a.append(row[0])
            coeff_b.append(row[1])
            coeff_c.append(row[2])
               
        return coeff_a, coeff_b,coeff_c
         
    def VSOP87_earth_from_file_L(self):
        """
        Read the main coefficient of the VSOP87 solution. Beware, L is in radian!!
        """
        coeff_a, coeff_b, coeff_c = self.read_VSOP87()
        L0, L1, L2, L3, L4, L5 = 0, 0,0,0,0,0
        for el in range(1,66):
            L0+=self.VSOP87_one_term(float(coeff_a[el])*100000000, float(coeff_b[el]), float(coeff_c[el]))
        for el in range(561,595):
            L1+=self.VSOP87_one_term(float(coeff_a[el])*100000000, float(coeff_b[el]), float(coeff_c[el]))
        for el in range(903,923):
            L2+=self.VSOP87_one_term(float(coeff_a[el])*100000000, float(coeff_b[el]), float(coeff_c[el]))
        for el in range(1046,1053):
            L3+=self.VSOP87_one_term(float(coeff_a[el])*100000000, float(coeff_b[el]), float(coeff_c[el]))
        for el in range(1069,1072):
            L4+=self.VSOP87_one_term(float(coeff_a[el])*100000000, float(coeff_b[el]), float(coeff_c[el]))
        L5 = self.VSOP87_one_term(float(coeff_a[1081])*100000000, float(coeff_b[1081]), float(coeff_c[1081]))        
        L = (L0 +
             L1 * self.obs_time.julian_millenia_j2000() +
             L2 * self.obs_time.julian_millenia_j2000()**2 +
             L3 * self.obs_time.julian_millenia_j2000()**3 +
             L4 * self.obs_time.julian_millenia_j2000()**4 +
             L5 * self.obs_time.julian_millenia_j2000()**5) * 0.00000001
        return L
    
    def VSOP87_earth_from_file_B(self):
        """
        Read the main coefficient of the VSOP87 solution. Beware, B is in radian!!
        """
        coeff_a, coeff_b, coeff_c = self.read_VSOP87()
        B0, B1 = 0,0
        for el in range(1087,1093):
            B0+=self.VSOP87_one_term(float(coeff_a[el])*100000000, float(coeff_b[el]), float(coeff_c[el]))
        for el in range(1272,1274):
            B1+=self.VSOP87_one_term(float(coeff_a[el])*100000000, float(coeff_b[el]), float(coeff_c[el]))
        B = (B0 +
             B1 * self.obs_time.julian_millenia_j2000()) * 0.00000001        
        return B

    def VSOP87_earth_from_file_R(self):
        coeff_a, coeff_b, coeff_c = self.read_VSOP87()
        R0, R1, R2, R3, R4 = 0, 0,0,0,0,
        for el in range(1440,1479):
            R0+=self.VSOP87_one_term(float(coeff_a[el])*100000000, float(coeff_b[el]), float(coeff_c[el]))
        for el in range(1967,1977):
            R1+=self.VSOP87_one_term(float(coeff_a[el])*100000000, float(coeff_b[el]), float(coeff_c[el]))
        for el in range(2260,2266):
            R2+=self.VSOP87_one_term(float(coeff_a[el])*100000000, float(coeff_b[el]), float(coeff_c[el]))
        for el in range(2400,2402):
            R3+=self.VSOP87_one_term(float(coeff_a[el])*100000000, float(coeff_b[el]), float(coeff_c[el])) 
        R4 = self.VSOP87_one_term(float(coeff_a[2428])*100000000, float(coeff_b[2428]), float(coeff_c[2428]))
        R = (R0 +
             R1 * self.obs_time.julian_millenia_j2000() +
             R2 * self.obs_time.julian_millenia_j2000()**2 +
             R3 * self.obs_time.julian_millenia_j2000()**3 +
             R4 * self.obs_time.julian_millenia_j2000()**4 ) * 0.00000001
        return R
      
    def aberration(self):
        """
        aberration error in degree.
        The algo is from Jean Meeus - Astronomical Algorithms, 1991, page 155.
        """
        #self.VSOP87_earth_from_file()
        return -20.4898/(3600 * self.VSOP87_earth_from_file_R())
    
    def mean_longitude_high_accuracy_VSOP(self):
        """
        The algo is from Jean Meeus - Astronomical Algorithms, 1991, page 154.
        """
        mean_long_VSOP = (self.VSOP87_earth_from_file_L() * 180/math.pi + 180)%360
        mean_long_FK5 =  mean_long_VSOP - 1.397 * self.T_j2000 - 0.00031 *  self.T_j2000**2
        #mean_long_FK5 = mean_long_VSOP - 0.000025
        return mean_long_VSOP

    def mean_longitude_high_accuracy_FK5(self):
        """
        The algo is from Jean Meeus - Astronomical Algorithms, 1991, page 154.
        """
        mean_long_VSOP = (self.VSOP87_earth_from_file_L() * 180/math.pi + 180)%360
        mean_long_FK5 =  mean_long_VSOP - 1.397 * self.T_j2000 - 0.00031 *  self.T_j2000**2
        #mean_long_FK5 = mean_long_VSOP - 0.000025
        return mean_long_FK5
    
    def apparent_longitude_high_accuracy(self):
        return self.mean_longitude_high_accuracy_VSOP() + self.nutation_longitude_ecliptic() + self.aberration()  
    
    def angle_P(self):
        x = math.atan( -math.cos((self.apparent_longitude_high_accuracy() - 0.005705)*math.pi/180.) *
                       math.tan( self.true_obliquity_ecliptic() * math.pi/180.)) * 180/math.pi
        y = math.atan(-math.cos( (self.apparent_longitude_high_accuracy() - self.longitude_ascending_node_solar_equator())*math.pi/180) *
                      math.tan(self.inclinaison_solar_equator*math.pi/180)) * 180/math.pi

        return (x + y)

    def angle_B0(self):

        return ( math.asin( math.sin( (self.apparent_longitude_high_accuracy() -
                                       self.longitude_ascending_node_solar_equator()) * math.pi/180) *
                            math.sin(self.inclinaison_solar_equator*math.pi/180)) * 180/math.pi)

    def angle_L0(self):

        tan_eta =  (math.tan( (self.apparent_longitude_high_accuracy() -
                               self.longitude_ascending_node_solar_equator()) * math.pi/180) *
                    math.cos(self.inclinaison_solar_equator * math.pi/180) )


        tan_num = (- math.sin( (self.apparent_longitude_high_accuracy() -
                               self.longitude_ascending_node_solar_equator()) * math.pi/180) *
                   math.cos(self.inclinaison_solar_equator * math.pi/180) )
        tan_deno = - math.cos( (self.apparent_longitude_high_accuracy() -
                               self.longitude_ascending_node_solar_equator()) * math.pi/180)

        eta = math.atan2(tan_num, tan_deno) * 180/math.pi
        res = (eta - self.theta())%360

        return res


