# IMPORT QT_CORE
from qt_core import *

# Data Manager Page UI Class
class UI_ParameterSummary(object):
    
	def setup_ui(self, parent : QTreeView):

		if not parent.objectName():
			parent.setObjectName('parameter_summary')


	def setup_stylesheet(self, parent):
		# CONSTANTS
		font = 'Microsoft New Tai Lue'
		font_color = '#757d8e'
		bg_color = '#F0F0F0'
		border_radius = 10

		parent.setStyleSheet(f'''
			#parameter_summary{{
				background-color: transparent;
				border: none;
				font: 500 13pt '{font}';
				color: {font_color};
			}}
		''')
