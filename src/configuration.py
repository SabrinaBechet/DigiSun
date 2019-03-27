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

__author__ = "Sabrina Bechet"

import os
from backports import configparser
import pymysql

class Config():

    def __init__(self, filename="../data/digisun.ini"):
        """
        By default, the default file is digisun.ini but
        it can be different if specified.
        """
        
        self.config = configparser.ConfigParser()
        self.config_file = filename
        #self.set_configuration()

    def set_drawing_analyse(self):
        """
        Configure the parameters related to level of details of
        the drawing analyse
        """
        try:
            with open(self.config_file) as config_file:
                self.config.read_file(config_file)
                self.level = self.config['analyse']['level']
                self.extra1 = self.config['analyse']['group_extra1']
                self.extra2 = self.config['analyse']['group_extra2']
                self.extra3 = self.config['analyse']['group_extra3']
                
        except IOError:
            print('IOError - config file not found !!')        

    def set_archdrawing(self):
        """
        Configure the parameters related to the drawing archive directory.
        """
        
        try:
            with open(self.config_file) as config_file:
                self.config.read_file(config_file)
                self.prefix = self.config['drawings']['prefix']
                self.archdrawing_directory = self.config['drawings']['path']
                self.suffix = self.config['drawings']['suffix']
                self.extension = self.config['drawings']['extension']
                self.filename_structure = self.config['drawings']['filename_structure']
                self.directory_structure = self.config['drawings']['directory_structure']
                
        except IOError:
            print('IOError - config file not found !!')

    def set_file_path(self, my_datetime):
        """
        Return a standard file path based on a given configuration
        """
        
        self.set_archdrawing()
        
        if self.filename_structure=='YYYYmmddHHMM':
            filename_strftime = '%Y%m%d%H%M'
        elif self.filename_structure=='YYYYmmdd':
            filename_strftime = '%Y%m%d'
        else:
            print("ERROR : filename structure unknown!!")
            
        self.filename = (
            self.prefix +
            my_datetime.strftime(filename_strftime) +
            "." +
            self.suffix +
            self.extension)
        
        if self.directory_structure=='YYYY/mm':
            dir_strftime = '%Y/%m'
        elif self.directory_structure=='YYYY':
            dir_strftime = '%Y'
        else:
            print("ERROR : directory structure unknown!!")
            

        self.directory = os.path.join(
            self.archdrawing_directory,
            my_datetime.strftime(dir_strftime))
        
        self.file_path = os.path.join(self.directory, self.filename)
              
        
    def set_scanner(self):
        try:
            with open(self.config_file) as config_file:
                self.config.read_file(config_file)
                self.dpi = int(self.config['scanner']['dpi'])
                self.width = float(self.config['scanner']['width'])
                self.height = float(self.config['scanner']['height'])
                self.top = float(self.config['scanner']['top'])
                self.left = float(self.config['scanner']['left'])
                self.scan_format = self.config['scanner']['format']

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

    """ def set_ephemeris(self):
        try:
            with open(self.config_file) as config_file:
                self.config.read_file(config_file)
                self.ephem_file = self.config['ephemeris']['VSOP87']
              
                return self.ephem_file
        except IOError:
            print('IOError - config file not found !!')
   """
   
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
