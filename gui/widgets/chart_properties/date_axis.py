# IMPORT QT MODULES
from qt_core import *

# IMPORT MODULES
import matplotlib.dates as mdates

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
		self.main_layout.setContentsMargins(5, 5, 5, 5)
		self.main_layout.setSpacing(10)
		self.setObjectName('item')

		# TEXT
		self.line = QLabel('Frequência')
		self.line.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
		self.line.setObjectName('line')

		# LOCATOR
		self.date_locator.setObjectName('combobox')
		self.date_locator.setFixedSize(100, 25)

		# FREQUENCY
		self.frequency.setObjectName('spinbox')
		self.frequency.setFixedSize(50, 25)

		# ADD TO MAIN LAYOUT
		self.main_layout.addWidget(self.line)
		self.main_layout.addWidget(self.frequency)
		self.main_layout.addWidget(self.date_locator)

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
			#spinbox, #combobox {
				font: 500 11pt 'Microsoft New Tai Lue';
			}
		''')


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
			'dd/mmm/yyyy' : "%d-%b-%Y",
			'mmm/yyyy' : "%b-%Y",
			'yyyy' : '%Y'
		}
		self.combobox = QComboBox()

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
		self.main_layout.setContentsMargins(5, 5, 5, 5)
		self.main_layout.setSpacing(5)
		self.setObjectName('item')

		# TEXT
		self.line = QLabel('Formatação')
		self.line.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
		self.line.setObjectName('line')

		# FONTSIZE
		self.combobox.setObjectName('combobox')
		self.combobox.setFixedSize(150, 25)

		# ADD TO MAIN LAYOUT
		self.main_layout.addWidget(self.line)
		self.main_layout.addWidget(self.combobox)

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
			#combobox {
				font: 500 11pt 'Microsoft New Tai Lue';
			}
		''')
