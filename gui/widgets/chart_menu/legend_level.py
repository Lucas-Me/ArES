# IMPORT QT MODULEs
from qt_core import *

# IMPORT CUSTOM WIDGETS
from gui.widgets.chart_menu.buttons import TopLevelButton

class LegendTopLevel(QWidget):

	propertyChanged = Signal(dict)
	def __init__(self, height):
		super().__init__()

		# PROPERTIES
		self.item_height = height

		# SETUP UI
		self.setupUI()
		self.toggle()

		# SIGNALS
		self.top_level.clicked.connect(self.toggle)
		self.column_count.valueChanged.connect(
			lambda x: self.propertyChanged.emit({'ncol': x})
		)
		self.font_size.valueChanged.connect(
			lambda x: self.propertyChanged.emit({'fontsize': x})
		)


	def toggle(self):
		hidden = self.top_level.getStatus()
		active = not hidden
	
		# toggle on (active) or off
		self.top_level.setActive(active)

		# show/hide widgets
		self.column_count.setHidden(hidden)
		self.font_size.setHidden(hidden)

		# size policty
		if active:
			self.setFixedHeight(self.item_height * 3)
		else:
			self.setFixedHeight(self.item_height)

	def setupUI(self):
		if not self.objectName():
			self.setObjectName("legend_top_level")

		self.main_layout = QVBoxLayout(self)
		self.main_layout.setContentsMargins(0, 0, 0, 0)
		self.main_layout.setSpacing(0)

		# OBJECTS
		self.top_level = TopLevelButton(text = "Legenda", height = self.item_height)
		
		# Column count
		self.column_count = LegendProperty(text = "Colunas", height = self.item_height, vmin = 1, vmax = 8)

		# FONT SIZE
		self.font_size = LegendProperty(text = "Tamanho da fonte", height = self.item_height, vmin = 1, vmax = 50)

		# add to layout
		self.main_layout.addWidget(self.top_level)
		self.main_layout.addWidget(self.column_count)
		self.main_layout.addWidget(self.font_size)


class LegendProperty(QWidget):
	
	valueChanged = Signal(int)
	def __init__(self, text, vmin, vmax, height):
		super().__init__()

		# PROPERTIES
		self.left_margin = 25
		self.label = QLabel(text)
		self.spinbox = QSpinBox()

		# SETTING WIDGETS
		self.spinbox.setRange(vmin, vmax)
		self.setFixedHeight(height)

		# SETUP UI
		self.setupUI()
		self.setupStyle()

		# SIGNALS
		self.spinbox.valueChanged.connect(self.emitValue)

	def emitValue(self):
		value = self.spinbox.value()
		self.valueChanged.emit(value)

	def setupUI(self):
		self.main_layout = QHBoxLayout(self)
		self.main_layout.setContentsMargins(self.left_margin, 3, 3, 3)
		self.main_layout.setSpacing(5)
		self.setObjectName('item')

		# TEXT
		self.label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
		self.label.setObjectName('text')

		# FONTSIZE
		self.spinbox.setObjectName('combobox')
		self.spinbox.setFixedSize(50, 25)

		# ADD TO MAIN LAYOUT
		self.main_layout.addWidget(self.label)
		self.main_layout.addWidget(self.spinbox)

	def setupStyle(self):
		self.setStyleSheet(f'''
			#item{{
				background-color: transparent;
				border: none;
			}}
			#text, #spinbox{{
				font: normal 10pt 'Microsoft New Tai Lue';
			}}
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
		