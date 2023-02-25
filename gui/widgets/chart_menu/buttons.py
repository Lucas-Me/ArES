# IMPORT QT MODULES
from qt_core import *

# IMPORT CUSTOM FUNCTIONS

class TopLevelButton(QPushButton):

	def __init__(
			self,
			height = 40,
			text = '',
			padding_left = 10,
			right_margin = 10,
			text_color = '#36475f',
			button_color = 'transparent',
			hover_color = '#edf0f5',
			pressed_color = '#d9e2f1'
		):

		# PROPERTIES
		self.text = text
		self.is_active = True
		self.text_padding = padding_left
		self.right_margin = right_margin
		self.text_color = text_color
		self.button_color = button_color
		self.hover_color = hover_color
		self.pressed_color = pressed_color
		self.font = QFont('Microsoft New Tai Lue', pointSize=12)

		# CONSTRUCTOR
		super().__init__()

		# SETTINGS
		self.setFixedHeight(height)
		self.setupStyle()

	def setupStyle(self):
		self.setStyleSheet(f'''
			QPushButton {{
				background-color: {self.button_color};
				border: none;
			}}
			QPushButton:hover {{
				background-color: {self.hover_color};
			}}
			QPushButton:pressed {{
				background-color: {self.pressed_color};
			}}
		''')

	def setGeometry(self):
		polygon_width = 10
		polygon_height = 10

		# coordinate points
		x1 = self.width() - self.right_margin
		x0 = x1 - polygon_width
		x2 = x1 - polygon_width // 2

		# coordinate points Y
		y1 = y0 = (self.height() - polygon_height) // 2
		y2 = y1 + polygon_height

		# triangle verices
		point0 = QPoint(x0, y0)
		point1 = QPoint(x1, y1)
		point2 = QPoint(x2, y2)

		return [point0, point1, point2]
	
	def setActive(self, status : bool):
		self.is_active = status

	def getStatus(self):
		return self.is_active

	def paintEvent(self, event: QPaintEvent) -> None:
		# Return default style
		QPushButton.paintEvent(self, event)

		# INIT PAINTER
		qp = QPainter()
		qp.begin(self)
		qp.setRenderHint(QPainter.Antialiasing)

		# draw text
		self.font.setBold(self.is_active)
		color = QColor(self.text_color)
		qp.setPen(QPen(color))
		qp.setFont(self.font)

		x = self.text_padding
		y = (self.height() - 12) // 2 + 12
		qp.drawText(x, y, self.text)

		# DRAW THE ACTIVE SYMBOL	
		if self.is_active:
			
			# Painter
			qp.setPen(Qt.NoPen)
			qp.setBrush(color)
			
			# get triangle vertices
			points = self.setGeometry()

			# draw triangle
			qp.drawConvexPolygon(points)

		qp.end()

