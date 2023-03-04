# IMPORT QT MODULES
from qt_core import *

# IMPOORT CUSTOM WIDGETS
from gui.widgets.chart_menu.buttons import TopLevelButton

class NumericalAxisTopLevel(QWidget):

	propertyChanged = Signal(dict)
	def __init__(self, title, height):
		super().__init__()

		# PROPERTIES
		self.item_height = height
		self.title = title

		# SETUP UI
		self.setupUI()
		self.toggle()

		# SIGNALS
		self.top_level.clicked.connect(self.toggle)
		self.vmin.valueChanged.connect(
			lambda x: self.propertyChanged.emit({'min' : x})
		)
		self.vmax.valueChanged.connect(
			lambda x: self.propertyChanged.emit({'max' : x})
		)
		self.total_ticks.valueChanged.connect(
			lambda x: self.propertyChanged.emit({'size' : x})
		)
		self.font_size.valueChanged.connect(
			lambda x: self.propertyChanged.emit({'fontsize' : x})
		)

	def toggle(self):
		hidden = self.top_level.getStatus()
		active = not hidden
	
		# toggle on (active) or off
		self.top_level.setActive(active)

		# show/hide widgets
		self.vmax.setHidden(hidden)
		self.vmin.setHidden(hidden)
		self.total_ticks.setHidden(hidden)
		self.font_size.setHidden(hidden)

		if active:
			self.setFixedHeight(self.item_height * 5)
		else:
			self.setFixedHeight(self.item_height)
	
	def setupUI(self):
		if not self.objectName():
			self.setObjectName("numerical_axis_top_level")

		self.main_layout = QVBoxLayout(self)
		self.main_layout.setContentsMargins(0, 0, 0, 0)
		self.main_layout.setSpacing(0)

		# OBJECTS
		self.top_level = TopLevelButton(text = self.title, height = self.item_height)
		
		# Max and Min Values
		self.vmax = AxisProperty(text = "Máximo", height = self.item_height, spinbox = QDoubleSpinBox())
		self.vmin = AxisProperty(text = "Mínimo", height = self.item_height, spinbox = QDoubleSpinBox())

		# NUMBER OF TICKS
		self.total_ticks = AxisProperty(text = "Rótulos", height = self.item_height, spinbox=QSpinBox())

		# FONT SIZE
		self.font_size = AxisProperty(text = "Tamanho da fonte", height = self.item_height, spinbox=QSpinBox())

		# add to layout
		self.main_layout.addWidget(self.top_level)
		self.main_layout.addWidget(self.vmax)
		self.main_layout.addWidget(self.vmin)
		self.main_layout.addWidget(self.total_ticks)
		self.main_layout.addWidget(self.font_size)


class AutoAdjustWidget(QWidget):
	
	def __init__(self, height, text, spinbox : QSpinBox):
		super().__init__()

		# settings
		self.setFixedHeight(height)

		# PROPERTIES
		self.text = text
		self.spinbox = spinbox
		self.left_margin = 25

		# SETUP UI
		self.setupUI()
		self.setupStyle()

		# SIGNALS AND SLOTS
		self.spinbox.editingFinished.connect(self.emitValue)

	def emitValue(self):
		self.valueChanged.emit(self.spinbox.value())

	def setupUI(self):
		self.main_layout = QHBoxLayout(self)
		self.main_layout.setContentsMargins(self.left_margin, 3, 3, 3)
		self.main_layout.setSpacing(5)
		self.setObjectName('item')

		# TEXT
		self.line = QLabel(self.text)
		self.line.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
		self.line.setObjectName('line')

		# FONTSIZE
		if isinstance(self.spinbox, QSpinBox):
			self.spinbox.setRange(1, 50)
		else:
			self.spinbox.setRange(-100000, 100000)
		self.spinbox.setObjectName('spinbox')

		# ADD TO MAIN LAYOUT
		self.main_layout.addWidget(self.line)
		self.main_layout.addWidget(self.spinbox)

	def setupStyle(self):
		self.setStyleSheet('''
			#item{
				background-color: transparent;
			}
			#line, #spinbox{
				font: normal 10pt 'Microsoft New Tai Lue';
			}
		''')

	def paintEvent(self, event: QPaintEvent) -> None:
		super().paintEvent(event)

		painter = QPainter()
		painter.begin(self)
		
		dx = 2
		x = (self.left_margin - dx) // 2
		y = 0
		dy = self.height()
		painter.fillRect(x, y, dx, dy, QColor('#36475f'))

		painter.end()

class AxisProperty(QWidget):
    
	valueChanged = Signal(object) # either a float or int
	def __init__(self, height, text, spinbox : QSpinBox):
		super().__init__()

		# settings
		self.setFixedHeight(height)

		# PROPERTIES
		self.text = text
		self.spinbox = spinbox
		self.left_margin = 25

		# SETUP UI
		self.setupUI()
		self.setupStyle()

		# SIGNALS AND SLOTS
		self.spinbox.editingFinished.connect(self.emitValue)

	def emitValue(self):
		self.valueChanged.emit(self.spinbox.value())

	def setupUI(self):
		self.main_layout = QHBoxLayout(self)
		self.main_layout.setContentsMargins(self.left_margin, 3, 3, 3)
		self.main_layout.setSpacing(5)
		self.setObjectName('item')

		# TEXT
		self.line = QLabel(self.text)
		self.line.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
		self.line.setObjectName('line')

		# FONTSIZE
		if isinstance(self.spinbox, QSpinBox):
			self.spinbox.setRange(1, 50)
		else:
			self.spinbox.setRange(-100000, 100000)
		self.spinbox.setObjectName('spinbox')

		# ADD TO MAIN LAYOUT
		self.main_layout.addWidget(self.line)
		self.main_layout.addWidget(self.spinbox)

	def setupStyle(self):
		self.setStyleSheet('''
			#item{
				background-color: transparent;
			}
			#line, #spinbox{
				font: normal 10pt 'Microsoft New Tai Lue';
			}
		''')

	def paintEvent(self, event: QPaintEvent) -> None:
		super().paintEvent(event)

		painter = QPainter()
		painter.begin(self)
		
		dx = 2
		x = (self.left_margin - dx) // 2
		y = 0
		dy = self.height()
		painter.fillRect(x, y, dx, dy, QColor('#36475f'))

		painter.end()
		