# IMPORTS
import gc

# IMPORT QT CORE
from qt_core import *

# IMPORT UI MODULES
from gui.ui_widgets.ui_parametersummary import UI_ParameterSummary

class ParameterSummary(QListWidget):

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		# PROPERTIES
		self.scroll_width = self.verticalScrollBar().height()

		# setup UI
		self.ui = UI_ParameterSummary()
		self.ui.setup_ui(self)
		self.ui.setup_stylesheet(self)

	def addRow(self, content : list[str]):
		row = self.rowCount()
		cols = self.columnCount()
		self.insertRow(row)

		for i in range(cols):
			widget_item = self.createItem(content[i], '#ffffff')
			self.setItem(row, i, widget_item)

	def createItem(self, text, color):
		pass

