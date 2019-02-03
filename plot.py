import MySQLdb
from matplotlib import pylab as plt
import datetime, calendar
import numpy as np
import database

def get_fields_per_date_uset_dev(my_date):

    db = MySQLdb.connect(host='soldb.oma.be',
                         user = 'usetdevadmin',
                         passwd='usetdevadmin',
                         db='uset_dev')

    cur = db.cursor()
    cur.execute('SELECT *  FROM drawings  WHERE DateTime=%s;',(my_date,))
    
    db.commit()
    result = cur.fetchall()
            
    return result[0]


def get_fields_per_date_uset(date):

    db = MySQLdb.connect(host='soldb.oma.be',
                         user = 'usetadmin',
                         passwd='usetadmin',
                         db='uset')

    cur = db.cursor()
    cur.execute('select * from drawings where DateTime <=> %s;', (date,))
    db.commit()
    result = cur.fetchall()
            
    return result[0]


def get_date_lst(date_min, date_max):
    db = database.database()
    tuple_drawings = db\
        .get_all_LastUpdateTime_time_interval("drawings",
                                  date_min,
                                  date_max)
    
    lst_drawing = [el[1] for el in tuple_drawings]
    return lst_drawing

if __name__=='__main__':


    date_max = datetime.datetime.now()
    date_min = datetime.datetime(2019,01,01,07,00)

    date_lst = get_date_lst(date_min, date_max)
    print("number of drawing analyzed: {}".format(len(date_lst)))

    
    carrington_diff = []
    julianDate_diff = []
    groupCount_diff = []
    spotCount_diff = []
    wolf_diff = []
    angleP_diff = []
    angleB_diff = []
    angleL_diff = []

    """date_lst = [datetime.datetime(2014,1,1,12,00),
                datetime.datetime(2014,1,5,9,15),
                datetime.datetime(2014,1,7,9,36),
                datetime.datetime(2014,1,8,12,00),]
    """
    for date in date_lst:
        all_uset_dev = get_fields_per_date_uset_dev(date)
        all_uset = get_fields_per_date_uset(date)

        carrington_diff.append((all_uset_dev[5] - all_uset[5]))
        julianDate_diff.append(abs(all_uset_dev[6] - all_uset[6]))

        group_diff = abs(all_uset_dev[9] - all_uset[9])
        if group_diff >1 :
            print date
        groupCount_diff.append(group_diff)
        
        spotCount_diff.append(abs(all_uset_dev[10] - all_uset[10]))
        wolf_diff.append(abs(all_uset_dev[11] - all_uset[11]))
        angleP_diff.append(all_uset_dev[12] - all_uset[12])
        angleB_diff.append(all_uset_dev[13] - all_uset[13])
        angleL_diff.append(all_uset_dev[14] - all_uset[14])
        
    
        

    plt.hist(carrington_diff)
    plt.title('carrington rotation number difference')
    plt.savefig("testing/plot/carrington.jpg")
    plt.close()

    plt.hist(julianDate_diff)
    plt.title('Julian date difference')
    plt.savefig("testing/plot/julianDate.jpg")
    plt.close()

    plt.hist(groupCount_diff)
    plt.title('group count difference')
    plt.savefig("testing/plot/groupCount.jpg")
    plt.close()

    plt.hist(spotCount_diff)
    plt.title('spot count difference')
    plt.savefig("testing/plot/spotCount.jpg")
    plt.close()

    plt.hist(wolf_diff)
    plt.title('wolf number difference')
    plt.savefig("testing/plot/wolf.jpg")
    plt.close()

    plt.hist(angleP_diff, bins = 100, range=[-0.005, 0.005])
    plt.title('angle P difference')
    plt.savefig("testing/plot/angleP.jpg")
    plt.close()

    plt.hist(angleB_diff, bins = 100, range=[-0.005, 0.005])
    plt.title('angle B difference')
    plt.savefig("testing/plot/angleB.jpg")
    plt.close()
    
    plt.hist(angleL_diff, bins = 100, range=[-0.005, 0.005])
    plt.title('angle L difference')
    plt.savefig("testing/plot/angleL.jpg")
    plt.close()
    
