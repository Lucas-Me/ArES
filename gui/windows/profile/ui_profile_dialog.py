# IMPORT QT CORE
from qt_core import *

# IMPORT CUSTOM WIDGETS
from gui.widgets.color_triangle import QtColorTriangle
from gui.widgets.method_table import MethodTable

# IMPORT CUSTOM FUNCTIONS
from backend.misc.functions import get_imagepath

class UI_ProfileDialog(object):

	def setup_ui(self, parent : QDialog):
		if not parent.objectName():
			parent.setObjectName("profile_dialog")

		# MAIN LAYOUT
		self.main_layout = QHBoxLayout(parent)
		self.main_layout.setSpacing(0)
		self.main_layout.setContentsMargins(0, 0, 0, 0)

		self.frame = QFrame()
		self.frame.setFixedSize(parent.width() - parent.margins, parent.height() - parent.margins)
		self.frame.setObjectName('frame')
		#
		self.frame_layout = QGridLayout(self.frame)
		self.frame_layout.setContentsMargins(10, 10, 10, 10)
		self.frame_layout.setSpacing(10)
		self.frame_layout.setColumnStretch(0, 2)
		self.frame_layout.setColumnStretch(1, 1)
		
		# PROPERTIES
		w, h = self.frame.width(), self.frame.height()

		# HEADER
		# /////////////////////////
		self.header_frame = QFrame()
		self.header_frame.setObjectName('header')
		self.header_frame.setFixedHeight(40)

		# header layout
		self.header_layout = QHBoxLayout(self.header_frame)
		self.header_layout.setContentsMargins(0, 0, 0, 0)
		self.header_layout.setSpacing(0)

		# line edit
		self.name = QLineEdit()
		self.name.setFixedSize(w / 2, 25)
		self.name.setObjectName('name')
		self.name.setClearButtonEnabled(True)
		self.name.setPlaceholderText('Digite um nome..')
		image = QPixmap(get_imagepath('pencil.svg', 'gui/images/icons'))
		image.scaled(QSize(25, 25), Qt.AspectRatioMode.KeepAspectRatio)
		self.name.addAction(image, QLineEdit.LeadingPosition)

		# color
		self.color_view = QFrame()
		self.color_view.setFixedSize(25, 25)
		# self.color_view.setObjectName('color_view')

		# save button
		self.save_button = QPushButton('Salvar')
		self.save_button.setFixedSize(70, 25)
		self.save_button.setObjectName('save')

		# cancel button
		self.cancel_button = QPushButton('Cancelar')
		self.cancel_button.setFixedSize(70, 25)
		self.cancel_button.setObjectName('cancel')

		# add to header layout
		self.header_layout.addWidget(self.name)
		self.header_layout.addWidget(self.color_view)
		self.header_layout.addWidget(self.save_button)
		self.header_layout.addWidget(self.cancel_button)
		#
		self.header_layout.setAlignment(self.name, Qt.AlignmentFlag.AlignLeft)
		self.header_layout.setAlignment(self.color_view, Qt.AlignmentFlag.AlignRight)
		self.header_layout.setAlignment(self.save_button, Qt.AlignmentFlag.AlignRight)
		self.header_layout.setAlignment(self.cancel_button, Qt.AlignmentFlag.AlignRight)

		# BOTTOM ITEMS
		# ///////////////////////////////////////

		# TABLE WIDGET
		self.table = MethodTable()
		self.table.setObjectName('table')

		# COLOR SELECTOR
		self.color_selector = QtColorTriangle()
		self.color_selector.set_color(QColor(255, 255, 255))
		self.color_selector.setMinimumWidth(w / 3)

		# SETTING UP MAIN LAYOUT
		# ///////////////////////////
		self.frame_layout.addWidget(self.header_frame, 0, 0, 1, 2, Qt.AlignmentFlag.AlignTop)
		self.frame_layout.addWidget(self.table, 1, 0, 1, 1)
		self.frame_layout.addWidget(self.color_selector, 1, 1, 1, 1)

		self.main_layout.addWidget(self.frame)
		self.main_layout.setAlignment(self.frame, Qt.AlignmentFlag.AlignCenter)

		# set style
		self.setup_style(parent)


	def setup_style(self, parent : QDialog):
		text_color = '#1c1c1c'
		font_family = 'Microsoft New Tai Lue'
		hover_color = '#e4e4e4'
		pressed_color ='#c1c1c1'
		radius = 2

		parent.setStyleSheet(f'''
			#frame{{
				background-color: white;
			}}
			#save, #cancel{{
				background-color: #fafafa;
				font: 500 12pt {font_family};
				color: #4ca0e0;
				border-radius: 4px;
				border: 1px solid #4ca0e0;
			}}
			#save:hover, #cancel:hover{{
				background-color: {hover_color};
			}}
			#save:pressed, #cancel:pressed{{
				background-color: {pressed_color};
			}}
			#save:disabled, #cancel:disabled{{
				background-color: #dfdfdf;
				color: #8f8f8f;
				border-color: #8f8f8f;
			}}
			#name{{
				background-color: transparent;
				font: bold 13pt {font_family};
				color: {text_color};
				border: none;
			}}
			#header{{
				background-color: transparent;
				border-bottom: 1px solid #c7c7c7;
			}}
			#table{{
				background-color: transparent;
				border: none;
			}}
		''')


		self.color_view.setStyleSheet(f'background-color: red;border: none;border-radius: {radius}px')