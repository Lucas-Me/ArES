# IMPORT QT MODULES
from qt_core import *

# IMPORT CUSTOM WIDGETS
from gui.widgets.menu.buttons import TopLevelButton
from gui.widgets.menu.chart_list_widget import ChartList
from gui.windows.settings.window import SettingsWindow

class Menu(QFrame):
    
	def __init__(self, parent):
		super().__init__()
		
		# PROPERTIES
		self.parent = parent

		# SETTINGS
		self.setFixedWidth(150)

		# SETUP UI
		self.setup_ui()

		# Signals
		self.charts_list.rowClicked.connect(self.establishSignal)
		self.btn_settings.clicked.connect(self.openSettings)

	def openSettings(self):
		dialog = SettingsWindow(parent = self.parent)
		dialog.show()
		
	def establishSignal(self, item : QListWidgetItem):
		self.parent.change_page(
			page = item,
			button = self.charts_list.itemWidget(item)
		)

	def setup_ui(self):
		self.setObjectName("main_menu")
		self.main_layout = QVBoxLayout(self)
		self.main_layout.setContentsMargins(0, 0, 0, 0)
		self.main_layout.setSpacing(0)

		# TOP
		# ////////////////////////////////////

		# LOGO
		self.top_logo = TopLevelButton(
			text_color='#ffffff',
			text = 'ArES',
			active_color = "#186B93",
			icon_name = 'ArES_logo_2.svg')
		self.top_logo.setDisabled(True)
		self.top_logo.setObjectName('logo')
		
		# HOME BUTTON
		self.btn_home = TopLevelButton(text = "Início", icon_name='icon_home.svg')
		self.btn_home.setActive(True)
		self.btn_home.setObjectName('home')
		
		# DADOS (DATA MANAGEMENT) BUTTON
		self.btn_data = TopLevelButton(text = "Dados", icon_name='icon_datamanager.svg')
		self.btn_data.setObjectName('data')
		
		# MÉTODO (PROCESSING SCREEN) BUTTON
		self.btn_process = TopLevelButton(text = "Método", icon_name = 'process_screen_icon.svg')
		self.btn_process.setObjectName('methods')
		
		# GRÁFICOS LABEL
		self.charts_label = TopLevelButton(
			text_color='#d9e2f1',
			text = 'Gráficos',
			active_color = "#0d7bbd",
			icon_name = 'chart_icon.svg')
		self.charts_label.setDisabled(True)
		self.charts_label.setObjectName('label')
		
		# LIST OF CHARTS
		self.charts_list = ChartList(width = self.width(), parent = self.parent)	

		# BOTTOM 
		# ////////////////////////////////////
		
		# AJUSTES (SETTINGS) BUTTON
		self.btn_settings = TopLevelButton(text = "Ajustes", icon_name = 'icon_settings.svg')
		self.btn_settings.setObjectName('settings')

		# ADD TO MAIN LAYOUT
		# ////////////////////////////////////

		self.main_layout.addWidget(self.top_logo)
		self.main_layout.addWidget(self.btn_home)
		self.main_layout.addWidget(self.btn_data)
		self.main_layout.addWidget(self.btn_process)
		self.main_layout.addWidget(self.charts_label)
		self.main_layout.addWidget(self.charts_list)
		self.main_layout.addWidget(self.btn_settings)

		# style
		self.setStyleSheet('''
			QFrame {
				background-color: #36475f;
			}
		''')