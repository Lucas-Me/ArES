# IMPORT QT MODULES
from qt_core import *

class AxisProperty(QFrame):
    
	valueChanged = Signal(object)

	def __init__(self, height, text, spinbox : QSpinBox, property_, *args, **kwargs):
		super().__init__(*args, **kwargs)

		# settings
		self.setFixedHeight(height)

		# PROPERTIES
		self.text = text
		self.spinbox = spinbox
		self.property = property_

		# SETUP UI
		self.setupUI()
		self.setupStyle()

		# SIGNALS AND SLOTS
		self.spinbox.editingFinished.connect(self.emitValue)

	def emitValue(self):
		self.valueChanged.emit([self.spinbox.value(), self.property])

	def setupUI(self):
		self.main_layout = QHBoxLayout(self)
		self.main_layout.setContentsMargins(5, 5, 5, 5)
		self.main_layout.setSpacing(5)
		self.setObjectName('item')

		# TEXT
		self.line = QLabel(self.text)
		self.line.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
		self.line.setObjectName('line')

		# FONTSIZE
		if isinstance(self.spinbox, QSpinBox):
			self.spinbox.setRange(0, 50)
		else:
			self.spinbox.setRange(-100000, 100000)
		self.spinbox.setObjectName('spinbox')
		self.spinbox.setFixedSize(100, 25)

		# ADD TO MAIN LAYOUT
		self.main_layout.addWidget(self.line)
		self.main_layout.addWidget(self.spinbox)

	def setupStyle(self):
		self.setStyleSheet('''
			#item{
				background-color: #fafafa;
				border: 1px solid #dcdcdc;
			}
			#line{
				font: 500 11pt 'Microsoft New Tai Lue';
				padding-left: 5px;
			}
			#spinbox {
				font: 500 11pt 'Microsoft New Tai Lue';
			}
		''')

class LegendProperty(QFrame):
	
	valueChanged = Signal(list)
	def __init__(self, text, vmin, vmax, prop):
		super().__init__()

		# PROPERTIES
		self.prop = prop
		self.label = QLabel(text)
		self.spinbox = QSpinBox()

		# SETTING WIDGETS
		self.spinbox.setRange(vmin, vmax)

		# SETUP UI
		self.setupUI()
		self.setupStyle()

		# SIGNALS
		self.spinbox.valueChanged.connect(self.emitValue)

	def emitValue(self):
		value = self.spinbox.value()
		self.valueChanged.emit([self.prop, value])

	def setupUI(self):
		self.main_layout = QHBoxLayout(self)
		self.main_layout.setContentsMargins(5, 5, 5, 5)
		self.main_layout.setSpacing(5)
		self.setObjectName('item')

		# TEXT
		self.label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
		self.label.setObjectName('line')

		# FONTSIZE
		self.spinbox.setObjectName('combobox')
		self.spinbox.setFixedSize(50, 25)

		# ADD TO MAIN LAYOUT
		self.main_layout.addWidget(self.label)
		self.main_layout.addWidget(self.spinbox)

	def setupStyle(self):
		self.setStyleSheet('''
			#item{
				background-color: #fafafa;
				border: 1px solid #dcdcdc;
			}
			#line{
				font: 500 11pt 'Microsoft New Tai Lue';
				padding-left: 5px;
			}
			#spinbox{
				font: 500 11pt 'Microsoft New Tai Lue';
			}
		''')