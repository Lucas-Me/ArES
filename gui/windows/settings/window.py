# IMPORT QT MODULES
from qt_core import *

# IMPORT UI
from gui.windows.settings.ui_settings import UI_SettingsWindow

# IMPORT CUSTOM FUNCTIONS
from backend.misc.functions import drawShadow


class SettingsWindow(QDialog):
    
	def __init__(self, parent = None):
		super().__init__(parent = parent)

		# PROPERTIES
		self.margins = 20

		# WINDOW SETTINGS
		self.setFixedSize(400 + self.margins, 350 + self.margins)
		self.setModal(True)
		self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint | Qt.NoDropShadowWindowHint)
		self.setAttribute(Qt.WA_TranslucentBackground, True)
		self.setAttribute(Qt.WA_DeleteOnClose, True)

		# SETUP UI
		self.ui = UI_SettingsWindow()
		self.ui.setup_ui(self)

		# SIGNALS AND SLOTS
		self.ui.btn_exit.clicked.connect(self.close)
	
	def show(self) -> None:
		self.adjustPosition()
		return super().show()

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

	def adjustPosition(self) -> None:
		if self.parent() is None:
			return None

		w, h = self.width(), self.height()
		target = self.parent()
		rect = QRect(target.geometry())

		topleft = QPoint()
		topleft.setX((rect.width() - w) / 2 + rect.x())
		topleft.setY((rect.height() - h) / 2 + rect.y())

		rect = QRect(topleft, QSize(w, h))
		self.setGeometry(rect)
