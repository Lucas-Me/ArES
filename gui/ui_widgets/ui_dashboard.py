# IMPORT QT_CORE
from qt_core import *

# IMPORT CUSTOM WIDGETS
from backend.plot.visualization import AbstractCanvas

# Data Manager Page UI Class
class UI_Dashboard(object):
    
	def setup_ui(self, parent : QWidget):
		
		if not parent.objectName():
			parent.setObjectName(u'dashboard')

		# CENTRAL LAYOUT
		self.main_layout = QHBoxLayout(parent)
		self.main_layout.setContentsMargins(0, 0, 0, 0)
		self.main_layout.setSpacing(0)

		# CANVAS AND MENU
		# ////////////////////////////////////////////////////////////////
		
		# CANVAS
		self.canvas = AbstractCanvas()

		# RIGHT MENU
		self.right_menu = QFrame()
		self.right_menu.setObjectName('right_menu')
		self.right_menu.setFixedWidth(200)

		# ADD TO MAIN LAYOUT
		# /////////////////////////////////////////////////////////////
		self.main_layout.addWidget(self.canvas)
		self.main_layout.addWidget(self.right_menu)

		# STYlE
		self.setup_stylesheet(parent)

	def setup_stylesheet(self, parent : QWidget):
		bg_color = '#ededed'

		parent.setStyleSheet(f'''
			#right_menu {{
				background-color: #6daaab;
			}}
		''')
