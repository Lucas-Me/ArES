# IMPORT QT MODULE
from qt_core import *
import os, json

# IMPORT SETTINGS
import backend.misc.settings as settings


class CustomColorTable(QWidget):
	'''A table in which each cell is a color'''

	colorSelected = Signal(object)
	saveColor = Signal(object)
	def __init__(self):
		super().__init__()

		# PROPERTIES
		self.nrows = len(settings.SETTINGS['cores'])
		self.ncols = len(settings.SETTINGS['cores'][0])
		self.colorsChanged = False

		# SETTINGS
		self.setupUI()

		# SIGNALS AND SLOTS
		self.update_color_button.clicked.connect(self.updateColor)

	def updateColor(self):
		self.update_color_button.setDisabled(True)

	def colorClicked(self, widget):
		if self.update_color_button.isEnabled():
			self.colorSelected.emit(widget.getColor())

		else:
			self.saveColor.emit(widget)
			self.colorsChanged = True
			self.update_color_button.setDisabled(False)

	def setupUI(self):
		self.main_layout = QGridLayout(self)
		self.main_layout.setSpacing(5)
		self.main_layout.setContentsMargins(5, 5, 5, 5)

		# LABEL
		self.label = QLabel("Cores personalizadas")
		self.label.setObjectName("label")
		self.main_layout.addWidget(self.label, 0, 1, 1, self.ncols - 1, Qt.AlignmentFlag.AlignLeft)
	
		# ADDING A FRAME FOR EACH CELL
		cores = settings.SETTINGS['cores']
		for row in range(self.nrows):
			for col in range(self.ncols):
				# creating RGB
				color = QColor(cores[row][col])

				# creating QColor and Widget
				widget = ColorCell(color, row, col)

				# signal
				widget.clicked.connect(self.colorClicked)

				# add to layout
				self.main_layout.addWidget(widget, row + 1, col)

		# update custom color
		self.update_color_button = QPushButton("Adicionar cor")
		self.update_color_button.setObjectName('button')
		self.main_layout.addWidget(self.update_color_button, self.nrows + 2, 0, 1, self.ncols)
		
		self.setupStyle()

	def setupStyle(self):
		color = '#303030'
		font_family = 'Microsoft New Tai Lue'
		hover_color = '#e4e4e4'
		pressed_color ='#c1c1c1'

		self.setStyleSheet(f'''
			#label{{
				font: 12pt normal '{font_family}';
				color: {color};
			}}
			#button{{
				background-color: #fafafa;
				font: 500 12pt '{font_family}';
				color: #4ca0e0;
				border-radius: 4px;
				border: 1px solid #4ca0e0;
			}}
			#button:hover{{
				background-color: {hover_color};
			}}
			#button:pressed{{
				background-color: {pressed_color};
			}}
			#button:disabled{{
				background-color: #dfdfdf;
				color: #8f8f8f;
				border-color: #8f8f8f;
			}}
		''')

	def exportSettings(self):
		if self.colorsChanged:
			# IMPORTAR E ATUALIZAR AS CONFIGURACOES, SE UMA MUDANCA FOI FEITA
			userhome_directory = os.path.expanduser("~")
			ArES_dir = os.path.join(userhome_directory, '.ArES')
			fname = os.path.join(ArES_dir, 'config.json')

			# reading config file
			with open(fname, 'r', encoding='utf-8') as f:
				existing_data = json.load(f)
			
			existing_data['cores'] = settings.SETTINGS['cores']

			# saving
			with open(fname, 'w', encoding='utf-8') as f:
				json.dump(existing_data, f, ensure_ascii=False, indent=4)


class ColorCell(QWidget):

	clicked = Signal(object)
	def __init__(self, color : QColor, row, col):
		super().__init__()

		self.row = row
		self.col = col

		# stylesheet
		self.color = color
		self.setStyleSheet(f'background-color: {color.name()}; border: 1px solid black;')

		# SETTINGS
		self.setObjectName('color_cell')

	def setColor(self, color: QColor):
		self.color = color
		settings.SETTINGS['cores'][self.row][self.col] = color.name()
		self.setStyleSheet(f'background-color: {color.name()}; border: 1px solid black;')

	def getColor(self):
		return self.color
	
	def mousePressEvent(self, event: QMouseEvent) -> None:
		super().mousePressEvent(event)

		self.clicked.emit(self)
	
	def paintEvent(self, event: QPaintEvent) -> None:
		# super().paintEvent(event)

		opt = QStyleOption()
		opt.initFrom(self)
		p = QPainter(self)
		self.style().drawPrimitive(QStyle.PE_Widget, opt, p, self)