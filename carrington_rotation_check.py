import carrington_rotation
from datetime import datetime
import database
from matplotlib import pyplot as plt

import sunpy.sun

def check():
    db = database.database()
    datetime_drawing = db.get_field_time_interval("drawings",
                                                  "Datetime",
                                                  "2016-03-03 00:00",
                                                  "2018-05-31 23:00")

    """carington_calculation = []
    carington_digisun = []
    carington_database = []
    """
    for el_date in datetime_drawing:

        print(el_date)
        carington_database = db.get_field_datetime("drawings", "CaringtonRotation", el_date)[0]

        carington_calculation = carrington_rotation.carrington_rotation(el_date)

        carington_digisun = int(sunpy.sun.carrington_rotation_number(el_date))
            
        #if carington_database!= carington_calculation:
        #    print(el_date, carington_database, carington_calculation)

        if carington_calculation != carington_digisun:
            print(el_date, carington_database, carington_digisun)
        
    """plt.plot(carington_calculation, carington_digisun, "o")
    plt.grid()
    plt.xlabel("Carrington rotation number DigiSun")
    plt.ylabel("Carrington rotation number SunPy")
    plt.show()
    """
if __name__=='__main__':
    check()
