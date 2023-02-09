# IMPORT QT CORE
from qt_core import *

# IMPORT CUSTOM WIDGETS
from gui.widgets.color_triangle import QtColorTriangle


class UI_ProfileDialog(object):

	def setup_ui(self, parent : QDialog):
		if not parent.objectName():
			parent.setObjectName("profile_dialog")

		# MAIN LAYOUT
		self.main_layout = QGridLayout(parent)
		self.main_layout.setContentsMargins(10, 10, 10, 10)
		self.main_layout.setSpacing(10)

		# HEADER
		# /////////////////////////
		self.header_frame = QFrame()
		self.header_frame.setObjectName('header')

		# header layout
		self.header_layout = QHBoxLayout(self.header_frame)
		self.header_layout.setContentsMargins(0, 0, 0, 0)
		self.header_layout.setSpacing(0)

		# edit button
		self.edit_name = QPushButton()
		self.edit_name.setFixedSize(25, 25)
		self.edit_name.setObjectName('edit_name')

		# line edit
		self.name = QLineEdit()
		self.name.setFixedSize(170, 25)
		self.name.setObjectName('name')

		# color
		self.color_box = QFrame()
		self.color_box.setFixedSize(25, 25)
		self.color_box.setObjectName('color_box')

		# save button
		self.save_button = QPushButton('Salvar')
		self.save_button.setFixedSize(25, 25)
		self.save_button.setObjectName('save')

		# cancel button
		self.cancel_button = QPushButton('Cancelar')
		self.cancel_button.setFixedSize(25, 25)
		self.cancel_button.setObjectName('cancel')

		# add to header layout
		self.header_layout.addWidget(self.edit_name)
		self.header_layout.addWidget(self.name)
		self.header_layout.addWidget(self.color_box)
		self.header_layout.addWidget(self.save_button)
		self.header_layout.addWidget(self.cancel_button)
		#
		self.header_layout.setAlignment(self.edit_name, Qt.AlignmentFlag.AlignLeft)
		self.header_layout.setAlignment(self.name, Qt.AlignmentFlag.AlignLeft)
		self.header_layout.setAlignment(self.color_box, Qt.AlignmentFlag.AlignRight)
		self.header_layout.setAlignment(self.save_button, Qt.AlignmentFlag.AlignRight)
		self.header_layout.setAlignment(self.cancel_button, Qt.AlignmentFlag.AlignRight)

		# BOTTOM ITEMS
		# ///////////////////////////////////////

		# TABLE WIDGET
		self.table = QTableWidget()

		# 
		# self.color_widget = QWidget(parent)
		self.color_selector = QtColorTriangle()
		self.color_selector.set_color(QColor(255, 255, 255))
		self.color_selector.setMinimumWidth(parent.width() / 2)

		# SETTING UP MAIN LAYOUT
		# ///////////////////////////
		self.main_layout.addWidget(self.header_frame, 0, 0, 1, 2, Qt.AlignmentFlag.AlignTop)
		self.main_layout.addWidget(self.table, 1, 0, 1, 1)
		self.main_layout.addWidget(self.color_selector, 1, 1, 1, 1)

		
		# set style
		self.setup_style(parent)


	def setup_style(self, parent : QDialog):
		text_color = '#1c1c1c'
		font_family = 'Microsoft New Tai Lue'

		parent.setStyleSheet(f'''
			#profile_dialog{{
				background-color: white;
			}}
			#save_button, #cancel_button, #
		''')

