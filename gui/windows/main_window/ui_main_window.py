# IMPORT QT CORE
from qt_core import *

# IMPORT CUSTOM WIDGETS
from gui.widgets.menu.widget import Menu
from gui.widgets.pages import StackedPages


# MAIN WINDOW
class UI_MainWindow(object):
    def setup_ui(self, parent):
        if not parent.objectName():
            parent.setObjectName("MainWindow")

        # SET INITIAL PARAMETERS
        parent.resize(1280, 720)
        parent.setMinimumSize(960, 540)
        
        # SET INITAL COLORS
        self.background_color = '#f5f5f5'
        self.top_bar_color = '#f5f5f5'
        self.left_menu_color = '#2a3f54'

        # CREATE CENTRAL WIDGET
        self.central_frame = QFrame()

        # CREATE MAIN LAYOUT
        self.main_layout = QHBoxLayout(self.central_frame)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        # LEFT MENU
        # //////////////////////////////////////////////////////////////////////
        self.left_menu = Menu(parent)
 
        # CONTENT
        # //////////////////////////////////////////////////////////////////////
        self.content = QFrame()
        
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
        self.pages = StackedPages(parent = parent, menu = self.left_menu)
        self.pages.setCurrentIndex(0)

        # Add to content layout
        self.content_layout.addWidget(self.pages)

        # ADD WIDGETS TO APP
        self.main_layout.addWidget(self.left_menu)
        self.main_layout.addWidget(self.content)
        
        # SET CENTRAL WIDGET
        parent.setCentralWidget(self.central_frame)