# IMPORT QT MODULES
from qt_core import *

# IMPORT CUSTOM FUNCTIONS
from backend.misc.functions import get_imagepath

class TopLevelButton(QPushButton):

	def __init__(
			self,
			icon_name,
			height = 40,
			text = '',
			padding_left = 55,
			text_color = '#d7e0ef',
			button_color = '#36475f',
			hover_color = '#30415a',
			active_color = '#2a394f',
			highlight = '#00ccff'
		):

		# PROPERTIES
		self.is_active = False
		self.left_margin = 5
		self.text_padding = padding_left
		self.spacing = 5
		self.text_color = text_color
		self.button_color = button_color
		self.hover_color = hover_color
		self.active_color = active_color
		self.highlight_color = highlight

		# CONSTRUCTOR
		super().__init__(text)

		# SETTINGS
		self.setFixedHeight(height)
		self.setupStyle()
		self.setImage(icon_name)


	def setupStyle(self):
		self.setStyleSheet(f'''
			QPushButton {{
				background-color: {self.button_color};
				color: {self.text_color};
				font: bold 13pt 'Microsoft New Tai Lue';
				padding-left: {self.text_padding};
				text-align: left;
				border: none;
			}}
			QPushButton:hover {{
				background-color: {self.hover_color};
			}}
			QPushButton:disabled {{
				background-color: {self.active_color};
			}}
			QPushButton:pressed {{
				background-color: {self.active_color};
			}}
		''')

	def setImage(self, icon_name):
		icon_path = get_imagepath(icon_name, 'gui\images\icons')
		icon = QPixmap(icon_path)

		# adjusting icon dimensions
		icon_dx, icon_dy = icon.width(), icon.height()
		scale_width = icon_dx >= icon_dy
		rect = QRect(0, 0, self.text_padding - self.left_margin - self.spacing, self.height())
		available_width = 30
		available_height = 30

		if scale_width:
			# uses width as reference
			self.dx = available_width
			self.dy = self.dx * icon_dy // icon_dx

			# position
			self.x = self.left_margin + (rect.width() - available_width) // 2
			self.y = (rect.height() - self.dy) // 2 # margins

		else:
			# uses height as reference
			self.dy = available_height
			self.dx = self.dy * icon_dx // icon_dy

			# position
			self.y = (rect.height() - available_height) // 2
			self.x = (rect.width() - self.dx) // 2  + self.left_margin # margins

		# scale icon ot dimensions
		self.icon = icon.scaled(self.dx, self.dy, Qt.AspectRatioMode.IgnoreAspectRatio, Qt.TransformationMode.SmoothTransformation)

	def setActive(self, status : bool):
		self.setDisabled(status)
		self.is_active = status

	def paintEvent(self, event: QPaintEvent) -> None:
		# Return default style
		QPushButton.paintEvent(self, event)

		# Painter
		qp = QPainter()
		qp.begin(self)
		qp.setRenderHint(QPainter.Antialiasing)
		qp.setPen(Qt.NoPen)
		
		# draw icon
		self.draw_icon(qp, self.text_color)
		
		# PAINT LEFT BORDER IF ACTIVE
		if self.is_active:
			qr = self.rect()
			qr.setWidth(self.left_margin)
			qp.fillRect(qr, QBrush(QColor(self.highlight_color)))

		qp.end()

	def draw_icon(self, qp, color):                
		# draw icon
		painter = QPainter(self.icon)
		painter.setCompositionMode(QPainter.CompositionMode_SourceIn)
		painter.fillRect(self.icon.rect(), color)

		qp.drawPixmap(self.x, self.y, self.dx, self.dy, self.icon)
		
		painter.end()