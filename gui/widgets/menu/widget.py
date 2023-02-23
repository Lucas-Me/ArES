# IMPORT QT MODULES
from qt_core import *

# IMPORT CUSTOM WIDGETS
from gui.widgets.menu.buttons import TopLevelButton

class Menu(QFrame):
    
	def __init__(self):
		super().__init__()
		
		# SETTINGS
		self.setFixedWidth(150)

		# SETUP UI
		self.setup_ui()


	def setup_ui(self):
		self.main_layout = QVBoxLayout(self)
		self.main_layout.setContentsMargins(0, 0, 0, 0)
		self.main_layout.setSpacing(0)

		# BUTTONS
		# ////////////////////////////////////

		shadow = QGraphicsDropShadowEffect()
		shadow.setBlurRadius(5)
		shadow.setOffset(5)

		# lOGO
		self.top_logo = TopLevelButton(
			text_color='#ffffff',
			text = 'ArES',
			active_color = "#186B93",
			icon_name = 'ArES_logo_2.svg')
		self.top_logo.setDisabled(True)
		self.top_logo.setObjectName('logo')
		self.top_logo.setGraphicsEffect(shadow)
		
		# HOME BUTTON
		self.btn_home = TopLevelButton(text = "Início", icon_name='icon_home.svg')
		self.btn_home.setActive(True)
		
		# DADOS (DATA MANAGEMENT) BUTTON
		self.btn_data = TopLevelButton(text = "Dados", icon_name='icon_datamanager.svg')
		
		# MÉTODO (PROCESSING SCREEN) BUTTON
		self.btn_process = TopLevelButton(text = "Método", icon_name = 'process_screen_icon.svg')
		
		# AJUSTES (SETTINGS) BUTTON
		self.btn_settings = TopLevelButton(text = "Ajustes", icon_name = 'icon_settings.svg')

		
		# BOTTOM 
		# ////////////////////////////////////
		
		# label version
		self.left_menu_label_version = QLabel("v1.3.0")
		self.left_menu_label_version.setAlignment(Qt.AlignmentFlag.AlignCenter)
		self.left_menu_label_version.setMinimumHeight(30)
		self.left_menu_label_version.setMaximumHeight(30)


		# ADD TO MAIN LAYOUT
		# ////////////////////////////////////

		self.main_layout.addWidget(self.top_logo)
		self.main_layout.addWidget(self.btn_home)
		self.main_layout.addWidget(self.btn_data)
		self.main_layout.addWidget(self.btn_process)
		self.main_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Expanding))
		self.main_layout.addWidget(self.btn_settings)

		# style
		self.setStyleSheet('background-color: #36475f')