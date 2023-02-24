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

class ChartButton(QPushButton):

	def __init__(
			self,
			height = 40,
			text = '',
			text_color = '#36475f',
			button_color = '#ffffff',
			hover_color = '#edf0f5',
			active_color = '#d9e2f1',
			highlight = '#00ccff'
		):

		# PROPERTIES
		self.is_active = False
		self.left_margin = 5
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

	def setupStyle(self):
		self.setObjectName('chart')
		self.setStyleSheet(f'''
			QPushButton {{
				background-color: {self.button_color};
				color: {self.text_color};
				font: normal 11pt 'Microsoft New Tai Lue';
				padding-left: 15px;
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

	def setActive(self, status : bool):
		self.setDisabled(status)
		self.is_active = status

	def paintEvent(self, event: QPaintEvent) -> None:
		# Return default style
		QPushButton.paintEvent(self, event)

		# PAINT BUTTON IF ACTIVE
		if self.is_active:

			# Painter
			qp = QPainter()
			qp.begin(self)
			qp.setRenderHint(QPainter.Antialiasing)
			qp.setPen(Qt.NoPen)
			
			# PAINT LEFT BORDER IF ACTIVE
			qr = self.rect()
			qr.setWidth(self.left_margin)
			qp.fillRect(qr, QBrush(QColor(self.highlight_color)))

			qp.end()


class CreateChartButton(QFrame):

	createRow = Signal(str)
	def __init__(
		self,
		height = 40
		):
		super().__init__()

		# PROPERTIES
		self.is_active = True
		self.placeholder = 'Novo Gráfico'

		# SETTINGS
		self.setFixedHeight(height)
		self.setupUI()
		self.setupStyle()

		# SIGNALS
		self.add_button.clicked.connect(self.emitSignal)

	def emitSignal(self, text):
		text = self.edit.text()
		if len(text) == 0:
			text = self.edit.placeholderText()

		self.createRow.emit(text)

	def setupUI(self):
		self.main_layout = QHBoxLayout(self)
		self.main_layout.setSpacing(0)
		self.main_layout.setContentsMargins(0, 0, 0, 0)

		# SYMBOL
		self.label = QLabel('+')
		self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
		self.label.setFixedSize(20, self.height())
		self.label.setObjectName('icon')

		# LINE EDIT
		self.edit = QLineEdit()
		self.edit.setPlaceholderText(self.placeholder)
		self.edit.setObjectName('name_edit')
		self.edit.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

		# ADD BUTTON
		self.add_button = QPushButton("Add")
		self.add_button.setObjectName('add_button')
		self.add_button.setFixedSize(self.height(), self.height())
		
		# ADD TO MAIN LAYOUT
		self.main_layout.addWidget(self.label)
		self.main_layout.addWidget(self.edit)
		self.main_layout.addWidget(self.add_button)


	def setupStyle(self):
		self.setStyleSheet('''
			#icon {
				background-color: #067fbd;
				color: #d9e2f1;
				font: bold 14pt 'Microsoft New Tai Lue';
				border: none;
			}
			#name_edit {
				background-color: #067fbd;
				color: #d9e2f1;
				font: bold 10pt 'Microsoft New Tai Lue';
				border: none;
			}
			#add_button {
				background-color: #0c92e6;
				color: #d9e2f1;
				font: bold 9pt 'Microsoft New Tai Lue';
				border: none;
			}
			#add_button:hover {
				background-color: #067fbd;
			}
			#add_button:pressed {
				background-color: #067fbd;
			}
		''')
