# IMPORT QT CORE
from qt_core import *

# IMPORT CUSTOM UI
from gui.pages.ui_processingscreen import UI_ProcessScreen

# IMPORT CUSTOM FUCTIONS
from backend.misc.functions import get_imagepath

# Data Manager Page Class
class ProcessingScreen(QWidget):

	def __init__(self, parent : QStackedWidget):
		super().__init__(parent = parent)

		# PRIVATE VARIABLES
		self.raw_data = []

		# SETUP UI
		self.ui = UI_ProcessScreen()
		self.ui.setup_ui(self)
		self.ui.setup_stylesheet(parent)

	def updateRawData(self, data):
		# reset list
		self.ui.parameter_list.reset_settings()

		# adding to list
		self.raw_data = data
		for _object in self.raw_data:
			self.ui.parameter_list.addRow(
				parameter = _object.metadata['parameter'],
				station = _object.metadata['name'],
				enterprise = _object.metadata['enterprise']
				)

	def paintEvent(self, event: QPaintEvent) -> None:
		'''
		Reinicia o painter deste QWidget, para que ele nao herde as propriedades do
		parent.
		'''
		# super().paintEvent(event)

		opt = QStyleOption()
		opt.initFrom(self)
		p = QPainter(self)
		self.style().drawPrimitive(QStyle.PE_Widget, opt, p, self)

