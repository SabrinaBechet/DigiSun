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

import time
import sys
import collections
from datetime import datetime, timedelta
import database
import drawing

import time
import sys
import collections
from datetime import datetime, timedelta
import database
import drawing
from PyQt5 import QtGui, QtCore, QtWidgets


class ListPage(QtWidgets.QWidget):
    """
    Mother class that shows a list (of years or months)
    with the percentage of drawing calibrated/analysed/with area done
    """
    def __init__(self):
        super(ListPage, self).__init__()
        #self.config = configuration.Config()
        #self.config.set_drawing_analyse()
        #self.level_info = self.config.level
        
        self.table = QtWidgets.QTableWidget()

        """if 'area' in self.level_info:
            self.table.setColumnCount(5)
        else:
            self.table.setColumnCount(4)
        """
        if sys.platform=='darwin':
            self.setAttribute(QtCore.Qt.WA_MacNormalSize)
            
    def draw_table(self, dico, level_info):
        """
        Method that draws the table with the list of drawings and
        the fraction of calibrated/analysed/area done.
        """
        #self.table.horizontalHeader().setDefaultSectionSize(150)
        if 'area' in level_info:
            self.table.setColumnCount(5)
            self.table.setHorizontalHeaderLabels(["date",
                                                  " # total",
                                                  "calibrated",
                                                  "analysed", "area"])
        else:
            self.table.setColumnCount(4)
            self.table.setHorizontalHeaderLabels(["date",
                                                  " # total",
                                                  "calibrated",
                                                  "analysed"])

        count = 0
        for dico_keys, dico_values in dico.items():

            date_drawing = QtWidgets.QTableWidgetItem(str(dico_values[0]))
        
            tot_number_drawing = QtWidgets.QTableWidgetItem(str(dico_values[1]))
            
            self.table.setItem(count, 0, date_drawing)
            self.table.setItem(count, 1, tot_number_drawing)
            
            progressBar_calib = QtWidgets.QProgressBar()
            progressBar_analysed = QtWidgets.QProgressBar()
            progressBar_area = QtWidgets.QProgressBar()
 
            progressBar_calib.setValue(dico_values[2])
            progressBar_analysed.setValue(dico_values[3])
            progressBar_area.setValue(dico_values[4])
            
            self.table.setCellWidget(count, 2, progressBar_calib)
            self.table.setCellWidget(count, 3, progressBar_analysed)
            if 'area' in level_info:
                self.table.setCellWidget(count, 4, progressBar_area)

            count+=1

        #self.table.resizeColumnsToContents()
                 
class DayListPage(ListPage):
    """
    Page that shows the list of days for a given month.
    It is used essentially to delete drawings.

    It inherits from ListPage the following attributes:
    - self.table

    It inherits from ListPage the following methods:
    - draw_table
    - get_lst_from_database
    """

    def __init__(self):
        """
        Define the QVBoxLayout and add two widgets:
        - the 'select' button
        - the table widget
        """
        super(DayListPage, self).__init__()
        self.but_back = QtWidgets.QPushButton("hide days list view", self)
        self.but_back.setMaximumWidth(200)
        self.but_select = QtWidgets.QPushButton("show drawing", self)
        self.but_select.setMaximumWidth(200)
        self.but_delete = QtWidgets.QPushButton("delete drawing", self)
        self.but_delete.setMaximumWidth(200)
        
        day_list_layout = QtWidgets.QVBoxLayout()
        day_list_layout.addWidget(self.table)
        day_list_layout.addWidget(self.but_select)
        day_list_layout.addWidget(self.but_delete)
        day_list_layout.addWidget(self.but_back)
        self.setLayout(day_list_layout)

class MonthListPage(ListPage):
    """
    Page that shows the list of months for a given period (
    year or between start/end date).
    It inherits from ListPage the following attributes:
    - self.table

    It inherits from ListPage the following methods:
    - draw_table
    - get_lst_from_database
    """

    def __init__(self):
        """
        Define the QVBoxLayout and add two widgets:
        - the 'select' button
        - the table widget
        """
        super(MonthListPage, self).__init__()
        self.but_select = QtWidgets.QPushButton("show drawings", self)
        self.but_all_day_drawings = QtWidgets.QPushButton("show days list view", self)
        
        if sys.platform=='darwin':
            self.but_select.setAttribute(QtCore.Qt.WA_MacNormalSize)

        month_list_layout = QtWidgets.QVBoxLayout()
        month_list_layout.addWidget(self.table)
        month_list_layout.addWidget(self.but_select)
        month_list_layout.addWidget(self.but_all_day_drawings)
        self.setLayout(month_list_layout)

        
class YearListPage(ListPage):
    """
    Page that shows the list of years present in the database.
    It inherits from ListPage the following methods:
    - draw_table
    - get_lst_from_database
    """
    def __init__(self, config):
        """
        Define the QVBoxLayout and add two widgets:
        - the 'select' button
        - the table widget
        """
        super(YearListPage, self).__init__()
        
        self.config = config
        self.config.set_drawing_analyse()
        
        self.get_year_dico()
        self.table.setRowCount(len(self.dict_year))
        self.draw_table(self.dict_year, self.config.level)

        self.but_select = QtWidgets.QPushButton("select year", self)
        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addWidget(self.table)
        self.layout.addWidget(self.but_select)
        self.setLayout(self.layout)

    def get_year_dico(self):
        
        datetime_drawing_min = datetime(1800, 1, 1)
        datetime_drawing_max = datetime(2100, 1, 1)#.now()
        db = database.database(self.config)
        tuple_drawings = db\
            .get_all_in_time_interval("drawings",
                                      datetime_drawing_min,
                                      datetime_drawing_max)

        year_lst = set(el[1].year for el in tuple_drawings)
        self.dict_year = {}

        for year_index in year_lst:
            total = [el for el in tuple_drawings if el[1].year==year_index]
            total_count = len(total)
            
            calib = [el for el in tuple_drawings if el[1].year==year_index and
                     el[7]==1]
            frac_calibrated = len(calib) * 100./len(total)

            analyzed = [el for el in tuple_drawings if el[1].year==year_index and
                     el[8]==1]
            frac_analyzed = len(analyzed) * 100./len(total)

            area_done = [el for el in tuple_drawings if el[1].year==year_index and
                     el[18]==1]
            frac_area_done = len(area_done) * 100./len(total)

            year_to_print = str(year_index)

            self.dict_year[year_index] = (year_to_print, total_count, frac_calibrated,
                                          frac_analyzed, frac_area_done)

            # OrderedDict remembers the order in which the elements have been inserted
            # and we use the sorted function to insert it by order of time
            self.dict_year = collections.OrderedDict(sorted(self.dict_year.items()))

class DateSelectionPage(QtWidgets.QWidget):

    def __init__(self):
        super(DateSelectionPage, self).__init__()

        layout_date_selection = QtWidgets.QHBoxLayout()

        form_layout = QtWidgets.QFormLayout()

        self.start_date = QtWidgets.QDateEdit()
        self.start_date.setDisplayFormat("dd/MM/yyyy")
        self.end_date = QtWidgets.QDateEdit()
        self.end_date.setDisplayFormat("dd/MM/yyyy")

        self.but_select = QtWidgets.QPushButton("select")

        form_layout.addRow('start date: ', self.start_date)
        form_layout.addRow('end date: ', self.end_date)
        form_layout.addRow(self.but_select)

        layout_date_selection.addLayout(form_layout)
        self.setLayout(layout_date_selection)


class BulkViewPage(QtWidgets.QWidget):
    """ Template for the BulkAnalysePage.
    It contains three sections:
    - left_up : selection per date
    - left_down : selection per year
    - center :  selection per month for a given date/year
    - right : selection of days for a given month
    """
    def __init__(self, config):
        super(BulkViewPage, self).__init__()
        self.setLayout(QtWidgets.QVBoxLayout())

        self.max_width = 600

        self.widget_right = QtWidgets.QWidget()
        self.widget_right.setStyleSheet("background-color:lightgray;")
        self.widget_right_layout = QtWidgets.QVBoxLayout()
        self.widget_right.setLayout(self.widget_right_layout)
        self.widget_right.setMinimumWidth(0)
        self.widget_right.setMaximumWidth(10)
        
        self.widget_center = QtWidgets.QWidget()
        self.widget_center.setStyleSheet("background-color:lightgray;")
        self.widget_center_layout = QtWidgets.QVBoxLayout()
        self.widget_center.setLayout(self.widget_center_layout)
        self.widget_center.setMinimumWidth(200)

        self.widget_left_up = QtWidgets.QWidget()
        self.widget_left_up.setStyleSheet("background-color:lightgray;")
        self.widget_left_layout_up = QtWidgets.QVBoxLayout()
        self.widget_left_up.setLayout(self.widget_left_layout_up)
        self.label_left_up = QtWidgets.QLabel('Drawing selection per date: ')
        self.widget_left_up.layout().addWidget(self.label_left_up)
        
        self.widget_left_down = QtWidgets.QWidget()
        self.widget_left_down.setStyleSheet("background-color:white;")
        self.widget_left_layout_down = QtWidgets.QVBoxLayout()
        self.widget_left_down.setLayout(self.widget_left_layout_down)
        title_left = QtWidgets.QLabel("Drawing selection per year:")
        title_left.setContentsMargins(0, 5, 0, 5)
        self.widget_left_layout_down.addWidget(title_left)
        
        
        splitter_left = QtWidgets.QSplitter(QtCore.Qt.Vertical, self)
        self.layout().addWidget(splitter_left)
        splitter_left.addWidget(self.widget_left_up)
        splitter_left.addWidget(self.widget_left_down)

        splitter_main = QtWidgets.QSplitter(QtCore.Qt.Horizontal, self)
        self.layout().addWidget(splitter_main)
        splitter_main.addWidget(splitter_left)
        splitter_main.addWidget(self.widget_center)
        splitter_main.addWidget(self.widget_right)


class BulkAnalysePage(BulkViewPage):

    def __init__(self, config):
        super(BulkAnalysePage, self).__init__(config)

        self.config = config
        #self.config.set_drawing_analyse()
        
        self.year_list_page = YearListPage(self.config)
        self.month_list_page = MonthListPage()
        self.day_list_page = DayListPage()
        self.date_selection_page = DateSelectionPage()

        self.widget_left_up.setMaximumHeight(self.height()/2.)
        self.widget_left_up.setMaximumWidth(self.width() )
        self.widget_left_down.setMinimumWidth(self.height()/2.)

        #self.widget_center.setMinimumHeight(self.height()*2.)
        
        self.widget_left_layout_up.addWidget(self.date_selection_page)
        self.widget_left_layout_down.addWidget(self.year_list_page)
        
        #self.datetime_min_lst, self.datetime_max_lst = [], []

        self.year_list_page\
            .but_select\
            .clicked\
            .connect(self.show_months_selection)

        self.month_list_page\
            .but_all_day_drawings\
            .clicked\
            .connect(self.show_days_selection)

        self.day_list_page\
            .but_delete\
            .clicked\
            .connect(self.delete_drawing)

        self.day_list_page\
            .but_back\
            .clicked\
            .connect(self.reduce_day_widget)

        self.date_selection_page\
            .but_select\
            .clicked\
            .connect(self.drawing_selection_per_date)

    def reduce_day_widget(self):
        self.widget_right.setMinimumWidth(0)
        self.widget_right.setMaximumWidth(10)
        
    def last_day_of_month(self, year, month):
        # algo found on stackexchange, works pretty well.
        any_day = datetime(year, month, 1)
        next_month = any_day.replace(day=28) + timedelta(days=4)
        last_day_current_month = next_month - timedelta(days=next_month.day)

        return int(last_day_current_month.day)

    def set_drawing_information(self):
        """
        Fonction used to extract the information from the database
        for which datetime is
        in [self.datetime_drawing_min, self.datetime_drawing_max]
        and fill the Drawing object.
        """

        start_set_drawing = time.process_time()
        db = database.database(self.config)

        #print("check day interval",
        #      self.datetime_drawing_min_day,
        #      self.datetime_drawing_max_day)
        
        try:
            tuple_drawings = db\
                .get_all_in_time_interval("drawings",
                                          self.datetime_drawing_min_day,
                                          self.datetime_drawing_max_day)
            lst_drawings_field = db.get_all_fields("drawings")

            tuple_calibrations = db\
                .get_all_in_time_interval("calibrations",
                                          self.datetime_drawing_min_day,
                                          self.datetime_drawing_max_day)
            tuple_groups = db\
                .get_all_in_time_interval("sGroups",
                                          self.datetime_drawing_min_day,
                                          self.datetime_drawing_max_day)
            lst_groups_field = db.get_all_fields("sGroups")
            
        except AttributeError:
            QtWidgets.QMessageBox\
                 .warning(self,
                          "Month selection",
                          "You did not specify a month!")

        lst_drawing = [el for el in tuple_drawings]
        lst_calibrations = [el for el in tuple_calibrations]
        lst_groups = [el for el in tuple_groups]
        drawing_lst = []

        for el in lst_drawing:

            drawing_dict = dict(zip(lst_drawings_field, el))
            
            drawing_tmp = drawing.Drawing(drawing_dict)
            drawing_type = lst_drawing[lst_drawing.index(el)][2]
            tuple_drawing_type = db.get_drawing_information("drawing_type",
                                                            drawing_type)
            drawing_tmp.set_drawing_type(tuple_drawing_type[0])

            for calib in lst_calibrations:
                if drawing_tmp.datetime == calib[1]:
                    drawing_tmp.set_calibration(calib)
                    break

            for group in lst_groups:

                group_dict = dict(zip(lst_groups_field, group))
                
                if drawing_tmp.datetime == group[1]:
                    drawing_tmp.set_group(group_dict)

            drawing_lst.append(drawing_tmp)

        end_set_drawing = time.process_time()
        # print("time for set drawing: ",
        #      end_set_drawing - start_set_drawing)

        drawing_lst.sort(key=lambda x : x.datetime)
        return drawing_lst

    def get_selection_interval(self):
        self.datetime_min, self.datetime_max = [], []
        date_min = self.date_selection_page.start_date.date().toPyDate()
        date_max = self.date_selection_page.end_date.date().toPyDate()
        self.datetime_drawing_min_day = datetime(date_min.year,
                                                   date_min.month,
                                                   date_min.day)
        self.datetime_drawing_max_day = datetime(date_max.year,
                                                   date_max.month,
                                                   date_max.day)

        # to do: check nb drawings<50 -> return true
        # else : warning box and return false
        return True
                                                 

    def get_month_interval(self):
        """
        Return the datemin and datemax for a selected year
        """
        selection = self.year_list_page.table.selectionModel()
        index_elSelectionne = selection.currentIndex()
        try:
            element_selectionne = self.year_list_page\
                                      .table\
                                      .item(index_elSelectionne.row(),
                                            0).text()
            self.selected_year = str(element_selectionne)[0:4]

            self.datetime_drawing_min_month = datetime(int(self.selected_year),
                                                       1, 1, 0, 0)
            self.datetime_drawing_max_month = datetime(int(self.selected_year),
                                                       12, 31, 23, 59)
            return True
        except AttributeError:
            QtWidgets.QMessageBox\
                 .warning(self,
                          "Year selection",
                          "Please select a year.")
            return False

    def get_day(self):
        selection = self.day_list_page.table.selectionModel()
        index_elSelectionne = selection.currentIndex()
        try:
            element_selectionne = self.day_list_page\
                                      .table\
                                      .item(index_elSelectionne.row(),
                                            0).text()
            self.selected_day = str(datetime.strptime(str(element_selectionne),
                                                      '%d %b %H:%M').day)
             
            self.datetime_drawing_min_day = datetime(int(self.selected_year),
                                                     int(self.selected_month),
                                                     int(self.selected_day), 0, 0)
            self.datetime_drawing_max_day = datetime(int(self.selected_year),
                                                     int(self.selected_month),
                                                     int(self.selected_day), 23, 59)
            return True
        
        except AttributeError:
            QtWidgets.QMessageBox\
                 .warning(self,
                          "Day selection",
                          "Please select a day.")
            return False    
        
    def get_day_interval(self):
        """
        Return the datemin and datemax for a selected month
        """
        selection = self.month_list_page.table.selectionModel()
        index_elSelectionne = selection.currentIndex()
        try:
            element_selectionne = self.month_list_page\
                                      .table\
                                      .item(index_elSelectionne.row(),
                                            0).text()
            self.selected_month = str(datetime.strptime(str(element_selectionne),'%b %Y').month)
            
            day_min = str(1) 
            day_max = str(self.last_day_of_month(int(self.selected_year),
                                                 int(self.selected_month)))
            
            self.datetime_drawing_min_day = datetime(int(self.selected_year),
                                                     int(self.selected_month),
                                                     int(day_min), 0, 0)
            self.datetime_drawing_max_day = datetime(int(self.selected_year),
                                                     int(self.selected_month),
                                                     int(day_max), 23, 59)
            return True
        
        except AttributeError:
            QtWidgets.QMessageBox\
                 .warning(self,
                          "Month selection",
                          "Please select a month.")
            return False    

    def get_month_dico(self):
        """
        Return a dictionary with the list of months and 
        nb of calibrated/analyzed drawings
        """
    
        db = database.database(self.config)
        tuple_drawings = db\
            .get_all_in_time_interval("drawings",
                                      self.datetime_drawing_min_month,
                                      self.datetime_drawing_max_month)

        month_lst = set(el[1].month for el in tuple_drawings)
        self.dict_month = {}

        for month_index in month_lst:
            total = [el for el in tuple_drawings if el[1].month==month_index]
            total_count = len(total)
            
            calib = [el for el in tuple_drawings if el[1].month==month_index and
                     el[7]==1]
            frac_calibrated = len(calib) * 100./len(total)
            
            analyzed = [el for el in tuple_drawings if el[1].month==month_index and
                     el[8]==1]
            frac_analyzed = len(analyzed) * 100./len(total)
            
            area_done = [el for el in tuple_drawings if el[1].month==month_index and
                     el[18]==1]
            frac_area_done = len(area_done) * 100./len(total)
            
            month_to_print =  (datetime.strftime(datetime(2000, month_index, 1), '%b') +
                               ' ' +
                               self.selected_year)

            self.dict_month[month_index] = (month_to_print, total_count, frac_calibrated,
                                            frac_analyzed, frac_area_done)

           # OrderedDict remembers the order in which the elements have been inserted
           # and we use the sorted function to insert it by order of time
            self.dict_month = collections.OrderedDict(sorted(self.dict_month.items())) 

    def get_day_dico(self):
      
        db = database.database(self.config)
        tuple_drawings = db\
            .get_all_in_time_interval("drawings",
                                      self.datetime_drawing_min_day,
                                      self.datetime_drawing_max_day)
 
        day_lst = [(el[1].day, el[1].hour, el[1].minute) for el in tuple_drawings]

        #print("day list", day_lst)
        
        self.dict_day = {}
        dict_day_tmp = {}
        
        for day_index in day_lst:

            total = [el for el in tuple_drawings if el[1].day==day_index[0] and
                     el[1].hour==day_index[1] and
                     el[1].minute==day_index[2]]
            total_count = len(total)
                     
            calib = [el for el in tuple_drawings if el[1].day==day_index[0] and
                     el[1].hour==day_index[1] and
                     el[1].minute==day_index[2] and
                     el[7]==1]
            frac_calibrated = len(calib) * 100./len(total)
            
            analyzed = [el for el in tuple_drawings if el[1].day==day_index[0] and
                        el[1].hour==day_index[1] and
                        el[1].minute==day_index[2] and
                        el[8]==1]
            frac_analyzed = len(analyzed) * 100./len(total)
            
            
            area_done = [el for el in tuple_drawings if el[1].day==day_index[0] and
                         el[1].hour==day_index[1] and
                         el[1].minute==day_index[2] and
                         el[18]==1]
            frac_area_done = len(area_done) * 100./len(total)
            day_to_print = ( datetime.strftime(
                datetime(2000,
                         int(self.selected_month),
                         day_index[0],
                         day_index[1],
                         day_index[2]),
                '%d %b %H:%M'))
            
            # trick to separte two same days: add the hour and minutes in decimal:
            dict_day_tmp[
                day_index[0] + day_index[1]/100. + day_index[2]/10000.] = (
                    day_to_print,
                    total_count,
                    frac_calibrated,
                    frac_analyzed,
                    frac_area_done)
            
        # OrderedDict remembers the order in which the elements have been inserted
        # and we use the sorted function to insert it by order of time
        self.dict_day = collections.OrderedDict(sorted(dict_day_tmp.items()))
            
        #print(self.dict_day)
        
    def drawing_selection_per_date(self):
        self.datetime_min, self.datetime_max = [], []
        date_min = self.date_selection_page.start_date.date().toPyDate()
        date_max = self.date_selection_page.end_date.date().toPyDate()
        current_date_min = datetime(date_min.year,
                                    date_min.month,
                                    date_min.day)
        current_date_max = datetime(date_min.year,
                                    date_min.month,
                                    self.last_day_of_month(date_min.year,
                                                           date_min.month))

        self.datetime_min.append(current_date_min)
        self.datetime_max.append(current_date_max)
        nb_month = 0

        while (current_date_max <
               datetime(date_max.year, date_max.month, date_max.day)):
            try:
                current_date_min = datetime(current_date_min.year,
                                            current_date_min.month + 1,
                                            1)
                current_date_max = datetime(current_date_max.year,
                                            current_date_max.month + 1,
                                            self.last_day_of_month(
                                                current_date_max.year,
                                                current_date_max.month + 1))

                self.datetime_min.append(current_date_min)
                self.datetime_max.append(current_date_max)

            except ValueError:
                current_date_min = datetime(current_date_min.year + 1,
                                            1,
                                            1)
                current_date_max = datetime(current_date_max.year + 1,
                                            1,
                                            self.last_day_of_month(
                                                current_date_max.year + 1,
                                                1))

                self.datetime_min.append(current_date_min)
                self.datetime_max.append(current_date_max)

            nb_month += 1

        self.datetime_max[-1] = datetime(self.datetime_max[-1].year,
                                         self.datetime_max[-1].month,
                                         date_max.day)

    def show_months_selection(self):

        year_selected = self.get_month_interval()
        if year_selected:
            self.get_month_dico()
            self.month_list_page.table.setRowCount(len(self.dict_month))
            self.month_list_page.draw_table(self.dict_month, self.config.level)
            self.month_list_page.setMinimumWidth(self.width()/2.)
            self.month_list_page.setMinimumHeight(self.height()/2.)
            self.widget_center_layout.addWidget(self.month_list_page,
                                                0,
                                                QtCore.Qt.AlignCenter)

    def show_days_selection(self):

        month_selected = self.get_day_interval()
        if month_selected :
            self.widget_right.setMinimumWidth(280)
            self.widget_right.setMaximumWidth(580)
            self.get_day_dico()
            self.day_list_page.table.setRowCount(len(self.dict_day))
            self.day_list_page.draw_table(self.dict_day, self.config.level)
            
            self.day_list_page.setMinimumWidth(self.width()/2.)
            self.day_list_page.setMinimumHeight(self.height()/2.)
            self.widget_right_layout.addWidget(self.day_list_page,
                                               0,
                                               QtCore.Qt.AlignCenter)

    def delete_drawing(self):
        """
        This method delete the entry of the selected drawing in the database.
        Note: it does NOT delete the drawing from its directory.
        """
        try:
            selection = self.day_list_page.table.selectionModel()
            index_elSelectionne = selection.currentIndex()
            element_selectionne = self.day_list_page\
                                      .table\
                                      .item(index_elSelectionne.row(),
                                            0).text()
            
            datetime_select = datetime.strptime(str(element_selectionne),
                                                '%d %b %H:%M')
            
            datetime_to_delete = datetime(int(self.selected_year),
                                          datetime_select.month,
                                          datetime_select.day,
                                          datetime_select.hour,
                                          datetime_select.minute)

            response = QtWidgets.QMessageBox.question(
                self,
                'drawing removal'
                '',
                'Do you confirm the removal from the database of the drawing made on the '+
                datetime_to_delete.strftime('%d %b %Y %H:%M') + '?',
                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
            if response == QtWidgets.QMessageBox.Yes:
                
                db = database.database(self.config)
                db.delete_drawing("drawings", datetime_to_delete)
                db.delete_drawing("sGroups", datetime_to_delete)
                db.delete_drawing("calibrations", datetime_to_delete)
                QtWidgets.QMessageBox.warning(self,
                                      'drawing removal',
                                      'Drawing successfully removed.')
                self.reduce_day_widget()
            elif response == QtWidgets.QMessageBox.No:
                pass
            

        except AttributeError:
            QtWidgets.QMessageBox\
                 .warning(self,
                          "Day selection",
                          "Please select a day.")
