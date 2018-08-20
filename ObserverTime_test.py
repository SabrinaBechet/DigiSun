import ObserverTime
import unittest
from datetime import datetime

class test_ObserverTime(unittest.TestCase):

    def test_julian_day(self):
        """
        Test from Jean Meeus - Astronomical Algorithms, 1991., pg 61
        """
        print('test on julian day...')
        obs_t_1 = ObserverTime.ObserverTime(datetime(1957,10,4,19,26,4))
        obs_t_2 = ObserverTime.ObserverTime(datetime(333,1,27,12,00,00))
        self.assertAlmostEqual(obs_t_1.julian_day(),2436116.31, places=2)
        self.assertAlmostEqual(obs_t_2.julian_day(),1842713.0, places=2)

    
    def test_julian_day_more(self):
        """
        Test from Jean Meeus - Astronomical Algorithms, 1991., pg 62
        """
        print('more test on julian day...')
        obs_t_1 = ObserverTime.ObserverTime(datetime(2000,1,1,12))
        obs_t_2 = ObserverTime.ObserverTime(datetime(1987,1,27))
        obs_t_3 = ObserverTime.ObserverTime(datetime(1987,6,19,12))
        obs_t_4 = ObserverTime.ObserverTime(datetime(1988,1,27))
        obs_t_5 = ObserverTime.ObserverTime(datetime(1988,6,19,12))
        obs_t_6 = ObserverTime.ObserverTime(datetime(1900,1,1))
        obs_t_7 = ObserverTime.ObserverTime(datetime(1600,1,1))
        obs_t_8 = ObserverTime.ObserverTime(datetime(1600,12,31))
        
        self.assertAlmostEqual(obs_t_1.julian_day(),2451545.0, places=2)
        self.assertAlmostEqual(obs_t_2.julian_day(),2446822.5, places=2)
        self.assertAlmostEqual(obs_t_3.julian_day(),2446966.0, places=2)
        self.assertAlmostEqual(obs_t_4.julian_day(),2447187.5, places=2)
        self.assertAlmostEqual(obs_t_5.julian_day(),2447332.0, places=2)
        self.assertAlmostEqual(obs_t_6.julian_day(),2415020.5, places=2)
        self.assertAlmostEqual(obs_t_7.julian_day(),2305447.5, places=2)
        self.assertAlmostEqual(obs_t_8.julian_day(),2305812.5, places=2)

        
if __name__ == '__main__':
    unittest.main()
