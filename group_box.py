# !/usr/bin/env python
# -*-coding:utf-8-*-

from PyQt4 import QtGui, QtCore

def inputVoid(self):
    pass

      
class QLabelClickable(QtGui.QLabel):
    """
    Label on which one can click (used to delete group)
    """    
    clicked = QtCore.pyqtSignal()
        
    def __init__(self):
        super(QtGui.QLabel, self).__init__()
        
    def mouseReleaseEvent(self, QMouseEvent):
        print("one click on the label!!")
        self.clicked.emit()
        

class GroupBox(QtGui.QWidget):
    """
    Represent the box associated to a group.
    It is used in the group_widget and in the group_toolbox.
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
        self.setStyleSheet("color: darkblue")
        self.setLayout(self.grid_layout)
        #self.setMinimumHeight(200)

    def get_confirm_spots(self):
        return self.grid_layout.itemAtPosition(0,4).widget()

    def get_spots(self):
        return self.grid_layout.itemAtPosition(0,1).widget()
    
    def get_zurich(self):
        return self.grid_layout.itemAtPosition(0,2).widget()
        
    def get_McIntosh(self):
        return self.grid_layout.itemAtPosition(0,3).widget()

    def get_dipole_button(self):
        return self.grid_layout.itemAtPosition(0,4).widget()

    def get_area_button(self):
        return self.grid_layout.itemAtPosition(0,5).widget()

    def get_del_button(self):
        return self.grid_layout.itemAtPosition(0,5).widget()
    
    def get_arrows(self):
        return (self.grid_layout.itemAtPosition(1,3).widget(),
                self.grid_layout.itemAtPosition(3,3).widget(),
                self.grid_layout.itemAtPosition(2,2).widget(),
                self.grid_layout.itemAtPosition(2,4).widget())

    def get_largest_spot_buttons(self):
        return (self.grid_layout.itemAtPosition(4,1).widget(),
                self.grid_layout.itemAtPosition(4,2).widget(),
                self.grid_layout.itemAtPosition(4,3).widget())
    
    def update_spots(self, spots):
        self.grid_layout.itemAtPosition(0,1).widget().setText(str(spots))
    
    def update_zurich(self, zurich):
        self.grid_layout.itemAtPosition(0,2)\
                        .widget()\
                        .setCurrentIndex(self.grid_layout\
                                         .itemAtPosition(0,2)\
                                         .widget().findText(zurich))
    
    def update_McIntosh(self, McIntosh):
        self.grid_layout.itemAtPosition(0,3)\
                        .widget()\
                        .setCurrentIndex(self.grid_layout\
                                         .itemAtPosition(0,3)\
                                         .widget().findText(McIntosh))
        
    def update_latitude(self, latitude):
        self.grid_layout.itemAtPosition(1,1).widget()\
                                            .setText(str(round(latitude,2)))
        
    def update_longitude(self, longitude):
        self.grid_layout.itemAtPosition(2,1).widget()\
                                            .setText(str(round(longitude,2)))
        

    def set_title(self, title, grid_position, colorised):
        self.title_label = QtGui.QLabel(title)
        """if colorised:
            self.title_label.setStyleSheet("background-color: orange")
        """
        self.title_label.sizeHint()
        self.grid_layout.addWidget(self.title_label,
                                   grid_position[0],
                                   grid_position[1])
        grid_position[1] += 1

    def set_area_button(self, grid_position):
        delete_button = QLabelClickable()
        delete_button_pix = QtGui.QPixmap("icons/Iconnice/pie_chart_24.png")
        delete_button.setPixmap(delete_button_pix)
	delete_button.setMaximumSize(24,24)
        delete_button.setStyleSheet(
                    "background-color: transparent") 
	self.grid_layout.addWidget(delete_button,
                                   grid_position[0],
                                   grid_position[1])
        
	grid_position[1]+=1

        
    def set_dipole_button(self, grid_position):
        delete_button = QLabelClickable()
        delete_button_pix = QtGui.QPixmap("icons/dipole_24.png")
        delete_button.setPixmap(delete_button_pix)
	delete_button.setMaximumSize(24,24)
        delete_button.setStyleSheet(
                    "background-color: transparent") 
	self.grid_layout.addWidget(delete_button,
                                   grid_position[0],
                                   grid_position[1])
        
	grid_position[1]+=1
        
 
    def set_delete_group_button(self, grid_position):
        
        delete_button = QLabelClickable()
        delete_button_pix = QtGui.QPixmap("icons/delete_cross_16.png")
        delete_button.setPixmap(delete_button_pix)
	delete_button.setMaximumSize(16,16)
        delete_button.setStyleSheet(
                    "background-color: transparent") 
	self.grid_layout.addWidget(delete_button,
                                   grid_position[0],
                                   grid_position[1]+1)
        
	grid_position[1]+=1
	
		
    def set_arrows_buttons(self):
        button_up = QtGui.QPushButton()
        button_up.setMinimumWidth(60)
        button_up.setMaximumWidth(60)
        arrow_up_pix = QtGui.QPixmap("icons/arrow_up");
        arrow_up = QtGui.QIcon(arrow_up_pix)
        button_up.setIcon(arrow_up);
        
        button_down = QtGui.QPushButton()
        button_down.setMinimumWidth(60)
        button_down.setMaximumWidth(60)
        arrow_down_pix = QtGui.QPixmap("icons/arrow_down");
        arrow_down = QtGui.QIcon(arrow_down_pix)
        button_down.setIcon(arrow_down);
        
        button_left = QtGui.QPushButton()
        button_left.setMinimumWidth(60)
        button_left.setMaximumWidth(60)
        arrow_left_pix = QtGui.QPixmap("icons/arrow_left");
        arrow_left = QtGui.QIcon(arrow_left_pix)
        button_left.setIcon(arrow_left);
        
        button_right = QtGui.QPushButton()
        button_right.setMinimumWidth(60)
        button_right.setMaximumWidth(60)
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
        self.spot_number_linedit.setStyleSheet("background-color: white; color: black")
        self.grid_layout.addWidget(self.spot_number_linedit,
                                   grid_position[0],
                                   grid_position[1])
        grid_position[1]+=1

    def set_zurich_combox_box(self, group_zurich_type, grid_position):
        #print("set zurich combo box")
        self.zurich_combo = QtGui.QComboBox(self)
        self.zurich_combo.setStyleSheet("background-color: white; color:black")
        self.zurich_combo.setMaximumWidth(50)

        #Cancel the usual Mouse Wheel Event by giving to it a void function
        self.zurich_combo.wheelEvent = inputVoid

        zurich_type_lst = ['X', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'J']
        for el in zurich_type_lst:
                self.zurich_combo.addItem(el)
                
        self.grid_layout.addWidget(self.zurich_combo,
                              grid_position[0],
                              grid_position[1])
        grid_position[1]+=1
        
        self.zurich_combo\
            .setCurrentIndex(self.zurich_combo.findText(group_zurich_type))
        
        self.zurich_combo\
            .setItemData(0, QtCore.Qt.black, QtCore.Qt.BackgroundRole)
        
        """self.zurich_combo\
            .currentIndexChanged\
            .connect(lambda : self.update_McIntosh_combo_box(self.zurich_combo.currentText()))
        """
    def update_McIntosh_combo_box(self, zurich_type):
        #print("update mcIntosh before clear", zurich_type)
        self.McIntosh_combo.clear() # this is giving the empty line in the drawing object!!! (signal of change)
        #print("update mcIntosh after clear", zurich_type)
        
        #Cancel the usual Mouse Wheel Event by giving to it a void function
        self.McIntosh_combo.wheelEvent = inputVoid

        zurich_McIntosh = {}
        zurich_McIntosh['X'] = ['Xxx']
        zurich_McIntosh['A'] = ['Axx']
        zurich_McIntosh['B'] = ['Bxo', 'Bxi', 'Bxc']
        zurich_McIntosh['C'] = ['Cro', 'Cri', 'Cso', 'Csi', 'Cao', 'Cai']
        zurich_McIntosh['D'] = ['Dro', 'Dri', 'Drc',
                                'Dso', 'Dsi', 'Dsc', 'Dao', 'Dai', 'Dac',
                                'Dho', 'Dhi', 'Dhc', 'Dko', 'Dki', 'Dkc']                        
        zurich_McIntosh['E'] = ['Esi', 'Esc', 'Eai', 'Eac',
                                'Ehi', 'Ehc', 'Eki', 'Ekc']
        zurich_McIntosh['F'] = ['Fhi', 'Fhc', 'Fki', 'Fkc']
        zurich_McIntosh['G'] = ['Eso', 'Eao', 'Eho', 'Eko',
                                'Fho', 'Fko']     
        zurich_McIntosh['H'] = ['Hkx', 'Hhx']
        zurich_McIntosh['J'] = ['Hsx', 'Hax']

        for el in zurich_McIntosh[str(zurich_type)]:
                self.McIntosh_combo.addItem(el)
    
    def set_mcIntosh_combo_box(self, mcIntosh_type, zurich_type, grid_position):
        self.McIntosh_combo = QtGui.QComboBox(self)
        self.McIntosh_combo.setMaximumWidth(70)
        
        self.update_McIntosh_combo_box(zurich_type)
        self.McIntosh_combo.setStyleSheet("background-color: white; color: black")
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
        self.longitude_linedit.setStyleSheet("background-color: white; color: black")
        self.grid_layout.addWidget(self.longitude_label, grid_position[0], 0)
        self.grid_layout.addWidget(self.longitude_linedit, grid_position[0], 1)
        
    def set_latitude(self, latitude, grid_position):
        grid_position[0]+=1
        
        self.latitude_label = QtGui.QLabel("Latitude")
        #self.latitude_label.setMaximumWidth(100)
        self.latitude_linedit = QtGui.QLineEdit(self)
        self.latitude_linedit.setText('{0:.2f}'.format(latitude))
        self.latitude_linedit.setMaximumWidth(60)
        self.latitude_linedit.setStyleSheet("background-color: white; color: black")
        self.grid_layout.addWidget(self.latitude_label, grid_position[0], 0)
        self.grid_layout.addWidget(self.latitude_linedit, grid_position[0], 1)

        
    def update_largest_spot(self, g_spot, zurich_type):
        """
        Need some adaptation when colum with largest_spot added in the database!
        then replace g_spot directly by largest_spot!
        value of g_spot:
        0 for unipolar group -> button should be dissabled
        1->9 for dipolar group -> green to indicate the type of the largest spot
        NULL if not filled -> button should be in orange

        """

        if g_spot in [1, 4, 7]:
            largest_spot = 'L'
        elif g_spot in [2, 5, 8]:
            largest_spot = 'T'
        elif g_spot in [3, 6, 9]:
            largest_spot = 'E'
        elif g_spot==0:
            largest_spot = None
        
        if (largest_spot is None and
            zurich_type.upper() not in ["B","C","D","E","F","G"]):
            self.largest_spot_leading.setDisabled(True)
            self.largest_spot_trailing.setDisabled(True)
            self.largest_spot_egal.setDisabled(True)
        elif largest_spot is None and zurich_type.upper() in ["B","C","D","E","F","G"]:
            self.largest_spot_leading.setStyleSheet("background-color: rgb(255, 165, 84)")
            self.largest_spot_trailing.setStyleSheet("background-color: rgb(255, 165, 84)")
            self.largest_spot_egal.setStyleSheet("background-color: rgb(255, 165, 84)")
            self.largest_spot_leading.setDisabled(False)
            self.largest_spot_trailing.setDisabled(False)
            self.largest_spot_egal.setDisabled(False)
        elif largest_spot is 'L':
            self.largest_spot_leading.setStyleSheet("background-color: rgb(77, 185, 88)")
            self.largest_spot_leading.setDisabled(False)
            self.largest_spot_trailing.setDisabled(False)
            self.largest_spot_egal.setDisabled(False)
        elif largest_spot is 'T':
            self.largest_spot_trailing.setStyleSheet("background-color: rgb(77, 185, 88)")
            self.largest_spot_leading.setDisabled(False)
            self.largest_spot_trailing.setDisabled(False)
            self.largest_spot_egal.setDisabled(False)
        elif largest_spot is 'E':
            self.largest_spot_egal.setStyleSheet("background-color: rgb(77, 185, 88)")
            self.largest_spot_leading.setDisabled(False)
            self.largest_spot_trailing.setDisabled(False)
            self.largest_spot_egal.setDisabled(False)
      
    def set_largest_spot(self, g_spot, zurich_type, grid_position):
        """
        Create the widget and update the value of it.
        """
        print("Enter in the larger spot function in group box", g_spot)
        grid_position[0]+=1
        self.largest_spot_label = QtGui.QLabel("Lead/trail")
        #self.largest_spot_label.setMaximumWidth(100)
        self.largest_spot_leading = QtGui.QPushButton("L")
        self.largest_spot_leading.setFixedWidth(self.latitude_linedit.width())
        self.largest_spot_egal = QtGui.QPushButton("=")
        self.largest_spot_egal.setFixedWidth(self.latitude_linedit.width())
        self.largest_spot_trailing = QtGui.QPushButton("T")
        self.largest_spot_trailing.setFixedWidth(self.latitude_linedit.width())
        
        self.grid_layout.addWidget(self.largest_spot_label, grid_position[0], 0)
        self.grid_layout.addWidget(self.largest_spot_leading, grid_position[0], 1)
        self.grid_layout.addWidget(self.largest_spot_egal, grid_position[0], 2)
        self.grid_layout.addWidget(self.largest_spot_trailing, grid_position[0], 3)
        
        self.update_largest_spot(g_spot, zurich_type)
            
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
        else:
            self.surface_linedit.setStyleSheet("background-color: white; color: black")
    
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
