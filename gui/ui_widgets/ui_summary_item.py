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

		# CREATING PROFILE IDENTIFIER
		self.profile_box = QWidget()
		self.profile_box.setFixedWidth(80)

		# INSERTING WIDGETS IN MAIN LAYOUT
		self.main_layout.addWidget(self.parameter_label)
		self.main_layout.addWidget(self.station_label)
		self.main_layout.addWidget(self.enterprise_label)
		self.main_layout.addWidget(self.profile_box)



