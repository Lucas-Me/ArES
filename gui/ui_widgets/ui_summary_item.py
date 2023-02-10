# IMPORT QT CORE
from qt_core import *

class UI_ParameterSummaryItem(object):

	def setup_ui(self, parent : QFrame):
		if not parent.objectName():
			parent.setObjectName("parameter_item")

		# MAIN LAYOUT
		self.main_layout = QHBoxLayout(parent)
		self.main_layout.setContentsMargins(10, 2, 10, 2)
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
		self.profile_frame = QFrame()
		self.profile_frame.setObjectName('profile')
		self.profile_frame.setFixedWidth(80)
		#
		self.profile_layout = QHBoxLayout(self.profile_frame)
		self.profile_layout.setContentsMargins(0, 0, 0, 0)
		self.profile_layout.addWidget(parent.profile_box)
		self.profile_layout.setAlignment(parent.profile_box, Qt.AlignmentFlag.AlignCenter)

		# INSERTING WIDGETS IN MAIN LAYOUT
		self.main_layout.addWidget(self.parameter_label)
		self.main_layout.addWidget(self.station_label)
		self.main_layout.addWidget(self.enterprise_label)
		self.main_layout.addWidget(self.profile_frame)



