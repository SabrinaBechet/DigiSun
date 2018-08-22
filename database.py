import pymysql


class database():
    """
    Object to interact with the database.
    """
    def __init__(self):
        self.db = pymysql.connect(host='soldb.oma.be',
                                  user='usetdevadmin',
                                  passwd='usetdevadmin',
                                  db='uset_dev')
        self.cursor = self.db.cursor()

    def get_field_time_interval(self, table_name, field, date_min, date_max):
        self.cursor.execute('SELECT ( '+ field +
                            ') FROM ' + table_name +
                            ' WHERE DateTime > %s && ' +
                            ' DateTime < %s ;',
                            (str(date_min) ,
                             str(date_max) ))

        self.db.commit()
        result = self.cursor.fetchall()
        field_lst = [x[0] for x in result]
        #print(date_min, date_max, result)
        return field_lst

    def get_field_datetime(self, table_name, field, date):
        """
        it returns a list
        """
        self.cursor.execute('SELECT ( '+ field +
                            ') FROM ' + table_name +
                            ' WHERE DateTime <=> %s ;',
                            (str(date)))

        self.db.commit()
        result = self.cursor.fetchall()
        field_lst = [x[0] for x in result]
        return field_lst

    def get_all_datetime(self, table_name, date):
        """
        it returns a list of the the entry that satisfy the datetime (should be only one)
        """
        self.cursor.execute('SELECT * FROM ' + table_name +
                            ' WHERE DateTime <=> %s ;',
                            (str(date)))

        self.db.commit()
        result = self.cursor.fetchall()
        #print(result)
        #field_lst = [x[0] for x in result]
        #print(date_min, date_max, result)
        return result
    
    def get_all_datetime_group_number(self, table_name, date, number):
        """
        it returns a list of the the entry that satisfy the datetime 
        (there should be only one)
        """
        self.cursor.execute('SELECT * FROM ' + table_name +
                            ' WHERE DateTime <=> %s && ' +
                            'Number <=> %s;',
                            (str(date),
                             str(number)))

        self.db.commit()
        result = self.cursor.fetchall()
        #print(result)
        #field_lst = [x[0] for x in result]
        #print(date_min, date_max, result)
        return result
    
    def replace_drawing(self, drawing):
        """
        REPLACE works exactly like INSERT, except that if an old row
        in the table has the same value as a new row for a PRIMARY key or
        a UNIQUE index, the old row is deleted before the new row is inserted.
        """
        self.cursor.execute('REPLACE INTO drawings (Datetime, TypeOfDrawing,'
                            'Quality, Observer, CaringtonRotation, JulianDate,'
                            'Calibrated, Analyzed, GroupCount, SpotCount,'
                            'Wolf, AngleP, AngleB, AngleL, AngleScan, Path,'
                            'Operator, LastUpdateTime) values (%s, %s, %s, %s,'
                            '%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,'
                            '%s, %s) ',
                            (drawing.datetime, drawing.drawing_type,
                             drawing.quality, drawing.observer,
                             drawing.carington_rotation, drawing.julian_date,
                             drawing.calibrated, drawing.analyzed,
                             drawing.group_count, drawing.spot_count,
                             drawing.wolf, drawing.angle_B, drawing.angle_L,
                             drawing.angle_P, drawing.angle_scan, drawing.path,
                             drawing.operator, drawing.last_update_time))
        self.db.commit()
        
    def get_variable_settings(self, variable):
        self.cursor.execute('SELECT usetvalue FROM technical_settings'
                            'WHERE usetkey=%s',
                            variable)
        self.db.commit()
        result = self.cursor.fetchall()
        results = result[0][0]
        return results

    def count_field_in_time_interval(self, table_name, field, value_min, value_max,
                               field2, value2):
        """
        Select the number of drawings in [date_min, date_max] &&  field2==value2.
        
        The mysql command is
        select count(DateTime) from drawings where DateTime>'2017-03-01' 
        && DateTime<'2017-03-31'  && Calibrated=0;
        Here:
        table_name = drawings
        field = DateTime
        field2 = Calibrated
        value_min = '2017-03-01'
        value_max = '2017-03-31'
        """
        self.cursor.execute('SELECT COUNT( DISTINCT ' + field +
                            ') FROM ' + table_name +
                            ' WHERE ' +
                            field + '> %s && ' +
                            field + '< %s && ' +
                            field2 +'<=> %s ;',
                            (str(value_min) + " 00:00",
                             str(value_max) + " 23:59", value2))

        self.db.commit()
        result = self.cursor.fetchall()
        return result[0][0]

    def count_field_in_time_interval_area(self, table_name, field, value_min, value_max,
                               field2, value2):
        """
        Join the drawings and the groups table. 
        Select groups.surface=Null only for drawings.analyzed=1.
        Otherwhise count twice analyzed.
        """
    
        self.cursor.execute('SELECT COUNT( DISTINCT groups.DateTime) ' +
                            'from groups inner join drawings on ' +
                            'groups.DateTime=drawings.DateTime where ' +
                            'drawings.DateTime > %s && drawings.DateTime< %s ' +
                            '&& (groups.Surface is NULL or groups.Surface=0) && drawings.Analyzed=%s;',
                            (str(value_min), str(value_max), str(1)))
        self.db.commit()
        result = self.cursor.fetchall()
        return result[0][0]
    
    def count_year(self, table_name, field, value_min, value_max):
        self.cursor.execute('SELECT COUNT(' + field +
                            ') FROM ' + table_name +
                            ' WHERE ' +
                            field + '> %s && ' +
                            field + '< %s;',
                            (str(value_min) + " 00:00",
                             str(value_max) + " 23:59"))

        self.db.commit()
        result = self.cursor.fetchall()
        return result[0][0]

    def get_year_interval(self, table_name, field):
        self.cursor.execute('SELECT ' + field + ' FROM ' + table_name)
        self.db.commit()
        result = self.cursor.fetchall()

        return result
    
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
        
