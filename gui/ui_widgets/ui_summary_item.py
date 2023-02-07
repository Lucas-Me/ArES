# IMPORT QT CORE
from qt_core import *

class UI_ParameterSummaryItem(object):

	def setup_ui(self, parent : QFrame):
		if not parent.objectName():
			parent.setObjectName("parameter_item")

		# MAIN LAYOUT
		self.main_layout = QHBoxLayout(parent)
		self.main_layout.setContentsMargins(10, 5, 10, 5)
		self.main_layout.setSpacing(10)

		# CREATING LABELS
		self.parameter_label = QLabel(parent.parameter)
		self.station_label = QLabel(parent.station)
		self.enterprise_label = QLabel(parent.enterprise)
		#
		self.parameter_label.setObjectName('parameter')
		self.station_label.setObjectName('station')
		self.enterprise_label.setObjectName('enterprise')

		# INSERTING WIDGETS IN MAIN LAYOUT
		self.main_layout.addWidget(self.parameter_label)
		self.main_layout.addWidget(self.station_label)
		self.main_layout.addWidget(self.enterprise_label)


	def style_sheet(self, parent):
		# UI PROPERTIES
		background_color = '#ffffff'
		font = 'Microsoft New Tai Lue'
		text_color = '#32495e'

		# stylesheets
		parent.setStyleSheet(f'''
			#parameter_item {{
				background-color : {background_color};
				border-bottom: 1px solid #cccccc;
			}}
			#parameter, #station, #enterprise {{
				font: 500 13pt {font};
				color: {text_color}; 
			}}
			'''
		)

