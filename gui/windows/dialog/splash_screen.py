# IMPORT QT MODULES
from qt_core import *

# IMPORT CUSTOM FUNCTIONS
from backend.misc.functions import get_imagepath, drawShadow

class SplashScreen(QMainWindow):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		# PROPERTIES
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
		self.setFixedSize(300, 300)
		self.setStructure()
		self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint | Qt.NoDropShadowWindowHint)
		self.setAttribute(Qt.WA_DeleteOnClose, True)
		self.setAttribute(Qt.WA_TranslucentBackground, True)

	def setStructure(self):
		#
		self.main_frame = QFrame()
		self.main_frame.setStyleSheet(f'background-color: {self.background_color}; border-radius:10px')
		margin = 5
		self.main_frame.setFixedSize(self.width() - margin * 2, self.height() - margin* 2)
		#
		self.main_layout = QVBoxLayout(self.main_frame)
		self.main_layout.setContentsMargins(0, 0, 0, 0)
		self.main_layout.setSpacing(10)
		
		# LOGO
		self.logo = SoftwareLogo(self.logo_width, 'ArES_logo_2.svg', self.logo_color)

		# ADD TO MAIN LAYOUT
		self.main_layout.addWidget(self.logo)
		self.main_layout.setAlignment(self.logo, Qt.AlignmentFlag.AlignCenter)
		self.setCentralWidget(self.main_frame)
		self.setContentsMargins(margin, margin, margin, margin)

	def paintEvent(self, event: QPaintEvent) -> None:
		painter = QPainter(self)
		drawShadow(
			painter,
			10,
			2.0,
			QColor(120, 120, 120, 32),
			QColor(255, 255, 255, 0),
			0.0,
			1.0,
			0.6,
			self.width(),
			self.height()
		)

		
# class ProgressBar(QWidget):

# 	def __init__(self, width, height, color, max_value):
# 		super().__init__()

# 		# PROPERTIES
# 		self.value = 0
# 		self.max_value = max_value
# 		self.margins = 2

# 		# VARIABLES
# 		self.progress_width = width - self.margins * 2
# 		self.progress_height = height - self.margins * 2
# 		self.pen = QPen()
# 		self.brush = QBrush()

# 		# SETTINGS
# 		self.setFixedSize(width, height)
# 		self.pen.setColor(QColor(color))
# 		self.brush.setColor(QColor(color))
# 		self.brush.setStyle(Qt.SolidPattern)

# 	def updateValue(self, value):
# 		self.value = value
# 		self.update()

# 	def getValue(self):
# 		return self.value

# 	def paintEvent(self, event: QPaintEvent) -> None:
# 		width = self.width()
# 		height = self.height()
# 		#
# 		width2 = self.progress_width
# 		height2 = self.progress_height

# 		# PAINTER
# 		paint = QPainter()
# 		paint.begin(self)
# 		paint.setRenderHint(QPainter.Antialiasing)

# 		# CREATE RECTANGLE
# 		rect = QRect(0, 0, width, height)
# 		paint.setBrush(Qt.NoBrush)
# 		paint.setPen(self.pen)
# 		paint.drawRect(rect)

# 		# PAINTER FOR PROFRESS
# 		# paint.setBrush(self.brush)
# 		paint.setPen(Qt.NoPen)

# 		# CREATE PROGRESS RECTANGLE
# 		progress = self.value / self.max_value * width2
# 		rect2 = QRect(self.margins, self.margins, progress, height2)
# 		paint.fillRect(rect2, self.brush)

# 		# END
# 		paint.end()


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