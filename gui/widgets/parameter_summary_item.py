# IMPORT QT CORE
from qt_core import *

# IMPORT UI MODULES
from gui.ui_widgets.ui_summary_item import UI_ParameterSummaryItem

# Paramater Selection Widget Class
class ParameterSummaryItem(QFrame):

	def __init__(
		self,
		parameter : str,
		station : str,
		enterprise : str,
		width : int,
		height : int,
	):
		super().__init__()

		# PROPERTIES
		self.parameter = parameter
		self.station = station
		self.enterprise = enterprise

		# CONFIGURATION
		self.setFixedHeight(height)
		self.setMinimumWidth(width)

		# SETUP UI
		self.ui = UI_ParameterSummaryItem()
		self.ui.setup_ui(self)

	def adjustColumnWidth(self):
		pass