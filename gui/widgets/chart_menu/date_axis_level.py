# IMPORT QT MODULES
from qt_core import *

# IMPOORT CUSTOM WIDGETS
from gui.widgets.chart_menu.buttons import TopLevelButton

# IMPORT MODULES
import matplotlib.dates as mdates

class DateAxisTopLevel(QWidget):

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
		self.date_formatter.formatterChanged.connect(self.propertyChanged.emit)
		self.date_locator.locatorChanged.connect(self.propertyChanged.emit)
		self.font_size.valueChanged.connect(
			lambda x: self.propertyChanged.emit({'fontsize' : x})
		)
		self.rotation.valueChanged.connect(
			lambda x: self.propertyChanged.emit({'rotation' : x})
		)

	def toggle(self):
		hidden = self.top_level.getStatus()
		active = not hidden
	
		# toggle on (active) or off
		self.top_level.setActive(active)

		# SHOW/HIDDEN widgets
		self.date_formatter.setHidden(hidden)
		self.date_locator.setHidden(hidden)
		self.font_size.setHidden(hidden)
		self.rotation.setHidden(hidden)

		# size policty
		if active:
			self.setFixedHeight(self.item_height * 5)
		else:
			self.setFixedHeight(self.item_height)

	def setupUI(self):
		if not self.objectName():
			self.setObjectName("date_axis_top_level")

		self.main_layout = QVBoxLayout(self)
		self.main_layout.setContentsMargins(0, 0, 0, 0)
		self.main_layout.setSpacing(0)

		# OBJECTS
		self.top_level = TopLevelButton(text = "Eixo Horizontal", height = self.item_height)
		
		# DATE PROPERTIES
		self.date_locator = DateLocatorProperty(height= self.item_height)
		self.date_formatter = DateFormatterProperty(height = self.item_height)

		# FONT SIZE
		self.font_size = DateLabelProperty(text = "Tamanho da fonte", height = self.item_height, vmin = 1, vmax = 30)

		# ROTATION
		self.rotation = DateLabelProperty(text = 'Rotação (°)', height = self.item_height, vmin=0, vmax = 90)

		# add to layout
		self.main_layout.addWidget(self.top_level)
		self.main_layout.addWidget(self.date_locator)
		self.main_layout.addWidget(self.date_formatter)
		self.main_layout.addWidget(self.font_size)
		self.main_layout.addWidget(self.rotation)


class DateLocatorProperty(QFrame):
	
	locatorChanged = Signal(dict)
	def __init__(self, height):
		super().__init__()

		# SETTINGS
		self.setFixedHeight(height)

		# PROPERTIES
		self.locators =  {
			'Hora' : mdates.HourLocator,
			'Dia' : mdates.DayLocator,
			'Mês' : mdates.MonthLocator,
			'Ano' : mdates.YearLocator
		    }
		self.date_locator = QComboBox()
		self.frequency = QSpinBox()
		self.left_margin = 25

		# SETTING WIDGETS
		self.date_locator.addItems(list(self.locators.keys()))
		self.frequency.setRange(1, 100)

		# INIT
		self.setupUI()
		self.setupStyle()

		# SIGNALS
		self.date_locator.currentTextChanged.connect(self.emitValues)
		self.frequency.editingFinished.connect(self.emitValues)

	def emitValues(self):
		item = self.locators[self.date_locator.currentText()](interval = self.frequency.value())
		self.locatorChanged.emit({'locator' :  item})

	def setupUI(self):
		self.main_layout = QHBoxLayout(self)
		self.main_layout.setContentsMargins(self.left_margin, 3, 3, 3)
		self.main_layout.setSpacing(10)
		self.setObjectName('item')

		# TEXT
		self.line = QLabel('Frequência')
		self.line.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
		self.line.setObjectName('line')

		# LOCATOR
		self.date_locator.setObjectName('combobox')

		# FREQUENCY
		self.frequency.setObjectName('spinbox')

		# ADD TO MAIN LAYOUT
		self.main_layout.addWidget(self.line)
		self.main_layout.addWidget(self.frequency)
		self.main_layout.addWidget(self.date_locator)

	def setupStyle(self):
		self.setStyleSheet('''
			#item{
				background-color: transparent;
			}
			#spinbox, #combobox, #line {
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


class DateFormatterProperty(QFrame):
    
	formatterChanged = Signal(dict)
	def __init__(self, height):
		super().__init__()

		# settings
		self.setFixedHeight(height)

		# PROPERTIES
		self.formats = {
			'dd/mm/yyyy' : '%d/%m/%Y',
			'dd/mm/yyyy HH' : '%d/%m/%Y %Hh',
			'dd/mm/yyyy HH:MM' : '%d/%m/%Y %H:%M',
			'dd/mmm/yyyy' : "%d/%b/%Y",
			'mmm/yyyy' : "%b/%Y",
			'yyyy' : '%Y'
		}
		self.combobox = QComboBox()
		self.left_margin = 25

		# SETUP WIDGETS
		self.combobox.addItems(list(self.formats.keys()))
	
		# SETUP UI
		self.setupUI()
		self.setupStyle()

		# SIGNALS AND SLOTS
		self.combobox.currentTextChanged.connect(self.emitValue)

	def emitValue(self):
		item = self.formats[self.combobox.currentText()]
		self.formatterChanged.emit({'formatter': mdates.DateFormatter(item)})

	def setupUI(self):
		self.main_layout = QHBoxLayout(self)
		self.main_layout.setContentsMargins(self.left_margin, 3, 3, 3)
		self.main_layout.setSpacing(5)
		self.setObjectName('item')

		# TEXT
		self.line = QLabel('Formatação')
		self.line.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
		self.line.setObjectName('line')

		# FONTSIZE
		self.combobox.setObjectName('combobox')

		# ADD TO MAIN LAYOUT
		self.main_layout.addWidget(self.line)
		self.main_layout.addWidget(self.combobox)

	def setupStyle(self):
		self.setStyleSheet('''
			#item{
				background-color: transparent;
			}
			#combobox, #line {
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

		
class DateLabelProperty(QFrame):
	
	valueChanged = Signal(int)
	def __init__(self, text, vmin, vmax, height):
		super().__init__()
		
		# SETTINGS
		self.setFixedHeight(height)

		# PROPERTIES
		self.label = QLabel(text)
		self.spinbox = QSpinBox()
		self.left_margin = 25

		# SETTING WIDGETS
		self.spinbox.setRange(vmin, vmax)

		# SETUP UI
		self.setupUI()
		self.setupStyle()

		# SIGNALS
		self.spinbox.editingFinished.connect(self.emitValue)

	def emitValue(self):
		self.valueChanged.emit(self.spinbox.value())

	def setupUI(self):
		self.main_layout = QHBoxLayout(self)
		self.main_layout.setContentsMargins(self.left_margin, 3, 3, 3)
		self.main_layout.setSpacing(5)
		self.setObjectName('item')

		# TEXT
		self.label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
		self.label.setObjectName('line')

		# FONTSIZE
		self.spinbox.setObjectName('combobox')

		# ADD TO MAIN LAYOUT
		self.main_layout.addWidget(self.label)
		self.main_layout.addWidget(self.spinbox)

	def setupStyle(self):
		self.setStyleSheet('''
			#item{
				background-color: transparent;
			}
			#spinbox, #line{
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
		