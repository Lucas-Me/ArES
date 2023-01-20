# IMPORT QT_CORE
from qt_core import *

# IMPORT CUSTOM WIDGETS
from gui.widgets.station_list_view import PyStationListView
from gui.widgets.py_push_button import ClassicButton
from gui.widgets.parameter_list_widget import ParameterSelectionWidget
from gui.widgets.py_date_select import PyDoubleDateEdit

# IMPORT CUSTOM MODULES
from backend.misc.functions import get_icon

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
        # station label
        self.table_station_label = QLabel("Estações de monitoramento")
        self.table_station_label.setFixedWidth(400)
        self.table_station_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        
        # parmeter label
        self.parameter_list_label = QLabel("Parâmetros monitorados")
        self.parameter_list_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        # Labels Layout
        self.title_label_layout = QHBoxLayout()
        self.title_label_layout.addWidget(self.table_station_label)
        self.title_label_layout.addWidget(self.parameter_list_label)

        # MAIN TABLE LIST DESIGN
        # /////////////////////////////////////////////////////////////////////
        self.table_item_frame = QFrame()
        self.table_item_frame.setMinimumHeight(self.frame_height)

        # MAIN TABLE LAYOUT
        self.table_item_layout = QHBoxLayout(self.table_item_frame)
        self.table_item_layout.setContentsMargins(0, 0, 0, 0)
        self.table_item_layout.setSpacing(0)

        # STATION LAYOUT
        self.monitoring_station_layout = QGridLayout()
        self.monitoring_station_layout.setContentsMargins(0, 0, 0, 0)
        self.monitoring_station_layout.setSpacing(0)
        dimh, dimw = (self.frame_height, 400)

        # SEARCH BAR
        self.search_bar = QLineEdit()
        self.search_bar.setFixedWidth(400)
        self.search_bar.setFixedHeight(50)
        self.search_bar.setClearButtonEnabled(True)
        image = QPixmap(get_icon('search.svg', 'gui/images/icons'))
        image.scaled(QSize(50, 50), Qt.AspectRatioMode.KeepAspectRatio)
        self.search_bar.addAction(image, QLineEdit.LeadingPosition)
        self.search_bar.setPlaceholderText("Buscar...")

        # LefT BAR MONITORING STATION
        left_width = 30
        btn_height = 30
        self.clear_items_button = QPushButton()
        self.clear_selection_button = QPushButton()
        self.clear_items_button.setFixedSize(left_width, btn_height)
        self.clear_selection_button.setFixedSize(left_width, btn_height)
        #
        self.scroll_bar_stations = QScrollBar(Qt.Orientation.Vertical)
        self.scroll_bar_stations.setFixedWidth(left_width)
        self.scroll_bar_stations.setMinimumHeight(
            dimh - self.search_bar.height() - self.clear_items_button.height() * 2
        )

        # MONITORING STATION LIST 
        self.monitoring_station_list = PyStationListView(parent = parent, scrollbar = self.scroll_bar_stations)
        self.monitoring_station_list.setMinimumHeight(dimh - self.search_bar.height())
        self.monitoring_station_list.setMinimumWidth(dimw - self.scroll_bar_stations.width())
        self.monitoring_station_list.setMaximumWidth(dimw - self.scroll_bar_stations.width())
        self.monitoring_station_list.updateItemDimensions(
            dimw - self.scroll_bar_stations.width(), 60
        )

        # PARAMETER LIST
        self.parameter_list = ParameterSelectionWidget()
        self.parameter_list.setMinimumHeight(self.frame_height - 10)
        self.parameter_list.setMinimumWidth(600)

        # ADD LISTS TO MAIN TABLE LAYOUT
        self.monitoring_station_layout.addWidget(self.search_bar, 0, 0, 1, 2)
        self.monitoring_station_layout.addWidget(self.clear_items_button, 1, 0, 1, 1)
        self.monitoring_station_layout.addWidget(self.clear_selection_button, 2, 0, 1, 1)
        self.monitoring_station_layout.addWidget(self.scroll_bar_stations, 3, 0, 1, 1)
        self.monitoring_station_layout.addWidget(self.monitoring_station_list, 1, 1, 3, 1)
        self.table_item_layout.addLayout(self.monitoring_station_layout)
        self.table_item_layout.addWidget(self.parameter_list)
               
        # BOTTOM WIDGETS
        # //////////////////////////////////////////////////////////////////////
        self.bottom_spacer = QSpacerItem(20, 30, QSizePolicy.Minimum, QSizePolicy.Minimum)

        # BUTTON LAYOUT
        self.bottom_btn_layout = QHBoxLayout()

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
        
        # CREATING IMPORT DATABASE BUTTON
        self.import_sql_btn = ClassicButton(
            text = "Importar\nSQL",
            icon_path = "icon_sql.svg",
            height = 90,
            width = 175,
            icon_width = 80,
            icon_color = '#232234'
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

        self.setup_stylesheets()

    def setup_stylesheets(self):

        # BUTTONS STYLE SHEET
        # //////////////////////////////////////////////////////////////
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
        
        # XLS and SQL buttons
        self.import_xls_btn.setStyleSheet(
            self.import_xls_btn.styleSheet() + self.button_style
        )
        self.import_sql_btn.setStyleSheet(
            self.import_sql_btn.styleSheet() + self.button_style
        )

        # LEFT BUTTONS ON STATION LIST
        pixmap_clear_btn = QPixmap(get_icon('clear_button.svg', 'gui/images/icons'))
        icon_clear_btn = QIcon(pixmap_clear_btn)
        self.clear_items_button.setIcon(icon_clear_btn)
        self.clear_items_button.setIconSize(pixmap_clear_btn.rect().size())

        pixmap_unsel_btn = QPixmap(get_icon('unselect_button.svg', 'gui/images/icons'))
        icon_unsel_btn = QIcon(pixmap_unsel_btn)
        self.clear_selection_button.setIcon(icon_unsel_btn)
        self.clear_selection_button.setIconSize(self.clear_selection_button.rect().size())

        left_btn_style = f'''
            QPushButton {{
                border: none;
            }}
            QPushButton:hover{{
                background-color: {self.border_color};
            }}
        '''
        self.clear_items_button.setStyleSheet(left_btn_style)
        self.clear_selection_button.setStyleSheet(left_btn_style)

        # SEARCH BAR STYLE
        # /////////////////////////////////////////////////////////////////
        self.search_bar.setStyleSheet(f'''
            border: none;
            border-right: 2px solid;
            border-bottom: 2px solid;
            border-color: #b7c4c8;
            color: #506369;
            font: 700 12pt {self.font};
        ''')

        # Frame styling
        # /////////////////////////////////////////////////////////////////
        self.table_item_frame.setStyleSheet(f'''
            background-color: {self.inner_frame_color};
            border-style: solid;
            border-width: 2px;
            border-color: {self.border_color};
            ''')

        # STATION AND PARAMETERS LIST LABELS
        # /////////////////////////////////////////////////////////////////
        self.parameter_list_label.setStyleSheet(f'''
            font : bold 15pt "{self.font}";
        ''')
        self.table_station_label.setStyleSheet(f'''
            font : bold 15pt "{self.font}";
            padding-left : 10px;
        ''')

        # SCROLL BAR
        # //////////////////////////////////////////////////////////////////
        track = "#b7c4c8"
        thumb = '#ffffff'
        slide = self.menu_color
        self.scroll_bar_stations.setStyleSheet(f'''
             QScrollBar:vertical {{              
                border: none;
                border-top: 1px solid;
                border-color: {track};
                background: {thumb};
                width: 10px;
                margin: 10px 5px 10px 5px;
            }}
            QScrollBar::handle:vertical {{
                background: {slide};
                min-height: 0px;
                width: 5px;
                margin: 0px 0px 0px 0px;
            }}
            QScrollBar::add-line:vertical, QScrollBar::add-page:vertical {{
                background: {track};
                height: 0px;
                subcontrol-position: bottom;
                subcontrol-origin: margin;
            }}
            QScrollBar::sub-line:vertical, QScrollBar::sub-page:vertical {{
                background: {track};
                height: 0 px;
                subcontrol-position: top;
                subcontrol-origin: margin;
            }}
        '''
        )