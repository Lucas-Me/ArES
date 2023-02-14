# IMPORT QT CORE
from qt_core import *

# IMPORT CUSTOM UI
from gui.ui_widgets.ui_dashboard import UI_Dashboard

# Data Manager Page Class
class Dashboard(QWidget):

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		self.ui = UI_Dashboard()
		self.ui.setup_ui(self)
