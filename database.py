# !/usr/bin/env python
# -*-coding:utf-8-*-
"""
DigiSun: a software to transform sunspot drawings into exploitable data. It allows to scan drawings, extract its information and store it in a database.
Copyright (C) 2019 Sabrina Bechet at Royal Observatory of Belgium (ROB)

This file is part of DigiSun.

DigiSun is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

DigiSun is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with DigiSun.  If not, see <https://www.gnu.org/licenses/>.
"""
import digisun
import pymysql

__author__ = "Sabrina Bechet"
__date__ = "April 2019"

class database():
    """
    Object to interact with the database.
    """
    def __init__(self, config):

        self.config = config #configuration.Config()
        
        (config_host, config_port, config_user,
         config_passwd, config_db) = self.config.set_database()

        #print("database: ", config_db)
        if config_host:
            self.db = pymysql.connect(host=config_host,
                                      port=config_port,
                                      user=config_user,
                                      passwd=config_passwd,
                                      db=config_db)
            self.cursor = self.db.cursor()

            
    def get_field_time_interval(self, table_name, field, date_min, date_max):
        self.cursor.execute('SELECT ( ' + field +
                            ') FROM ' + table_name +
                            ' WHERE DateTime > %s && ' +
                            ' DateTime < %s ;',
                            (str(date_min),
                             str(date_max)))

        self.db.commit()
        result = self.cursor.fetchall()
        field_lst = [x[0] for x in result]
        return field_lst

    def set_combo_box_drawing(self, field, table_name, linedit):
        """
        Define automatically the combo box list with all the element
        named in the database
        """
        values = self.get_values(field, table_name)
        for el in values:
            linedit.addItem(el[0])

    def get_all_fields(self, table_name):
        self.cursor.execute('DESCRIBE ' + table_name )

        self.db.commit()
        result = self.cursor.fetchall()
        result_lst = [x[0] for x in result]
        return result_lst
            
    def get_all_in_time_interval(self, table_name, date_min, date_max):
        self.cursor.execute('SELECT * FROM ' + table_name +
                            ' WHERE DateTime >= %s && ' +
                            ' DateTime <= %s ;',
                            (str(date_min),
                             str(date_max)))

        self.db.commit()
        result = self.cursor.fetchall()
        return result

    def get_all_LastUpdateTime_time_interval(self, table_name, date_min, date_max):
        self.cursor.execute('SELECT * FROM ' + table_name +
                            ' WHERE LastUpdateTime > %s && ' +
                            ' DateTime < %s ;',
                            (str(date_min),
                             str(date_max)))

        self.db.commit()
        result = self.cursor.fetchall()
        return result

    def get_values(self, field, table_name):
        self.cursor.execute('SELECT ' + field + ' FROM ' +
                            table_name)

        self.db.commit()
        result = self.cursor.fetchall()
        return result

    def get_drawing_information(self, table_name, drawing_type):
        self.cursor.execute('SELECT * FROM ' + table_name +
                            ' WHERE name <=> %s ;',
                            (str(drawing_type)))

        self.db.commit()
        result = self.cursor.fetchall()
        return result
    
    def delete_group_info(self, datetime, number):
        self.cursor.execute('DELETE FROM  sGroups where DateTime <=> %s and '
                            'DigiSunNumber >= %s; ',
                            (str(datetime), str(number)))
        self.db.commit()

    def write_group_info(self, *var):
        """
        Write in the database all the info related to a group.
        REPLACE works exactly like INSERT, except that if an old row
        in the table has the same value as a new row for a PRIMARY key or
        a UNIQUE index, the old row is deleted before the new row is inserted.
        """
        """self.cursor.execute('REPLACE INTO sGroups (DateTime, DigiSunNumber, Latitude, '
                            'Longitude, Lcm, CenterToLimbAngle, Quadrant, '
                            'McIntosh, Zurich, Spots, '
                            'Dipole1Lat, Dipole1Long, Dipole2Lat, '
                            'Dipole2Long, DeprojArea_msh, RawArea_px, '
                            'ProjArea_msd, GSpot, PosX, PosY, '
                            'Dipole1PosX, Dipole1PosY, Dipole2PosX, '
                            'Dipole2PosY, LargestSpot, GroupNumber, '
                            'GroupExtra1, GroupExtra2, GroupExtra3 ) '
                            'values (%s, %s, %s, %s, %s, %s, %s, %s, %s, '
                            '%s, %s, %s, %s, %s, %s, %s, %s,'
                            '%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ',
                            var)
        """
        self.cursor.execute('INSERT INTO sGroups (DateTime, DigiSunNumber, Latitude, '
                            'Longitude, Lcm, CenterToLimbAngle, Quadrant, '
                            'McIntosh, Zurich, Spots, '
                            'Dipole1Lat, Dipole1Long, Dipole2Lat, '
                            'Dipole2Long, DeprojArea_msh, RawArea_px, '
                            'ProjArea_msd, GSpot, PosX, PosY, '
                            'Dipole1PosX, Dipole1PosY, Dipole2PosX, '
                            'Dipole2PosY, LargestSpot, GroupNumber, '
                            'GroupExtra1, GroupExtra2, GroupExtra3 ) '
                            'values (%s, %s, %s, %s, %s, %s, %s, %s, %s, '
                            '%s, %s, %s, %s, %s, %s, %s, %s,'
                            '%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) '
                            'ON DUPLICATE KEY UPDATE '
                            'DigiSunNumber=VALUES(DigiSunNumber), '
                            'Latitude=VALUES(Latitude), Longitude=VALUES(Longitude), '
                            'Lcm=VALUES(Lcm), '
                            'CenterToLimbAngle=VALUES(CenterToLimbAngle), '
                            'Quadrant=VALUES(Quadrant), '
                            'McIntosh=VALUES(McIntosh), Zurich=VALUES(Zurich), '
                            'Spots=VALUES(Spots), '
                            'Dipole1Lat=VALUES(Dipole1Lat), '
                            'Dipole1Long=VALUES(Dipole1Long), '
                            'Dipole2Lat=VALUES(Dipole2Lat), '
                            'Dipole2Long=VALUES(Dipole2Long), '
                            'DeprojArea_msh=VALUES(DeprojArea_msh), '
                            'RawArea_px=VALUES(RawArea_px), '
                            'ProjArea_msd=VALUES(ProjArea_msd), '
                            'GSpot=VALUES(GSpot), '
                            'PosX=VALUES(PosX), PosY=VALUES(PosY), '
                            'Dipole1PosX=VALUES(Dipole1PosX), '
                            'Dipole1PosY=VALUES(Dipole1PosY), '
                            'Dipole2PosX=VALUES(Dipole2PosX), '
                            'Dipole2PosY=VALUES(Dipole2PosY), '
                            'LargestSpot=VALUES(LargestSpot), '
                            'GroupNumber=VALUES(GroupNumber), '
                            'GroupExtra1=VALUES(GroupExtra1), '
                            'GroupExtra2=VALUES(GroupExtra2), '
                            'GroupExtra3=VALUES(GroupExtra3) ',
                            var)
        
        self.db.commit()

    def write_calibration_info(self, *var):
        """
        Write in the database all the info related
        to the calibration identified by its datetime
        """
        """self.cursor.execute('REPLACE INTO calibrations (NorthX, NorthY, '
                            'CenterX, CenterY, Radius, AngleScan, DateTime) '
                            'values '
                            '(%s, %s, %s, %s, %s, %s, %s) ', var)
        """
        self.cursor.execute('INSERT INTO calibrations (NorthX, NorthY, '
                            'CenterX, CenterY, Radius, AngleScan, DateTime) '
                            'values '
                            '(%s, %s, %s, %s, %s, %s, %s) '
                            'ON DUPLICATE KEY UPDATE '
                            'NorthX=VALUES(NorthX), '
                            'NorthY=VALUES(NorthY), '
                            'CenterX=VALUES(CenterX), '
                            'CenterY=VALUES(CenterY), '
                            'Radius=VALUES(Radius), '
                            'AngleScan=VALUES(AngleScan)',
                            var)
        
        self.db.commit()

    def write_digisun_history(self, drawing_datetime):

        self.cursor.execute('select version_firstUpdate from digisun_history '
                            'where DateTime <=> %s',
                            str(drawing_datetime))
        self.db.commit()
        result = self.cursor.fetchall()

        if len(result)<1:
            self.cursor.execute('INSERT INTO digisun_history (DateTime, version_firstUpdate) '
                                'values '
                                '(%s, %s) ',
                                (drawing_datetime, digisun.__version__))
            self.db.commit()

        else:
            self.cursor.execute('UPDATE digisun_history set version_lastUpdate=%s'
                                'where datetime <=>%s',
                                (digisun.__version__, drawing_datetime))
            self.db.commit()
    
    def write_drawing_info(self, *var):
        """
        Write in the database all the info related
        to a drawing identified by its datetime
        """
        self.cursor.execute('INSERT into drawings (TypeOfDrawing, Quality, '
                            'Observer, CarringtonRotation,'
                            'JulianDate, Calibrated, Analyzed, GroupCount, '
                            'SpotCount, Wolf, AngleP, '
                            'AngleB, AngleL, Filename, Operator, LastUpdateTime, '
                            'DateTime) values '
                            '(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, '
                            '%s, %s, %s, %s, %s, %s, %s) '
                            'ON DUPLICATE KEY UPDATE '
                            'TypeOfDrawing=VALUES(TypeOfDrawing), '
                            'Quality=VALUES(Quality), '
                            'Observer=VALUES(Observer), '
                            'CarringtonRotation=VALUES(CarringtonRotation), '
                            'JulianDate=VALUES(JulianDate), '
                            'Calibrated=VALUES(Calibrated), '
                            'Analyzed=VALUES(Analyzed), '
                            'GroupCount=VALUES(GroupCount), '
                            'SpotCount=VALUES(SpotCount), '
                            'Wolf=VALUES(Wolf), AngleP=VALUES(AngleP), '
                            'AngleB=VALUES(AngleB), AngleL=VALUES(AngleL), '
                            'Filename=VALUES(Filename), '
                            'Operator=VALUES(Operator), '
                            'LastUpdateTime=VALUES(LastUpdateTime) ',
                            var)

        self.db.commit()

    def write_field_datetime_group(self, table_name, field, value, date,
                                   group_number):

        self.cursor.execute('UPDATE ' + table_name +
                            ' set ' + field + '= %s '
                            'WHERE DateTime <=> %s and DigiSunNumber <=> %s;',
                            (str(value), str(date), str(group_number)))

        self.db.commit()

    def write_field_datetime(self, table_name, field, value, date):

        self.cursor.execute('UPDATE ' + table_name +
                            ' set ' + field + '= %s '
                            'WHERE DateTime <=> %s;',
                            (str(value), str(date)))

        self.db.commit()

    def get_field_datetime(self, table_name, field, date):
        """
        it returns a list
        """
        self.cursor.execute('SELECT ( ' + field +
                            ') FROM ' + table_name +
                            ' WHERE DateTime <=> %s ;',
                            (str(date)))

        self.db.commit()
        result = self.cursor.fetchall()
        field_lst = [x[0] for x in result]
        return field_lst

    def get_all_datetime(self, table_name, date):
        """
        it returns a list of the the entry that satisfy
        the datetime (should be only one)
        """
        self.cursor.execute('SELECT * FROM ' + table_name +
                            ' WHERE DateTime <=> %s ;',
                            (str(date)))

        self.db.commit()
        result = self.cursor.fetchall()
        return result

    def get_all_datetime_group_number(self, table_name, date, number):
        """
        it returns a list of the the entry that satisfy the datetime
        (there should be only one)
        """
        self.cursor.execute('SELECT * FROM ' + table_name +
                            ' WHERE DateTime <=> %s && ' +
                            'DigiSunNumber <=> %s;',
                            (str(date),
                             str(number)))

        self.db.commit()
        result = self.cursor.fetchall()
        return result
    
    
    def replace_drawing(self, drawing):
        """
        REPLACE works exactly like INSERT, except that if an old row
        in the table has the same value as a new row for a PRIMARY key or
        a UNIQUE index, the old row is deleted before the new row is inserted.
        """
        self.cursor.execute('REPLACE INTO drawings (Datetime, TypeOfDrawing,'
                            'Quality, Observer, CarringtonRotation, JulianDate,'
                            'Calibrated, Analyzed, GroupCount, SpotCount,'
                            'Wolf, AngleP, AngleB, AngleL, Filename,'
                            'Operator, LastUpdateTime) values (%s, %s, %s, %s,'
                            '%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,'
                            '%s) ',
                            (drawing.datetime, drawing.drawing_type,
                             drawing.quality, drawing.observer,
                             drawing.carrington_rotation, drawing.julian_date,
                             drawing.calibrated, drawing.analyzed,
                             drawing.group_count, drawing.spot_count,
                             drawing.wolf, drawing.angle_P,
                             drawing.angle_B, drawing.angle_L,
                             drawing.path, drawing.operator,
                             drawing.last_update_time))
        self.db.commit()
    
        
    def get_variable_settings(self, variable):
        self.cursor.execute('SELECT usetvalue FROM technical_settings'
                            'WHERE usetkey=%s',
                            variable)
        self.db.commit()
        result = self.cursor.fetchall()
        results = result[0][0]
        return results

    def delete_drawing(self, table_name, drawing_datetime):

       self.cursor.execute("DELETE FROM " + table_name +
                           ' WHERE DateTime <=> %s; ',
                           str(drawing_datetime))
       
       self.db.commit()
    
    def exist_in_db(self, table_name, field, value):
        self.cursor.execute('SELECT COUNT(' + field +
                            ') FROM ' + table_name +
                            ' WHERE ' + field + '=%s;',
                            str(value))

        self.db.commit()
        result = self.cursor.fetchall()

        if result[0][0] > 0:
            return True
        else:
            return False
