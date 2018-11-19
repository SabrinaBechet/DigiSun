# !/usr/bin/env python
# -*-coding:utf-8-*-
from PyQt5 import QtGui, QtCore, QtWidgets
from datetime import datetime, timedelta
import database, drawing


class ListPage(QtWidgets.QWidget):
    """
    Mother class that shows a list (of years or months) 
    with the percentage of drawing calibrated/analysed/with area done
    """
    def __init__(self):
        super(ListPage, self).__init__()
        self.table = QtWidgets.QTableWidget()
        self.table.setColumnCount(5)

    def draw_table(self, list_drawings):
        """
        Method that draws the table with the list of drawings and 
        the fraction of calibrated/analysed/area done.
        """
        self.table.horizontalHeader().setDefaultSectionSize(150)
        self.table.setHorizontalHeaderLabels(["date", " # total",
                                              "calibrated", "analysed"])
        for i in range(len(list_drawings)):
            date_drawing = QtWidgets.QTableWidgetItem(str(list_drawings[i]))
            #date_drawing.setFlags(QtCore.Qt.ItemIsSelectable and
            #                      QtCore.Qt.ItemIsEnabled)
            
            tot_number_drawing = QtWidgets.QTableWidgetItem(str(self.lst_tot[i]))
            #tot_number_drawing.setFlags(QtCore.Qt.ItemIsSelectable and
            #                            QtCore.Qt.ItemIsEnabled)

            self.table.setItem(i, 0, date_drawing)
            self.table.setItem(i, 1, tot_number_drawing)
            
            progressBar_calib = QtWidgets.QProgressBar()
            progressBar_analysed = QtWidgets.QProgressBar()
            progressBar_area = QtWidgets.QProgressBar()
            
            if self.lst_tot[i] > 0:
                frac_calibrated = self.lst_calib[i] * 100. / self.lst_tot[i]
                progressBar_calib.setValue(frac_calibrated)
                frac_analysed = self.lst_analysed[i] * 100. / self.lst_tot[i]
                progressBar_analysed.setValue(frac_analysed)
                frac_area =  100 - (self.lst_area_not_done[i] * 100. / self.lst_tot[i])
                progressBar_area.setValue(frac_area)
                #print(frac_area, self.lst_area_not_done[i] * 100. / self.lst_tot[i])
            else:
                progressBar_calib.setValue(100)
                progressBar_analysed.setValue(100)

            self.table.setCellWidget(i, 2, progressBar_calib)
            self.table.setCellWidget(i, 3, progressBar_analysed)
            self.table.setCellWidget(i, 4, progressBar_area)

    def get_lst_from_database(self, datetime_min, datetime_max):
        """
        For a given list of years (or months), a list of datetime_min and max, 
        Connect to the database and extract:
        - the total number of drawings for the selected year/month
        - the number of calibrated drawings for the selected year/month
        - the number of analyzed drawings for the selected year/month
        - the number of area done for the selected year/month
        """
        db = database.database()
        self.lst_tot = []
        self.lst_calib = []
        self.lst_analysed = []
        self.lst_area_not_done = []
        
        for i in range(len(datetime_min)):
            nb_drawing_surface_null = 0
            nb_drawing_not_analysed = 0
            self.lst_tot.append(
                db.count_year("drawings",
                              "DateTime",
                              datetime_min[i],
                              datetime_max[i]) )          
            self.lst_calib.append(
                db.count_field_in_time_interval("drawings",
                                                "DateTime",
                                                datetime_min[i],
                                                datetime_max[i],
                                                "Calibrated",
                                                str(1)) )
            self.lst_analysed.append(
                db.count_field_in_time_interval("drawings",
                                                "DateTime",
                                                datetime_min[i],
                                                datetime_max[i],
                                                "Analyzed",
                                                str(1)) )

            nb_drawing_not_analysed = db.count_field_in_time_interval(
                "drawings",
                "DateTime",
                datetime_min[i],
                datetime_max[i],
                "Analyzed",
                str(0))
            
            nb_drawing_surface_null = db.count_field_in_time_interval_area(
                "groups",
                "DateTime",
                datetime_min[i],
                datetime_max[i],
                "Surface",
                None)
            
            self.lst_area_not_done.append(nb_drawing_not_analysed +
                                          nb_drawing_surface_null)


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
        self.but_select = QtWidgets.QPushButton("select", self)
        month_list_layout = QtWidgets.QVBoxLayout()
        month_list_layout.addWidget(self.table)
        month_list_layout.addWidget(self.but_select)
        self.setLayout(month_list_layout)
              
    def set_date(self, datetime_min, datetime_max):
        """ set the dates to show in the table (rows)"""
        self.datetime_min = datetime_min
        self.datetime_max = datetime_max
        
        self.get_lst_from_database([x.strftime("%Y-%m-%d") for x in datetime_min],
                                   [x.strftime("%Y-%m-%d") for x in datetime_max])
        date_list = [datetime_min[i].strftime("%d") + " - " +
                     datetime_max[i].strftime("%d") + "   " +
                     datetime_min[i].strftime("%b %Y")
                     for i in range(len(datetime_min))]
        
        self.table.setRowCount(len(datetime_min))
        self.draw_table(date_list)


class YearListPage(ListPage):
    """
    Page that shows the list of years present in the database.
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
        super(YearListPage, self).__init__()
        self.lst_year = []
        self.set_year()
        self.but_select = QtWidgets.QPushButton("select", self)
        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addWidget(self.table)
        self.layout.addWidget(self.but_select)
        self.setLayout(self.layout)
        
    def set_year(self):
        """ Show the list of years in the table (rows)"""
        self.get_lst_year()
        datetime_min, datetime_max = [], []
        for el in self.lst_year:
            datetime_min.append(str(el) + "-01-01")
            datetime_max.append(str(el) + "-12-31")
        self.get_lst_from_database(datetime_min,
                                   datetime_max)
        self.table.setRowCount(len(self.lst_year))
        self.draw_table(self.lst_year)
        
    def get_lst_year(self):
        """ Get the list of years from the database"""
        db = database.database()
        list_years_from_db = db.get_year_interval("drawings", "DateTime")
        set_year = set()
        for el in list_years_from_db:
            set_year.add(el[0].year)
        # to do: ordonner la liste
        self.lst_year = list(set_year)


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
    """
    def __init__(self):
        super(BulkViewPage, self).__init__()
        self.setLayout(QtWidgets.QVBoxLayout())
        
        self.widget_right = QtWidgets.QWidget()
        print("check size", self.width(), self.height())
        #self.widget_right.setMinimumWidth(self.width()/2.)#1300)
        self.widget_right.setStyleSheet("background-color:lightgray;")
        self.widget_right_layout = QtWidgets.QVBoxLayout()
        #self.widget_right_layout.setContentsMargins(0, 0, 0, 0) # this line
        #self.widget_right_layout.setSpacing(0)
        #self.widget_right_layout.setAlignment(QtCore.Qt.AlignCenter)
        self.widget_right.setLayout(self.widget_right_layout)
     
        self.widget_left_up = QtWidgets.QWidget()
        self.widget_left_up.setStyleSheet("background-color:lightgray;")
        #self.widget_left_up.setMinimumHeight(self.height()/4.) #200)
        self.widget_left_layout_up = QtWidgets.QVBoxLayout()
        #self.widget_left_layout_up.setContentsMargins(0, 0, 0, 0) # this line
        #self.widget_left_layout_up.setSpacing(0)
        self.widget_left_up.setLayout(self.widget_left_layout_up)
        my_font = QtGui.QFont("Comic Sans MS", 15)
        self.label_left_up = QtWidgets.QLabel('Drawing selection per date')
        self.label_left_up.setFont(my_font)
        #self.label_left_up.setAlignment(QtCore.Qt.AlignCenter)
        #label_left.setStyleSheet("background-color:lightgray;")
        self.label_left_up.setContentsMargins(0, 0, 0, 0)
        #self.label_left_up.setMaximumWidth(300)
        self.widget_left_up.layout().addWidget(self.label_left_up)

        self.widget_left_down = QtWidgets.QWidget()
        self.widget_left_down.setStyleSheet("background-color:white;")
        #self.widget_left_down.setMinimumHeight(self.height())
        #self.widget_left_down.setMinimumWidth(200)
        self.widget_left_layout_down = QtWidgets.QVBoxLayout()
        #self.widget_left_layout_down.setContentsMargins(0, 0, 0, 0) # this line
        #self.widget_left_layout_down.setSpacing(0)
        self.widget_left_down.setLayout(self.widget_left_layout_down)
        self.label_left_down = QtWidgets.QLabel('Drawing selection per year')
        self.label_left_down.setFont(my_font)
        #self.label_left_down.setAlignment(QtCore.Qt.AlignCenter)
        #label_left.setStyleSheet("background-color:lightgray;")
        self.label_left_down.setContentsMargins(0, 0, 0, 0)
        #self.label_left_down.setMaximumWidth(300)
        self.widget_left_down.layout().addWidget(self.label_left_down)

        splitter_left = QtWidgets.QSplitter(QtCore.Qt.Vertical, self)
        self.layout().addWidget(splitter_left)
        splitter_left.addWidget(self.widget_left_up)
        splitter_left.addWidget(self.widget_left_down)

        splitter_main = QtWidgets.QSplitter(QtCore.Qt.Horizontal, self)
        self.layout().addWidget(splitter_main)
        splitter_main.addWidget(splitter_left)
        splitter_main.addWidget(self.widget_right)
       
class BulkAnalysePage(BulkViewPage):
    """
    This is the Bulk analyse page with three sections:
    - left_up : selection per date
    - left_down : selection per year
    - right :  selection per month for a given date/year
    """
    def __init__(self):
        super( BulkAnalysePage, self).__init__()

        #self.operator = operator
        
        self.year_list_page = YearListPage()
        self.month_list_page = MonthListPage()
        self.date_selection_page = DateSelectionPage()

        self.widget_left_up.setMaximumHeight(self.height()/2.) #200)
        self.widget_left_down.setMinimumWidth(self.height()/2.)
        
        #self.drawing_analyse = drawing_analyse.DrawingAnalysePage(self.operator)
        
        self.widget_left_layout_up.addWidget(self.date_selection_page)
        self.widget_left_layout_down.addWidget(self.year_list_page)

        self.datetime_min, self.datetime_max = [], []
        
        self.year_list_page\
            .but_select\
            .clicked\
            .connect(self.drawing_selection_per_year)
        self.year_list_page\
            .but_select\
            .clicked\
            .connect(self.clic_selection)

        self.date_selection_page\
            .but_select\
            .clicked\
            .connect(self.drawing_selection_per_date)
        self.date_selection_page\
            .but_select\
            .clicked\
            .connect(self.clic_selection)
     
    def last_day_of_month(self, year, month):
        # algo found on stackexchange, works pretty well.
        any_day = datetime(year, month, 1)
        next_month = any_day.replace(day=28) + timedelta(days=4)
        last_day_current_month = next_month - timedelta(days=next_month.day)
        
        return int(last_day_current_month.day)

    def drawing_selection_per_month(self):
        self.datetime_min, self.datetime_max = [], []
        selection = self.month_list_page.table.selectionModel()
        index_elSelectionne = selection.currentIndex()
        element_selectionne = self.month_list_page.table.item(index_elSelectionne.row(),
                                                             0).text()
        year_selected = str(element_selectionne[14:18])
        month_selected = str(element_selectionne[8:13])
        day_min = str(element_selectionne[0:3])
        day_max = str(element_selectionne[5:8])

        #print(year_selected + ' ' + month_selected + ' ' + day_min)
        #print(year_selected + ' ' + month_selected + ' ' + day_max)
        
        self.datetime_drawing_min = datetime.strptime(year_selected + ' ' +
                                                      month_selected + ' ' +
                                                      day_min + "00:00",
                                                      '%Y %b %d %H:%M')
        
        self.datetime_drawing_max = datetime.strptime(year_selected + ' ' +
                                                      month_selected + ' ' +
                                                      day_max + "23:59",
                                                      '%Y %b %d %H:%M')
        
        #print( self.datetime_drawing_min, self.datetime_drawing_max)

    def set_drawing_information(self):
        """
        Get the information of drawings for which datetime is 
        in [self.datetime_drawing_min, self.datetime_drawing_max].
        return the list of drawing object.
        """
        db = database.database()
        
        lst_path = db.get_field_time_interval("drawings", "path",
                                self.datetime_drawing_min,
                                self.datetime_drawing_max)
        lst_datetime = db.get_field_time_interval("drawings", "DateTime",
                                                  self.datetime_drawing_min,
                                                  self.datetime_drawing_max)
        
        
        drawing_lst = []
        
        for date in lst_datetime:
            #print("***********", date)
            drawing_tmp = drawing.Drawing()
            drawing_tmp.fill_from_database(date)
            drawing_lst.append(drawing_tmp)
            #print(drawing_tmp.datetime, drawing_tmp.observer)

        return drawing_lst
        
    def drawing_selection_per_year(self):
        self.datetime_min, self.datetime_max = [], []
        selection = self.year_list_page.table.selectionModel()
        index_elSelectionne = selection.currentIndex()
        element_selectionne = self.year_list_page\
                                  .table\
                                  .item(index_elSelectionne.row(),
                                        0).text()
        selected_year = str(element_selectionne)[0:4]
        self.lst_month = list(range(1,13))
          
        for el in self.lst_month:
            self.datetime_min.append(
                datetime(int(selected_year),
                         el,
                         1 ) )
            self.datetime_max.append(
                datetime(int(selected_year),
                         el,
                         self.last_day_of_month(int(selected_year),
                                                el) ) )

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
                
            nb_month+=1
            
        self.datetime_max[-1] = datetime(self.datetime_max[-1].year,
                                         self.datetime_max[-1].month,
                                         date_max.day)
               
    def clic_selection(self):
              
        self.month_list_page.set_date(self.datetime_min, self.datetime_max)
        self.month_list_page.setMinimumWidth(self.width()/2.)#800)
        self.month_list_page.setMinimumHeight(self.height()/2.)#700)
        self.widget_right_layout.addWidget(self.month_list_page,
                                           0,
                                           QtCore.Qt.AlignCenter)
        
