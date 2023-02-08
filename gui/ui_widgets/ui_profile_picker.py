# IMPORT QT MODULES
from qt_core import *

class UI_ProfilePicker(object):

	def setup_ui(self, parent : QWidget):
		if not parent.objectName():
			parent.setObjectName('profile_picker')

		# MAIN LAYOUT
		self.main_layout = QGridLayout(parent)
		self.main_layout.setContentsMargins(10, 10, 10, 10)
		self.main_layout.setSpacing(5)

		# TOP HEADER
		# ////////////////////
		
		# LABEL
		self.label = QLabel("Perfil")
		self.label.setFixedHeight(25)
		self.label.setMinimumWidth(50)
		self.label.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Fixed)

		# Add button
		self.add_button = QPushButton('+')
		self.add_button.setFixedSize(25, 25)

		# REMOVE BUTTON
		self.remove_button = QPushButton('-')
		self.remove_button.setFixedSize(25, 25)

		# ADDING TO MAIN LAYOUT
		# ////////////////////////

		self.main_layout.addWidget(self.label, 0, 0)
		self.main_layout.addWidget(self.add_button, 0, 1, Qt.AlignmentFlag.AlignRight)
		self.main_layout.addWidget(self.remove_button, 0, 2, Qt.AlignmentFlag.AlignRight)
		self.main_layout.addWidget(parent.list, 1, 0, 1, 3)
		
		# STYLE
		self.setup_style()

	def setup_style(self):
		text_color = '#1c1c1c'
		font_family = 'Microsoft New Tai Lue'

		label_style = f'font: 500 16pt {font_family}; color: {text_color};'
		btn_style = f'''
			QPushButton {{
				font: 500 16pt {font_family};
				color: {text_color};
				border: 1px solid #c7c7c7;
				border-radius: 2px;
				background-color: #fafafa;
			}}
			QPushButton:hover{{
				background-color: #e4e4e4;
			}}
			QPushButton:pressed{{
				background-color: #c1c1c1;
			}}
		'''

		
		# SETTING UP
		self.label.setStyleSheet(label_style)
		self.add_button.setStyleSheet(btn_style)
		self.remove_button.setStyleSheet(btn_style)

