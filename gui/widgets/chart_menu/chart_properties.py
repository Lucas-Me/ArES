# IMPORT QT MODULES
from qt_core import *

# IMPORT CUSTOM WIDGETS
from gui.widgets.chart_menu.ui_properties import UI_AbstractMenu

# IMPORT CUSTOM FUNCTIONS
from backend.misc.functions import get_imagepath

class AbstractChartMenu(QFrame):
    
	def __init__(self):
		super().__init__()
		
		# PROPERTIES
		self.item_height = 30

		# SETUP UI
		self.ui = UI_AbstractMenu()
		self.ui.setupUI(self)


class TimeSeriesMenu(AbstractChartMenu):

	def __init__(self):
		super().__init__()