# IMPORT QT_CORE
from qt_core import *

# IMPORT CUSTOM MODULE
from gui.widgets.py_push_button import ClassicButton

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
        self.shadow = QGraphicsDropShadowEffect()
        self.shadow.setBlurRadius(15)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0)
        self.content_frame.setGraphicsEffect(self.shadow)

        # CONTENT LAYOUT
        self.content_layout = QHBoxLayout(self.content_frame)
        self.content_layout.setContentsMargins(0, 0, 0, 0)
        self.content_layout.setSpacing(0)

        # UPDATES FRAME
        # //////////////////////////////////////////////////////////////////
        self.left_frame = QFrame()
        self.left_frame.setFixedSize(w // 2, h)

        self.right_frame = QStackedWidget()

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
        self.field_spacer = QSpacerItem(w // 2, 30, QSizePolicy.Minimum, QSizePolicy.Minimum)

        # LOGIN BUTTON
        self.login_btn = QPushButton("Conectar")
        self.login_btn.setFixedSize(QSize(250, 40))

        # SERVER AND STATUS LABELS
        self.host_label = QLabel()
        self.host_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.host_label.setFixedSize(QSize(250, 20))

        self.status_label = QLabel()
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.status_label.setFixedSize(QSize(250, 20))

        # add widgets to login layout
        self.login_frame_layout.addWidget(parent.logo)
        self.login_frame_layout.addWidget(self.welcome_label)
        self.login_frame_layout.addWidget(self.username)
        self.login_frame_layout.addWidget(self.password)
        self.login_frame_layout.addWidget(self.remember_me)
        self.login_frame_layout.addItem(self.field_spacer)
        self.login_frame_layout.addWidget(self.login_btn)
        self.login_frame_layout.addItem(self.login_spacer)
        self.login_frame_layout.addWidget(self.host_label)
        self.login_frame_layout.addWidget(self.status_label)
        
        # alignment
        self.login_frame_layout.setAlignment(parent.logo, Qt.AlignmentFlag.AlignCenter)
        self.login_frame_layout.setAlignment(self.welcome_label, Qt.AlignmentFlag.AlignCenter)
        self.login_frame_layout.setAlignment(self.username, Qt.AlignmentFlag.AlignCenter)
        self.login_frame_layout.setAlignment(self.password, Qt.AlignmentFlag.AlignCenter)
        self.login_frame_layout.setAlignment(self.remember_me, Qt.AlignmentFlag.AlignCenter)
        self.login_frame_layout.setAlignment(self.login_btn, Qt.AlignmentFlag.AlignCenter)
        self.login_frame_layout.setAlignment(self.host_label, Qt.AlignmentFlag.AlignCenter)
        self.login_frame_layout.setAlignment(self.status_label, Qt.AlignmentFlag.AlignCenter)

        # WELCOME FRAME
        # ///////////////////////////////////////////////////////////////////////
        self.welcome_frame = QFrame()
        self.welcome_frame.setFixedSize(w // 2, h)

        self.welcome_frame_layout = QVBoxLayout(self.welcome_frame)
        self.welcome_frame_layout.setSpacing(20)
        self.welcome_frame_layout.setContentsMargins(0, 30, 0, 0)

        # WELCOME LABEL
        self.greetings_label = QLabel()
        self.greetings_label.setMinimumWidth(250)
        self.greetings_label.setFixedHeight(50)
        self.greetings_label.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignBottom)
        self.greetings_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        # LOGGED LABEL
        self.logged_label = QLabel()
        self.logged_label.setMinimumWidth(340)
        self.logged_label.setFixedHeight(50)
        self.logged_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.logged_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        # LAST VERIFICATION LABEL
        self.verification_label = QLabel()
        self.verification_label.setObjectName("verification_label")
        self.verification_label.setFixedSize(QSize(350, 20))
        self.verification_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        # REFRESH BUTTON
        self.refresh_btn = ClassicButton(
            text = 'Verificar',
            height = 70,
            width = 200,
            icon_width=50,
            icon_path='refresh_button.svg',
            icon_color = '#ffffff'
        )
        self.refresh_btn.setObjectName("refresh_button")

        # DISCONNECT BUTTON
        self.disconnect_btn = QPushButton("Desconectar")
        self.disconnect_btn.setFixedSize(QSize(150, 40))

        # spacers
        self.spacer_logged = QSpacerItem(w // 2, 10, QSizePolicy.Minimum, QSizePolicy.Minimum)

        # add to layout
        self.welcome_frame_layout.addWidget(parent.profile_image)
        self.welcome_frame_layout.addWidget(self.greetings_label)
        self.welcome_frame_layout.addItem(self.spacer_logged)
        self.welcome_frame_layout.addWidget(self.logged_label)
        self.welcome_frame_layout.addWidget(self.verification_label)
        self.welcome_frame_layout.addWidget(self.refresh_btn)
        self.welcome_frame_layout.addWidget(self.disconnect_btn)
      
        # adjustin alignment
        self.welcome_frame_layout.setAlignment(parent.profile_image, Qt.AlignmentFlag.AlignCenter)
        self.welcome_frame_layout.setAlignment(self.greetings_label, Qt.AlignmentFlag.AlignCenter)
        self.welcome_frame_layout.setAlignment(self.logged_label, Qt.AlignmentFlag.AlignCenter)
        self.welcome_frame_layout.setAlignment(self.disconnect_btn, Qt.AlignmentFlag.AlignRight)
        self.welcome_frame_layout.setAlignment(self.verification_label, Qt.AlignmentFlag.AlignCenter)
        self.welcome_frame_layout.setAlignment(self.refresh_btn, Qt.AlignmentFlag.AlignCenter)

        # ADD FRAMES TO CONTENT LAYOUT
        # //////////////////////////////////////////////////////////////////
        self.right_frame.addWidget(self.login_frame)
        self.right_frame.addWidget(self.welcome_frame)
        self.right_frame.setCurrentIndex(0)
        self.content_layout.addWidget(self.left_frame)
        self.content_layout.addWidget(self.right_frame)

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
        
        # objects name
        self.login_frame.setObjectName('login_frame')
        self.welcome_label.setObjectName('welcome_label')
        self.username.setObjectName('username')
        self.password.setObjectName('password')
        self.remember_me.setObjectName('remember_me')
        self.login_btn.setObjectName('login_button')
        self.host_label.setObjectName('host_label')
        self.status_label.setObjectName('status_label')
        #
        self.welcome_frame.setObjectName('welcome_frame')
        self.greetings_label.setObjectName('greetings_label')
        self.logged_label.setObjectName("logged_label")
        self.disconnect_btn.setObjectName("disconnect_button")

        # SETTING UP STYLESHEET OF OBJETS IN UI
        self.content_frame.setStyleSheet(f'''
            background-color: transparent;
        ''')
        
        # update frame
        self.left_frame.setStyleSheet(f'''
            background-color: {update_color};
            border-top-left-radius: {border_radius}px;
            border-bottom-left-radius:  {border_radius}px;
        '''
        )
        
        # login frame
        self.login_frame.setStyleSheet(f'''
            #login_frame {{
                background-color: {login_color};
                border-top-right-radius: {border_radius}px;
                border-bottom-right-radius: {border_radius}px;
                padding-bottom: 20px;
            }}
            #username, #password{{
                background-color: {line_edit_bg_color};
                color: {line_edit_color};
                border: none;
                border-radius: {border_radius}px;
                font: Bold 13pt "Open Sans";
                padding-left: 10px;
            }}
            #welcome_label {{
                font: bold 25pt "Microsoft New Tai Lue";
                color: {line_edit_color};
            }}
            #remember_me {{
                font: bold 13pt "Microsoft New Tai Lue";
                color: {line_edit_color};
            }}
            #login_button {{
                font: bold 13pt "Microsoft New Tai Lue";
                background-color: #1e374d;
                color: #ffffff;
                border-radius: {border_radius};
            }}
            #login_button:hover {{
                background-color: #1c4d6e;
            }}
            #login_button:pressed {{
                background-color: #52a9c7;
            }}
            #login_button:disabled{{
                background-color: #8396a2;
            }}
            #host_label, #status_label {{
                font: bold 13pt "Microsoft New Tai Lue";
                background-color: transparent;
                color: #409cc1;
            }}
        ''')

        self.welcome_frame.setStyleSheet(f'''
            #welcome_frame {{
                background-color: {login_color};
                border-top-right-radius: {border_radius}px;
                border-bottom-right-radius: {border_radius}px;
                padding-bottom: 10px;
            }}
            #greetings_label {{
                font: bold 18pt "Open Sans";
                color: #409cc1;
            }}
            #logged_label {{
                font: bold 14pt "Microsoft New Tai Lue";
                color: {line_edit_color};
            }}
            #verification_label{{
                font: bold 14pt "Microsoft New Tai Lue";
                color: #409cc1;
            }}
            #disconnect_button {{
                background-color: none;
                border: none;
                font: bold 13pt "Open Sans";
                color: #da0239;
            }}
            #disconnect_button:hover {{
                color: #5a043a;
            }}
            #disconnect_button:pressed {{
                color: #ff000e;
            }}
            #refresh_button{{
                background-color: #409cc1;
                color : #ffffff;
                padding-left: 20px;
                font: bold 14pt "Microsoft New Tai Lue";
                border-radius: {border_radius}px;
            }}
            #refresh_button:hover{{
                background-color: #1e5375;
            }}
            #refresh_button:pressed{{
                background-color: #57aecf;
            }}
        '''
        )