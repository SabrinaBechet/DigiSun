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
    It consits of
    - combo box for zurich type
    - combo box for mcIntosh type
    - etc...
    Attributes:
    - grid_layout : layout of the group box
    - zurich_dipolar : list of zurich group being dipolar + "x"
    - widget_maximum_width : the maximum width of a widget in the group box
    - area_button: indicate the status of the group area
    - dipole_button: indicate the status of the group dipole
    - delete_button: allow to suppress a group
    - button_up, button_down, button_right, button_left : buttons to udpate the positions
    """
    def __init__(self):
        super(GroupBox, self).__init__()
        layout = QtGui.QVBoxLayout()
        self.grid_layout = QtGui.QGridLayout()
        self.setStyleSheet("color: darkblue")
        self.setLayout(self.grid_layout)      
        self.zurich_dipolar = ["B","C","D","E","F","G", "X"]
        self.widget_maximum_width= 60

    def set_title(self, title, grid_position):
        """ title on the top of the group box"""
        title_label = QtGui.QLabel(title)
        title_label.setStyleSheet("background-color: transparent")
        self.grid_layout.addWidget(title_label,
                                   grid_position[0],
                                   grid_position[1])

    def set_area_button(self, grid_position):
        """ button orange if surface not complete, transparent otherwhise"""
        self.area_button = QLabelClickable()
        area_pix = QtGui.QPixmap("icons/Iconnice/pie_chart_24.png")
        self.area_button.setPixmap(area_pix)
	self.area_button.setMaximumSize(24,24)
        self.area_button.setStyleSheet(
                    "background-color: transparent") 
	self.grid_layout.addWidget(self.area_button,
                                   grid_position[0],
                                   grid_position[1])   
	   
    def set_dipole_button(self, grid_position):
        """ 
        button orange if dipole not complete, transparent otherwhise.
        A dipole is not complete when:
        - if dipolar and position not filled
        - if dipolar and LTS not filled
        """
        self.dipole_button = QLabelClickable()
        dipole_pix = QtGui.QPixmap("icons/dipole_24.png")
        self.dipole_button.setPixmap(dipole_pix)
	self.dipole_button.setMaximumSize(24,24)
        self.dipole_button.setStyleSheet(
                    "background-color: transparent") 
	self.grid_layout.addWidget(self.dipole_button,
                                   grid_position[0],
                                   grid_position[1])
        
    def set_delete_group_button(self, grid_position):
        """ button to suprress a group"""
        self.delete_button = QLabelClickable()
        delete_pix = QtGui.QPixmap("icons/delete_cross_16.png")
        self.delete_button.setPixmap(delete_pix)
	self.delete_button.setMaximumSize(16,16)
        self.delete_button.setStyleSheet(
                    "background-color: transparent") 
	self.grid_layout.addWidget(self.delete_button,
                                   grid_position[0],
                                   grid_position[1])
		
    def set_arrows_buttons(self, grid_position):
        
        self.button_up = QtGui.QPushButton()
        arrow_up_pix = QtGui.QPixmap("icons/arrow_up.png");
        arrow_up = QtGui.QIcon(arrow_up_pix)
        self.button_up.setIcon(arrow_up);
        
        self.button_down = QtGui.QPushButton()
        arrow_down_pix = QtGui.QPixmap("icons/arrow_down.png");
        arrow_down = QtGui.QIcon(arrow_down_pix)
        self.button_down.setIcon(arrow_down);
        
        self.button_left = QtGui.QPushButton()
        arrow_left_pix = QtGui.QPixmap("icons/arrow_left.png");
        arrow_left = QtGui.QIcon(arrow_left_pix)
        self.button_left.setIcon(arrow_left);
        
        self.button_right = QtGui.QPushButton()
        self.button_right.setMinimumWidth(self.widget_maximum_width)
        self.button_right.setMaximumWidth(self.widget_maximum_width)
        arrow_right_pix = QtGui.QPixmap("icons/arrow_right.png");
        arrow_right = QtGui.QIcon(arrow_right_pix)
        self.button_right.setIcon(arrow_right);
        
        self.grid_layout.addWidget(self.button_up,
                                   grid_position[0],
                                   grid_position[1] + 1)
        self.grid_layout.addWidget(self.button_down,
                                   grid_position[0] + 2,
                                   grid_position[1] + 1)
        self.grid_layout.addWidget(self.button_left,
                                   grid_position[0] + 1,
                                   grid_position[1])
        self.grid_layout.addWidget(self.button_right,
                                   grid_position[0] + 1,
                                   grid_position[1] + 2)

    def set_spot_count(self, spot_count, grid_position):
        self.spot_number_linedit = QtGui.QLineEdit(str(spot_count))
        self.spot_number_linedit.setMaximumWidth(self.widget_maximum_width)
        self.spot_number_linedit.setStyleSheet("background-color: white; color: black")
        self.grid_layout.addWidget(self.spot_number_linedit,
                                   grid_position[0],
                                   grid_position[1])
       

    def set_zurich_combox_box(self, group_zurich_type, grid_position):
        self.zurich_combo = QtGui.QComboBox(self)
        self.zurich_combo.setStyleSheet("background-color: white; color:black")
        #Cancel the usual Mouse Wheel Event by giving to it a void function
        self.zurich_combo.wheelEvent = inputVoid
        zurich_type_lst = ['X', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'J']
        for el in zurich_type_lst:
                self.zurich_combo.addItem(el)
                
        self.grid_layout.addWidget(self.zurich_combo,
                              grid_position[0],
                              grid_position[1])
        
        
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
        # this is giving the empty line in the
        # drawing object!!! (signal of change)
        self.McIntosh_combo.clear() 
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
        #self.McIntosh_combo.setMaximumWidth(70)
        
        self.update_McIntosh_combo_box(zurich_type)
        self.McIntosh_combo.setStyleSheet("background-color: white; color: black")
        self.grid_layout.addWidget(self.McIntosh_combo,
                                   grid_position[0],
                                   grid_position[1]) 
        index = self.McIntosh_combo.findText(mcIntosh_type)
        self.McIntosh_combo.setCurrentIndex(index)
        
    def set_longitude(self, longitude, grid_position):
        
        self.longitude_label = QtGui.QLabel("Longitude")
        self.longitude_linedit = QtGui.QLineEdit(self)
        self.longitude_linedit.setText('{0:.2f}'.format(longitude))
        #self.longitude_linedit.setMaximumWidth(self.widget_maximum_width)
        self.longitude_linedit.setStyleSheet("background-color: white; color: black")
        self.grid_layout.addWidget(self.longitude_label,
                                   grid_position[0],
                                   grid_position[1])
        self.grid_layout.addWidget(self.longitude_linedit,
                                   grid_position[0],
                                   grid_position[1] + 1)
        
    def set_latitude(self, latitude, grid_position):
        self.latitude_label = QtGui.QLabel("Latitude")
        self.latitude_linedit = QtGui.QLineEdit(self)
        self.latitude_linedit.setText('{0:.2f}'.format(latitude))
        #self.latitude_linedit.setMaximumWidth(self.widget_maximum_width)
        self.latitude_linedit.setStyleSheet("background-color: white; color: black")
        self.grid_layout.addWidget(self.latitude_label,
                                   grid_position[0],
                                   grid_position[1])
        self.grid_layout.addWidget(self.latitude_linedit,
                                   grid_position[0],
                                    grid_position[1] + 1)

        
    def update_largest_spot(self, largest_spot, zurich_type):
        """
        Need some adaptation when colum with largest_spot added in the database!
        then replace g_spot directly by largest_spot!
        value of g_spot:
        0 for unipolar group -> button should be dissabled
        1->9 for dipolar group -> green to indicate the type of the largest spot
        NULL if not filled -> button should be in orange
        """

        print("update largest spot", largest_spot, zurich_type)
        
        if (largest_spot is None and
            zurich_type.upper() not in self.zurich_dipolar):
            self.largest_spot_leading.setStyleSheet("background-color: lightblue")
            self.largest_spot_trailing.setStyleSheet("background-color: lightblue")
            self.largest_spot_egal.setStyleSheet("background-color: lightblue")
            self.largest_spot_leading.setDisabled(True)
            self.largest_spot_trailing.setDisabled(True)
            self.largest_spot_egal.setDisabled(True)
            
        elif largest_spot is None and zurich_type.upper() in self.zurich_dipolar:
            self.largest_spot_leading.setStyleSheet("background-color: rgb(255, 165, 84)")
            self.largest_spot_trailing.setStyleSheet("background-color: rgb(255, 165, 84)")
            self.largest_spot_egal.setStyleSheet("background-color: rgb(255, 165, 84)")
            self.largest_spot_leading.setDisabled(False)
            self.largest_spot_trailing.setDisabled(False)
            self.largest_spot_egal.setDisabled(False)
        elif largest_spot is 'L':
            self.largest_spot_leading.setStyleSheet("background-color: rgb(77, 185, 88)")
            self.largest_spot_trailing.setStyleSheet("background-color: lightblue")
            self.largest_spot_egal.setStyleSheet("background-color: lightblue")
            self.largest_spot_leading.setDisabled(False)
            self.largest_spot_trailing.setDisabled(False)
            self.largest_spot_egal.setDisabled(False)
        elif largest_spot is 'T':
            self.largest_spot_trailing.setStyleSheet("background-color: rgb(77, 185, 88)")
            self.largest_spot_leading.setStyleSheet("background-color: lightblue")
            self.largest_spot_egal.setStyleSheet("background-color: lightblue")
            self.largest_spot_leading.setDisabled(False)
            self.largest_spot_trailing.setDisabled(False)
            self.largest_spot_egal.setDisabled(False)
        elif largest_spot is 'E':
            self.largest_spot_egal.setStyleSheet("background-color: rgb(77, 185, 88)")
            self.largest_spot_leading.setStyleSheet("background-color: lightblue")
            self.largest_spot_trailing.setStyleSheet("background-color: lightblue")
            self.largest_spot_leading.setDisabled(False)
            self.largest_spot_trailing.setDisabled(False)
            self.largest_spot_egal.setDisabled(False)
      
    def set_largest_spot(self, largest_spot, zurich_type, grid_position):
        """
        Create the widget and update the value of it.
        """
        self.largest_spot_label = QtGui.QLabel("Lead/Trail")
        self.largest_spot_leading = QtGui.QPushButton("L")
        self.largest_spot_egal = QtGui.QPushButton("=")
        self.largest_spot_trailing = QtGui.QPushButton("T")
        
        self.grid_layout.addWidget(self.largest_spot_label,
                                   grid_position[0],
                                   grid_position[1])
        self.grid_layout.addWidget(self.largest_spot_leading,
                                   grid_position[0],
                                   grid_position[1] + 1)
        self.grid_layout.addWidget(self.largest_spot_egal,
                                   grid_position[0],
                                   grid_position[1] + 2)
        self.grid_layout.addWidget(self.largest_spot_trailing,
                                   grid_position[0],
                                   grid_position[1] + 3)
        
        self.update_largest_spot(largest_spot, zurich_type)
            
    def set_surface(self, surface, grid_position):
        self.surface_label = QtGui.QLabel("Surface")
        self.surface_linedit = QtGui.QLineEdit(self)
        #self.surface_linedit.setMaximumWidth(self.widget_maximum_width)
        self.grid_layout.addWidget(self.surface_label,
                                   grid_position[0],
                                   grid_position[1])
        self.grid_layout.addWidget(self.surface_linedit,
                                   grid_position[0],
                                   grid_position[1] + 1)
        
        if surface is None:
            surface = 0.
        self.surface_linedit.setText('{0:.2f}'.format(surface))
        if surface==0.:
            self.surface_linedit.setStyleSheet("background-color: rgb(255, 165, 84)")
        else:
            self.surface_linedit.setStyleSheet("background-color: white; color: black")
    
