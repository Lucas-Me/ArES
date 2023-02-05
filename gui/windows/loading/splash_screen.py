# IMPORT QT MODULES
from qt_core import *

# IMPORT CUSTOM FUNCTIONS
from backend.misc.functions import get_imagepath

class SplashScreen(QMainWindow):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		# PROPERTIES
		self.width = 300
		self.height = 300
		#
		self.background_color= '#1e374d'
		self.logo_color = 'white'
		self.progress_color = 'white'
		self.value = 0
		self.max_value = 100
		self.progress_width = 180
		self.progress_height = 15
		self.logo_width = 150
		self.enable_shadow = True

		# SETTINGS
		self.setFixedSize(self.width, self.height)
		self.setStructure()
		self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint | Qt.NoDropShadowWindowHint)
		self.setAttribute(Qt.WA_DeleteOnClose, True)

		# SIGNALS AND SLOTS
		self.slider.valueChanged.connect(self.updateProgress)

	def updateProgress(self, i):
		self.progress_bar.updateValue(i)
		if i == self.max_value: self.close()

	def setStructure(self):
		self.setStyleSheet(f'background-color: {self.background_color}')
		#
		self.main_layout = QVBoxLayout(self)
		self.main_layout.setContentsMargins(0, 40, 0, 40)
		self.main_layout.setSpacing(10)
		
		# LOGO
		self.logo = SoftwareLogo(self.logo_width, 'ArES_logo_2.svg', self.logo_color)

		# PROGRESS BAR
		self.progress_bar = ProgressBar(self.progress_width, self.progress_height, self.progress_color, self.max_value)

		# SLIDER
		self.slider = QSlider()
		self.slider.setRange(0, self.max_value)

		# ADD TO MAIN LAYOUT
		self.main_layout.addWidget(self.logo)
		self.main_layout.addWidget(self.progress_bar)
		self.main_layout.addWidget(self.slider)

		self.main_layout.setAlignment(self.logo, Qt.AlignmentFlag.AlignHCenter)
		self.main_layout.setAlignment(self.progress_bar, Qt.AlignmentFlag.AlignHCenter)
		self.main_layout.setAlignment(self.slider, Qt.AlignmentFlag.AlignHCenter)


class ProgressBar(QWidget):

	def __init__(self, width, height, color, max_value):
		super().__init__()

		# PROPERTIES
		self.value = 0
		self.max_value = max_value
		self.margins = 2

		# VARIABLES
		self.progress_width = width - self.margins * 2
		self.progress_height = height - self.margins * 2
		self.pen = QPen()
		self.brush = QBrush()

		# SETTINGS
		self.setFixedSize(width, height)
		self.pen.setColor(QColor(color))
		self.brush.setColor(QColor(color))
		self.brush.setStyle(Qt.SolidPattern)

	def updateValue(self, value):
		self.value = value
		self.update()

	def getValue(self):
		return self.value

	def paintEvent(self, event: QPaintEvent) -> None:
		width = self.width()
		height = self.height()
		#
		width2 = self.progress_width
		height2 = self.progress_height

		# PAINTER
		paint = QPainter()
		paint.begin(self)
		paint.setRenderHint(QPainter.Antialiasing)

		# CREATE RECTANGLE
		rect = QRect(0, 0, width, height)
		paint.setBrush(Qt.NoBrush)
		paint.setPen(self.pen)
		paint.drawRect(rect)

		# PAINTER FOR PROFRESS
		# paint.setBrush(self.brush)
		paint.setPen(Qt.NoPen)

		# CREATE PROGRESS RECTANGLE
		progress = self.value / self.max_value * width2
		rect2 = QRect(self.margins, self.margins, progress, height2)
		paint.fillRect(rect2, self.brush)

		# END
		paint.end()


class SoftwareLogo(QWidget):

	def __init__(self, width, image, color):
		super().__init__()

		self.image_name = image
		self.color = color

		# properties
		self.setFixedSize(width, width)

	def paintEvent(self, event: QPaintEvent) -> None:
		super().paintEvent(event)

		# Painter
		qp = QPainter()
		qp.begin(self)
		qp.setRenderHint(QPainter.Antialiasing)
		qp.setPen(Qt.NoPen)

		# format Path
		icon_path = get_imagepath(self.image_name, 'gui/images/icons')
		icon = QPixmap(icon_path)
		dx, dy = self.width(), self.height()

		# scale icon ot dimensions
		icon = icon.scaled(dx, dy, Qt.AspectRatioMode.IgnoreAspectRatio, Qt.TransformationMode.SmoothTransformation)
		
		# fill rect
		painter = QPainter(icon)
		painter.setCompositionMode(QPainter.CompositionMode_SourceIn)
		painter.fillRect(icon.rect(), self.color)

		qp.drawPixmap(icon.rect(), icon)
		qp.end()
		painter.end()