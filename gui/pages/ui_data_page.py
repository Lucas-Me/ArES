# IMPORT QT_CORE
from qt_core import *

# IMPORT CUSTOM WIDGETS
from gui.widgets.station_list_view import PyStationListView
from gui.widgets.py_push_button import ClassicButton
from gui.widgets.parameter_list_widget import ParameterSelectionWidget
from gui.widgets.py_date_select import PyDoubleDateEdit

# IMPORT CUSTOM MODULES
from backend.misc.functions import get_imagepath

# Data Manager Page UI Class
class UI_DataManager(object):
    
    def setup_ui(self, parent):
        
        # FRAME CONSTANTS
        parent.setObjectName(u'data_page')
        self.frame_height = 500

        # MAIN LAYOUT
        self.main_layout = QGridLayout(parent)
        self.main_layout.setSpacing(20)
        self.main_layout.setContentsMargins(30, 30, 30, 0)

        # TOOL BAR
        # ///////////////////////////////////////////////////////////////////
        self.tool_bar_frame = QFrame()
        self.tool_bar_frame.setObjectName("tool_bar")
        self.tool_bar_layout = QHBoxLayout(self.tool_bar_frame)
        self.tool_bar_layout.setSpacing(0)
        self.tool_bar_layout.setContentsMargins(10, 10, 10, 10)

        # SQL BUTTON
        self.sql_btn = ClassicButton(
            text = "Importar SQL",
            icon_path = "icon_sql.svg",
            height = 30,
            width = 150,
            icon_width = 20,
            icon_allign = 'left',
            icon_color="#008299"
        )
        self.sql_btn.setObjectName("sql_button")

        # XLS BUTTON
        self.xls_btn = ClassicButton(
            text = "Importar XLS",
            icon_path = "icon_xls_file.svg",
            height = 30,
            width = 150,
            icon_width = 20,
            icon_allign = 'left',
            icon_color="#398e3d"
        )
        self.xls_btn.setObjectName("xls_button")

        # "CLEAR" BUTTON
        self.clear_btn = ClassicButton(
            text = "Limpar",
            icon_path = "clear_button.svg",
            height = 30,
            width = 100,
            icon_width = 20,
            icon_allign = 'left',
            icon_color="#333333"
        )
        self.clear_btn.setObjectName("clear_button")

        # CLEAR SELECTIONS BUTTON
        self.clear_sel_btn = ClassicButton(
            text = "Remover seleções",
            icon_path = "unselect_button.svg",
            height = 30,
            width = 175,
            icon_width = 20,
            icon_allign = 'left',
            icon_color="#333333"
        )
        self.clear_sel_btn.setObjectName("clear_sel_button")
        
        # spacer
        self.tool_bar_spacer = QSpacerItem(20, 30, QSizePolicy.Expanding, QSizePolicy.Minimum)

        # DATE EDIT CALENDAR WIDGET
        self.date_edit = PyDoubleDateEdit(parent = parent)
        self.date_edit.setObjectName("double_date_edit")
        self.date_edit.setFixedSize(300, 30)

        # add widgets to tool bar layout
        self.tool_bar_layout.addWidget(self.sql_btn)
        self.tool_bar_layout.addWidget(self.xls_btn)
        self.tool_bar_layout.addWidget(self.clear_btn)
        self.tool_bar_layout.addWidget(self.clear_sel_btn)
        self.tool_bar_layout.addItem(self.tool_bar_spacer)
        self.tool_bar_layout.addWidget(self.date_edit)

        # STATION VIEW LIST AND RELATED
        # ////////////////////////////////////////////////////////////////////
        # main frame
        w, h = (330, 700) 
        self.station_view_frame = QFrame()
        self.station_view_frame.setObjectName("station_view")
        self.station_view_frame.setFixedWidth(w)
        # self.station_view_frame.setMinimumHeight(h)
        #
        self.station_view_layout = QVBoxLayout(self.station_view_frame)
        self.station_view_layout.setSpacing(0)
        self.station_view_layout.setContentsMargins(0, 0, 0, 0)

        # SEARCH BAR
        self.search_bar = QLineEdit()
        self.search_bar.setFixedWidth(w)
        self.search_bar.setFixedHeight(50)
        self.search_bar.setClearButtonEnabled(True)
        image = QPixmap(get_imagepath('search.svg', 'gui/images/icons'))
        image.scaled(QSize(50, 50), Qt.AspectRatioMode.KeepAspectRatio)
        self.search_bar.addAction(image, QLineEdit.LeadingPosition)
        self.search_bar.setPlaceholderText("Buscar...")

        # STATION MANAGER lIST
        self.station_manager_list = PyStationListView(parent = parent)
        self.station_manager_list.setFixedWidth(w) 
        self.station_manager_list.setSpacing(5) # spacing between list items

        # MAIN LAYOUT CONFIGURATION
        # ////////////////////////////////////////////////////////////////////
        self.main_layout.addWidget(self.tool_bar_frame, 0, 0, 1, 2, Qt.AlignmentFlag.AlignTop)

        # # Insert objects into top layout
        # self.top_layout.addItem(self.top_spacer)
        # self.top_layout.addWidget(self.date_edit)
        # self.top_layout.addItem(self.top_spacer)

        # # LABELS ON TOP OF TABLES
        # # station label
        # self.table_station_label = QLabel("Estações de monitoramento")
        # self.table_station_label.setFixedWidth(400)
        # self.table_station_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        
        # # parmeter label
        # self.parameter_list_label = QLabel("Parâmetros monitorados")
        # self.parameter_list_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        # # Labels Layout
        # self.title_label_layout = QHBoxLayout()
        # self.title_label_layout.addWidget(self.table_station_label)
        # self.title_label_layout.addWidget(self.parameter_list_label)

        # # MAIN TABLE LIST DESIGN
        # # /////////////////////////////////////////////////////////////////////
        # self.table_item_frame = QFrame()
        # self.table_item_frame.setMinimumHeight(self.frame_height)

        # # MAIN TABLE LAYOUT
        # self.table_item_layout = QHBoxLayout(self.table_item_frame)
        # self.table_item_layout.setContentsMargins(0, 0, 0, 0)
        # self.table_item_layout.setSpacing(0)

        # # STATION LAYOUT
        # self.monitoring_station_layout = QGridLayout()
        # self.monitoring_station_layout.setContentsMargins(0, 0, 0, 0)
        # self.monitoring_station_layout.setSpacing(0)
        # dimh, dimw = (self.frame_height, 400)

        # # SEARCH BAR
       

        # # LefT BAR MONITORING STATION
        # left_width = 30
        # btn_height = 30
        # self.clear_items_button = QPushButton()
        # self.clear_selection_button = QPushButton()
        # self.clear_items_button.setFixedSize(left_width, btn_height)
        # self.clear_selection_button.setFixedSize(left_width, btn_height)
        # #
        # self.scroll_bar_stations = QScrollBar(Qt.Orientation.Vertical)
        # self.scroll_bar_stations.setFixedWidth(left_width)
        # self.scroll_bar_stations.setMinimumHeight(
        #     dimh - self.search_bar.height() - self.clear_items_button.height() * 2
        # )

        # # MONITORING STATION LIST 
       

        # # PARAMETER LIST
        # self.parameter_list = ParameterSelectionWidget()
        # self.parameter_list.setMinimumHeight(self.frame_height - 10)
        # self.parameter_list.setMinimumWidth(600)

        # # ADD LISTS TO MAIN TABLE LAYOUT
        # self.monitoring_station_layout.addWidget(self.search_bar, 0, 0, 1, 2)
        # self.monitoring_station_layout.addWidget(self.clear_items_button, 1, 0, 1, 1)
        # self.monitoring_station_layout.addWidget(self.clear_selection_button, 2, 0, 1, 1)
        # self.monitoring_station_layout.addWidget(self.scroll_bar_stations, 3, 0, 1, 1)
        # self.monitoring_station_layout.addWidget(self.monitoring_station_list, 1, 1, 3, 1)
        # self.table_item_layout.addLayout(self.monitoring_station_layout)
        # self.table_item_layout.addWidget(self.parameter_list)
               
        # # BOTTOM WIDGETS
        # # //////////////////////////////////////////////////////////////////////
        # self.bottom_spacer = QSpacerItem(20, 30, QSizePolicy.Minimum, QSizePolicy.Minimum)

        # # BUTTON LAYOUT
        # self.bottom_btn_layout = QHBoxLayout()

        # # CREATING IMPORT XLS BUTTON
        # self.import_xls_btn = ClassicButton(
        #     text = "Importar\nXLS",
        #     icon_path = "icon_xls_file.svg",
        #     height = 90,
        #     width = 175,
        #     icon_width = 80,
        #     icon_allign = 'left',
        #     icon_color="#398e3d"
        # )
        
        # # CREATING IMPORT DATABASE BUTTON
        # self.import_sql_btn = ClassicButton(
        #     text = "Importar\nSQL",
        #     icon_path = "icon_sql.svg",
        #     height = 90,
        #     width = 175,
        #     icon_width = 80,
        #     icon_color = '#232234'
        # )
        
        # # CREATNG SPACER
        # self.spacer_import = QSpacerItem(830, 60, QSizePolicy.Expanding, QSizePolicy.Minimum)

        # # ADDING BUTTONS TO LAYOUT
        # self.bottom_btn_layout.addWidget(self.import_xls_btn)
        # self.bottom_btn_layout.addWidget(self.import_sql_btn)
        # self.bottom_btn_layout.addItem(self.spacer_import)

        # # ADD TO MAIN LAYOUT
        # self.main_layout.addLayout(self.top_layout)
        # self.main_layout.addLayout(self.title_label_layout)
        # self.main_layout.addWidget(self.table_item_frame)
        # self.main_layout.addItem(self.bottom_spacer) 
        # self.main_layout.addLayout(self.bottom_btn_layout)

        # self.setup_stylesheets()

    def setup_stylesheets(self):
        # Properties
        font = 'sans-serif'
        font_color = '#32495e'
        border_color = '#919191'
        background_color = '#f0f0f0'
        header_color = '#dcdcdc'
        inner_frame_color = "#ffffff"
        border_radius = 10
        
        # SETTING UP TOOL BAR STYLE SHEET
        self.tool_bar_frame.setStyleSheet(f'''
            #tool_bar {{
                background-color: {inner_frame_color};
                border: none;
                border-radius: {border_radius};
            }}
            #sql_button {{
                background-color: transparent;
                border-radius: 0px;
                border: none;
                font: 12pt {font};
                color: {font_color};
                padding-left: 25px;
            }}
            #xls_button, #clear_button, #clear_sel_button {{
                background-color: transparent;
                border-radius: 0px;
                border: none;
                border-left: 1px solid;
                border-color: {border_color};
                font: 12pt {font};
                color: {font_color};
                padding-left: 25px;
            }}
            #xls_button:hover, #sql_button:hover, #clear_button:hover, #clear_sel_button:hover {{
                background-color: {background_color};
            }}
            #xls_button:pressed, #sql_button:pressed, #clear_button:pressed, #clear_sel_button:pressed {{
                background-color: {header_color};
            }}
        '''
        )

        # self.button_style = f'''
        #         QPushButton {{
        #             color : {self.menu_color};
        #             background-color: {self.inner_frame_color};
        #             font: 700 12pt {self.font};
        #             text-align: middle;
        #             vertical-align: middle;
        #             border: solid;
        #             border-width: 2px;
        #             padding-left: 65px;
        #             border-radius: 0px;
        #             border-color: {self.border_color};
        #             }}
        #         QPushButton:hover {{
        #             border-color: #3f40f0;
        #             }}
        #         '''
        
        # # XLS and SQL buttons
        # self.import_xls_btn.setStyleSheet(
        #     self.import_xls_btn.styleSheet() + self.button_style
        # )
        # self.import_sql_btn.setStyleSheet(
        #     self.import_sql_btn.styleSheet() + self.button_style
        # )

        # # LEFT BUTTONS ON STATION LIST
        # pixmap_clear_btn = QPixmap(get_imagepath('clear_button.svg', 'gui/images/icons'))
        # icon_clear_btn = QIcon(pixmap_clear_btn)
        # self.clear_items_button.setIcon(icon_clear_btn)
        # self.clear_items_button.setIconSize(pixmap_clear_btn.rect().size())

        # pixmap_unsel_btn = QPixmap(get_imagepath('unselect_button.svg', 'gui/images/icons'))
        # icon_unsel_btn = QIcon(pixmap_unsel_btn)
        # self.clear_selection_button.setIcon(icon_unsel_btn)
        # self.clear_selection_button.setIconSize(self.clear_selection_button.rect().size())

        # left_btn_style = f'''
        #     QPushButton {{
        #         border: none;
        #     }}
        #     QPushButton:hover{{
        #         background-color: {self.border_color};
        #     }}
        # '''
        # self.clear_items_button.setStyleSheet(left_btn_style)
        # self.clear_selection_button.setStyleSheet(left_btn_style)

        # # SEARCH BAR STYLE
        # # /////////////////////////////////////////////////////////////////
        # self.search_bar.setStyleSheet(f'''
        #     border: none;
        #     border-right: 2px solid;
        #     border-bottom: 2px solid;
        #     border-color: #b7c4c8;
        #     color: #506369;
        #     font: 700 12pt {self.font};
        # ''')

        # # Frame styling
        # # /////////////////////////////////////////////////////////////////
        # self.table_item_frame.setStyleSheet(f'''
        #     background-color: {self.inner_frame_color};
        #     border-style: solid;
        #     border-width: 2px;
        #     border-color: {self.border_color};
        #     ''')

        # # STATION AND PARAMETERS LIST LABELS
        # # /////////////////////////////////////////////////////////////////
        # self.parameter_list_label.setStyleSheet(f'''
        #     font : bold 15pt "{self.font}";
        # ''')
        # self.table_station_label.setStyleSheet(f'''
        #     font : bold 15pt "{self.font}";
        #     padding-left : 10px;
        # ''')

        # # SCROLL BAR
        # # //////////////////////////////////////////////////////////////////
        # track = "#b7c4c8"
        # thumb = '#ffffff'
        # slide = self.menu_color
        # self.scroll_bar_stations.setStyleSheet(f'''
        #      QScrollBar:vertical {{              
        #         border: none;
        #         border-top: 1px solid;
        #         border-color: {track};
        #         background: {thumb};
        #         width: 10px;
        #         margin: 10px 5px 10px 5px;
        #     }}
        #     QScrollBar::handle:vertical {{
        #         background: {slide};
        #         min-height: 0px;
        #         width: 5px;
        #         margin: 0px 0px 0px 0px;
        #     }}
        #     QScrollBar::add-line:vertical, QScrollBar::add-page:vertical {{
        #         background: {track};
        #         height: 0px;
        #         subcontrol-position: bottom;
        #         subcontrol-origin: margin;
        #     }}
        #     QScrollBar::sub-line:vertical, QScrollBar::sub-page:vertical {{
        #         background: {track};
        #         height: 0 px;
        #         subcontrol-position: top;
        #         subcontrol-origin: margin;
        #     }}
        # '''
        # )
    