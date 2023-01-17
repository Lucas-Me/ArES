# IMPORTS
import os
import re

# IMPORT QT CORE
from qt_core import *

# IMPORT CUSTOM UI
from gui.pages.ui_data_page import UI_DataManager

# IMPORT CUSTOM MODULES
from backend.data_management.functions import xls_reader

# Data Manager Page Class
class DataManager(QWidget):

    def __init__(self):
        super().__init__()

        # SETUP MAIN UI 
        self.ui = UI_DataManager()
        self.ui.setup_ui(self)
        
        # PROPERTIES
        self.archives = {} # Opened station archives
        self.selected_parameters = {} # selected parameters for each station
        self.browse_folder = os.path.expanduser("~") # user home directory

        # SIGNALS AND SLOTS
        self.ui.import_xls_btn.clicked.connect(self.browse_xls_files)
        self.ui.monitoring_station_list.active_row.valueChanged.connect(self.update_parameter_viewer)

    def save_parameter_selection(self, selection, signature):
        if signature in self.selected_parameters:
            self.selected_parameters[signature] = selection

    def update_parameter_viewer(self):
        # Save selection of parameters before deleting
        old_results =  self.ui.parameter_list.reset_settings()
        self.save_parameter_selection(*old_results)

        # geting new selected row
        monitoring_list  = self.ui.monitoring_station_list
        active_row = monitoring_list.active_row.value()

        # tests
        if active_row >= 0:
            station = monitoring_list.itemWidget(monitoring_list.item(active_row)).station_object
            i = 0
            for k in station.parameters.keys():
                splitted = re.split('[][]', k)
                self.ui.parameter_list.add_item(
                    name = splitted[0],
                    theme = station.parameter_theme[k],
                    unit = splitted[1],
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
                    self.ui.monitoring_station_list.add_station_item(v)
        


