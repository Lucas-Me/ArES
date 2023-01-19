# IMPORT QT_CORE
from qt_core import *

# IMPORT CUSTOM WIDGETS
from gui.widgets.station_list_view import PyStationListView
from gui.widgets.py_push_button import ClassicButton
from gui.widgets.parameter_list_widget import ParameterSelectionWidget
from gui.widgets.py_date_select import PyDoubleDateEdit

# Data Manager Page UI Class
class UI_DataManager(object):
    
    def setup_ui(self, parent):
        if not parent.objectName():
            parent.setObjectName(u'data_page')

        # Properties
        self.font = 'Open Sans'
        self.border_color = '#b7c4c8'
        self.menu_color = '#4969b2'
        self.background_color = '#f5f5f5'
        self.inner_frame_color = "#ffffff"
        self.btn_color = '#fb8500'
        self.btn_border_color = '#ffb703'
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
        self.table_station_label.setStyleSheet(f'''
            font : bold 15pt "{self.font}";
            padding-left : 10px;
        ''')
        #
        self.parameter_list_label = QLabel("Parâmetros monitorados")
        self.parameter_list_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.parameter_list_label.setStyleSheet(f'''
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

        # VERICAL STATION LAYOUT
        self.monitoring_station_layout = QVBoxLayout()
        self.monitoring_station_layout.setContentsMargins(0, 0, 0, 0)
        self.monitoring_station_layout.setSpacing(0)

        # SEARCH BAR
        self.search_bar = QLineEdit()
        self.search_bar.setFixedWidth(400)
        self.search_bar.setFixedHeight(50)
        self.search_bar.setStyleSheet(f'''
            border: none;
            border-right: 2px solid;
            border-bottom: 2px solid;
            border-color: #b7c4c8;
            color: #506369;
            font: 700 12pt {self.font};
        ''')
        self.search_bar.setClearButtonEnabled(True)
        image = QPixmap("./gui/images/icons/search.svg")
        image.scaled(QSize(50, 50), Qt.AspectRatioMode.KeepAspectRatio)
        self.search_bar.addAction(image, QLineEdit.LeadingPosition)
        self.search_bar.setPlaceholderText("Buscar...")

        # MONITORING STATION LIST 
        self.monitoring_station_list = PyStationListView(parent = parent)
        self.monitoring_station_list.setMinimumHeight(self.frame_height)
        self.monitoring_station_list.setMinimumWidth(400)
        self.monitoring_station_list.setMaximumWidth(400)
        
        # PARAMETER LIST
        self.parameter_list = ParameterSelectionWidget()
        self.parameter_list.setMinimumHeight(self.frame_height - 10)
        self.parameter_list.setMinimumWidth(600)

        # ADD LISTS TO MAIN TABLE LAYOUT
        self.monitoring_station_layout.addWidget(self.search_bar)
        self.monitoring_station_layout.addWidget(self.monitoring_station_list)
        self.table_item_layout.addLayout(self.monitoring_station_layout)
        self.table_item_layout.addWidget(self.parameter_list)
               
        # BOTTOM WIDGETS
        # //////////////////////////////////////////////////////////////////////
        self.bottom_spacer = QSpacerItem(20, 30, QSizePolicy.Minimum, QSizePolicy.Minimum)

        # BUTTON LAYOUT
        self.bottom_btn_layout = QHBoxLayout()

        # BUTTON STYLESHEET
        self.button_style = f'''
                QPushButton {{
                    color : {self.menu_color};
                    background-color: {self.inner_frame_color};
                    font: 700 12pt {self.font};
                    text-align: middle;
                    vertical-align: middle;
                    border: solid;
                    border-width: 2px;
                    padding-left: 65px;
                    border-radius: 0px;
                    border-color: {self.border_color};
                    }}
                QPushButton:hover {{
                    border-color: #3f40f0;
                    }}
                '''

        # CREATING IMPORT XLS BUTTON
        self.import_xls_btn = ClassicButton(
            text = "Importar\nXLS",
            icon_path = "icon_xls_file.svg",
            height = 90,
            width = 175,
            icon_width = 80,
            icon_allign = 'left',
            icon_color="#398e3d"
        )
        self.import_xls_btn.setStyleSheet(
            self.import_xls_btn.styleSheet() + self.button_style
        )

        # CREATING IMPORT DATABASE BUTTON
        self.import_sql_btn = ClassicButton(
            text = "Importar\nSQL",
            icon_path = "icon_sql.svg",
            height = 90,
            width = 175,
            icon_width = 80,
            icon_color = '#232234'
        )
        self.import_sql_btn.setStyleSheet(
            self.import_sql_btn.styleSheet() + self.button_style
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



        

