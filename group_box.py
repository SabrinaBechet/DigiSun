# !/usr/bin/env python
# -*-coding:utf-8-*-
from PyQt4 import QtGui, QtCore

def patter(self):
	pass

class GroupBox(QtGui.QWidget):
    """
    Represent the box associated to a group.
    It consist of
    - combo box for zurich type
    - combo box for mcIntosh type
    - etc...
    """
    def __init__(self):
        super(GroupBox, self).__init__()
        layout = QtGui.QVBoxLayout()
        self.grid_layout = QtGui.QGridLayout()
        self.arrow_layout = QtGui.QGridLayout()
        #self.grid_layout.setSpacing(0)
        #self.grid_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.grid_layout)

    def get_zurich(self):
        return self.grid_layout.itemAtPosition(0,2).widget()
        
    def get_McIntosh(self):
        return self.grid_layout.itemAtPosition(0,3).widget()
    
    def set_title(self, title, grid_position,colorised):
        self.title_label = QtGui.QLabel(title)
        if colorised:
            self.title_label.setStyleSheet("background-color: rgb(255, 165, 84)")
        #self.title_label.setMaximumWidth(50)
        self.grid_layout.addWidget(self.title_label,
                                   grid_position[0],
                                   grid_position[1])
        grid_position[1]+=1
            
    def set_arrows_buttons(self):
        button_up = QtGui.QPushButton()
        arrow_up_pix = QtGui.QPixmap("icons/arrow_up");
        arrow_up = QtGui.QIcon(arrow_up_pix)
        button_up.setIcon(arrow_up);
        
        button_down = QtGui.QPushButton()
        arrow_down_pix = QtGui.QPixmap("icons/arrow_down");
        arrow_down = QtGui.QIcon(arrow_down_pix)
        button_down.setIcon(arrow_down);
        
        button_left = QtGui.QPushButton()
        arrow_left_pix = QtGui.QPixmap("icons/arrow_left");
        arrow_left = QtGui.QIcon(arrow_left_pix)
        button_left.setIcon(arrow_left);
        
        button_right = QtGui.QPushButton()
        arrow_right_pix = QtGui.QPixmap("icons/arrow_right");
        arrow_right = QtGui.QIcon(arrow_right_pix)
        button_right.setIcon(arrow_right);
        
        self.grid_layout.addWidget(button_up,1,3)
        self.grid_layout.addWidget(button_down,3,3)
        self.grid_layout.addWidget(button_left,2,2)
        self.grid_layout.addWidget(button_right,2,4)


    
    def set_spot_count(self, spot_count, grid_position):
        self.spot_number_linedit = QtGui.QLineEdit(str(spot_count),self)
        self.spot_number_linedit.setMaximumWidth(60)
        self.grid_layout.addWidget(self.spot_number_linedit,
                                   grid_position[0],
                                   grid_position[1])
        grid_position[1]+=1

    def set_zurich_type(self, group_zurich_type, grid_position):
        self.zurich_combo = QtGui.QComboBox(self)
        self.zurich_combo.setStyleSheet("color:black")


        self.zurich_combo.wheelEvent = patter
        
        self.zurich_combo.setMaximumWidth(50)
        self.zurich_combo.addItem("A")
        self.zurich_combo.addItem("B")
        self.zurich_combo.addItem("C")
        self.zurich_combo.addItem("D")
        self.zurich_combo.addItem("E")
        self.zurich_combo.addItem("F")
        self.zurich_combo.addItem("G")
        self.zurich_combo.addItem("H")
        self.zurich_combo.addItem("J")
        self.grid_layout.addWidget(self.zurich_combo,
                              grid_position[0],
                              grid_position[1])
        grid_position[1]+=1
        index = self.zurich_combo.findText(group_zurich_type)
        self.zurich_combo.setCurrentIndex(index)
        self.zurich_combo.currentIndexChanged.connect(lambda : self.update_McIntosh_type(self.zurich_combo.currentText()))

    def update_McIntosh_type(self,zurich_type):
        self.McIntosh_combo.clear()
        
        self.McIntosh_combo.wheelEvent = patter
    
        if zurich_type=='A':
            self.McIntosh_combo.addItem("Axx")
        elif zurich_type=='B':
            self.McIntosh_combo.addItem("Bxo")
            self.McIntosh_combo.addItem("Bxi")
            self.McIntosh_combo.addItem("Bxc")
        elif zurich_type=='C':
            self.McIntosh_combo.addItem("Cro")
            self.McIntosh_combo.addItem("Cri")
            self.McIntosh_combo.addItem("Crc")
            self.McIntosh_combo.addItem("Cso")
            self.McIntosh_combo.addItem("Csi")
            self.McIntosh_combo.addItem("Csc")
            self.McIntosh_combo.addItem("Cao")
            self.McIntosh_combo.addItem("Cai")
            self.McIntosh_combo.addItem("Cac")
            self.McIntosh_combo.addItem("Cho")
            self.McIntosh_combo.addItem("Chi")
            self.McIntosh_combo.addItem("Chc")
            self.McIntosh_combo.addItem("Cko")
            self.McIntosh_combo.addItem("Cki")
            self.McIntosh_combo.addItem("Ckc")
        elif zurich_type=='D':
            self.McIntosh_combo.addItem("Dro")
            self.McIntosh_combo.addItem("Dri")
            self.McIntosh_combo.addItem("Drc")
            self.McIntosh_combo.addItem("Dso")
            self.McIntosh_combo.addItem("Dsi")
            self.McIntosh_combo.addItem("Dsc")
            self.McIntosh_combo.addItem("Dao")
            self.McIntosh_combo.addItem("Dai")
            self.McIntosh_combo.addItem("Dac")
            self.McIntosh_combo.addItem("Dho")
            self.McIntosh_combo.addItem("Dhi")
            self.McIntosh_combo.addItem("Dhc")
            self.McIntosh_combo.addItem("Dko")
            self.McIntosh_combo.addItem("Dki")
            self.McIntosh_combo.addItem("Dkc")
        elif zurich_type=='E':
            self.McIntosh_combo.addItem("Ero")
            self.McIntosh_combo.addItem("Eri")
            self.McIntosh_combo.addItem("Erc")
            self.McIntosh_combo.addItem("Eso")
            self.McIntosh_combo.addItem("Esi")
            self.McIntosh_combo.addItem("Esc")
            self.McIntosh_combo.addItem("Eao")
            self.McIntosh_combo.addItem("Eai")
            self.McIntosh_combo.addItem("Eac")
            self.McIntosh_combo.addItem("Eho")
            self.McIntosh_combo.addItem("Ehi")
            self.McIntosh_combo.addItem("Ehc")
            self.McIntosh_combo.addItem("Eko")
            self.McIntosh_combo.addItem("Eki")
            self.McIntosh_combo.addItem("Ekc")
        elif zurich_type=='F':
            self.McIntosh_combo.addItem("Fro")
            self.McIntosh_combo.addItem("Fri")
            self.McIntosh_combo.addItem("Frc")
            self.McIntosh_combo.addItem("Fso")
            self.McIntosh_combo.addItem("Fsi")
            self.McIntosh_combo.addItem("Fsc")
            self.McIntosh_combo.addItem("Fao")
            self.McIntosh_combo.addItem("Fai")
            self.McIntosh_combo.addItem("Fac")
            self.McIntosh_combo.addItem("Fho")
            self.McIntosh_combo.addItem("Fhi")
            self.McIntosh_combo.addItem("Fhc")
            self.McIntosh_combo.addItem("Fko")
            self.McIntosh_combo.addItem("Fki")
            self.McIntosh_combo.addItem("Fkc")
        elif zurich_type=='G':
            self.McIntosh_combo.addItem("Eso")    
            self.McIntosh_combo.addItem("Eao")    
            self.McIntosh_combo.addItem("Eho")    
            self.McIntosh_combo.addItem("Eko")    
            self.McIntosh_combo.addItem("Fho")    
            self.McIntosh_combo.addItem("Fko")
        elif zurich_type=='H':
            self.McIntosh_combo.addItem("Hhx")
            self.McIntosh_combo.addItem("Hkx")
        elif zurich_type=='J':
            self.McIntosh_combo.addItem("Hsx")
            self.McIntosh_combo.addItem("Hax")
            
        
        
    
    def set_mcIntosh_type(self, mcIntosh_type, zurich_type, grid_position):
        self.McIntosh_combo = QtGui.QComboBox(self)
        self.McIntosh_combo.setStyleSheet("color: black")
        self.McIntosh_combo.setMaximumWidth(70)
        
        self.update_McIntosh_type(zurich_type)
        
        self.grid_layout.addWidget(self.McIntosh_combo,
                                   grid_position[0],
                                   grid_position[1])
        grid_position[1]+=1 
        index = self.McIntosh_combo.findText(mcIntosh_type)
        self.McIntosh_combo.setCurrentIndex(index)
        
    def set_longitude(self, longitude, grid_position):
        grid_position[0] +=1
        self.longitude_label = QtGui.QLabel("Longitude")
        #self.longitude_label.setMaximumWidth(100)
        self.longitude_linedit = QtGui.QLineEdit(self)
        self.longitude_linedit.setText('{0:.2f}'.format(longitude))
        self.longitude_linedit.setMaximumWidth(60)
        self.grid_layout.addWidget(self.longitude_label, grid_position[0], 0)
        self.grid_layout.addWidget(self.longitude_linedit, grid_position[0], 1)
        
    def set_latitude(self, latitude, grid_position):
        grid_position[0]+=1
        
        self.latitude_label = QtGui.QLabel("Latitude")
        #self.latitude_label.setMaximumWidth(100)
        self.latitude_linedit = QtGui.QLineEdit(self)
        self.latitude_linedit.setText('{0:.2f}'.format(latitude))
        self.latitude_linedit.setMaximumWidth(60)
        self.grid_layout.addWidget(self.latitude_label, grid_position[0], 0)
        self.grid_layout.addWidget(self.latitude_linedit, grid_position[0], 1)

    def set_larger_spot(self, larger_spot, grid_position):
        grid_position[0]+=1
        self.larger_spot_label = QtGui.QLabel("Lead/trail")
        #self.larger_spot_label.setMaximumWidth(100)
        self.larger_spot_leading = QtGui.QPushButton("L")
        self.larger_spot_leading.setFixedWidth(self.latitude_linedit.width())
        self.larger_spot_egal = QtGui.QPushButton("=")
        self.larger_spot_egal.setFixedWidth(self.latitude_linedit.width())
        self.larger_spot_trailing = QtGui.QPushButton("T")
        self.larger_spot_trailing.setFixedWidth(self.latitude_linedit.width())
        
        self.grid_layout.addWidget(self.larger_spot_label, grid_position[0], 0)
        self.grid_layout.addWidget(self.larger_spot_leading, grid_position[0], 1)
        self.grid_layout.addWidget(self.larger_spot_egal, grid_position[0], 2)
        self.grid_layout.addWidget(self.larger_spot_trailing, grid_position[0], 3)
        
        if larger_spot is None:
            self.larger_spot_linedit.setStyleSheet("background-color: rgb(255, 165, 84)")
        elif larger_spot in [1, 4, 7]:
            self.larger_spot_leading.setStyleSheet("background-color: rgb(77, 185, 88)");
        elif larger_spot in [2, 5, 8]:
            self.larger_spot_trailing.setStyleSheet("background-color: rgb(77, 185, 88)");
        elif larger_spot in [3, 6, 9]:
            self.larger_spot_egal.setStyleSheet("background-color: rgb(77, 185, 88)");
        elif larger_spot==0:
            self.larger_spot_leading.setStyleSheet("background-color: rgb(255, 165, 84)");
            self.larger_spot_trailing.setStyleSheet("background-color: rgb(255, 165, 84)");
            self.larger_spot_egal.setStyleSheet("background-color: rgb(255, 165, 84)");
        elif larger_spot==-1:
            self.larger_spot_leading.setDisabled(True)
            self.larger_spot_trailing.setDisabled(True)
            self.larger_spot_egal.setDisabled(True)
            
    def set_surface(self, surface, grid_position):
        grid_position[0]+=1
        self.surface_label = QtGui.QLabel("Surface")
        #self.surface_label.setMaximumWidth(50)
        self.surface_linedit = QtGui.QLineEdit(self)
        self.surface_linedit.setMaximumWidth(60)
        self.grid_layout.addWidget(self.surface_label, grid_position[0], 0)
        self.grid_layout.addWidget(self.surface_linedit, grid_position[0], 1)
        
        if surface is None:
            surface = 0.
        self.surface_linedit.setText('{0:.2f}'.format(surface))
        if surface==0.:
            self.surface_linedit.setStyleSheet("background-color: rgb(255, 165, 84)")
    
    def set_empty(self):
        #Empty the layout
        for i in reversed(range(self.grid_layout.count())):
            """if (self.grid_layout.itemAt(i).widget().isLayout()):
                pass
            else:"""
            self.grid_layout.itemAt(i).widget().setParent(None)
              
    def set_welcome(self):
        label = QtGui.QLabel("Click on a group to see more informations")
        self.grid_layout.addWidget(label)
