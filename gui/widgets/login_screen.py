# IMPORT QT CORE
from qt_core import *

# IMPORT CUSTOM UI
from gui.pages.ui_loginscreen import UI_LoginScreen

# IMPORT CUSTOM FUCTIONS
from backend.misc.functions import get_imagepath

# Data Manager Page Class
class LoginScreen(QWidget):

	def __init__(self):
		super().__init__()

		# LOGO
		self.logo = Logo(100, 100)

		# SETUP UI
		self.ui = UI_LoginScreen()
		self.ui.setup_ui(self)
		self.ui.setup_stylesheet()

	def paintEvent(self, event: QPaintEvent) -> None:
		# super().paintEvent(event)

		opt = QStyleOption()
		opt.initFrom(self)
		p = QPainter(self)
		self.style().drawPrimitive(QStyle.PE_Widget, opt, p, self)

	def resizeEvent(self, event: QResizeEvent) -> None:
		super().resizeEvent(event)
		bkgnd = QImage(get_imagepath('login_splash.jpg', 'gui/images/backgrounds'))
		bkgnd = bkgnd.scaled(self.size())
		palette = self.palette()
		palette.setBrush(QPalette.Window, bkgnd)
		self.setAutoFillBackground(True)
		self.setPalette(palette)


class Logo(QWidget):

	def __init__(self, width, height):
		super().__init__()

		# properties
		self.setFixedHeight(height)
		self.setFixedWidth(width)

	def paintEvent(self, event: QPaintEvent) -> None:
		super().paintEvent(event)

		# Painter
		qp = QPainter()
		qp.begin(self)
		qp.setRenderHint(QPainter.Antialiasing)
		qp.setPen(Qt.NoPen)

		rect = QRect(0, 0, self.width(), self.height())

		# format Path
		icon_path =  get_imagepath('ArES_logo.svg', 'gui/images/icons')

		# Draw icon
		icon = QPixmap(icon_path)
		qp.drawPixmap(self.rect(), icon)

		qp.end()

		