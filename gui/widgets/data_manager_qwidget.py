# IMPORTS
import os
import re

# IMPORT QT CORE
from qt_core import *

# IMPORT CUSTOM UI
from gui.pages.ui_data_page import UI_DataManager

# IMPORT CUSTOM MODULES
from backend.data_management.functions import xls_reader
from backend.data_management.data_management import SQlStationData

# IMPORT CUSTOM FUNCTIONS
from backend.misc.functions import find_unit

# Data Manager Page Class
class DataManager(QWidget):

    def __init__(self):
        super().__init__()

        # SETUP MAIN UI 
        self.ui = UI_DataManager()
        self.ui.setup_ui(self)
        self.ui.setup_stylesheets()
        
        # PROPERTIES
        self.archives = {} # Opened station archives
        self.selected_parameters = {} # selected parameters for each station
        self.browse_folder = os.path.expanduser("~") # user home directory

        # SIGNALS AND SLOTS
        self.ui.xls_btn.clicked.connect(self.browse_xls_files)
        self.ui.search_bar.editingFinished.connect(self.search_station)
        self.ui.station_manager_list.active_row.valueChanged.connect(self.update_parameter_viewer)
        # self.ui.parameter_list.stateChanged.connect(self.save_parameter_selection)

    def search_station(self):
        # getting text and setting properties
        text = self.ui.search_bar.text()
        text = text.rstrip().strip()
        chars = len(text)

        # tests
        station_list = self.ui.monitoring_station_list
        rows = station_list.count()

        # reset filter
        for row in range(rows):
            station_list.item(row).setHidden(False)
        
        if chars > 0:
            keywords = re.split("\s+", text.lower())
            for row in range(rows):
                widget = station_list.item(row)
                item = station_list.itemWidget(widget)
                name = re.split('\s+', item.station_name_label.text().lower())
                enterprise = re.split('\s+', item.station_enterprise_label.text().lower())
                condition = False
                for kw in keywords:
                    condition1 = condition or any(map(lambda element: kw in element, name))
                    condition2 = any(map(lambda element: kw in element, enterprise))
                    condition = condition1 or condition2

                widget.setHidden(not condition)

    def save_parameter_selection(self, args):
        state, row = args
        signature = self.ui.parameter_list.get_signature()
        if signature in self.selected_parameters:
            self.selected_parameters[signature][row] = state

        ms = self.ui.monitoring_station_list
        active_row = ms.active_row.value()
        active_parameters = sum(self.selected_parameters[signature])
        ms.itemWidget(ms.item(active_row)).marked.updateCount(active_parameters)

    def update_parameter_viewer(self):
        # Save selection of parameters before deleting
        self.ui.parameter_list.reset_settings()

        # geting new selected row
        monitoring_list  = self.ui.monitoring_station_list
        active_row = monitoring_list.active_row.value()

        # tests
        if active_row >= 0:
            # get station object
            station = monitoring_list.itemWidget(monitoring_list.item(active_row)).station_object
            if station.metadata['source'] == 'xls':
                var_list = station.parameters.keys()
            else:
                var_list = station.parameters
            
            # adding to paramter view widget
            i = 0
            for k in var_list:
                unit = find_unit(k)
                name = k[:k.find(unit)]
                self.ui.parameter_list.add_item(
                    name = name,
                    theme = station.parameter_theme[k],
                    unit = unit,
                    selected = self.selected_parameters[station.metadata['signature']][i]
                )
                i += 1

            self.ui.parameter_list.set_signature(station.metadata['signature'])

    def browse_xls_files(self):
        file_paths, x = QFileDialog.getOpenFileNames(
            self,
            "Selecione um arquivo",
            filter = "Excel files (*.xls)",
            dir= self.browse_folder
        )

        # file_path is a list with a path to each file.
        if len(file_paths) > 0:
            self.browse_folder = os.path.dirname(file_paths[0])
            files = {}
            for path in file_paths:
                try:
                    # read files and extract information
                    files.update(xls_reader(path))

                except:
                    continue

            for k, v in files.items():
                if k not in self.archives:
                    # add station into archives
                    self.archives[k] = v

                    # add parameters list
                    self.selected_parameters[k] = [0] * len(v.parameters)

                    # add station into list frame
                    self.ui.station_manager_list.add_station_item(v)
    
    def browse_sql(self, server):
        for i, name in enumerate(server.station_names):
            _object = SQlStationData(
                name = name,
                enterprise = server.station_enterprises[i],
                dates = server.dates[name],
                parameters = server.table_vars[name],
                parameters_cols = server.table_vars_columns[name]
            )
            
            k = _object.metadata['signature']
            self.archives[k] = _object

            # add parameters list
            self.selected_parameters[k] = [0] * len(_object.parameters)

            # add station into lsit frame
            self.ui.station_manager_list.add_station_item(_object)

    def paintEvent(self, event: QPaintEvent) -> None:
        # super().paintEvent(event)

        opt = QStyleOption()
        opt.initFrom(self)
        p = QPainter(self)
        self.style().drawPrimitive(QStyle.PE_Widget, opt, p, self)

