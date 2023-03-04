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
		self.setFixedSize(500 + self.margins, 250 + self.margins)

		# SETUP UI
		self.ui = UI_LegendDialog()
		self.ui.setup_ui(self)

		# SIGNALS AND SLOTS
		self.ui.color_selector.color_changed.connect(self.changeArtistColor)
		self.ui.table.colorSelected.connect(self.changeArtistColor)
		self.ui.save_button.clicked.connect(self.saveContents)
		self.ui.cancel_button.clicked.connect(self.close)


	def saveContents(self):
		text = self.ui.line_edit.text()
		if len(text) > 0:
			self.changeArtistLabel(text)

		# update legend and draw figure
		self.canvas.updateLegend()
		self.canvas.draw()

		# close dialog
		return super().close()

	@Slot(QColor)
	def changeArtistColor(self, color : QColor):
		self.canvas.updateColor(self.artist_id, color.name())

		# draw new canvas
		self.canvas.draw()

		# update dialog
		self.updateColor(color)

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

	def showWindow(self):
		self.adjustPosition()
		self.show()

	def updateColor(self, color : QColor):
		style = self.ui.color_view.styleSheet()
		index = style.index(';')
		new_style = f'background-color: {color.name()}' + style[index:]
		self.ui.color_view.setStyleSheet(new_style)
		self.ui.color_selector.set_color(color)

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

	def close(self) -> bool:
		# revert to original color if necessary
		if self.origColor != self.ui.color_selector.cur_color:
			self.changeArtistColor(self.origColor)

		# update legend and draw figure
		self.canvas.updateLegend()
		self.canvas.draw()

		return super().close()