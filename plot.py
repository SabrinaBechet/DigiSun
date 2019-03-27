import MySQLdb
from matplotlib import pylab as plt
import datetime, calendar
import numpy as np
import database
import math

def get_fields_per_date_uset_dev(my_date, table_name):

    db = MySQLdb.connect(host='soldb.oma.be',
                         user = 'usetdevadmin',
                         passwd='usetdevadmin',
                         db='uset_dev')

    cur = db.cursor()
    cur.execute('SELECT *  FROM ' + table_name + '  WHERE DateTime=%s;',
                (my_date,))
    
    db.commit()
    result = cur.fetchall()
    return result

def get_fields_per_date_uset(date, table_name):

    db = MySQLdb.connect(host='soldb.oma.be',
                         user = 'usetadmin',
                         passwd='usetadmin',
                         db='uset')

    cur = db.cursor()
    cur.execute('select * from ' + table_name + ' where DateTime <=> %s;',
                (date,))
    db.commit()
    result = cur.fetchall()
    return result
  
def get_date_lst(date_min, date_max):
    db = database.database()
    tuple_drawings = db\
        .get_all_LastUpdateTime_time_interval("drawings",
                                  date_min,
                                  date_max)
    
    lst_drawing = [el[1] for el in tuple_drawings]
    return lst_drawing


def match_group(uset_group, uset_dev_group):
    """
    Build the matrix of position difference 
    between uset_group and uset_dev_group
    """

    #print("enter in the match group module...", len(uset_group), len(uset_dev_group))
    
    diff_array = np.ones((len(uset_group), len(uset_dev_group))) * 100
    lst_index = None
    if len(uset_group) == len(uset_dev_group):
    
        for el_std in uset_group:
            lat_std = el_std[4]
            long_std = el_std[5]
            for el_dev in uset_dev_group:
                lat_dev = el_dev[3]
                long_dev = el_dev[4]
                long_diff = abs(long_dev - long_std)
                index_el_std = uset_group.index(el_std)
                index_el_dev = uset_dev_group.index(el_dev)

                diff = (math.sin(lat_std) * math.sin(lat_dev) +
                        math.cos(lat_std) * math.cos(lat_dev) * math.cos(long_diff))

                if diff >1 and diff <1.00001 :
                    diff=1.0

                diff_distance = math.acos(diff)
                #print(index_el_dev, index_el_std, diff_distance, diff_array.shape)
                diff_array[index_el_dev,index_el_std]=diff_distance

        #print(diff_array)
        if diff_array.shape[0]>0:
            lst_index = np.argmin(diff_array, axis=0)
            #print(lst_index)
            unique, counts = np.unique(lst_index, return_counts=True)
            tst = np.where(counts>1)
            if tst[0]>0:
                print("BAM", unique, counts, tst, uset_group[0])
            
    return lst_index
    

if __name__=='__main__':

    date_max = datetime.datetime.now()
    date_min = datetime.datetime(2019,01,01,07,00)

    date_lst = get_date_lst(date_min, date_max)
    #date_lst = [(datetime.datetime(2004, 2, 20, 8, 50))]
    #print(date_lst)
    
    print("number of drawing analyzed: {}".format(len(date_lst)))
    
    carrington_diff = []
    julianDate_diff = []
    groupCount_diff = []
    spotCount_diff = []
    wolf_diff = []
    angleP_diff = []
    angleB_diff = []
    angleL_diff = []

    lat_diff = []
    long_diff = []
    surface_ratio = []
  
    for date in date_lst:
        all_uset_dev = get_fields_per_date_uset_dev(date, 'drawings')[0]
        all_uset = get_fields_per_date_uset(date, 'drawings')[0]
        
        all_group_uset_dev = get_fields_per_date_uset_dev(date, 'groups')
        all_group_uset = get_fields_per_date_uset(date, 'groups')

        carrington = (all_uset_dev[5] - all_uset[5])
        carrington_diff.append(carrington)
        if carrington >0 :
            print("carrington diff! ", date, all_uset[5], all_uset_dev[5])
        
        julianDate_diff.append(abs(all_uset_dev[6] - all_uset[6]))

        group_diff = abs(all_uset_dev[9] - all_uset[9])
        if group_diff >0 :
            print('group diff', group_diff, date)
        groupCount_diff.append(group_diff)

        spot_diff = abs(all_uset_dev[10] - all_uset[10])
        if spot_diff >0 :
            print('spot diff', spot_diff, date)
        spotCount_diff.append(spot_diff)

        wolf_diff.append(abs(all_uset_dev[11] - all_uset[11]))

        P_angle = all_uset_dev[12] - all_uset[12]
        angleP_diff.append(P_angle)
        if abs(P_angle)>0.02:
            print('***P angle out of the histo value: ', date)
            print(all_uset_dev[12], all_uset[12])

        B_angle = all_uset_dev[13] - all_uset[13]
        angleB_diff.append(B_angle)
        if abs(B_angle)>0.005:
            print('***B angle out of the histo value: ', date)
            print(all_uset_dev[13], all_uset[13])


        L_angle = all_uset_dev[14] - all_uset[14]
        angleL_diff.append(L_angle)
        if abs(L_angle)>0.05:
            print('***L angle out of the histo value: ', date)
            print(all_uset_dev[14], all_uset[14])

        if len(all_group_uset) == len(all_group_uset_dev):
            lst_index = match_group(all_group_uset, all_group_uset_dev)

            if lst_index is not None:
                for index in range(lst_index.shape[0]):
                
                    dev_lat = all_group_uset_dev[lst_index[index]][3]
                    dev_long = all_group_uset_dev[lst_index[index]][4]
                    dev_surface = all_group_uset_dev[lst_index[index]][16]
                    
                    uset_lat = all_group_uset[index][4]
                    uset_long = all_group_uset[index][5]
                    uset_surface = all_group_uset[index][19]
                    
                    lat = (uset_lat - dev_lat) * 180/math.pi
                    lat_diff.append(lat)
                    if abs(lat)>10:
                       print(lst_index)
                       print('**latitude: ', uset_lat, dev_lat, date)
                       print(all_group_uset[index])
                       print(all_group_uset_dev[lst_index[index]])
                    
                    longi = (uset_long - dev_long) * 180/math.pi
                    long_diff.append(longi)
                    if abs(longi)>10:
                        print(lst_index)
                        print('**longitude: ', uset_long, dev_long, date)
                        print(all_group_uset[index])  
                        print(all_group_uset_dev[lst_index[index]])

                    if uset_surface and dev_surface:
                        surface = abs(uset_surface - dev_surface)*100/uset_surface
                        surface_ratio.append(surface)
                        if abs(surface)>200:
                            print(lst_index)
                            print('**surface: ', uset_surface, dev_surface, date)
                            print(all_group_uset[index])  
                            print(all_group_uset_dev[lst_index[index]])
                      
                    
    surface_min = min(surface_ratio)
    surface_max = 100 #max(surface_ratio)
    surface_bin = int(abs(surface_max - surface_min))/10

    print("check surface ", surface_min, surface_max, surface_bin)
    
    surface_mean = np.mean(surface_ratio)
    surface_std = np.std(surface_ratio)
    surface_len = len(surface_ratio)
    f = plt.figure()
    ax = f.add_subplot(111)
    print('range', surface_min, surface_max)
    plt.text(0.9, 0.95,' N = {0}'.format(surface_len),
             horizontalalignment='center',
             verticalalignment='center',
             transform=ax.transAxes)
    plt.text(0.9, 0.9,'$\mu$={0:.2f} '.format(float(surface_mean)),
             horizontalalignment='center',
             verticalalignment='center',
             transform=ax.transAxes)
    plt.text(0.9, 0.85,'$\sigma$={0:.2f}'.format(float(surface_std)),
             horizontalalignment='center',
             verticalalignment='center',
             transform=ax.transAxes)
    plt.hist(surface_ratio, bins=surface_bin, range=(surface_min, surface_max))
    plt.title('group surface ratio')
    plt.grid()
    plt.savefig("testing/plot/group_surface.jpg")
    plt.close()
    
    
    lat_min = min(lat_diff)
    lat_max = max(lat_diff)
    lat_bin = int(abs(lat_max - lat_min)) * 10

    print("check latitude ", lat_min, lat_max, lat_bin)
    
    lat_mean = np.mean(lat_diff)
    lat_std = np.std(lat_diff)
    lat_len = len(lat_diff)
    f = plt.figure()
    ax = f.add_subplot(111)
    plt.text(0.9, 0.95,' N = {0}'.format(lat_len),
             horizontalalignment='center',
             verticalalignment='center',
             transform=ax.transAxes)
    plt.text(0.9, 0.9,'$\mu$={0:.2f} deg.'.format(float(lat_mean)),
             horizontalalignment='center',
             verticalalignment='center',
             transform=ax.transAxes)
    plt.text(0.9, 0.85,'$\sigma$={0:.2f} deg'.format(float(lat_std)),
             horizontalalignment='center',
             verticalalignment='center',
             transform=ax.transAxes)
    plt.hist(lat_diff, bins=lat_bin, range=(lat_min, lat_max))
    plt.title('group latitude difference')
    plt.xlabel('degree')
    plt.grid()
    plt.savefig("testing/plot/group_latitude.jpg")
    plt.close()

    long_min = min(long_diff)
    long_max = max(long_diff)
    long_bin = int(abs(long_max - long_min)) * 10

    print("check longitude ", long_min, long_max, long_bin)
    
    long_mean = np.mean(long_diff)
    long_std = np.std(long_diff)
    long_len = len(long_diff)
    f = plt.figure()
    ax = f.add_subplot(111)
    plt.text(0.9, 0.95,' N = {0}'.format(long_len),
             horizontalalignment='center',
             verticalalignment='center',
             transform=ax.transAxes)
    plt.text(0.9, 0.9,'$\mu$={0:.2f} deg.'.format(float(long_mean)),
             horizontalalignment='center',
             verticalalignment='center',
             transform=ax.transAxes)
    plt.text(0.9, 0.85,'$\sigma$={0:.2f} deg'.format(float(long_std)),
             horizontalalignment='center',
             verticalalignment='center',
             transform=ax.transAxes)
    plt.hist(long_diff, bins = long_bin, range=(long_min, long_max))
    plt.title('group longitude difference')
    plt.grid()
    plt.xlabel('degree')
    plt.savefig("testing/plot/group_longitude.jpg")
    plt.close()

    carr_min = min(carrington_diff)
    carr_max = max(carrington_diff)
    carr_bin = int(abs(carr_max - carr_min)) * 10
    carr_mean = np.mean(carrington_diff)
    carr_std = np.std(carrington_diff)
    carr_len = len(carrington_diff)
    f = plt.figure()
    ax = f.add_subplot(111)
    plt.text(0.9, 0.95,' N = {0}'.format(carr_len),
             horizontalalignment='center',
             verticalalignment='center',
             transform=ax.transAxes)
    plt.text(0.9, 0.9,'$\mu$={0:.2f}'.format(float(carr_mean)),
             horizontalalignment='center',
             verticalalignment='center',
             transform=ax.transAxes)
    plt.text(0.9, 0.85,'$\sigma$={0:.2f}'.format(float(carr_std)),
             horizontalalignment='center',
             verticalalignment='center',
             transform=ax.transAxes)
    plt.hist(carrington_diff)
    plt.title('carrington rotation number difference')
    plt.grid()
    plt.savefig("testing/plot/carrington.jpg")
    plt.close()

    julian_min = min(julianDate_diff)
    julian_max = max(julianDate_diff)
    julian_bin = int(abs(julian_max - julian_min)) * 10
    julian_mean = np.mean(julianDate_diff)
    julian_std = np.std(julianDate_diff)
    julian_len = len(julianDate_diff)
    f = plt.figure()
    ax = f.add_subplot(111)
    plt.text(0.9, 0.95,' N = {0}'.format(julian_len),
             horizontalalignment='center',
             verticalalignment='center',
             transform=ax.transAxes)
    plt.text(0.9, 0.9,'$\mu$={0:.2f}'.format(float(julian_mean)),
             horizontalalignment='center',
             verticalalignment='center',
             transform=ax.transAxes)
    plt.text(0.9, 0.85,'$\sigma$={0:.2f}'.format(float(julian_std)),
             horizontalalignment='center',
             verticalalignment='center',
             transform=ax.transAxes)
    plt.hist(julianDate_diff)
    plt.title('Julian date difference')
    plt.grid()
    plt.savefig("testing/plot/julianDate.jpg")
    plt.close()

    groupCount_min = min(groupCount_diff)
    groupCount_max = max(groupCount_diff)
    groupCount_bin = int(abs(groupCount_max - groupCount_min)) * 10
    groupCount_mean = np.mean(groupCount_diff)
    groupCount_std = np.std(groupCount_diff)
    groupCount_len = len(groupCount_diff)
    f = plt.figure()
    ax = f.add_subplot(111)
    plt.text(0.9, 0.95,' N = {0}'.format(groupCount_len),
             horizontalalignment='center',
             verticalalignment='center',
             transform=ax.transAxes)
    plt.text(0.9, 0.9,'$\mu$={0:.2f}'.format(float(groupCount_mean)),
             horizontalalignment='center',
             verticalalignment='center',
             transform=ax.transAxes)
    plt.text(0.9, 0.85,'$\sigma$={0:.2f}'.format(float(groupCount_std)),
             horizontalalignment='center',
             verticalalignment='center',
             transform=ax.transAxes)
    plt.hist(groupCount_diff)
    plt.title('group count difference')
    plt.grid()
    plt.savefig("testing/plot/groupCount.jpg")
    plt.close()

    spotCount_min = min(spotCount_diff)
    spotCount_max = max(spotCount_diff)
    spotCount_bin = int(abs(spotCount_max - spotCount_min)) * 10
    spotCount_mean = np.mean(spotCount_diff)
    spotCount_std = np.std(spotCount_diff)
    spotCount_len = len(spotCount_diff)
    f = plt.figure()
    ax = f.add_subplot(111)
    plt.text(0.9, 0.95,' N = {0}'.format(spotCount_len),
             horizontalalignment='center',
             verticalalignment='center',
             transform=ax.transAxes)
    plt.text(0.9, 0.9,'$\mu$={0:.2f}'.format(float(spotCount_mean)),
             horizontalalignment='center',
             verticalalignment='center',
             transform=ax.transAxes)
    plt.text(0.9, 0.85,'$\sigma$={0:.2f}'.format(float(spotCount_std)),
             horizontalalignment='center',
             verticalalignment='center',
             transform=ax.transAxes)
    plt.hist(spotCount_diff)
    plt.title('spot count difference')
    plt.grid()
    plt.savefig("testing/plot/spotCount.jpg")
    plt.close()

    """plt.hist(wolf_diff)
    plt.title('wolf number difference')
    plt.grid()
    plt.savefig("testing/plot/wolf.jpg")
    plt.close()
    """
    
    angleP_min = min(angleP_diff)
    angleP_max = max(angleP_diff)
    angleP_bin = int(abs(angleP_max - angleP_min) * 1000)
    print("angleP bin",angleP_bin)
    angleP_mean = np.mean(angleP_diff)
    angleP_std = np.std(angleP_diff)
    angleP_len = len(angleP_diff)
    f = plt.figure()
    ax = f.add_subplot(111)
    plt.text(0.9, 0.95,' N = {0}'.format(angleP_len),
             horizontalalignment='center',
             verticalalignment='center',
             transform=ax.transAxes)
    plt.text(0.9, 0.9,'$\mu$={0:.3f}'.format(float(angleP_mean)),
             horizontalalignment='center',
             verticalalignment='center',
             transform=ax.transAxes)
    plt.text(0.9, 0.85,'$\sigma$={0:.3f}'.format(float(angleP_std)),
             horizontalalignment='center',
             verticalalignment='center',
             transform=ax.transAxes)
    plt.hist(angleP_diff, bins=angleP_bin, range=(angleP_min, angleP_max))
    plt.title('angle P difference')
    plt.xlabel('degree')
    plt.grid()
    plt.savefig("testing/plot/angleP.jpg")
    plt.close()

    angleB_min = min(angleB_diff)
    angleB_max = max(angleB_diff)
    angleB_bin = int(abs(angleB_max - angleB_min) * 1000)
    print("angleB bin", angleB_bin)
    angleB_mean = np.mean(angleB_diff)
    angleB_std = np.std(angleB_diff)
    angleB_len = len(angleB_diff)
    f = plt.figure()
    ax = f.add_subplot(111)
    plt.text(0.9, 0.95,' N = {0}'.format(angleB_len),
             horizontalalignment='center',
             verticalalignment='center',
             transform=ax.transAxes)
    plt.text(0.9, 0.9,'$\mu$={0:.4f}'.format(float(angleB_mean)),
             horizontalalignment='center',
             verticalalignment='center',
             transform=ax.transAxes)
    plt.text(0.9, 0.85,'$\sigma$={0:.4f}'.format(float(angleB_std)),
             horizontalalignment='center',
             verticalalignment='center',
             transform=ax.transAxes)
    plt.hist(angleB_diff, bins=angleB_bin, range=(angleB_min, angleB_max))
    plt.title('angle B difference')
    plt.xlabel('degree')
    plt.grid()
    plt.savefig("testing/plot/angleB.jpg")
    plt.close()

    angleL_min = min(angleL_diff)
    angleL_max = max(angleL_diff)
    angleL_bin = int(abs(angleL_max - angleL_min) * 1000)
    #print("angleL bin", angleL_bin)
    angleL_mean = np.mean(angleL_diff)
    angleL_std = np.std(angleL_diff)
    angleL_len = len(angleL_diff)
    f = plt.figure()
    ax = f.add_subplot(111)
    plt.text(0.9, 0.95,' N = {0}'.format(angleL_len),
             horizontalalignment='center',
             verticalalignment='center',
             transform=ax.transAxes)
    plt.text(0.9, 0.9,'$\mu$={0:.4f}'.format(float(angleL_mean)),
             horizontalalignment='center',
             verticalalignment='center',
             transform=ax.transAxes)
    plt.text(0.9, 0.85,'$\sigma$={0:.4f}'.format(float(angleL_std)),
             horizontalalignment='center',
             verticalalignment='center',
             transform=ax.transAxes)
    plt.hist(angleL_diff, bins=angleL_bin, range=(angleL_min, angleL_max))
    plt.title('angle L difference')
    plt.grid()
    plt.xlabel('degree')
    plt.savefig("testing/plot/angleL.jpg")
    plt.close()
    
