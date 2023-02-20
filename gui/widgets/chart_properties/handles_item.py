# IMPORT QT MODULES
from qt_core import *

# IMPORT CUSTOM WIDGETS
from gui.widgets.py_radio_button import PyCheckButton, PyRadioButton

class HandlesItem(QFrame):
    
	def __init__(self, text, height, *args, **kwargs):
		super().__init__(*args, **kwargs)

		# settings
		self.setFixedHeight(height)

		# PROPERTIES
		self.text = text

		# SETUP UI
		self.setupUI()
		self.setupStyle()


	def setupUI(self):
		self.main_layout = QHBoxLayout(self)
		self.main_layout.setContentsMargins(5, 0, 0, 0)
		self.main_layout.setSpacing(5)
		self.setObjectName('handle')

		# RADIO BUTTON
		self.button = PyRadioButton(height = self.height(), width = self.height())
		self.button.setObjectName('button')

		# TEXT
		self.label = QLabel(self.text)
		self.label.setObjectName('label')

		# ADD TO MAIN LAYOUT
		self.main_layout.addWidget(self.button)
		self.main_layout.addWidget(self.label)

	def setupStyle(self):
		self.setStyleSheet('''
			#handle{
				background-color: #fafafa;
				border: 1px solid #dcdcdc;
				border-radius: 3px;
			}
			#label{
				background-color: transparent;
				font: 500 10pt 'Microsoft New Tai Lue';
				color: #4f6375;
				padding-left: 5px;
			}
		''')
