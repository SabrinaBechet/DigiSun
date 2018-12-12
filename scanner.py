import sys
if sys.platform == "win32":
    import twain
from PIL import Image
from StringIO import StringIO
import os
#import GUI_prototype
from PIL import Image

class scanner():
    """
    This class is strongly inspired by webagent-scanner on gitHub
    """
    def __init__(self):
        self.set_parameters()
        
    def set_parameters(self, from_db=False):
        """
        The technical settings of the scanner should be set via 
        the database.
        """
        if not from_db:
            self.dpi = 300
            self.directory = os.path.join('C:\\Users','USET - SILSO',
                                      'DigiSun_2018','archdrawing')
        else:
            settings_db = database.database()
            #self.dpi = settings_db.get_variable_settings('scandpi')
            #self.directory = settings_db.get_variable_settings('drawingpath')
            

    def get_scanner_name(self):
        """Get available the scanners""" 
        self.sourceManager = twain.SourceManager(0)
        scanners = self.sourceManager.GetSourceList()
        if scanners:
            return scanners
        else:
            return None

    def set_scanner(self, scanner_name):
        """
        connect to the scanner using the scanner_name
        arguments:
        scanner_name = name return by get_scanner()
        """
        #self.settings_from_database(table_name)
        try: 
            self.scanner = self.sourceManager.OpenSource(scanner_name)
            self.scanner.SetCapability(twain.ICAP_XRESOLUTION,
                                       twain.TWTY_FIX32,
                                       float(self.dpi))
            self.scanner.SetCapability(twain.ICAP_YRESOLUTION,
                                       twain.TWTY_FIX32,
                                       float(self.dpi))
            print("worked!!")
            return True
        except:
            # TO do: check that digisun do not crach completely because
            # the scanner is not set.
            self.scanner = None
            print("did not work!!")
            #print("there is a pb setting the scanner!!")
            return False
            
    def set_scan_area(self, left=0.0,
                      top=0.0,
                      width=11.69,
                      height=16.53):
        #By default, the dimension are in inches
        self.scanner.SetCapability(twain.ICAP_UNITS,
                                   twain.TWTY_UINT16,
                                   twain.TWUN_CENTIMETERS)
        
        width = float(28.2)
        height = float(36.0)
        left = float(left)
        top = float(top)

        self.scanner.SetImageLayout((left, top, width, height),1,1,1)
        
    def scan(self, filename):
        """
        scan and return PIL object if sucess else return False
        """
        print("enter in the scan method..")
        
        self.scanner.RequestAcquire(0,1)
        info = self.scanner.GetImageInfo()
        output_name_tmp = os.path.join(self.directory, 'test')#filename)
        output_name = os.path.join(self.directory, filename)
        
        #try:
        self.handle = self.scanner.XferImageNatively()[0]
        img = twain.DIBToBMFile(self.handle,output_name_tmp)
        twain.GlobalHandleFree(self.handle)
        img_scanned = Image.open(output_name_tmp)
        img_scanned.save(output_name,'JPEG', dpi=(300,300))
        return img_scanned
        #except:
        #    print('there is a problem, but which one?')
        #    return False

    def close_scanner(self):
        if self.scanner:
            self.scanner.destroy()
        self.scanner = None


if '__name__'=='__main__':
    my_scanner = scanner()
    scanner_name = my_scanner.get_scanner()
    my_scanner.set_scanner(scanner_name[0])
    my_scanner.set_scan_area()
    dir_name = os.path.join('C:\Users','USET - SILSO','DigiSun_2018','first.jpg')
    my_scanner.scan(dir_name)


"""sourceManager = twain.SourceManager(0)
scanner_name = sourceManager.GetSourceList()

print(scanner_name)

scanner = sourceManager.OpenSource(scanner_name[0])

width_a3 = 11.69
height_a3 = 16.53
width_a4 = 8.27
height_a4 = 11.69

scanner.SetImageLayout((0.0,0.0, width_a4, height_a4),1,1,1)

dir_name = os.path.join('C:\Users','USET - SILSO','DigiSun_2018','tst.jpg')
print(dir_name)

info = scanner.GetImageInfo()
print(info)

scanner.RequestAcquire(0,1)
handle = scanner.XferImageNatively()[0]
img = twain.DIBToBMFile(handle,dir_name)
twain.GlobalHandleFree(handle)

"""