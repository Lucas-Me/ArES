# QT CORE
from qt_core import *

class ClickableLabel(QLabel):

	clicked = Signal()
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

	def mousePressEvent(self, ev: QMouseEvent) -> None:
		self.clicked.emit()
		return super().mousePressEvent(ev)
	