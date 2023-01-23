# IMPORT QT_CORE
from qt_core import *

# IMPORT CUSTOM WIDGETS
from gui.widgets.station_list_view import PyStationListView
from gui.widgets.py_push_button import ClassicButton
from gui.widgets.parameter_list_widget import ParameterSelectionWidget
from gui.widgets.py_date_select import PyDoubleDateEdit

# IMPORT CUSTOM MODULES
from backend.misc.functions import get_imagepath
from gui.widgets.py_radio_button import PyRadioButton


# Data Manager Page UI Class
class UI_DataManager(object):
    
    def setup_ui(self, parent):
        
        # FRAME CONSTANTS
        parent.setObjectName(u'data_page')
        self.frame_height = 500

        # MAIN LAYOUT
        self.main_layout = QGridLayout(parent)
        self.main_layout.setVerticalSpacing(20)
        self.main_layout.setHorizontalSpacing(20)
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
        w, h = (330, 500) 
        self.station_view_frame = QFrame()
        self.station_view_frame.setObjectName("station_view")
        self.station_view_frame.setFixedWidth(w)
        self.station_view_frame.setFixedHeight(h)
        #
        self.station_view_layout = QVBoxLayout(self.station_view_frame)
        self.station_view_layout.setSpacing(0)
        self.station_view_layout.setContentsMargins(0, 0, 0, 0)

        # SEARCH BAR
        self.search_bar = QLineEdit()
        self.search_bar.setObjectName('search_bar')
        self.search_bar.setFixedWidth(w)
        self.search_bar.setFixedHeight(50)
        self.search_bar.setClearButtonEnabled(True)
        image = QPixmap(get_imagepath('search.svg', 'gui/images/icons'))
        image.scaled(QSize(50, 50), Qt.AspectRatioMode.KeepAspectRatio)
        self.search_bar.addAction(image, QLineEdit.LeadingPosition)
        self.search_bar.setPlaceholderText("Buscar...")

        # STATION MANAGER lIST
        self.station_manager_list = PyStationListView(parent = parent, width = w)
        self.station_manager_list.setSpacing(5) # spacing between list items

        # add to station layout
        self.station_view_layout.addWidget(self.search_bar)
        self.station_view_layout.addWidget(self.station_manager_list)
        
        # PARAMETER VIEW LIST AND RELATED
        # ///////////////////////////////////////////////////////////////////
        # main frme
        self.parameter_view_frame = QFrame()
        self.parameter_view_frame.setObjectName("parameter_view_frame")
        self.parameter_view_frame.setMinimumWidth(w)
        self.parameter_view_frame.setMinimumHeight(h)
        #
        self.parameter_view_layout = QVBoxLayout(self.parameter_view_frame)
        self.parameter_view_layout.setSpacing(30)
        self.parameter_view_layout.setContentsMargins(0, 0, 0, 0)

        # SELECTED STATION INFORMATION WIDGET
        self.information_view_frame = QFrame()
        self.information_view_frame.setObjectName("information_view")
        self.information_view_frame.setMinimumWidth(w)
        self.information_view_frame.setFixedHeight(50)
        #
        self.information_view_layout = QHBoxLayout(self.information_view_frame)
        self.information_view_layout.setSpacing(0)
        self.information_view_layout.setContentsMargins(15, 0, 15, 0)
        #
        self.information_station = QLabel()
        self.information_station.setObjectName('station_label')
        self.information_station.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
        self.information_station.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        #
        self.information_dates = QLabel()
        self.information_dates.setObjectName('dates_label')
        self.information_dates.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
        self.information_dates.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        #
        self.information_view_layout.addWidget(self.information_station)
        self.information_view_layout.addWidget(self.information_dates)

        # PARAMETER VIEWER
        self.parameter_viewer_layout = QVBoxLayout()
        self.parameter_viewer_layout.setContentsMargins(0,0, 0,0)
        self.parameter_viewer_layout.setSpacing(0)

        # HEADER
        self.viewer_header = QFrame()
        self.viewer_header.setObjectName('header')
        self.viewer_header.setMinimumWidth(w)
        self.viewer_header.setFixedHeight(50)
        #
        self.header_layout = QHBoxLayout(self.viewer_header)
        self.header_layout.setContentsMargins(10, 0, 10, 0)
        self.header_layout.setSpacing(10)
        #
        self.check_box = PyRadioButton(40, 40)
        self.name_label = QLabel("Parâmetro")
        self.theme_label = QLabel("Temática")
        self.unit_label = QLabel("Unidade")
        self.name_label.setObjectName("name")
        self.theme_label.setObjectName("theme")
        self.unit_label.setObjectName("unit")
        self.theme_label.setFixedWidth(150)
        self.unit_label.setFixedWidth(100)
        #
        self.header_layout.addWidget(self.check_box)
        self.header_layout.addWidget(self.name_label)
        self.header_layout.addWidget(self.theme_label)
        self.header_layout.addWidget(self.unit_label)

        self.parameter_viewer = ParameterSelectionWidget(width=w, item_height=50)
        self.parameter_viewer.setMinimumHeight(h - 200)
        self.parameter_viewer.setObjectName('parameter_viewer')

        self.parameter_viewer_layout.addWidget(self.viewer_header)
        self.parameter_viewer_layout.addWidget(self.parameter_viewer)

        # add to paramater view layout
        self.parameter_view_layout.addWidget(self.information_view_frame)
        self.parameter_view_layout.addLayout(self.parameter_viewer_layout)

        # MAIN LAYOUT CONFIGURATION
        # ////////////////////////////////////////////////////////////////////
        
        # bottom spacer
        spacer = QSpacerItem(1050, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.main_layout.addWidget(self.tool_bar_frame, 0, 0, 1, 2, Qt.AlignmentFlag.AlignTop)
        self.main_layout.addWidget(self.station_view_frame, 1, 0, 1, 1)
        self.main_layout.addWidget(self.parameter_view_frame, 1, 1, 1, 1)
        self.main_layout.addItem(spacer, 2, 0, 1, 2)
       

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
                font: 500 13pt {font};
                color: {font_color};
                padding-left: 25px;
            }}
            #xls_button, #clear_button, #clear_sel_button {{
                background-color: transparent;
                border-radius: 0px;
                border: none;
                border-left: 1px solid;
                border-color: {border_color};
                font: 500 13pt {font};
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

        # SETTING UP MANAGER STATION LIST STYLESHEET
        self.station_view_frame.setStyleSheet(f'''
            #search_bar {{
                font: 500 14pt {font};
                color: {font_color};
                background-color: #ffffff;
                border-radius: {border_radius};
                border: none;
                padding-left: 10px;
            }}
        '''
        )

        # SETTING UP PARAMETER LIST view STYLESHEET
        self.parameter_view_frame.setStyleSheet(f'''
            #parameter_view_frame {{
                background-color: transparent;
                border: none;
            }}
            #information_view{{
                background-color: #ffffff;
                border: none;
                border-radius: {border_radius};
            }}
            #station_label, #dates_label{{
                font: 500 14pt {font};
                color: #32495e; 
            }}
            #header {{
                background-color: #dcdcdc;
                border: 1px solid;
                border-color: #000000;
            }}
            #name, #theme, #unit {{
                font: 500 13pt {font};
                color: #32495e;
            }}
        ''')

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
    