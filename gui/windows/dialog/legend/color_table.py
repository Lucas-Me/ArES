# IMPORT QT MODULE
from qt_core import *

# IMPORT BUILT-IN MODULES
from random import randint

class ColorTable(QWidget):
	'''A table in which each cell is a color'''

	colorSelected = Signal(object)
	def __init__(self):
		super().__init__()

		# PROPERTIES
		self.nrows = 6
		self.ncols = 8

		# SETTINGS
		self.setupUI()

	def setupUI(self):
		self.main_layout = QGridLayout(self)
		self.main_layout.setSpacing(5)
		self.main_layout.setContentsMargins(5, 5, 5, 5)

		# ADDING A FRAME FOR EACH CELL
		for row in range(self.nrows):
			for col in range(self.ncols):
				color = QColor(randint(0, 255), randint(0, 255), randint(0, 255))
				widget = ColorCell(color)

				# signal
				widget.clicked.connect(
					lambda x: self.colorSelected.emit(x)
				)

				# add to layout
				self.main_layout.addWidget(widget, row, col)


class ColorCell(QWidget):

	clicked = Signal(object)
	def __init__(self, color : QColor):
		super().__init__()

		# stylesheet
		self.color = color
		self.setStyleSheet(f'background-color: {color.name()}; border: 1px solid black;')

	
	def mousePressEvent(self, event: QMouseEvent) -> None:
		super().mousePressEvent(event)

		self.clicked.emit(self.color)
	
	def paintEvent(self, event: QPaintEvent) -> None:
		# super().paintEvent(event)

		opt = QStyleOption()
		opt.initFrom(self)
		p = QPainter(self)
		self.style().drawPrimitive(QStyle.PE_Widget, opt, p, self)