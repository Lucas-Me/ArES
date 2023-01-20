# IMPORT QT_CORE
from qt_core import *

# IMPORT CUSTOM FUCTIONS
from backend.misc.functions import get_imagepath

# Data Manager Page UI Class
class UI_LoginScreen(object):
    
    def setup_ui(self, parent : QWidget):
        
        parent.setObjectName(u'login_page')
		

        # CENTRAL LAYOUT
        self.central_layout = QVBoxLayout(parent)

        # CONTENT FRAME
        w, h = (700, 500)
        self.content_frame = QFrame()
        self.content_frame.setFixedSize(w, h)

        # CONTENT LAYOUT
        self.content_layout = QHBoxLayout(self.content_frame)
        self.content_layout.setContentsMargins(0, 0, 0, 0)
        self.content_layout.setSpacing(0)

        # UPDATES FRAME
        # //////////////////////////////////////////////////////////////////
        self.update_frame = QFrame()
        self.update_frame.setFixedSize(w // 2, h)

        # LOGIN FRAME
        # //////////////////////////////////////////////////////////////////
        self.login_frame = QFrame()
        self.login_frame.setFixedSize(w // 2, h)

        # ADD FRAMES TO CONTENT LAYOUT
        # //////////////////////////////////////////////////////////////////
        self.content_layout.addWidget(self.update_frame)
        self.content_layout.addWidget(self.login_frame)

        # SPACERS
        spacer = QSpacerItem(parent.width(), (parent.height() - h) // 2, QSizePolicy.Minimum, QSizePolicy.Expanding)
        
        # COPYRIGHT SYMBOL IN BOTTOM RIGHT.
        self.bottom_label_right = QLabel("@2023")
        self.bottom_label_right.setStyleSheet('font: 700 14pt "Open Sans";color: #ffffff')

        # ADD TO CENTRAL LAYOUT
        self.central_layout.addItem(spacer)
        self.central_layout.addWidget(self.content_frame)
        self.central_layout.addItem(spacer)
        self.central_layout.addWidget(self.bottom_label_right)

        # OTHER OPERATIONS
        self.central_layout.setAlignment(self.content_frame, Qt.AlignmentFlag.AlignCenter)
        self.central_layout.setAlignment(self.bottom_label_right, Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignRight)
    
    def setup_stylesheet(self):
        # colors
        update_color =  '#576cd6'
        login_color = '#ffffff'
        line_edit_bg_color = '#e3e8f3'
        line_edit_color =  '#a7a7b8'

        # other properties
        border_radius = 10

        # SETTING UP STYLESHEET OF OBJETS IN UI
        self.update_frame.setStyleSheet(f'''
            background-color: {update_color};
            border-top-left-radius: {border_radius}px;
            border-bottom-left-radius:  {border_radius}px;
        '''
        )
        self.content_frame.setStyleSheet(f'''
            background-color: transparent;
        ''')
        self.login_frame.setStyleSheet(f'''
            background-color: {login_color};
            border-top-right-radius: {border_radius}px;
            border-bottom-right-radius: {border_radius}px;
        ''')
    


