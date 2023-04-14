# IMPORT QT_CORE
from qt_core import *

# IMPORT CUSTOM MODULES
from backend.misc.functions import get_imagepath
from gui.widgets.login_screen import Logo

# Data Manager Page UI Class
class UI_OpenAirScreen(object):
    
	def setup_ui(self, parent):

		# FRAME CONSTANTS
		parent.setObjectName(u'openair_page')

		# MAIN LAYOUT
		self.main_layout = QGridLayout(parent)
		self.main_layout.setVerticalSpacing(20)
		self.main_layout.setHorizontalSpacing(20)
		self.main_layout.setContentsMargins(20, 20, 20, 20)

		# R AND SAVE DIRECTORY FOLDERS
		# ///////////////////////////////////////////////////////////
		# icons
		r_icon = Logo(35, 25, get_imagepath('R_logo.svg', 'gui/images/icons'))
		folder_icon = Logo(30, 25, get_imagepath('folder_icon.svg', 'gui/images/icons'))
		
		# Lines
		self.r_directory = QLabel('<Selecione a pasta do executável R>')
		self.r_directory.setFixedHeight(25)
		self.r_directory.setObjectName('directory')
		self.r_directory.setCursor(Qt.PointingHandCursor)
		#
		self.save_directory = QLabel(parent.save_dir)
		self.save_directory.setFixedHeight(25)
		self.save_directory.setObjectName('directory')
		self.save_directory.setCursor(Qt.PointingHandCursor)

		# FIGURE PROPERTIES GROUBOX
		# ///////////////////////////////////////////////////////////
		groupbox = QGroupBox("Figura")
		groupbox_layout = QGridLayout(groupbox)
		groupbox_layout.setVerticalSpacing(20)
		groupbox_layout.setHorizontalSpacing(20)
		groupbox_layout.setContentsMargins(20, 20, 20, 20)

		# dpi
		dpi_label = QLabel('DPI')

		# proporcao
		prop_label = QLabel('Proporção')

		# ADD TO MAIN LAYOUT
		# ///////////////////////////////////////////////////////////
		self.main_layout.addWidget(parent.resources_list, 0, 0, 3, 1)
		self.main_layout.addWidget(r_icon, 0, 1, 1, 1)
		self.main_layout.addWidget(folder_icon, 1, 1, 1, 1)
		self.main_layout.addWidget(self.r_directory, 0, 2, 1, 1)
		self.main_layout.addWidget(self.save_directory, 1, 2, 1, 1)
		self.main_layout.addWidget(groupbox, 0, 3, 2, 1)

		# SETTING STYLESHEET
		self.setup_stylesheet(parent)

	def setup_stylesheet(self, parent):
		color_pallette = ['#20252a', '#394251', '#0d7bbd', '#d9e2f1']

		parent.setStyleSheet(f'''
			#openair_page {{
				background-color: {color_pallette[0]};
			}}
			#directory {{
				background-color: {color_pallette[1]};
				color: {color_pallette[-1]};
				font: normal 12pt 'Microsoft New Tai Lue';
				border-radius: 5px;
				vertical-align: middle;
				padding-left: 5px;
			}}
		''')