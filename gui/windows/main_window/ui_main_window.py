# IMPORT QT CORE
from qt_core import *

# IMPORT MODULES
from gui.pages.ui_pages import UI_StackedPages

# IMPORT CUSTOM WIDGETS
from gui.widgets.py_push_button import PyPushButton


# MAIN WINDOW
class UI_MainWindow(object):
    def setup_ui(self, parent):
        if not parent.objectName():
            parent.setObjectName("MainWindow")

        # SET INITIAL PARAMETERS
        parent.resize(1200, 720)
        parent.setMinimumSize(960, 540)
        
        # SET INITAL COLORS
        self.background_color = '#f5f5f5'
        self.top_bar_color = '#f5f5f5'
        self.left_menu_color = '#4969b2'

        # CREATE CENTRAL WIDGET
        self.central_frame = QFrame()

        # CREATE MAIN LAYOUT
        self.main_layout = QHBoxLayout(self.central_frame)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        # LEFT MENU
        # //////////////////////////////////////////////////////////////////////
        self.left_menu = QFrame()
        self.left_menu.setStyleSheet(f'''
            background-color: {self.left_menu_color}; 
            ''')
        self.left_menu.setMaximumWidth(150)
        self.left_menu.setMinimumWidth(150)
        
        # left menu layout
        self.left_menu_layout = QVBoxLayout(self.left_menu)
        self.left_menu_layout.setContentsMargins(0, 0, 0, 0)
        self.left_menu_layout.setSpacing(5)

        # TOP FRAME MENU
        self.left_menu_top_frame = QFrame()
        self.left_menu_top_frame.setMinimumHeight(90)
        self.left_menu_top_frame.setStyleSheet(f"background-color: {self.left_menu_color}")

        # TOP FRAME LAYOUT
        self.left_menu_top_layout = QVBoxLayout(self.left_menu_top_frame)
        self.left_menu_top_layout.setContentsMargins(0, 0, 0, 0)
        self.left_menu_top_layout.setSpacing(0)

        # TOP BINS
        btn_properties = {
            'height' : 50,
            'text_color' : self.background_color,
            'icon_color' : self.background_color,
            'btn_color' : self.left_menu_color,
            'btn_hover' : '#ffb703',
            'width' : 135
        }
        self.btn_1 = PyPushButton("Início", icon_path='icon_home.svg', **btn_properties)
        self.btn_2 = PyPushButton("Dados", icon_path='icon_datamanager.svg', **btn_properties)
        self.btn_3 = PyPushButton("Ajustes", icon_path = 'icon_settings.svg', **btn_properties)

        # menu spacer
        self.left_menu_spacer = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)
        
        # label version
        self.left_menu_label_version = QLabel("v1.2.0")
        self.left_menu_label_version.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.left_menu_label_version.setMinimumHeight(30)
        self.left_menu_label_version.setMaximumHeight(30)
        self.left_menu_label_version.setStyleSheet(f'color: {self.background_color}; background-color: {self.left_menu_color}; font: 700 12pt "Microsoft New Tai Lue"')
        
        # ADD TO LEFT MENU LAYOUT# ADD TOP BINS TO LAYOUT
        self.left_menu_layout.addWidget(self.left_menu_top_frame)
        self.left_menu_layout.addWidget(self.btn_1)
        self.left_menu_layout.addWidget(self.btn_2)
        self.left_menu_layout.addWidget(self.btn_3)
        self.left_menu_layout.addItem(self.left_menu_spacer)
        self.left_menu_layout.addWidget(self.left_menu_label_version)

        # CONTENT
        # //////////////////////////////////////////////////////////////////////
        self.content = QFrame()
        self.content.setStyleSheet(f"background-color: {self.background_color}")
        
        # CONTENT LAYOUT
        self.content_layout = QVBoxLayout(self.content)
        self.content_layout.setContentsMargins(0, 0, 0, 0)
        self.content_layout.setSpacing(0)

        # BOTTOM BAR
        self.bottom_bar = QFrame()
        self.bottom_bar.setMinimumHeight(30)
        self.bottom_bar.setMaximumHeight(30)
        self.bottom_bar.setStyleSheet(f"background-color: {self.background_color}; color: {self.left_menu_color}")
        self.bottom_bar_layout = QHBoxLayout(self.bottom_bar)
        self.bottom_bar_layout.setContentsMargins(10, 0, 10, 0)

        # top spacer
        self.bottom_spacer = QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        
        # Right label
        self.bottom_label_right = QLabel("@ 2023")
        self.bottom_label_right.setStyleSheet('font: 700 12pt "Microsoft New Tai Lue"')

        # Add to top bar layout
        self.bottom_bar_layout.addItem(self.bottom_spacer)
        self.bottom_bar_layout.addWidget(self.bottom_label_right)
       
        # Application pages
        self.pages = QStackedWidget()
        self.pages.setStyleSheet("font-size: 12pt; color: #22280b")
        self.ui_pages = UI_StackedPages()
        self.ui_pages.setup_ui(self.pages)
        self.pages.setCurrentWidget(self.ui_pages.page_1)

        # Add to content layout
        self.content_layout.addWidget(self.pages)
        self.content_layout.addWidget(self.bottom_bar)

        # ADD WIDGETS TO APP
        self.main_layout.addWidget(self.left_menu)
        self.main_layout.addWidget(self.content)
        
        # SET CENTRAL WIDGET
        parent.setCentralWidget(self.central_frame)