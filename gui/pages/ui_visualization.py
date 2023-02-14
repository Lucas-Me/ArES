# IMPORT QT_CORE
from qt_core import *

# IMPORT CUSTOM WIDGETS
from backend.plot.visualization import AbstractCanvas

# Data Manager Page UI Class
class UI_DataVisualization(object):
    
	def setup_ui(self, parent : QWidget):
		
		if not parent.objectName():
			parent.setObjectName(u'visualization_page')

		# CENTRAL LAYOUT
		self.main_layout = QVBoxLayout(parent)
		self.main_layout.setContentsMargins(0, 0, 0, 0)
		self.main_layout.setSpacing(0)
		
		# TOP FRAME
		# /////////////////////////////////////////////
		self.top_frame = QFrame()
		self.top_frame.setFixedHeight(35)
		self.top_frame.setObjectName('top_frame')
		
		# layout
		self.top_frame_layout = QHBoxLayout(self.top_frame)

		# CENTRAL LAYOUT
		# ////////////////////////////////////////////
		self.central_layout = QHBoxLayout()
		self.central_layout.setContentsMargins(0, 0, 0, 0)
		self.central_layout.setSpacing(0)

		# CANVAS
		self.canvas = AbstractCanvas()

		# RIGHT MENU
		self.right_menu = QFrame()
		self.right_menu.setObjectName('right_menu')
		self.right_menu.setFixedWidth(200)

		# add to central layout
		self.central_layout.addWidget(self.canvas)
		self.central_layout.addWidget(self.right_menu)

		# ADD TO CENTRAL LAYOUT
		# ///////////////////////////////////////////
		self.main_layout.addWidget(self.top_frame)
		self.main_layout.addLayout(self.central_layout)

		# STYlE
		self.setup_stylesheet(parent)

	def setup_stylesheet(self, parent : QWidget):
		bg_color = '#ededed'

		parent.setStyleSheet(f'''
			#top_frame {{
				background-color: {bg_color};
			}}
			#right_menu {{
				background-color: #6daaab;
			}}
		''')
