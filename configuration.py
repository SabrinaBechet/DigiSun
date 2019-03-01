# !/usr/bin/env python
# -*-coding:utf-8-*-

"""
This class handles the configuration of Digisun that needs:
- database path, user and passwd
- archdrawing directory
It reads these values in a file called 'digisun.ini'.
"""

from backports import configparser
import pymysql

class Config():

    def __init__(self):
        
        self.config = configparser.ConfigParser()
        self.config_file = "digisun.ini"
        #self.set_configuration()

    def set_archdrawing(self):
        """
        Configure the parameters related to the drawing archive directory.
        """
        
        try:
            with open(self.config_file) as config_file:
                self.config.read_file(config_file)
                self.prefix = self.config['drawings']['prefix']
                self.archdrawing_directory = self.config['drawings']['path']
                self.extension = self.config['drawings']['extension']
                
        except IOError:
            print('IOError - config file not found !!')


    def set_database(self):
        """
        Configure the parameters related to the database.
        """
        
        try:
            with open(self.config_file) as config_file:
                self.config.read_file(config_file)
                self.host = self.config['database']['host']
                self.user = self.config['database']['user']
                self.passwd = self.config['database']['passwd']
                self.db = self.config['database']['name']

                return self.host, self.user, self.passwd, self.db
        except IOError:
            print('IOError - config file not found !!')

            
    def check_database_connection(self):

        try:
            db = pymysql.connect(host=self.host,
                                 user=self.user,
                                 passwd=self.passwd,
                                 db=self.db)
            
            cursor = db.cursor()        
            cursor.execute("SELECT VERSION()")
            results = cursor.fetchone()
            # Check if anything at all is returned
            if results:
                return True
            else:
                return False               
        except pymysql.Error:
            print "ERROR IN CONNECTION"
        return False