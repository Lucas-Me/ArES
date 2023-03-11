# IMPORT QT CORE
from qt_core import *

# IMPORT UI
from gui.windows.dialog.chart.ui_chart_selection import UI_ChartDialog

# IMPORT CUSTOM FUNCTIONS
from backend.misc.functions import drawShadow


class ChartCreationDialog(QDialog):

	selection = Signal(bool)
	def __init__(self, parent = None):
		super().__init__(parent = parent)

		# PROPERTIES
		self.margins = 20
		self.options = [
			"Série temporal",
			"Ultrapassagem"
		]

		# SETTINGS
		self.setModal(True)
		self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint | Qt.NoDropShadowWindowHint)
		self.setAttribute(Qt.WA_TranslucentBackground, True)
		self.setAttribute(Qt.WA_DeleteOnClose, True)
		self.setFixedSize(300 + self.margins, 100 + self.margins)

		# SETUP UI
		self.ui = UI_ChartDialog()
		self.ui.setup_ui(self)

		# SIGNALS AND SLOTS
		self.ui.ok_button.clicked.connect(self.confirm)
		self.ui.cancel_button.clicked.connect(self.close)

	def show(self):
		self.adjustPosition()
		super().show()
		
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

		topleft = target.mapToGlobal(rect.topLeft())
		topleft.setX((rect.width() - w) / 2 + topleft.x() / 2)
		topleft.setY((rect.height() - h) / 2 + topleft.y() / 2)

		self.setGeometry(QRect(topleft, QSize(w, h)))

	def confirm(self):
		self.selection.emit(True)
		return super().close()
	
	def close(self) -> bool:
		self.selection.emit(False)
		return super().close()
	