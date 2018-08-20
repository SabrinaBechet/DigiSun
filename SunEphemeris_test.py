import SunEphemeris
import ObserverTime
import unittest
from datetime import datetime
import math


class test_SunEphemeris(unittest.TestCase):

    def test_nutation_obliquity_ecliptic(self):
        """
        Test from Jean Meeus - Astronomical Algorithms, 1991., pg 136
        """
        print('test the nutation and the obliquity of the ecliptic...')
        obs_t = ObserverTime.ObserverTime(datetime(1987,4,10))
        sun = SunEphemeris.SunEphemeris(datetime(1987,4,10))
        
        self.assertAlmostEqual(obs_t.julian_ephemeris_day(),2446895.5, places=2)
        self.assertAlmostEqual(obs_t.julian_century_j2000(),-0.127296372348, places=12)
        
        self.assertAlmostEqual(sun.mean_anomaly_earth(),94.9792, places=4)
        self.assertAlmostEqual(sun.longitude_ascending_node_moon(),11.2531, places=4)
        self.assertAlmostEqual(sun.nutation_longitude_ecliptic(),-0.001052, places=4)
        self.assertAlmostEqual(sun.nutation_obliquity_ecliptic(),0.002623, places=3)
        self.assertAlmostEqual(sun.true_obliquity_ecliptic(),23.4435, places=3)
        self.assertAlmostEqual(sun.mean_obliquity_ecliptic(),23.4409, places=3)


    def test_position_sun_high_accuracy(self):
        """
        Test from Jean Meeus - Astronomical Algorithms, 1991., pg 157
        """
        print('test the position of the sun with high accuracy...')
        obs_t = ObserverTime.ObserverTime(datetime(1992,10,13))
        sun = SunEphemeris.SunEphemeris(datetime(1992,10,13))

        self.assertAlmostEqual((sun.VSOP87_earth_from_file_L()*180/math.pi)%360,19.907372, places=4)
        #self.assertAlmostEqual((sun.VSOP87_earth_from_file_B()*180/math.pi)%360,0.000179, places=4)
        self.assertAlmostEqual(sun.VSOP87_earth_from_file_R(),0.99760775, places=4)
        self.assertAlmostEqual(sun.mean_longitude_high_accuracy_VSOP(),199.907372, places=4)
        #self.assertAlmostEqual(sun.mean_longitude_high_accuracy_FK5(),199.907347, places=4)
        self.assertAlmostEqual(sun.nutation_longitude_ecliptic(),0.004418, places=4)
        #self.assertAlmostEqual(sun.nutation_obliquity_ecliptic(),0.000085, places=5)
        self.assertAlmostEqual(sun.true_obliquity_ecliptic(),23.4401443, places=3)
        self.assertAlmostEqual(sun.aberration(),-00.0057, places=4)
        self.assertAlmostEqual(sun.apparent_longitude_high_accuracy(),199.906, places=3)

    def test_physical_ephemeris_sun(self):
        """
        Test from Jean Meeus - Astronomical Algorithms, 1991., pg 178
        """
        print('test the physical ephemeris of the sun...')
        obs_t = ObserverTime.ObserverTime(datetime(1992,10,13))
        sun = SunEphemeris.SunEphemeris(datetime(1992,10,13))

        self.assertAlmostEqual(sun.theta(),65.8252, places=3)
        self.assertAlmostEqual(sun.inclinaison_solar_equator,7.25, places=3)
        self.assertAlmostEqual(sun.longitude_ascending_node_solar_equator(),75.6597, places=3)
        #self.assertAlmostEqual(sun.mean_longitude(),199.902340, places=3) 
        
if __name__ == '__main__':
    unittest.main()
