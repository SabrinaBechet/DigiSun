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


import sys
import os
#import configuration
from PIL import Image
if sys.platform == "win32":
    import twain


class scanner():
    """
    The scanner object interact whit the scanner 
    via the TWAIN protocol (only working on Windows)
    This class is strongly inspired by webagent-scanner on gitHub
    """
    def __init__(self, config):
    
        self.config = config
        self.config.set_scanner()
        

    def get_scanner_name(self):
        """Get the available scanners"""
        self.sourceManager = twain.SourceManager(0)
        scanners = self.sourceManager.GetSourceList()
        if scanners:
            return scanners
        else:
            return None

    def set_scanner(self, scanner_name):
        """
        connect to the scanner using the scanner_name
        """
        try:
            self.scanner = self.sourceManager.OpenSource(scanner_name)
            self.scanner.SetCapability(twain.ICAP_XRESOLUTION,
                                       twain.TWTY_FIX32,
                                       float(self.config.dpi))
            self.scanner.SetCapability(twain.ICAP_YRESOLUTION,
                                       twain.TWTY_FIX32,
                                       float(self.config.dpi))
            print("set the scanner worked!!")
            return True
        except:
            # TO do: check that digisun do not crach completely because
            # the scanner is not set.
            self.scanner = None
            print("did not work!!")
            return False

    def set_scan_area(self,
                      left=0.0,
                      top=0.0,
                      width=11.69,
                      height=16.53):
        # By default, the dimension are in inches
        # Here we change it to cm
        self.scanner.SetCapability(twain.ICAP_UNITS,
                                   twain.TWTY_UINT16,
                                   twain.TWUN_CENTIMETERS)

        width = self.config.width # 28.2)
        height = self.config.height # 36.0)
        left = self.config.left
        top = self.config.top

        self.scanner.SetImageLayout((left, top, width, height), 1, 1, 1)

    def scan(self, output_name):
        """
        scan and return PIL object if sucess else return False.
        The input is the complete name of the file 
        to scan (directory + filename).
        For the moment only tesed JPEF format.
        TODO: test other formats
        
        """
        print("enter in the scan method..")

        self.scanner.RequestAcquire(0, 1)
        info = self.scanner.GetImageInfo()
       
        self.handle = self.scanner.XferImageNatively()[0]
        img = twain.DIBToBMFile(self.handle, output_name)
        twain.GlobalHandleFree(self.handle)
        img_scanned = Image.open(output_name)
        img_scanned.save(output_name,
                         self.config.scan_format,
                         dpi=(self.config.dpi, self.config.dpi))
        return img_scanned

    def close_scanner(self):
        if self.scanner:
            self.scanner.destroy()
        self.scanner = None

