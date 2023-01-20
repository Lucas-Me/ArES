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



		