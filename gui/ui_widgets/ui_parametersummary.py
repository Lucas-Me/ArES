# IMPORT QT_CORE
from qt_core import *

# Data Manager Page UI Class
class UI_ParameterSummary(object):
    
	def setup_ui(self, parent : QListWidget):

		if not parent.objectName():
			parent.setObjectName('parameter_summary')
	
		# setting stylesheet
		self.setup_stylesheet(parent)

	def setup_stylesheet(self, parent):
		# CONSTANTS
		font = 'Microsoft New Tai Lue'
		font_color = '#32495e'
		bg_color = '#FAFAFA'
		border_radius = 10

		parent.setStyleSheet(f'''
			#parameter_summary{{
				background-color: white;
				border: 1px solid #cccccc;
				border-radius: {border_radius}px;
			}}
			#parameter_summary::item {{
                border-bottom: 1px solid #cccccc;
            }}
		''')
