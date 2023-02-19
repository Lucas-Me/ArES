# IMPORT QT_CORE
from qt_core import *

# IMPORT CUSTOM WIDGETS
from backend.plot.visualization import TimeSeriesCanvas
from gui.widgets.py_push_button import IconButton

# Data Manager Page UI Class
class UI_Dashboard(object):
    
	def setup_ui(self, parent : QWidget):
		
		if not parent.objectName():
			parent.setObjectName(u'dashboard')

		# CENTRAL LAYOUT
		self.main_layout = QVBoxLayout(parent)
		self.main_layout.setContentsMargins(0, 0, 0, 10)
		self.main_layout.setSpacing(10)

		# CANVAS AND MENU
		# ////////////////////////////////////////////////////////////////
		self.canvas_layout = QHBoxLayout()
		self.canvas_layout.setContentsMargins(0, 0, 0, 0)
		self.canvas_layout.setSpacing(0)

		# CANVAS
		self.canvas = TimeSeriesCanvas()

		# RIGHT MENU
		self.right_menu = QFrame()
		self.right_menu.setObjectName('right_menu')
		self.right_menu.setFixedWidth(0)
		self.right_menu.hide()

		# add to layout
		self.canvas_layout.addWidget(self.canvas)
		self.canvas_layout.addWidget(self.right_menu)

		# BOTTOM TOOLBAR
		# //////////////////////////////////////////////////////////////
		self.toolbar_frame = QFrame()
		self.toolbar_frame.setObjectName('toolbar')
		self.toolbar_frame.setFixedHeight(50)
		self.toolbar_frame.setMinimumWidth(400)
		self.toolbar_frame.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Fixed)
		
		# Layout
		self.toolbar_layout = QHBoxLayout(self.toolbar_frame)
		self.toolbar_layout.setSpacing(5)
		self.toolbar_layout.setContentsMargins(5, 5, 5, 5)

		# TOGGLE MENU BUTTON
		self.toggle_menu = IconButton(
			height = 40,
			width = 40,
			icon_path= 'icon_menu.svg',
			icon_color = '#5d5d5d',
			paint_icon=True,
			hover_color= '#2a2a2a'
		)
		self.toggle_menu.setObjectName('toggle_menu')

		# add to layout
		self.toolbar_layout.addWidget(self.toggle_menu)

		# ADD TO MAIN LAYOUT
		# /////////////////////////////////////////////////////////////
		self.main_layout.addLayout(self.canvas_layout)
		self.main_layout.addWidget(self.toolbar_frame, alignment= Qt.AlignmentFlag.AlignHCenter)

		# STYlE
		self.setup_stylesheet(parent)

	def setup_stylesheet(self, parent : QWidget):
		bg_color = '#ededed'

		parent.setStyleSheet(f'''
			#dashboard {{
				background-color: #ffffff;
			}}
			#right_menu {{
				background-color: #6daaab;
				border: 1px solid #398d8f;
				border-bottom-left-radius: 10px;
			}}
			#toolbar{{
				background-color: #fafafa;
				border: 1px solid #dcdcdc;
				border-radius: 10px;
			}}
			#toggle_menu{{
				border: none;
				background-color: transparent;
			}}
		''')
