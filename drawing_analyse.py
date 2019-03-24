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

import os
from datetime import datetime
import math
import database
import group_box
import qlabel_drawing
import qlabel_group_surface
import coordinates
import toolbar
import statusbar
import drawing_view_page
import drawing_information
import group_frame
import configuration
import numpy as np
from PyQt4 import QtGui, QtCore


class DrawingAnalysePage(QtGui.QMainWindow):
    """
    The classes defined here contains only information related
    to the GUI of the drawing analyse.
    Keep the analyse itself somwhere else!
    - DrawingViewPage : the template of the DrawingViewPage
    - DrawingAnalysePage: the page itself with all the widgets
    Page that shows the drawing and where the analyse is done.
    Depending on the info_analysed list,it will shows:
    - only the info related to groups
    - additional info related to dipoles
    - additional info related to area

    Attributes:
    - config
    - drawing_page : structure of the GUI
    - vertical_scroll_bar
    - horizontal_scroll_bar
    - operator : operator name
    - zurich_dipolar : list of dipolar zurich type


    Methods:
    - setCentralWidget
    - add_drawing_information
    - add_current_session
    - set_toolbar
    - set_status_bar
    - set_button_color

    - set_large_grid
    - set_small_grid
    - set_group_visualisation
    - set_dipole_visualisation

    - set_helper_grid
    - start_calibration
    - set_add_group_mode
    - set_add_dipole_mode
    - set_surface_mode

    ----general:

    - scroll_position: scroll to a given position
    - check_information_complete
    - update_linedit_drawing
    - update_combo_box_drawing
    - jump_to_drawing_linedit
    - save_drawing
    - update_counter
    - drawing_value_changed
    - set_drawing_lst
    - update_session_lineEdit
    - set_drawing_lineEdit
    - set_path_to_qlabel
    - set_drawing


    ----related to groups:
    - add_group_box : when one click on the drawing with add group mode on
    - set_group_widget : associate a widget to each group
    - set_group_toolbox : associate a toolbox for the group on focus
    - set_focus_group_box : highlight the element on focus
    - update_group_visu : update the index of the group on focus for the visu
    - delete_group : delete a group by a click on the red cross
                     in the group toolbox
    - scroll_group_position
    - update_HGC_position
    - modify_drawing_spot_number
    - modify_drawing_zurich
    - modify_drawing_mcIntosh


    ----related to dipole:
    - check_dipole : check if the type of the current group is dipolar
                     -> write message
    - update_largest_spot : update the largest spot by clicking
                            on the LTS button
    - update_dipole_button

    ----related to area:
    - add_surface_widget
    - update_surface_qlabel
    - set_green_frame_around_surface

    """
    def __init__(self, operator=None):
        super(DrawingAnalysePage, self).__init__()
        
        self.setContextMenuPolicy(QtCore.Qt.PreventContextMenu)
        
        self.config = configuration.Config()
        self.config.set_archdrawing()
        self.config.set_drawing_analyse()

        self.drawing_page = drawing_view_page.DrawingViewPage()

        self.setCentralWidget(self.drawing_page)

        self.operator = operator
        self.level_info = ['group', 'dipole', 'area']  # group always included

        if (self.config.archdrawing_directory and os.path.isdir(
                self.config.archdrawing_directory)):

            self.add_drawing_information()
            self.add_current_session()
            self.label_right = qlabel_drawing.QLabelDrawing()

            self.label_right.right_click.connect(self.set_right_click_zoom)
    
            self.label_right.drawing_clicked.connect(
                lambda: self.set_focus_group_box(
                    self.label_right.selected_element))

            self.label_right.drawing_clicked.connect(
                lambda: self.set_group_toolbox(
                    self.label_right.selected_element))

            self.label_right.drawing_clicked.connect(
                lambda: self.update_surface_qlabel(
                    self.label_right.selected_element))

            self.label_right.drawing_clicked.connect(
                lambda: self.update_group_visu(
                    self.label_right.selected_element))

            self.label_right.drawing_clicked.connect(
                lambda: self.check_dipole(
                    self.label_right.selected_element))

            self.label_right.drawing_clicked.connect(
                lambda: self.scroll_group_position(
                    self.label_right.selected_element))

            self.label_right\
                .center_clicked\
                .connect(lambda: self.scroll_position(self.fraction_width_pt2,
                                                      self.fraction_height_pt2,
                                                      0,
                                                      self.point_name_pt2))

            self.label_right.north_clicked.connect(
                lambda: self.label_right.setCursor(QtCore.Qt.ArrowCursor))
            self.label_right.north_clicked.connect(
                lambda:  self.drawing_info.calibrated.setText(
                    str(self.drawing_lst[self.current_count].calibrated)))

            scroll = QtGui.QScrollArea()
            scroll.setWidget(self.label_right)

            scroll.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
            scroll.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
            scroll.setWidgetResizable(True)
            self.vertical_scroll_bar = scroll.verticalScrollBar()
            self.horizontal_scroll_bar = scroll.horizontalScrollBar()
            self.drawing_page.widget_right_layout.addWidget(scroll)

            if 'area' in self.level_info:
                self.add_surface_widget()

            self.drawing_lst = []

            self.set_toolbar()
            self.set_status_bar()

            self.label_right.north_clicked.connect(self.statusBar().clean)
            self.label_right.group_added.connect(self.add_group_box)
            self.label_right.group_pos_changed.connect(self.change_group_pos)
            self.label_right.dipole_added.connect(
                lambda: self.update_dipole_button(self.listWidget_groupBox.currentRow()))

            self.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
            self.zurich_dipolar = ["B", "C", "D", "E", "F", "G", "X"]

            self.step = 0
            self.group_box_shortcut = QtGui.QShortcut(QtGui.QKeySequence("q"), self)
            

        """else:
            my_font = QtGui.QFont("Comic Sans MS", 20)
            no_drawing_msg = QtGui.QLabel()
            no_drawing_msg.setText('No drawings corresponding to this entry')
            no_drawing_msg.setFont(my_font)
            no_drawing_msg.setAlignment(QtCore.Qt.AlignCenter)
            #no_drawing_msg.setContentsMargins(0, 0, 0, 0)
            self.drawing_page.widget_right_layout.addWidget(no_drawing_msg)
        """

    def set_status_bar(self):
        digisun_status_bar = statusbar.StatusBar()
        self.setStatusBar(digisun_status_bar)

    def set_toolbar(self):
        """
        Define the digisun toolbar.
        if dipole in the level of info -> dipole button
        if surface in the level of info -> surface button
        """

        digisun_toolbar = toolbar.Toolbar(self.label_right, self.level_info)
        self.addToolBar(digisun_toolbar)

        digisun_toolbar.zoom_in_but.clicked.connect(
            lambda: self.label_right.zoom_in(1.1))
        digisun_toolbar.zoom_in_but.clicked.connect(
            lambda: self.scroll_group_position(
                self.listWidget_groupBox.currentRow()))

        digisun_toolbar.zoom_out_but.clicked.connect(
            lambda: self.label_right.zoom_in(1/1.1))
        digisun_toolbar.zoom_out_but.clicked.connect(
            lambda: self.scroll_group_position(
                self.listWidget_groupBox.currentRow()))

        digisun_toolbar.quick_zoom_but.clicked.connect(self.set_quick_zoom)
        digisun_toolbar.large_grid_but.clicked.connect(self.set_large_grid)
        digisun_toolbar.small_grid_but.clicked.connect(self.set_small_grid)
        digisun_toolbar.group_visu_but.clicked\
                                      .connect(self.set_group_visualisation)
        digisun_toolbar.dipole_visu_but.clicked\
                                       .connect(self.set_dipole_visualisation)
        digisun_toolbar.helper_grid_but.clicked.connect(self.set_helper_grid)
        digisun_toolbar.calibration_but.clicked.connect(self.start_calibration)
        digisun_toolbar.add_group_but.clicked.connect(self.set_add_group_mode)
        digisun_toolbar.change_group_pos_but.clicked.connect(
            self.set_change_group_position_mode)

        if 'dipole' in self.level_info:
            digisun_toolbar.add_dipole_but.clicked\
                                          .connect(self.set_add_dipole_mode)

        if 'area' in self.level_info:
            digisun_toolbar.surface_but.clicked.connect(
                lambda: self.set_surface_mode(
                    self.listWidget_groupBox.currentRow()))

    def start_calibration(self):
        """
        Contains two parts:
        1. put the drawing on the center and click on the center -> signal
        2. put the drawing on the north and click on the norht -> signal
        here it is what happens when one click on the calibrate button
        (the rest is described in the mouse event)
        """
        self.label_right.calibration_mode.set_opposite_value()
        QtGui.QApplication.restoreOverrideCursor()

        if self.label_right.calibration_mode.value:
            self.label_right.setCursor(QtCore.Qt.CrossCursor)
            self.statusBar().name.setText("Calibration mode")

            self.label_right.calibration_mode.value = True
            self.label_right.center_done = False
            self.label_right.north_done = False

            self.label_right.group_visu.value = False
            self.label_right.dipole_visu.value = False
            self.label_right.large_grid_overlay.value = False
            self.label_right.small_grid_overlay.value = False

            self.label_right.helper_grid.value = False
            self.label_right.add_group_mode.value = False
            self.label_right.change_group_position_mode.value = False
            self.label_right.add_dipole_mode.value = False
            self.label_right.surface_mode.value = False
            self.drawing_page.widget_middle_up.setMinimumWidth(0)
            self.drawing_page.widget_middle_up.setMaximumWidth(10)

            self.label_right.zoom_in(
                5./self.label_right.scaling_factor)

            fraction_width_pt1 = self.drawing_lst[self.current_count]\
                                     .pt1_fraction_width
            fraction_height_pt1 = self.drawing_lst[self.current_count]\
                                      .pt1_fraction_height
            point_name_pt1 = self.drawing_lst[self.current_count].pt1_name
            self.scroll_position(fraction_width_pt1,
                                 fraction_height_pt1,
                                 0,
                                 point_name_pt1)

            self.fraction_width_pt2 = self.drawing_lst[self.current_count]\
                                          .pt2_fraction_width
            self.fraction_height_pt2 = self.drawing_lst[self.current_count]\
                                           .pt2_fraction_height
            self.point_name_pt2 = self.drawing_lst[self.current_count].pt2_name

        else:
            QtGui.QApplication.restoreOverrideCursor()
            self.label_right.zoom_in(
                1/self.label_right.scaling_factor)
            self.statusBar().clean()

    def set_helper_grid(self):
        """
        - reset the cursor shape to the original one
        - inverse the boolean value of the helper_grid mode
        - show a message in the status bar
        - if helper_grid is active, desactive all the other action modes
        The rest is done in the mouseEvent of the qlabel object.
        """

        self.label_right.setCursor(QtCore.Qt.ArrowCursor)
        self.label_right.helper_grid.set_opposite_value()

        if self.label_right.helper_grid.value:
            self.statusBar().name.setText("Helper grid mode")
            if self.drawing_lst[self.current_count].calibrated == 0:

                self.statusBar().comment.setText(" Warning :" +
                                                 " The calibration must" +
                                                 " be  done before using" +
                                                 " the helper grid!")
            else:
                self.statusBar().comment.setText("Click on a point" +
                                                 " on the solar disk" +
                                                 " to see the helper" +
                                                 " grid ")

            if self.label_right.calibration_mode.value:
                self.start_calibration()
            self.label_right.add_group_mode.value = False
            self.label_right.change_group_position_mode.value = False
            self.label_right.add_dipole_mode.value = False
            self.label_right.surface_mode.value = False
            self.drawing_page.widget_middle_up.setMinimumWidth(0)
            self.drawing_page.widget_middle_up.setMaximumWidth(10)

        else:
            self.statusBar().clean()
            self.label_right.set_img()

    def set_add_group_mode(self):
        """
        - reset the cursor to its original shape
        - set all the other action mode to false
        - if group visu mode not activated -> activate it
        - set the cursor to one showing that we are in the add group mode
        """
        QtGui.QApplication.restoreOverrideCursor()
        self.label_right.add_group_mode.set_opposite_value()

        if self.label_right.add_group_mode.value:
            self.statusBar().name.setText("Add group mode")

            if not self.label_right.group_visu.value:
                self.label_right.group_visu.value = True
                self.label_right.set_img()

            if self.drawing_lst[self.current_count].calibrated == 0:
                self.statusBar().comment.setText(" Warning :" +
                                                 " The calibration must" +
                                                 " be  done before adding" +
                                                 " groups!")
            else:
                self.statusBar().comment.setText("Click on a the group" +
                                                 " position to add it")
                cursor_img = ("cursor/Pixel_perfect/target_24.png")
                cursor_add_group = QtGui.QCursor(QtGui.QPixmap(cursor_img))
                # QtGui.QApplication.setOverrideCursor(cursor_add_group)
                self.label_right.setCursor(cursor_add_group)

            if self.label_right.calibration_mode.value:
                self.start_calibration()
            self.label_right.helper_grid.value = False
            self.label_right.change_group_position_mode.value = False
            self.label_right.add_dipole_mode.value = False
            self.label_right.surface_mode.value = False
            self.drawing_page.widget_middle_up.setMinimumWidth(0)
            self.drawing_page.widget_middle_up.setMaximumWidth(10)

        else:
            # print("restore the old cursor")
            # QtGui.QApplication.restoreOverrideCursor()
            self.label_right.setCursor(QtCore.Qt.ArrowCursor)
            self.statusBar().clean()


    def set_change_group_position_mode(self):
        """
        Change the position of the group highlighted.
        """
        QtGui.QApplication.restoreOverrideCursor()
        self.label_right.change_group_position_mode.set_opposite_value()

        if self.label_right.change_group_position_mode.value:
            self.statusBar().name.setText("Change group position mode")

            if not self.label_right.group_visu.value:
                self.label_right.group_visu.value = True
                self.label_right.set_img()

            if self.drawing_lst[self.current_count].calibrated == 0:
                self.statusBar().comment.setText(" Warning :" +
                                                 " The calibration must" +
                                                 " be  done before change the " +
                                                 " groups position!")
            else:
                self.statusBar().comment.setText("Click on a the group" +
                                                 " position to change it")
                cursor_img = ("cursor/Pixel_perfect/target_24.png")
                cursor_add_group = QtGui.QCursor(QtGui.QPixmap(cursor_img))
                # QtGui.QApplication.setOverrideCursor(cursor_add_group)
                self.label_right.setCursor(cursor_add_group)

            if self.label_right.calibration_mode.value:
                self.start_calibration()
            self.label_right.helper_grid.value = False
            self.label_right.add_group_mode.value = False
            self.label_right.add_dipole_mode.value = False
            self.label_right.surface_mode.value = False
            self.drawing_page.widget_middle_up.setMinimumWidth(0)
            self.drawing_page.widget_middle_up.setMaximumWidth(10)

        else:
            # print("restore the old cursor")
            # QtGui.QApplication.restoreOverrideCursor()
            self.label_right.setCursor(QtCore.Qt.ArrowCursor)
            self.statusBar().clean()


    def add_group_box(self):
        """
        Fonction triggered when one click on the drawing while
        the add_group_mode is on.
        - add a widget for the new group
        - put the focus on the new group
        - add a toolbox for the new group
        - display the updated wolf number
        """
        self.set_group_widget()
        self.set_focus_group_box(
            self.drawing_lst[self.current_count].group_count - 1)
        self.set_group_toolbox(
            self.drawing_lst[self.current_count].group_count - 1)
        self.update_group_visu(
            self.drawing_lst[self.current_count].group_count - 1)
        self.drawing_info.wolf_number.setText(
            str(self.drawing_lst[self.current_count].wolf))

    def change_group_pos(self):
        """
        Fonction triggered when on click on the drawing while
        the change_group_pos is on.
        - update the group toolbox (value of longitude and latitude)
        - update the visu of the group
        """
        group_index = self.listWidget_groupBox.currentRow()
        self.set_group_toolbox(group_index)
        self.update_group_visu(group_index)
            
    def set_add_dipole_mode(self):
        """
        - reset the cursor to its original shape
        - set all the other action mode to false
        - if dipole visu mode not activated -> activate it
        - set the cursor to one showing that we are in the add dipole mode
        - check that the group is dipolar
        """
        QtGui.QApplication.restoreOverrideCursor()
        self.label_right.add_dipole_mode.set_opposite_value()

        if self.label_right.add_dipole_mode.value:
            self.statusBar().name.setText("Add dipole mode")

            if not self.label_right.dipole_visu.value:
                self.label_right.dipole_visu.value = True
                self.label_right.set_img()

            if self.drawing_lst[self.current_count].calibrated == 0:
                self.statusBar().comment.setText(" Warning :" +
                                                 " The calibration must" +
                                                 " be  done before adding" +
                                                 " dipole!")

            elif (self.drawing_lst[self.current_count].calibrated == 1 and
                  self.drawing_lst[self.current_count].group_count == 0):
                self.statusBar().comment.setText(" Warning :" +
                                                 " Dipolar groups must" +
                                                 " be  added before adding" +
                                                 " dipole!")

            elif (self.drawing_lst[self.current_count].calibrated == 1 and
                  self.drawing_lst[self.current_count].group_count > 0):
                cursor_img = ("cursor/Dario_Ferrando/expand_16.png")
                cursor_add_dipole = QtGui.QCursor(QtGui.QPixmap(cursor_img))
                # QtGui.QApplication.setOverrideCursor(cursor_add_group)
                self.label_right.setCursor(cursor_add_dipole)
                # self.label_right.setCursor(
                #    QtCore.Qt.SizeBDiagCursor)
                self.check_dipole(self.listWidget_groupBox.currentRow())

            if self.label_right.calibration_mode.value:
                self.start_calibration()
            self.label_right.helper_grid.value = False
            self.label_right.add_group_mode.value = False
            self.label_right.change_group_position_mode.value = False
            self.label_right.surface_mode.value = False
            self.drawing_page.widget_middle_up.setMinimumWidth(0)
            self.drawing_page.widget_middle_up.setMaximumWidth(10)
        else:
            # QtGui.QApplication.restoreOverrideCursor()
            self.label_right.setCursor(QtCore.Qt.ArrowCursor)
            self.statusBar().clean()

    def set_surface_mode(self, n=0):
        """
        - reset the cursor to its original shape
        - open the widget_middle_up where the surface module is defined
        - set all the other action mode to false
        - zoom the original drawing x5
        - scroll at the group position
        """
        #QtGui.QApplication.restoreOverrideCursor()
        self.label_right.setCursor(QtCore.Qt.ArrowCursor)
        self.label_right.surface_mode.set_opposite_value()
        self.statusBar().clean()
        surface_module_size_min = 380
        surface_module_size_max = 580

        if self.label_right.surface_mode.value:
            self.drawing_page\
                .widget_middle_up\
                .setMinimumWidth(surface_module_size_min)
            self.drawing_page\
                .widget_middle_up\
                .setMaximumWidth(surface_module_size_max)

            self.label_right.helper_grid.value = False
            self.label_right.calibration_mode.value = False
            self.label_right.add_group_mode.value = False
            self.label_right.add_dipole_mode.value = False
            self.label_right.large_grid_overlay.value = False
            self.label_right.small_grid_overlay.value = False

            self.zoom_area = 5. / self.label_right.scaling_factor
            self.label_right.zoom_in(self.zoom_area)

            if self.drawing_lst[self.current_count].group_count > 0:
                pos_x = (self.drawing_lst[self.current_count]
                         .group_lst[self.listWidget_groupBox.currentRow()]
                         .posX / self.label_right.drawing_pixMap.width())
                pos_y = (self.drawing_lst[self.current_count]
                         .group_lst[self.listWidget_groupBox.currentRow()].
                         posY / self.label_right.drawing_pixMap.height())
                self.scroll_position(pos_x, pos_y, surface_module_size_max)

            self.update_surface_qlabel(
                self.listWidget_groupBox.currentRow())

            self.label_right.set_img()

        elif self.label_right.surface_mode.value is False:
            self.drawing_page.widget_middle_up.setMinimumWidth(0)
            self.drawing_page.widget_middle_up.setMaximumWidth(10)
            self.label_right.large_grid_overlay.value = True
            self.label_right.zoom_in(
                1./self.zoom_area)
            self.label_right.setCursor(QtCore.Qt.ArrowCursor)

    def update_surface_qlabel(self, n, step=0):
        """
        Update the QLabelGroupSurface object which represents
        an image of the drawing to calculate the surface.
        """
        if step:
            self.step += step
        else:
            self.step = 0

        if (self.drawing_lst[self.current_count].calibrated and
                self.label_right.surface_mode and
                self.label_right.get_img_array() is not None):

            if self.drawing_lst[self.current_count].group_count > 0:
                posX = self.drawing_lst[self.current_count]\
                           .group_lst[n]\
                           .posX
                posY = self.drawing_lst[self.current_count]\
                           .group_lst[n]\
                           .posY

                # don't forget to document this:
                # print("------------------------------------CHECK!!!!!!!",
                #       self.label_right.pixmap().height(),
                # self.label_right.drawing_pixMap.height())

                """frame_size = self.group_surface_widget.update_frame_surface(
                    self.drawing_lst[self.current_count].calibrated_radius,
                    step)

                """
                frame_size = group_frame.group_frame(
                    self.drawing_lst[self.current_count].group_lst[n].zurich,
                    self.drawing_lst[self.current_count].calibrated_radius,
                    self.drawing_lst[self.current_count].group_lst[n].posX,
                    self.drawing_lst[self.current_count].group_lst[n].posY,
                    self.drawing_lst[self.current_count].calibrated_center.x,
                    self.drawing_lst[self.current_count].calibrated_center.y)

                if self.step:
                    frame_step = (self.step *
                                  self.drawing_lst[self.current_count]
                                  .calibrated_radius/30)

                    if frame_size + frame_step > 0:
                        frame_size += frame_step

                    else:
                        self.step -= step
                        frame_step = (self.step *
                                      self.drawing_lst[self.current_count]
                                      .calibrated_radius/30)
                        frame_size += frame_step

                self.label_right.frame_size = frame_size
                if step != 0:
                    self.label_right.set_img()

                img_pix = self.label_right.get_img_array()

                # take a bigger matrix to have the border at 0
                bigger_matrix = np.ones((img_pix.shape[0] + 200,
                                         img_pix.shape[1] + 200),
                                        dtype=np.uint8) * 255
                bigger_matrix[100: 100 + img_pix.shape[0],
                              100: 100 + img_pix.shape[1]] = img_pix

                x_min = int(100 + posX - frame_size/2)
                x_max = int(100 + posX + frame_size/2)
                y_min = int(100 + posY - frame_size/2)
                y_max = int(100 + posY + frame_size/2)

                selection_array = bigger_matrix[y_min: y_max,
                                                x_min: x_max]
                # print("selection array: {}".format(selection_array.shape))

                self.group_surface_widget.set_group_info(
                    self.drawing_lst[self.current_count],
                    n,
                    posX - frame_size/2,
                    posY - frame_size/2)

                self.group_surface_widget.set_array(selection_array)

            else:
                self.group_surface_widget.qlabel_group_surface.setText(
                    "No groups defined for this drawing!")

        elif (not self.drawing_lst[self.current_count].calibrated and
              self.label_right.surface_mode):
            self.group_surface_widget.qlabel_group_surface.setText(
                "No calibration done for this drawing!")

    def scroll_position(self, pos_x, pos_y, extra_width=0, point_name=None):
        """
        Automatically scroll to the position given
        by the pos_x and pos_y.
        """
        if point_name:
            self.statusBar().comment.setText(
                "Click on the " + point_name + " position")

        if self.label_right:
            self.vertical_scroll_bar.setMinimum(0)
            self.horizontal_scroll_bar.setMinimum(0)
            self.vertical_scroll_bar.setMaximum(
                self.label_right.pixmap().height() -
                self.vertical_scroll_bar.pageStep())
            self.horizontal_scroll_bar.setMaximum(
                self.label_right.pixmap().width() -
                self.horizontal_scroll_bar.pageStep() +
                extra_width)
        
            self.horizontal_scroll_bar.setValue(
                self.horizontal_scroll_bar.maximum() * pos_x)
            self.vertical_scroll_bar.setValue(
                self.vertical_scroll_bar.maximum() * pos_y)

    def set_group_visualisation(self):
        self.label_right.group_visu.set_opposite_value()
        self.label_right.set_img()

    def set_dipole_visualisation(self):
        self.label_right.dipole_visu.set_opposite_value()
        self.label_right.set_img()

    def set_right_click_zoom(self):
        self.label_right.quick_zoom.set_opposite_value()

        if self.label_right.quick_zoom.value:
            self.label_right.zoom_in(5/self.label_right.scaling_factor)
        else:
            self.label_right.zoom_in(1./self.label_right.scaling_factor)

        self.scroll_position(self.label_right.right_click_x/
                             self.label_right.drawing_pixMap.width(),
                             self.label_right.right_click_y/
                             self.label_right.drawing_pixMap.height())
             
        
    def set_quick_zoom(self):
        self.label_right.quick_zoom.set_opposite_value()

        if self.label_right.quick_zoom.value:
            self.label_right.zoom_in(5/self.label_right.scaling_factor)
        else:
            self.label_right.zoom_in(1./self.label_right.scaling_factor)

        self.scroll_group_position(
            self.listWidget_groupBox.currentRow())

    def set_large_grid(self):
        self.label_right.large_grid_overlay.set_opposite_value()
        if self.label_right.large_grid_overlay.value:
            self.label_right.small_grid_overlay.value = False
        self.label_right.set_img()

    def set_small_grid(self):
        self.label_right.small_grid_overlay.set_opposite_value()
        if self.label_right.small_grid_overlay.value:
            self.label_right.large_grid_overlay.value = False
        self.label_right.set_img()

    def set_group_widget(self):
        """
        Associate a widget to each group.
        """
        # A widget is deleted when its parents is deleted.
        for i in reversed(
                range(self.drawing_page.widget_left_down_layout.count())):
                self.drawing_page.widget_left_down_layout\
                                 .itemAt(i)\
                                 .widget()\
                                 .setParent(None)

        title_left_down = QtGui.QLabel("Group information")
        title_left_down.setAlignment(QtCore.Qt.AlignCenter)
        title_left_down.setContentsMargins(0, 5, 0, 5)
        self.drawing_page.widget_left_down_layout.addWidget(title_left_down)

        group_count = self.drawing_lst[self.current_count].group_count

        self.listWidget_groupBox = QtGui.QListWidget(self)
        #self.listWidget_groupBox.setTabKeyNavigation(True)
        self.listWidget_groupBox.setStyleSheet(
            "QListView::item:selected {background : rgb(77, 185, 88);}")

        self.groupBoxLineList = []
        for i in range(group_count):

            grid_position = [0, 0]
            groupBoxLine = group_box.GroupBox()
            groupBoxLine.set_title(
                "Group " +
                str(self.drawing_lst[self.current_count].group_lst[i].number),
                grid_position)

            grid_position[1] += 1
            groupBoxLine.set_spot_count(
                self.drawing_lst[self.current_count].group_lst[i].spots,
                grid_position)

            grid_position[1] += 1
            groupBoxLine.set_zurich_combox_box(
                self.drawing_lst[self.current_count].group_lst[i].zurich,
                grid_position)

            grid_position[1] += 1
            groupBoxLine.set_mcIntosh_combo_box(
                self.drawing_lst[self.current_count].group_lst[i].McIntosh,
                self.drawing_lst[self.current_count].group_lst[i].zurich,
                grid_position)

            grid_position[1] += 1
            groupBoxLine.set_dipole_button(grid_position)

            grid_position[1] += 1
            groupBoxLine.set_area_button(grid_position)

            if self.drawing_lst[self.current_count].group_lst[i].zurich == "X":
                groupBoxLine.zurich_combo.setStyleSheet(
                    "background-color: rgb(255, 165, 84)")

            if self.drawing_lst[self.current_count].group_lst[i].spots == 0:
                groupBoxLine.spot_number_spinbox.setStyleSheet(
                    "background-color: rgb(255, 165, 84)")


            """group_zurich = self.drawing_lst[self.current_count]\
                               .group_lst[i].zurich.upper()
            group_g_spot = self.drawing_lst[self.current_count]\
                               .group_lst[i].g_spot
            group_dip1_lat = self.drawing_lst[self.current_count]\
                                 .group_lst[i].dipole1_lat

            if (group_zurich in self.zurich_dipolar and
                    (group_g_spot == 0 or group_dip1_lat is None)):
                groupBoxLine.dipole_button.setStyleSheet(
                    "background-color: rgb(255, 165, 84)")
            """
            #self.update_dipole_button()

            group_surface = self.drawing_lst[self.current_count]\
                                .group_lst[i].surface
            if (group_surface is None or group_surface == 0):
                groupBoxLine.area_button.setStyleSheet(
                    "background-color: rgb(255, 165, 84)")

            groupBoxLine.spot_number_spinbox.valueChanged.connect(
                lambda: self.modify_drawing_spot_number(
                    self.listWidget_groupBox.currentRow(),
                    False))
            groupBoxLine.zurich_combo.currentIndexChanged.connect(
                lambda: self.modify_drawing_zurich(
                    self.listWidget_groupBox.currentRow(),
                    False))
            groupBoxLine.McIntosh_combo.currentIndexChanged.connect(
                lambda: self.modify_drawing_mcIntosh(
                    self.listWidget_groupBox.currentRow(),
                    False))

            self.groupBoxLineList.append(groupBoxLine)

            item = QtGui.QListWidgetItem(self.listWidget_groupBox)
            item.setSizeHint(groupBoxLine.sizeHint())
            self.listWidget_groupBox.setItemWidget(item, groupBoxLine)

            self.update_dipole_button(i)

        self.drawing_page.widget_left_down_layout.addWidget(
            self.listWidget_groupBox)

        # Signals related to the change of item in the group box
        self.listWidget_groupBox.itemSelectionChanged.connect(
            lambda: self.set_focus_group_box(
                self.listWidget_groupBox.currentRow()))

        self.listWidget_groupBox.itemSelectionChanged.connect(
            lambda: self.set_group_toolbox(
                self.listWidget_groupBox.currentRow()))

        self.listWidget_groupBox.itemSelectionChanged.connect(
            lambda: self.update_surface_qlabel(
                self.listWidget_groupBox.currentRow()))

        self.listWidget_groupBox.itemSelectionChanged.connect(
            lambda: self.update_group_visu(
                self.listWidget_groupBox.currentRow()))

        self.listWidget_groupBox.itemSelectionChanged.connect(
            lambda: self.check_dipole(
                self.listWidget_groupBox.currentRow()))

        self.listWidget_groupBox.itemSelectionChanged.connect(
            lambda: self.scroll_group_position(
                self.listWidget_groupBox.currentRow()))
        
        self.group_box_shortcut.activated.connect(
            lambda: self.set_focus_group_box(
                self.listWidget_groupBox.currentRow()))
        
    def check_dipole(self, element_number):
        """
        Only for the add_dipole_mode.
        Check if the type of the element_number is dipolar and write
        the relevant message in the status bar.
        """
        if (self.label_right.add_dipole_mode.value and
                self.drawing_lst[self.current_count]
                .group_lst[element_number]
                .zurich.upper() not in self.zurich_dipolar):

            self.statusBar().name.setText("Add dipole mode")
            self.statusBar().comment.setStyleSheet("QLabel { color : red; }")
            self.statusBar().comment.setText(
                "Warning this is not a dipolar group!!")
            # self.label_right.setCursor(QtCore.Qt.ArrowCursor)

        elif (self.label_right.add_dipole_mode.value and
              self.drawing_lst[self.current_count].group_lst[element_number]
              .zurich.upper()
              in self.zurich_dipolar):

            self.statusBar().name.setText("Add dipole mode")
            self.statusBar().comment.setStyleSheet(
                "QLabel { color : black; }")
            self.statusBar().comment.setText("Click on a dipole" +
                                             " positions to add it")
        else:
            self.statusBar().clean()

    def set_focus_group_box(self, element_number):
        """
        - highlight the element under focus while the others are disabled.
        - if area mode: scroll on the element under focus
        """
        if self.listWidget_groupBox.count() > 0 and element_number >= 0:
            self.listWidget_groupBox.blockSignals(True)
            # itemchanged -> update group tool box
            self.listWidget_groupBox.item(element_number).setSelected(True)
            self.listWidget_groupBox.blockSignals(False)

        self.listWidget_groupBox.setCurrentRow(element_number)
        self.listWidget_groupBox.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.listWidget_groupBox.setFocus()
        # to change only the line on which the focus is
        for i in range(0, self.listWidget_groupBox.count()):
            if i == element_number:
                self.groupBoxLineList[i].spot_number_spinbox.setEnabled(True)
                self.groupBoxLineList[i].zurich_combo.setEnabled(True)
                self.groupBoxLineList[i].McIntosh_combo.setEnabled(True)
            else:
                self.groupBoxLineList[i].spot_number_spinbox.setEnabled(False)
                self.groupBoxLineList[i].zurich_combo.setEnabled(False)
                self.groupBoxLineList[i].McIntosh_combo.setEnabled(False)
                
    def scroll_group_position(self, element_number):
        """
        Scroll to the position of the group given by
        the element_number.
        """
        if (self.listWidget_groupBox.count() > 0):
            pos_x = (self.drawing_lst[self.current_count]
                     .group_lst[element_number].posX /
                     self.label_right.drawing_pixMap.width())
            pos_y = (self.drawing_lst[self.current_count]
                     .group_lst[element_number].posY /
                     self.label_right.drawing_pixMap.height())
            self.scroll_position(pos_x, pos_y)

    def set_group_toolbox(self, n=0):
        """
        Associate a toolbox with more detailled information
        for the group on focus.
        """
        # A widget is deleted when its parents is deleted.
        layout_object = self.drawing_page.widget_left_down_bis_layout.count()
        for i in reversed(range(layout_object)):
            self.drawing_page\
                .widget_left_down_bis_layout\
                .itemAt(i)\
                .widget()\
                .setParent(None)

        if len(self.drawing_lst[self.current_count].group_lst) > 0:
            self.group_toolbox = group_box.GroupBox()
            self.drawing_page.widget_left_down_bis_layout\
                             .addWidget(self.group_toolbox)

            # don't forget : [y, x]
            grid_position = [0, 0]
            self.group_toolbox.set_title(
                "Group " +
                str(self.drawing_lst[self.current_count].group_lst[n].number),
                grid_position)

            grid_position[1] += 1
            self.group_toolbox.set_spot_count(
                self.drawing_lst[self.current_count].group_lst[n].spots,
                grid_position)

            grid_position[1] += 1
            self.group_toolbox.set_zurich_combox_box(
                self.drawing_lst[self.current_count].group_lst[n].zurich,
                grid_position)

            grid_position[1] += 1
            self.group_toolbox.set_mcIntosh_combo_box(
                self.drawing_lst[self.current_count].group_lst[n].McIntosh,
                self.drawing_lst[self.current_count].group_lst[n].zurich,
                grid_position)

            grid_position[1] += 1
            self.group_toolbox.set_delete_group_button(grid_position)

            grid_position = [1, 0]

            self.group_toolbox.set_group_nb(
                self.drawing_lst[self.current_count]\
                .group_lst[n].number,
                grid_position)

            grid_position[0] += 1
            self.group_toolbox.set_latitude(
                self.drawing_lst[self.current_count]
                .group_lst[n].latitude * 180/math.pi,
                grid_position)

            grid_position[0] += 1
            self.group_toolbox.set_longitude(
                self.drawing_lst[self.current_count]
                .group_lst[n].longitude * 180/math.pi,
                grid_position)

            grid_position[0] += 1
            self.group_toolbox.set_surface(
                self.drawing_lst[self.current_count].group_lst[n].surface,
                grid_position)

            grid_position[0] += 1
            grid_position[1] = 0
            self.group_toolbox.set_largest_spot(
                self.drawing_lst[self.current_count].group_lst[n].largest_spot,
                self.drawing_lst[self.current_count].group_lst[n].zurich,
                grid_position)

            if self.config.extra1 :
                grid_position[0] += 1
                self.group_toolbox.set_extra_field1(
                    None,
                    self.config.extra1,
                    grid_position)

            grid_position = [1, 2]
            self.group_toolbox.set_arrows_buttons(grid_position)

            self.group_toolbox\
                .spot_number_spinbox\
                .valueChanged\
                .connect(lambda: self.modify_drawing_spot_number(
                    self.listWidget_groupBox.currentRow(),
                    True))

            self.group_toolbox\
                .zurich_combo\
                .currentIndexChanged\
                .connect(lambda: self.modify_drawing_zurich(
                    self.listWidget_groupBox.currentRow(),
                    True))

            self.group_toolbox\
                .McIntosh_combo\
                .currentIndexChanged\
                .connect(lambda: self.modify_drawing_mcIntosh(
                    self.listWidget_groupBox.currentRow(),
                    True))

            self.group_toolbox.delete_button.clicked.connect(self.delete_group)

            position_step = 0.1 * math.pi/180
            self.group_toolbox.button_up.clicked.connect(
                lambda: self.update_HGC_position('latitude', position_step))
            self.group_toolbox.button_down.clicked.connect(
                lambda: self.update_HGC_position('latitude', -position_step))
            self.group_toolbox.button_left.clicked.connect(
                lambda: self.update_HGC_position('longitude', position_step))
            self.group_toolbox.button_right.clicked.connect(
                lambda: self.update_HGC_position('longitude', -position_step))

            self.group_toolbox.largest_spot_leading_but.clicked.connect(
                lambda: self.update_largest_spot('L'))
            self.group_toolbox.largest_spot_egal_but.clicked.connect(
                lambda: self.update_largest_spot('E'))
            self.group_toolbox.largest_spot_trailing_but.clicked.connect(
                lambda: self.update_largest_spot('T'))

        else:
            print("no toolbox because there are no groups")

    def delete_group(self):
        """
        Delete a group by clicking on the red cross in the group_toolbox.
        """

        reponse = QtGui\
            .QMessageBox\
            .question(self,
                      "delete group",
                      "This will delete the group permanently from the database. "
                      "Do you confirm your action?",
                      QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)

        if reponse == QtGui.QMessageBox.Yes:
            index = self.current_count
            group_index = self.listWidget_groupBox.currentRow()
            
            self.drawing_lst[index].delete_group(group_index)
            self.set_group_widget()
            self.set_focus_group_box(0)
            self.set_group_toolbox()
            self.label_right.set_img()
            
            self.drawing_info.wolf_number.setText(
                str(self.drawing_lst[self.current_count].wolf))
        else:
            pass

    def update_largest_spot(self, largest_spot):
        """
        - update the largest spot when clicking on the LTS buttons.
        - update the g_spot value.
        - change the color of the group box if needed
        """
        group_index = self.listWidget_groupBox.currentRow()

        self.drawing_lst[self.current_count]\
            .group_lst[group_index].largest_spot = largest_spot

        self.drawing_lst[self.current_count]\
            .group_lst[group_index].update_g_spot()

        self.group_toolbox.update_largest_spot_buttons(
            largest_spot,
            self.drawing_lst[self.current_count]
            .group_lst[group_index].zurich)

        self.update_dipole_button(self.listWidget_groupBox.currentRow())

    def check_information_complete(self, index, level):
        """
        return the list missing_information with
        all the information not filled for the group
        of a given index and a given level of details.
        """

        group = self.drawing_lst[self.current_count].group_lst[index]

        group_complete = {"posX": False, "posY": False,
                          "zurich": False, "McIntosh": False, "spots": False}
        dipole_complete = {"dipole1_posX": False, "dipole1_posY": False,
                           "dipole2_posX": False, "dipole2_posY": False,
                           "largest_spot": False}
        area_complete = {"area": False}

        if level == 'group' or level == 'dipole' or level == 'area':
            info_complete = group_complete
            if group.posX:
                info_complete["posX"] = True
            if group.posY:
                info_complete["posY"] = True
            if group.zurich != 'X':
                info_complete["zurich"] = True
            if group.McIntosh != 'Xxx':
                info_complete["McIntosh"] = True
            if group.spots:
                info_complete["spots"] = True

        if level == 'dipole' and group.zurich.upper() in self.zurich_dipolar:
            info_complete.update(dipole_complete)
            if group.dipole1_lat:
                info_complete["dipole1_posX"] = True
            if group.dipole1_long:
                info_complete["dipole1_posY"] = True
            if group.dipole2_lat:
                info_complete["dipole2_posX"] = True
            if group.dipole2_long:
                info_complete["dipole2_posY"] = True
            if group.largest_spot:
                info_complete["largest_spot"] = True

        if level == 'area':
            info_complete.update(area_complete)
            if group.surface:
                info_complete["area"] = True

        missing_info = []
        for key, value in info_complete.items():
            if value is False:
                missing_info.append(key)

        return missing_info

    def update_area_button(self):
        
        group_index = self.listWidget_groupBox.currentRow()
        missing_info = self.check_information_complete(group_index,
                                                       'area')
        if missing_info:
            self.groupBoxLineList[group_index].area_button.setStyleSheet(
                "background-color: rgb(255, 165, 84)")
        else:
            self.groupBoxLineList[group_index].area_button.setStyleSheet(
                    "background-color: transparent")

    def update_dipole_button(self, group_index):
        """
        The information concerning the dipole (zurich in zurich dipolar)
        is complete when:
        - position is filled
        - LTS is filled
        if one of the two condition is not met -> dipole button in orange
        else -> dipole button in green
        """
        #group_index = self.listWidget_groupBox.currentRow()
        missing_info = self.check_information_complete(group_index,
                                                       'dipole')
        if missing_info:
            self.groupBoxLineList[group_index].dipole_button.setStyleSheet(
                "background-color: rgb(255, 165, 84)")
        else:
            self.groupBoxLineList[group_index].dipole_button.setStyleSheet(
                    "background-color: transparent")

    def update_HGC_position(self, coordinate, value):
        """
        Steps:
         - takes the current values of latitude/longitude.
         - Change it of a given value according to the user modification
         - Convert it to corresponding value of X and Y on the drawing
        !!! the new posX and posY is then not integer !!!
         - Record the new latitude, longitude, X and Y in the drawing object
          (the change group position function change as well Lcm and all
          other quantity related to the position of the group)
        - Display the new latitude/longitude in the linedit.
        - Show the image with the new position of the group.
        """
        index = self.current_count
        group_index = self.listWidget_groupBox.currentRow()

        longitude = self.drawing_lst[index].group_lst[group_index].longitude
        latitude = self.drawing_lst[index].group_lst[group_index].latitude

        drawing_height = self.label_right.drawing_height

        if coordinate == 'longitude':
            longitude += value
            longitude = longitude % (2 * math.pi)

        if coordinate == 'latitude':
            latitude += value

        if self.drawing_lst[index].p_oriented:
            angle_P_drawing = 0.0
        elif not self.drawing_lst[index].p_oriented:
            angle_P_drawing = self.drawing_lst[index].angle_P
            
            
        posX, posY, posZ = coordinates.cartesian_from_HGC_upper_left_origin(
            self.drawing_lst[index].calibrated_center.x,
            self.drawing_lst[index].calibrated_center.y,
            self.drawing_lst[index].calibrated_north.x,
            self.drawing_lst[index].calibrated_north.y,
            longitude,
            latitude,
            angle_P_drawing,
            self.drawing_lst[index].angle_B,
            self.drawing_lst[index].angle_L,
            drawing_height)

        self.drawing_lst[index].change_group_position(group_index,
                                                      latitude,
                                                      longitude,
                                                      posX,
                                                      posY)

        self.group_toolbox.longitude_linedit.setText('{0:.2f}'.format(
            self.drawing_lst[index].group_lst[group_index].longitude *
            180/math.pi))
        self.group_toolbox.latitude_linedit.setText('{0:.2f}'.format(
            self.drawing_lst[index].group_lst[group_index].latitude *
            180/math.pi))

        self.label_right.set_img()

    def modify_drawing_spot_number(self, n, is_toolbox):
        """
        A change in the spots number consists in:
        - update the drawing object
        - display the right number in the toolbox and the groupbox
        - put the linedit in orange in case the number is 0, white otherwhise
        TO DO: check that the value entered is a number!
        """
        if is_toolbox:
            new_sunspot_number = self.group_toolbox.spot_number_spinbox.value()

        else:
            new_sunspot_number = self.groupBoxLineList[n]\
                                     .spot_number_spinbox.value()

        try:
            self.drawing_lst[self.current_count].update_spot_number(
                self.listWidget_groupBox.currentRow(),
                int(new_sunspot_number))

        except ValueError:
            QtGui.QMessageBox\
                 .warning(self,
                          "sunspot number value",
                          "One of the sunspot number is not a number!")

        if self.drawing_lst[self.current_count].group_lst[n].spots == 0:
            self.groupBoxLineList[n].spot_number_spinbox.setStyleSheet(
                "background-color: rgb(255, 165, 84)")
        else:
            self.groupBoxLineList[n].spot_number_spinbox.setStyleSheet(
                "background-color: white")

        self.groupBoxLineList[n].spot_number_spinbox.setValue(
            self.drawing_lst[self.current_count].group_lst[n].spots)
        self.group_toolbox.spot_number_spinbox.setValue(
            self.drawing_lst[self.current_count].group_lst[n].spots)

        self.drawing_info.wolf_number.setText(
            str(self.drawing_lst[self.current_count].wolf))
        self.update_dipole_button(self.listWidget_groupBox.currentRow())

    def modify_drawing_zurich(self, n, is_toolbox):
        """
        A change in the zurich type consits in :
        - record temporary the old zurich type
        - update the value in the toolbox or group box
        - change the value of the new zurich type in the drawing object
        - update the list of McIntosh type enabled for the give zurich type
        - enable/disable the LTS buttons depending on the new/old zurich:
          - old zurich unipolar and new zurich unipolar -> no change
          - old zurich unipolar and new zurich dipolar -> enable LTS button
        """

        old_zurich_type = self.drawing_lst[self.current_count]\
                              .group_lst[self.listWidget_groupBox
                                         .currentRow()]\
                              .zurich
        if is_toolbox:
            new_zurich_type = str(self.group_toolbox.zurich_combo
                                  .currentText())
            new_zurich_index = self.group_toolbox.zurich_combo.currentIndex()
        else:
            new_zurich_type = str(self.groupBoxLineList[n]
                                  .zurich_combo.currentText())
            new_zurich_index = self.groupBoxLineList[n]\
                                   .zurich_combo.currentIndex()

        if new_zurich_type != old_zurich_type:
            self.drawing_lst[self.current_count]\
                .group_lst[self.listWidget_groupBox.currentRow()]\
                .zurich = new_zurich_type

        self.groupBoxLineList[n].zurich_combo.setCurrentIndex(new_zurich_index)
        self.groupBoxLineList[n].update_McIntosh_combo_box(new_zurich_type)
        self.group_toolbox.zurich_combo.setCurrentIndex(new_zurich_index)
        self.group_toolbox.update_McIntosh_combo_box(new_zurich_type)

        if new_zurich_type == "X":
            self.groupBoxLineList[n].zurich_combo.setStyleSheet(
                "background-color: orange")
            self.group_toolbox.zurich_combo.setStyleSheet(
                "background-color: rgb(255, 165, 84)")
        else:
            self.groupBoxLineList[n].zurich_combo.setStyleSheet(
                "background-color: white")
            self.group_toolbox.zurich_combo.setStyleSheet(
                "background-color: white")

        if ((new_zurich_type.upper() in self.zurich_dipolar and
             old_zurich_type.upper() not in self.zurich_dipolar) or
            (new_zurich_type.upper() not in self.zurich_dipolar and
             old_zurich_type.upper() in self.zurich_dipolar)):
            self.drawing_lst[self.current_count].group_lst[n]\
                                                .largest_spot = None
            self.drawing_lst[self.current_count].group_lst[n].update_g_spot()

        self.update_dipole_button(self.listWidget_groupBox.currentRow())
        self.group_toolbox.update_largest_spot_buttons(
            self.drawing_lst[self.current_count].group_lst[n].largest_spot,
            new_zurich_type)

        self.check_dipole(n)

    def modify_drawing_mcIntosh(self, n, is_toolbox):
        old_mcIntosh_type = self.drawing_lst[self.current_count]\
                                .group_lst[self.listWidget_groupBox
                                           .currentRow()]\
                                .McIntosh

        if is_toolbox:
            new_mcIntosh_type = str(self.group_toolbox
                                    .McIntosh_combo.currentText())
            new_mcIntosh_index = self.group_toolbox\
                                     .McIntosh_combo.currentIndex()
        else:
            new_mcIntosh_type = str(self.groupBoxLineList[n]
                                    .McIntosh_combo.currentText())
            new_mcIntosh_index = self.groupBoxLineList[n]\
                                     .McIntosh_combo.currentIndex()

        if new_mcIntosh_type != old_mcIntosh_type:
            self.drawing_lst[self.current_count]\
                .group_lst[self.listWidget_groupBox.currentRow()]\
                .McIntosh = new_mcIntosh_type

        self.groupBoxLineList[n].McIntosh_combo.setCurrentIndex(
            new_mcIntosh_index)
        self.group_toolbox.McIntosh_combo.setCurrentIndex(new_mcIntosh_index)

    def update_surface(self):
        """
        Display the surface value in the appropriate linedit
        """
        surface = self.drawing_lst[self.current_count]\
                      .group_lst[self.listWidget_groupBox.currentRow()].surface

        if isinstance(surface, float):
            self.group_toolbox.surface_linedit.setText(
                '{0:.2f}'.format(surface))
        if surface == 0.:
            self.group_toolbox.surface_linedit.setStyleSheet(
                "background-color: rgb(255, 165, 84)")
        else:
            self.group_toolbox.surface_linedit.setStyleSheet(
                "background-color: white; color: black")

        self.update_area_button()

    def update_group_visu(self, n):
        """
        Update the index of the group on the focus,
        this group is then shown in green.
        """
        self.label_right.group_visu_index = n
        self.label_right.set_img()

    def add_drawing_information(self):
        """
        Add all the linedits related to the drawing information
        """
        title_left_up = QtGui.QLabel("Drawing information")
        title_left_up.setAlignment(QtCore.Qt.AlignCenter)
        title_left_up.setContentsMargins(0, 5, 0, 5)
        self.drawing_page.widget_left_up_layout.addWidget(title_left_up)

        self.drawing_info = drawing_information.DrawingInformationWidget()

        self.drawing_info.drawing_observer.textEdited.connect(
            lambda: self.update_linedit_drawing('observer',
                                                self.drawing_info.
                                                drawing_observer))

        self.drawing_info.drawing_quality.currentIndexChanged.connect(
            lambda: self.update_combo_box_drawing('quality',
                                                  self.drawing_info.
                                                  drawing_quality))

        self.drawing_info.drawing_type.currentIndexChanged.connect(
            lambda: self.update_combo_box_drawing('type',
                                                  self.drawing_info.
                                                  drawing_type))

        self.drawing_page.widget_left_up_layout.addWidget(self.drawing_info)

    def update_linedit_drawing(self, field, linedit):
        """
        Update the drawing object with the value given
        in the line edit, check if this value exists in the
        database.
        """
        uset_db = database.database()

        if uset_db.exist_in_db(field, 'name', linedit.text()):
            if field == 'observer':
                self.drawing_lst[self.current_count]\
                    .observer = str(linedit.text())
            linedit.setStyleSheet("background-color: white")

        else:
            linedit.setStyleSheet(
                "background-color: rgb(232, 103, 101)")

    def update_combo_box_drawing(self, parameter_name, combo_box):
        """
        Update the drawing object with the value given
        in the combo box, check if this value exists in the
        database.
        """
        db = database.database()

        if parameter_name == 'quality':
            self.drawing_lst[self.current_count]\
                .quality = str(combo_box.currentText())

        elif parameter_name == 'type':
            self.drawing_lst[self.current_count]\
                .drawing_type = str(combo_box.currentText())
            tuple_drawing_type = db\
                .get_drawing_information("drawing_type",
                                         str(combo_box.currentText()))
            self.drawing_lst[self.current_count]\
                .set_drawing_type(tuple_drawing_type[0])

        else:
            print("your parameter name: {} does not" +
                  " exist!".format(parameter_name))

    def add_surface_widget(self):

        self.group_surface_widget = qlabel_group_surface.GroupSurfaceWidget()
        self.drawing_page.widget_middle_up_layout.addWidget(
            self.group_surface_widget)
        self.drawing_page.widget_middle_up_layout.setSpacing(10)
        self.group_surface_widget.bigger_frame.connect(
            lambda: self.update_surface_qlabel(
                self.listWidget_groupBox.currentRow(),
                +1))
        self.group_surface_widget.smaller_frame.connect(
            lambda: self.update_surface_qlabel(
                self.listWidget_groupBox.currentRow(),
                -1))

        self.group_surface_widget\
            .surface_saved.connect(self.update_surface)

    def add_current_session(self):

        form_layout = QtGui.QFormLayout()
        form_layout.setSpacing(5)

        title_left_middle = QtGui.QLabel("Current session")
        title_left_middle.setAlignment(QtCore.Qt.AlignCenter)
        title_left_middle.setContentsMargins(0, 2, 0, 2)
        self.drawing_page.widget_left_middle_layout\
                         .addWidget(title_left_middle)

        current_operator_linedit = QtGui.QLineEdit(
            str(self.operator).upper(), self)
        current_operator_linedit.setEnabled(False)
        current_operator_linedit.setStyleSheet(
            "background-color: lightgray; color: black")

        self.but_previous = QtGui.QPushButton('previous', self)
        self.but_previous.setShortcut(QtGui.QKeySequence("Left"))
        self.but_previous.setToolTip("\'Left\'")
        self.but_next = QtGui.QPushButton('next', self)
        self.but_next.setShortcut(QtGui.QKeySequence("Right"))
        self.but_next.setToolTip("\'Right\'")
        
        self.but_next.clicked.connect(
            lambda: self.update_counter(self.current_count+1))
        self.but_next.clicked.connect(self.set_drawing)
        self.but_previous.clicked.connect(
            lambda: self.update_counter(self.current_count-1))
        self.but_previous.clicked.connect(self.set_drawing)

        layout_but = QtGui.QHBoxLayout()
        layout_but.addWidget(self.but_previous)
        layout_but.addWidget(self.but_next)

        layout_goto = self.jump_to_drawing_linedit()

        self.but_save = QtGui.QPushButton('save', self)
        self.but_save.setShortcut(QtGui.QKeySequence("Ctrl+s"))
        self.but_save.setToolTip('shortcut: \'Ctrl+s\'')                  
        self.but_save.clicked.connect(self.save_drawing)

        form_layout.addRow("Current operator: ", current_operator_linedit)
        form_layout.setLayout(1, QtGui.QFormLayout.SpanningRole, layout_goto)
        form_layout.setLayout(2, QtGui.QFormLayout.SpanningRole, layout_but)
        form_layout.setWidget(3, QtGui.QFormLayout.SpanningRole, self.but_save)

        self.drawing_page.widget_left_middle_layout.addLayout(form_layout)

    def jump_to_drawing_linedit(self):
        self.goto_drawing_linedit = QtGui.QLineEdit()
        self.goto_drawing_label1 = QtGui.QLabel()
        self.goto_drawing_label2 = QtGui.QLabel()
        self.goto_drawing_button = QtGui.QPushButton()

        self.goto_drawing_label1.setText("Jump to drawing")
        self.goto_drawing_linedit.setText("1")
        self.goto_drawing_linedit.setStyleSheet(
            "background-color: white; color: black")
        self.goto_drawing_label2.setText("out of 0")
        self.goto_drawing_button.setText("Go!")

        self.goto_drawing_button.clicked.connect(
            lambda: self.update_counter(
                int(self.goto_drawing_linedit.text())-1))
        self.goto_drawing_button.clicked.connect(
            lambda: self.set_drawing())

        self.goto_drawing_button.clicked.connect(
            lambda: self.update_surface_qlabel(0))

        layout_goto = QtGui.QHBoxLayout()
        layout_goto.addWidget(self.goto_drawing_label1)
        layout_goto.addWidget(self.goto_drawing_linedit)
        layout_goto.addWidget(self.goto_drawing_label2)
        layout_goto.addWidget(self.goto_drawing_button)
        return layout_goto

    def warning_box_info_incomplete(self, level):
        if level in self.level_info:

            missing_info_len = [len(self.check_information_complete(x, level))
                                for x in
                                range(0, self.drawing_lst[self.current_count].
                                      group_count)]

            range_lst = list(range(0, len(missing_info_len)))
            missing_info_group = [x for x in range_lst if
                                  missing_info_len[range_lst.index(x)] > 0]

            missing_group = ["Group {}: {} ".format(
                x,
                self.check_information_complete(x, level))
                             for x in missing_info_group]

            missing_group.insert(0, " information incomplete for ")

            if sum(missing_info_len):
                QtGui.QMessageBox.warning(self,
                                          "save information",
                                          level +
                                          "\n".join(missing_group))

    def save_drawing(self):
        """
        Save the drawing information in the database
        """
        self.warning_box_info_incomplete("dipole")
        self.warning_box_info_incomplete("area")

        operator_name = str(self.operator).upper()
        self.drawing_lst[self.current_count].operator = operator_name
        self.drawing_lst[self.current_count].last_update_time = datetime.now()

        if (self.drawing_lst[self.current_count].calibrated == 1 and
                self.drawing_lst[self.current_count].group_count == 0):
            reponse = QtGui\
                .QMessageBox\
                .question(self,
                          "save information",
                          "There is no groups recorded for this drawing. "
                          "Do you confirm that the analyse is finished?",
                          QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
            if reponse == QtGui.QMessageBox.Yes:
                self.drawing_lst[self.current_count].analyzed = 1
            else:
                self.drawing_lst[self.current_count].analyzed = 0

        if (self.drawing_lst[self.current_count].calibrated == 1 and
                self.drawing_lst[self.current_count].group_count > 0):
                self.drawing_lst[self.current_count].analyzed = 1

        self.drawing_lst[self.current_count].save_info()
        self.drawing_info\
            .set_drawing_linedit(self.drawing_lst[self.current_count])

    def drawing_recorded(self):
        """
        Set the save button to lightgray and
        the changed value to False
        """
        self.but_save.setStyleSheet("background-color: lightgray")
        self.drawing_lst[self.current_count].changed = False

    def update_counter(self, value):

        if value >= self.len_drawing_lst:
            value = self.len_drawing_lst-1
        elif value < 0:
            value = 0

        self.current_count = value

        if (self.current_count > 0 and
                self.current_count < self.len_drawing_lst - 1):
            self.but_next.setEnabled(True)
            self.but_previous.setEnabled(True)

        elif self.current_count == self.len_drawing_lst - 1:
            self.but_next.setDisabled(True)
            self.but_previous.setEnabled(True)

        elif self.current_count == 0:
            self.but_next.setEnabled(True)
            self.but_previous.setDisabled(True)

        self.set_drawing_lineEdit()
        self.update_session_lineEdit()

    def drawing_value_changed(self):
        """
        Set the save button in orange as soon as a new value is introduced
        """
        for el in self.drawing_lst:
            # print(el, el.changed)
            if el.changed:
                self.but_save\
                    .setStyleSheet("background-color: rgb(255, 165, 84)")

    def set_drawing_lst(self, drawing_lst):
        """
        Get the list of drawings from bulk analysis page.
        Set the counter to 0.
        """
        self.drawing_lst = drawing_lst

        for el in self.drawing_lst:
            el.info_saved.connect(self.drawing_recorded)
            el.value_changed.connect(self.drawing_value_changed)

        self.len_drawing_lst = len(drawing_lst)

        self.current_count = 0
        if len(drawing_lst) >= 1:
            self.but_next.setEnabled(True)
            self.but_previous.setEnabled(True)
            self.set_drawing_lineEdit()
            self.update_session_lineEdit()
        else:
            self.but_next.setDisabled(True)
            self.but_previous.setDisabled(True)

    def update_session_lineEdit(self):
        self.goto_drawing_linedit.setText(str(self.current_count + 1))
        self.goto_drawing_label2.setText("out of "+str(self.len_drawing_lst))

    def set_drawing_lineEdit(self):
        """
        Fill the linEdits with the information of the drawing.
        """

        if self.drawing_lst[self.current_count].changed:
            self.but_save\
                .setStyleSheet("background-color: rgb(255, 165, 84)")
        else:
            self.but_save\
                .setStyleSheet("background-color: lightgray")

        self.drawing_info\
            .set_drawing_linedit(self.drawing_lst[self.current_count])

    def set_path_to_qlabel(self):
        """
        set the path to the image of the drawing based
        on the information contained
        in the configuration file (digisun.ini).
        Here is fixed the structure of the filename and
        the structure of the directory.
        """
        if self.drawing_lst:

            self.config.set_file_path(self.drawing_lst[self.current_count].datetime)
            self.label_right.file_path = self.config.file_path

    def set_drawing(self):
        """
        - Get the right path of the image
        - check if 1) the drawing list is non null (entry in the db) and
        2) if the path exist
        (the corresponding drawing has an image in the drawing directory)
        - update the current_drawing of the qlabel image
        - set the group widget
        - set the group toolbox
        - set the img
        Note: this method should be called only
        when the current drawing change!
        otherwhise use self.label_right.set_img() to refresh the img
        """
        self.set_path_to_qlabel()

        if self.drawing_lst and os.path.isfile(self.label_right.file_path):
            self.label_right\
                .current_drawing = self.drawing_lst[self.current_count]
            self.label_right.group_visu_index = 0
            self.label_right.calibration_mode.value = False
            self.label_right.helper_grid.value = False
            self.label_right.add_group_mode.value = False
            self.label_right.change_group_position_mode.value = False
            self.label_right.add_dipole_mode.value = False
            self.label_right.setCursor(QtCore.Qt.ArrowCursor)

            if self.label_right.surface_mode.value:
                self.update_surface_qlabel(0)
            self.label_right.set_img()

            self.set_group_widget()

            self.set_focus_group_box(0)

            self.set_group_toolbox()
            if self.label_right.scaling_factor > 1.5:
                self.scroll_group_position(0)

            self.statusBar().name.setText("")
            self.statusBar().comment.setText("")

        else:
            self.label_right.set_msg_no_entry()
            self.drawing_info.set_empty()
            self.goto_drawing_linedit.setText("0")
            self.goto_drawing_label2.setText("out of 0")
            for i in reversed(
                    range(self.drawing_page.widget_left_down_layout.count())):
                self.drawing_page.widget_left_down_layout\
                                 .itemAt(i)\
                                 .widget()\
                                 .setParent(None)

            for i in reversed(
                    range(self.drawing_page
                          .widget_left_down_bis_layout.count())):
                self.drawing_page\
                    .widget_left_down_bis_layout\
                    .itemAt(i)\
                    .widget()\
                    .setParent(None)
