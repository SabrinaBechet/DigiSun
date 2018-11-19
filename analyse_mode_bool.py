# !/usr/bin/env python
# -*-coding:utf-8-*-
from PyQt5 import QtCore

class analyseModeBool(QtCore.QObject):
    """
    This represents the mode of the analysis.
    
    There are 4 viewing modes wich are overlays:
    - large grid
    - small grid
    - helper grid
    - group visualisation
    - dipole visualisation
    
    There a 5 action modes:
    - helper grid
    - calibrate 
    - add group
    - add dipole
      * input parameter: group number! works only for a given group
    - calculate the surface
      * input parameter: group number! works only for a given group
    """
    
    value_changed = QtCore.pyqtSignal()
    
    def __init__(self, input_value='False'):
        super(analyseModeBool, self).__init__()
        self._value = input_value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, input_value):
        #print("**the value of the mode has changed to ", input_value)
        self._value = input_value
        self.value_changed.emit()
        
    def set_opposite_value(self):
        if self._value==True:
            self._value=False
            self.value_changed.emit()
        else:
            self._value=True
            self.value_changed.emit()
