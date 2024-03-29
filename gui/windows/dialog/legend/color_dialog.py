# IMPORT MODULES
import numpy as np

# IMPORT QT CORE
from qt_core import *

# IMPORT UI
from gui.windows.dialog.legend.ui_dialog import UI_LegendDialog

# IMPORT CUSTOM FUNCTIONS
from backend.misc.functions import drawShadow


class LegendDialog(QDialog):

	def __init__(self, canvas, parent = None):
		super().__init__(parent = parent)

		# PROPERTIES
		self.margins = 20
		self.canvas = canvas
		self.dragPos = QPoint()

		# SETTINGS
		self.setModal(True)
		self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint | Qt.NoDropShadowWindowHint)
		self.setAttribute(Qt.WA_TranslucentBackground, True)
		self.setAttribute(Qt.WA_DeleteOnClose, True)
		self.setFixedSize(500 + self.margins, 400 + self.margins)

		# SETUP UI
		self.ui = UI_LegendDialog()
		self.ui.setup_ui(self)

		# SIGNALS AND SLOTS
		self.ui.color_selector.color_changed.connect(lambda x: self.changeArtistColor(x, 'text'))
		self.ui.table.colorSelected.connect(lambda x: self.changeArtistColor(x, 'both'))
		self.ui.custom_colors.colorSelected.connect(lambda x: self.changeArtistColor(x, 'both'))
		self.ui.custom_colors.saveColor.connect(self.saveColor)
		self.ui.save_button.clicked.connect(self.saveContents)
		self.ui.cancel_button.clicked.connect(self.close)
		self.ui.color_codes.colorChanged.connect(lambda x: self.changeArtistColor(x, 'triangle'))

	def saveColor(self, widget):
		cur_color = self.ui.color_selector.cur_color
		widget.setColor(cur_color)

	def saveContents(self):
		text = self.ui.line_edit.text()
		if len(text) > 0:
			self.changeArtistLabel(text)

		# update legend and draw figure
		self.canvas.updateLegend()
		self.canvas.draw()

		# save custom colors
		self.ui.custom_colors.exportSettings()

		# close dialog
		return super().close()

	@Slot(QColor)
	def changeArtistColor(self, color : QColor, which: str):
		self.canvas.updateColor(self.artist_id, color.name())

		# draw new canvas
		self.canvas.draw()

		# update dialog
		self.updateColor(color, which)

	def changeArtistLabel(self, text):
		self.canvas.labels[self.artist_id] = text

	def loadContents(self, artist_label):
		# storing original values
		self.artist_id = artist_label
		self.origLabel = self.canvas.labels[self.artist_id]
		self.origColor = self.canvas.colors[self.artist_id]
		
		if isinstance(self.origColor, tuple) or isinstance(self.origColor, list):
			self.origColor = QColor(*map(lambda x: x*255, self.origColor))

		elif isinstance(self.origColor, np.ndarray):
			transform = self.origColor*255
			self.origColor = QColor(*transform)

		else:
			self.origColor = QColor(self.origColor)
			
		# updating window properties
		line_edit = self.ui.line_edit
		line_edit.setText(self.origLabel)
		self.updateColor(self.origColor)

	def show(self):
		self.adjustPosition()
		super().show()

	def updateColor(self, color : QColor, which = 'triangle'):
		if which == 'triangle':
			self.ui.color_selector.set_color(color)
		elif which == 'text':
			self.ui.color_codes.setColor(color)
		else:
			self.ui.color_selector.set_color(color)
			self.ui.color_codes.setColor(color)

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
		topleft.setX((rect.width() - w) / 2 + topleft.x())
		topleft.setY((rect.height() - h) / 2 + topleft.y())

		self.setGeometry(QRect(topleft, QSize(w, h)))

	def mousePressEvent(self, event):          
		self.dragPos = event.globalPos()
		self.move_event = True
		
	def mouseMoveEvent(self, event):                          
		if event.buttons() == Qt.LeftButton:
			self.move(self.pos() + event.globalPos() - self.dragPos)
			self.dragPos = event.globalPos()
			event.accept()

	def close(self) -> bool:
		# revert to original color if necessary
		if self.origColor != self.ui.color_selector.cur_color:
			self.changeArtistColor(self.origColor, which = 'both')

		# update legend and draw figure
		self.canvas.updateLegend()
		self.canvas.draw()

		return super().close()
	
	def keyPressEvent(self, arg__1: QKeyEvent) -> None:
		if arg__1.key() == Qt.Key_Enter or arg__1.key() == Qt.Key_Return:
			return None
		return super().keyPressEvent(arg__1)