# IMPORT QT MODULES
from qt_core import *


class TopLevelItem(QFrame):
    
	def __init__(self, text, height, *args, **kwargs):
		super().__init__(*args, **kwargs)

		# settings
		self.setFixedHeight(height)

		# PROPERTIES
		self.text = text
		self.isExpanded = False

		# SETUP UI
		self.setupUI()
		self.setupStyle()

	def setupUI(self):
		self.main_layout = QHBoxLayout(self)
		self.main_layout.setContentsMargins(0, 0, 0, 0)
		self.main_layout.setSpacing(0)
		self.setObjectName('top_level')

		# TEXT
		self.label = QLabel(self.text)
		self.label.setObjectName('label')

		# ADD TO MAIN LAYOUT
		self.main_layout.addWidget(self.label)

	def setupStyle(self):
		self.setStyleSheet('''
			#top_level{
				background-color: #fafafa;
				border: 1px solid #dcdcdc;
				border-radius: 3px;
			}
			#label{
				background-color: transparent;
				font: 500 14pt 'Microsoft New Tai Lue';
				color: #4f6375;
				padding-left: 5px;
			}
		''')


