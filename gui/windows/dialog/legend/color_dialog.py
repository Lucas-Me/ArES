# IMPORT QT CORE
from qt_core import *

# IMPORT UI
from gui.windows.dialog.legend.ui_dialog import UI_LegendDialog

# IMPORT CUSTOM FUNCTIONS
from backend.misc.functions import drawShadow

# IMPORT CUSTOM MODULES
from backend.data_management.methods import Profile


class LegendDialog(QDialog):

	profileSaved = Signal(Profile)

	def __init__(self, *args, **kwargs):
		super().__init__(parent = kwargs.pop('parent', None))

		# PROPERTIES
		self.margins = 20

		# SETTINGS
		self.setModal(True)
		self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint | Qt.NoDropShadowWindowHint)
		self.setAttribute(Qt.WA_TranslucentBackground, True)
		self.setAttribute(Qt.WA_DeleteOnClose, True)
		self.setFixedSize(500 + self.margins, 250 + self.margins)

		# SETUP UI
		self.ui = UI_LegendDialog()
		self.ui.setup_ui(self)

		# SIGNALS AND SLOTS
		self.ui.color_selector.color_changed.connect(self.updateColor)
		# self.ui.save_button.clicked.connect(self.saveContents)
		self.ui.save_button.clicked.connect(self.close)
		self.ui.cancel_button.clicked.connect(self.close)

		# LOAD CONTENTS
		# self.loadContents()
	
	def showWindow(self):
		self.adjustPosition()
		self.show()

	@Slot(QColor)
	def updateColor(self, color : QColor):
		self.color = color
		style = self.ui.color_view.styleSheet()
		index = style.index(';')
		new_style = f'background-color: {self.color.name()}' + style[index:]
		self.ui.color_view.setStyleSheet(new_style)

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
		self.adjustPosition()

	def adjustPosition(self) -> None:
		if self.parent() is None:
			return None

		w, h = self.width(), self.height()
		target = self.parent()
		rect = QRect(target.geometry())

		topleft = QPoint()
		topleft.setX((rect.width() - w) / 2)
		topleft.setY((rect.height() - h) / 2)

		self.setGeometry(QRect(topleft, QSize(w, h)))
