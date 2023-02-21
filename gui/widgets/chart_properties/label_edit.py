# IMPORT QT MODULES
from qt_core import *


class LabelEdit(QFrame):
    
	labelEdited = Signal(list)
	def __init__(self, text, height, prop, *args, **kwargs):
		super().__init__(*args, **kwargs)

		# settings
		self.setFixedHeight(height)

		# PROPERTIES
		self.text = text
		self.property = prop

		# SETUP UI
		self.setupUI()
		self.setupStyle()

		# SIGNALS AND SLOTS
		self.line.editingFinished.connect(self.emitSignal)
		self.bold.clicked.connect(self.emitSignal)
		self.fontsize.valueChanged.connect(self.emitSignal)

	def emitSignal(self):
		# texto, negrito, font size, property
		this = [self.line.text(), self.bold.isChecked(), self.fontsize.value(), self.property]
		self.labelEdited.emit(this)

	def setupUI(self):
		self.main_layout = QHBoxLayout(self)
		self.main_layout.setContentsMargins(5, 5, 5, 5)
		self.main_layout.setSpacing(5)
		self.setObjectName('item')

		# TEXT
		self.line = QLineEdit()
		self.line.setPlaceholderText(self.text)
		self.line.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
		self.line.setObjectName('label_edit')

		# BOLD
		self.bold = QPushButton('B')
		self.bold.setCheckable(True)
		self.bold.setObjectName('bold_button')
		self.bold.setFixedSize(25, 25)

		# FONTSIZE
		self.fontsize = QSpinBox()
		self.fontsize.setRange(0, 50)
		self.fontsize.setObjectName('fontsize')
		self.fontsize.setFixedSize(40, 25)

		# ADD TO MAIN LAYOUT
		self.main_layout.addWidget(self.line)
		self.main_layout.addWidget(self.bold)
		self.main_layout.addWidget(self.fontsize)

	def setupStyle(self):
		self.setStyleSheet('''
			#item{
				background-color: #fafafa;
				border: 1px solid #dcdcdc;
			}
			#label_edit{
				font: 500 11pt 'Microsoft New Tai Lue';
				padding-left: 5px;
			}
			#bold_button {
				font: 600 11pt 'Microsoft New Tai Lue';
			}
		''')
