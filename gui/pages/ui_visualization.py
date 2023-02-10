# IMPORT QT_CORE
from qt_core import *

# IMPORT CUSTOM WIDGETS
from backend.plot.visualization import AbstractCanvas

# Data Manager Page UI Class
class UI_DataVisualization(object):
    
	def setup_ui(self, parent : QWidget):
		
		if not parent.objectName():
			parent.setObjectName(u'visualization_page')

		# CENTRAL LAYOUT
		self.central_layout = QVBoxLayout(parent)

		# CANVAS
		# ////////////////////////////////////////////
		self.canvas = AbstractCanvas()

		# ADD TO CENTRAL LAYOUT
		# ///////////////////////////////////////////
		self.central_layout.addWidget(self.canvas)