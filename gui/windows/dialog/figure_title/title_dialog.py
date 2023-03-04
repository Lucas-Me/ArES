# IMPORT QT CORE
from qt_core import *

# IMPORT UI
from gui.windows.dialog.figure_title.ui_dialog import UI_TitleDialog

# IMPORT CUSTOM FUNCTIONS
from backend.misc.functions import drawShadow


class TitleEditDialog(QDialog):

	def __init__(self, canvas, which : str, display : str, parent = None):
		super().__init__(parent = parent)

		# PROPERTIES
		self.margins = 20
		self.canvas = canvas
		self.dragPos = QPoint()
		self.display_label = display
		self.which = which
		self.current_title = canvas.params[f'{which}-label']
		self.current_fontsize = canvas.params[f'{which}-fontsize']
		self.current_fontweight = canvas.params[f'{which}-fontweight']

		# SETTINGS
		self.setModal(True)
		self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint | Qt.NoDropShadowWindowHint)
		self.setAttribute(Qt.WA_TranslucentBackground, True)
		self.setAttribute(Qt.WA_DeleteOnClose, True)
		self.setFixedSize(300 + self.margins, 100 + self.margins)

		# SETUP UI
		self.ui = UI_TitleDialog()
		self.ui.setup_ui(self)

		# SIGNALS AND SLOTS
		self.ui.line.editingFinished.connect(self.updateText)
		self.ui.bold.clicked.connect(self.updateFontWeight)
		self.ui.fontsize.valueChanged.connect(self.updateFontSize)
		self.ui.cancel_button.clicked.connect(self.close)
		self.ui.save_button.clicked.connect(self.save)

	def updateTitle(self, **kwargs):
		if self.which == 'title':
			self.canvas.setTitle(**kwargs)
		else:
			self.canvas.setLabel(axis = self.which[0], **kwargs)

		# draw
		self.canvas.draw()

	def updateText(self):
		text = self.ui.line.text()
		self.updateTitle(label = text)
		
	def updateFontWeight(self):
		set_bold = self.ui.bold.isChecked()
		value = 'bold' if set_bold else 'normal'
		self.updateTitle(fontweight = value)

	@Slot(int)
	def updateFontSize(self, value):
		self.updateTitle(fontsize = value)

	def showWindow(self):
		self.adjustPosition()
		self.show()
		
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
		topleft.setX((rect.width() - w) / 2)
		topleft.setY((rect.height() - h) / 2)

		self.setGeometry(QRect(topleft, QSize(w, h)))

	def mousePressEvent(self, event):          
		self.dragPos = event.globalPos()
		self.move_event = True
		
	def mouseMoveEvent(self, event):                          
		if event.buttons() == Qt.LeftButton:
			self.move(self.pos() + event.globalPos() - self.dragPos)
			self.dragPos = event.globalPos()
			event.accept()

	def save(self):
		return super().close()
	
	def close(self) -> bool:
		# revert to original color if necessary
		self.updateTitle(
			label = self.current_title,
			fontsize = self.current_fontsize,
			fontweight = self.current_fontweight
		)

		return super().close()