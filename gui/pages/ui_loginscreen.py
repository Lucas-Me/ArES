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

        self.login_frame_layout = QVBoxLayout(self.login_frame)
        self.login_frame_layout.setSpacing(10)
        self.login_frame_layout.setContentsMargins(0, 10, 0, 0)

        # WELCOME LABEL
        self.welcome_label = QLabel("Bem-vindo!")
        self.welcome_label.setFixedSize(QSize(250, 40))
        self.welcome_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        # USERNAME LINE
        self.username = QLineEdit()
        self.username.setPlaceholderText("Usuário")
        self.username.setFixedSize(QSize(250, 40))
        self.username.setAlignment(Qt.AlignmentFlag.AlignLeft)
        
        # PASSWORD LINE
        self.password = QLineEdit()
        self.password.setPlaceholderText("Senha")
        self.password.setEchoMode(QLineEdit.Password)
        self.password.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.password.setFixedSize(QSize(250, 40))

        # REMEMBER ME BUTTON
        self.remember_me = QRadioButton("Lembrar-se")
        self.remember_me.setFixedSize(QSize(250, 20))

        # spacer
        self.login_spacer = QSpacerItem(w // 2, 140, QSizePolicy.Minimum, QSizePolicy.Expanding)

        # add widgets to login layout
        self.login_frame_layout.addWidget(parent.logo)
        self.login_frame_layout.addWidget(self.welcome_label)
        self.login_frame_layout.addWidget(self.username)
        self.login_frame_layout.addWidget(self.password)
        self.login_frame_layout.addWidget(self.remember_me)
        self.login_frame_layout.addItem(self.login_spacer)
        
        # alignment
        self.login_frame_layout.setAlignment(parent.logo, Qt.AlignmentFlag.AlignCenter)
        self.login_frame_layout.setAlignment(self.welcome_label, Qt.AlignmentFlag.AlignCenter)
        self.login_frame_layout.setAlignment(self.username, Qt.AlignmentFlag.AlignCenter)
        self.login_frame_layout.setAlignment(self.password, Qt.AlignmentFlag.AlignCenter)
        self.login_frame_layout.setAlignment(self.remember_me, Qt.AlignmentFlag.AlignCenter)

        # ADD FRAMES TO CONTENT LAYOUT
        # //////////////////////////////////////////////////////////////////
        self.content_layout.addWidget(self.update_frame)
        self.content_layout.addWidget(self.login_frame)

        # SPACERS
        spacer = QSpacerItem(parent.width(), (parent.height() - h) // 2, QSizePolicy.Minimum, QSizePolicy.Expanding)
        
        # COPYRIGHT SYMBOL IN BOTTOM RIGHT.
        self.bottom_label_right = QLabel("©2023")
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
        
        # style sheets
        line_edit = f'''
            background-color: {line_edit_bg_color};
            color: {line_edit_color};
            border: none;
            border-radius: {border_radius}px;
            font: Bold 13pt "Open Sans";
            padding-left: 10px;
        '''

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
        self.username.setStyleSheet(line_edit)
        self.password.setStyleSheet(line_edit)
        self.welcome_label.setStyleSheet(f'''
            font: bold 25pt "Microsoft New Tai Lue";
            color: {line_edit_color};
        '''
        )
        self.remember_me.setStyleSheet(f'''
            font: bold 13pt "Microsoft New Tai Lue";
            color: {line_edit_color};
        '''
        )


