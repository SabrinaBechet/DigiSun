from datetime import datetime
import math

class ObserverTime():
    """
    Represent the time of the observation.
    Can be easily converted to julian day, century, millenia 
    for the purpose of ephemeris calculation.
    """

    def __init__(self,input_time):
        """
        input time in datetime format
        """
        if isinstance(input_time, datetime):
            self.time = input_time
            self.year = input_time.year
            self.month = input_time.month
            self.day = input_time.day
            self.hour = input_time.hour
            self.minute = input_time.minute
            self.second = input_time.second
            self.jd = self.julian_day()
        else:
            print("wrong time format! it should be in datetime format")
            
    def julian_day(self):
        """ julian day is the number of days
        between the queried day and the reference date 
        of 12:00 (noon) Jan 1, 4713 BC. 
        The algo is from Jean Meeus - Astronomical Algorithms, 1991., pg 61 """

        month_jd = self.month
        year_jd = self.year
        if month_jd<3:
            year_jd-=1
            month_jd+=12

        if year_jd > 1582:
            b = 2 - int(year_jd/100.) + int(year_jd/400.)
        else:
            b = 0

        day_frac = (self.hour + self.minute/60.)/24.
        julian_day = (int(1461 * (year_jd + 4716)/4.) +
                      int(153 * (month_jd + 1)/5.) +
                      self.day + day_frac + b - 1524.5)
        
        return julian_day

    def julian_ephemeris_day(self):
        """ It differs from the julian day by the small quantity delta_t. """
        return self.julian_day() + self.delta_t()/ 86400.
    
    def julian_century_j2000(self):
        """number of julian centuries between the epoch and 2000 January 1 12th"""
        return (self.jd - 2451545)/36525.
    
    def julian_millenia_j2000(self):
        """number of julian millenia between the epoch and 2000 January 1 12th"""
        return (self.jd - 2451545.0)/365250.

    def julian_century_j1900(self):
        """number of julian centuries between the epoch and 1900 January 1 12th"""
        #dj = self.julian_day + (80./86400.)
        julian_century_j1900 = (self.jd - 2415020)/36525.
        return julian_century_j1900
   
    
    def delta_t(self):
        """
        Polnymial expressions for delta 
        From five Millennium Canon of Solar Eclipses, Espenak and Meeus.
        """
        if self.year in range(1920, 1941):
            t = self.year - 1920
            return math.ceil(21.20 + 0.84493*t - 0.076100 * t**2 + 0.0020936 * t**3)

        elif self.year in range(1941, 1961):
            t = self.year - 1950
            return math.ceil(29.07 + 0.407*t - t**2/233 + t**3 / 2547)

        elif self.year in range(1961, 1986):
            t = self.year - 1975
            return math.ceil(45.45 + 1.067*t - t**2/260 - t**3 / 718)
        
        elif self.year in range(1986, 2005):
            t = self.year - 2000
            return math.ceil(63.86 + 0.3345 * t - 0.060374 * t**2 + 0.0017275 * t**3 + 0.000651814 * t**4  + 0.00002373599 * t**5)
        elif self.year in range(2005, 2050):
            t = self.year - 2000
            return math.ceil(62.92 + 0.32217 * t + 0.005589 * t**2)
	
        else:
            print('did not estimate the delta t, put it to zero. year:', self.year)
            return 0
    
