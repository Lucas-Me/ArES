# IMPORT QT_CORE
from qt_core import *

# IMPORT CUSTOM WIDGETS
from gui.widgets.station_list_view import PyStationListView
from gui.widgets.py_push_button import PyPushButton
from gui.widgets.parameter_list_widget import ParameterSelectionWidget
from gui.widgets.py_date_select import PyDoubleDateEdit

# Data Manager Page UI Class
class UI_DataManager(object):
    
    def setup_ui(self, parent):
        if not parent.objectName():
            parent.setObjectName(u'data_page')

        # Properties
        self.font = 'Microsoft New Tai Lue'
        self.border_color = '#b7c4c8'
        self.menu_color = '#4969b2'
        self.background_color = '#f5f5f5'
        self.inner_frame_color = "#ffffff"
        self.btn_color = '#fb8500'
        self.btn_border_color = '#ffb703f'
        self.frame_height = 500

        # MAIN LAYOUT
        self.main_layout = QVBoxLayout(parent)

        # TOP LAYOUT
        self.top_layout = QHBoxLayout()

        # Top Horizontal Spacer
        self.top_spacer = QSpacerItem(20, 40, QSizePolicy.Expanding, QSizePolicy.Minimum)

        # Top Date Edit
        self.date_edit = PyDoubleDateEdit(parent = parent)
        self.date_edit.setMinimumHeight(30)
        self.date_edit.setMaximumHeight(30)
        self.date_edit.setMinimumWidth(300)
        self.date_edit.setMaximumWidth(300)

        # Insert objects into top layout
        self.top_layout.addItem(self.top_spacer)
        self.top_layout.addWidget(self.date_edit)
        self.top_layout.addItem(self.top_spacer)

        # LABELS ON TOP OF TABLES
        self.table_station_label = QLabel("Estações de monitoramento")
        self.table_station_label.setFixedWidth(400)
        self.table_station_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.table_station_label.setStyleSheet('''
            font : bold 15pt "{self.font}";
            padding-left : 10px;
        ''')
        #
        self.parameter_list_label = QLabel("Parâmetros monitorados")
        self.parameter_list_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.parameter_list_label.setStyleSheet('''
            font : bold 15pt "{self.font}";
        ''')

        # Labels Layout
        self.title_label_layout = QHBoxLayout()
        self.title_label_layout.addWidget(self.table_station_label)
        self.title_label_layout.addWidget(self.parameter_list_label)

        # MAIN TABLE LIST DESIGN
        # /////////////////////////////////////////////////////////////////////
        self.table_item_frame = QFrame()
        self.table_item_frame.setMinimumHeight(self.frame_height)

        # Frame styling
        self.table_item_frame.setStyleSheet(f'''
            background-color: {self.inner_frame_color};
            border-style: solid;
            border-width: 2px;
            border-color: {self.border_color};
            ''')

        # MAIN TABLE LAYOUT
        self.table_item_layout = QHBoxLayout(self.table_item_frame)
        self.table_item_layout.setContentsMargins(0, 0, 0, 0)
        self.table_item_layout.setSpacing(0)

        # MONITORING STATION LIST 
        self.monitoring_station_list = PyStationListView(parent = parent)
        self.monitoring_station_list.setMinimumHeight(self.frame_height - 10)
        self.monitoring_station_list.setMinimumWidth(400)
        self.monitoring_station_list.setMaximumWidth(400)
        
        # PARAMETER LIST
        self.parameter_list = ParameterSelectionWidget()
        self.parameter_list.setMinimumHeight(self.frame_height - 10)
        self.parameter_list.setMinimumWidth(600)

        # ADD LISTS TO MAIN TABLE LAYOUT
        self.table_item_layout.addWidget(self.monitoring_station_list)
        self.table_item_layout.addWidget(self.parameter_list)
               
        # BOTTOM WIDGETS
        # //////////////////////////////////////////////////////////////////////
        self.bottom_spacer = QSpacerItem(20, 30, QSizePolicy.Minimum, QSizePolicy.Minimum)

        # BUTTON LAYOUT
        self.bottom_btn_layout = QHBoxLayout()

        # CREATING IMPORT XLS BUTTON
        self.import_xls_btn = PyPushButton(
            text = "Importar\nXLS",
            icon_path = "icon_xls_file.svg",
            icon_color = '#398e3d',
            height = 90,
            width = 175,
            icon_width = 80,
            setup = False,
        )
        self.import_xls_btn.setStyleSheet(
            self.import_xls_btn.styleSheet() + f'''
                QPushButton {{
                    color : {self.menu_color};
                    background-color: {self.inner_frame_color};
                    font: 900 14pt "Microsoft New Tai Lue";
                    text-align: middle;
                    vertical-align: middle;
                    border: solid;
                    border-width: 4px;
                    padding-left: 65px;
                    border-radius: 0px;
                    border-color: {self.border_color};
                }}
            '''
        )


        # CREATING IMPORT DATABASE BUTTON
        self.import_sql_btn = PyPushButton(
            text = "Importar\nSQL",
            icon_path = "icon_sql.svg",
            icon_color = '#000000',
            height = 90,
            width = 175,
            icon_width = 80,
            setup = False,
        )
        self.import_sql_btn.setStyleSheet(
            self.import_xls_btn.styleSheet() + f'''
                QPushButton {{
                    color : {self.menu_color};
                    background-color: {self.inner_frame_color};
                    font: 900 14pt "Microsoft New Tai Lue";
                    text-align: middle;
                    vertical-align: middle;
                    border: solid;
                    border-width: 4px;
                    padding-left: 65px;
                    border-radius: 0px;
                    border-color: {self.border_color};
                }}
            '''
        )

        # CREATNG SPACER
        self.spacer_import = QSpacerItem(830, 60, QSizePolicy.Expanding, QSizePolicy.Minimum)

        # ADDING BUTTONS TO LAYOUT
        self.bottom_btn_layout.addWidget(self.import_xls_btn)
        self.bottom_btn_layout.addWidget(self.import_sql_btn)
        self.bottom_btn_layout.addItem(self.spacer_import)

        # ADD TO MAIN LAYOUT
        self.main_layout.addLayout(self.top_layout)
        self.main_layout.addLayout(self.title_label_layout)
        self.main_layout.addWidget(self.table_item_frame)
        self.main_layout.addItem(self.bottom_spacer) 
        self.main_layout.addLayout(self.bottom_btn_layout)



        

