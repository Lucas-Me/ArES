# IMPORT QT CORE
from qt_core import *

# IMPORT CUSTOM UI
from gui.pages.ui_processingscreen import UI_ProcessScreen

# IMPORT CUSTOM MODULES
from gui.widgets.profile_picker import Profile

# Data Manager Page Class
class ProcessingScreen(QWidget):

	def __init__(self, parent : QStackedWidget):
		super().__init__(parent = parent)

		# PRIVATE VARIABLES
		self.raw_data = []
		self.selected_profiles = {}
		self.standard_profile = Profile(color = QColor('#fafafa'), name = 'simple')
		self.profileBoxes = []

		# SETUP UI
		self.ui = UI_ProcessScreen()
		self.ui.setup_ui(self)
		self.ui.setup_stylesheet(parent)

		# SIGNALS AND SLOTS
		self.ui.profile_picker.list.removedProfile.connect(self.resetProfileBox)
		self.ui.profile_picker.list.profileDoubleClicked.connect(self.showProfileEditor)

	@Slot(QDialog)
	def showProfileEditor(self, dialog : QDialog):
		dialog.setParent(self)
		dialog.showWindow()

	def updateDates(self, start_date, end_date):
		fmt = '%Y %b %d'
		text = f"{start_date.strftime(fmt)} - {end_date.strftime(fmt)}"
		self.ui.date_label.setText(text)

	def updateRawData(self, data):
		# reset list
		self.ui.parameter_list.reset_settings()

		# adding to list
		n = len(data)
		profile_boxes = [None]*n
		for i in range(n):
			item = self.ui.parameter_list.addRow(
				parameter = data[i].metadata['parameter'],
				station = data[i].metadata['name'],
				enterprise = data[i].metadata['enterprise']
				)

			# STANDARD PROFILE
			self.selected_profiles[data[i]] = self.standard_profile
			profile_boxes[i] = item.profile

			# SIGNALS
			item.profile.pressed.connect(self.profileBoxClicked)

		# SETTING PROPERTIES
		self.profileBoxes = profile_boxes
		self.raw_data = data

	@Slot(QWidget)
	def profileBoxClicked(self, item):
		# getting properies
		_object = self.raw_data[self.profileBoxes.index(item)]
		current_profile = self.selected_profiles[_object]
		profile = self.ui.profile_picker.nextProfile(current_profile)

		# test if None
		if profile is None:
			self.selected_profiles[_object] = self.standard_profile
		else:
			self.selected_profiles[_object] = profile

		# setting color in table
		item.setColor(self.selected_profiles[_object].color)

	@Slot(object)
	def resetProfileBox(self, profile):
		for k, v in self.selected_profiles.items():
			if v == profile:
				row = self.raw_data.index(k)
				item = self.ui.parameter_list.item(row)
				item_widget = self.ui.parameter_list.itemWidget(item)
				#
				self.selected_profiles[k] = self.standard_profile
				item_widget.profile.setColor(self.standard_profile.color)

	def paintEvent(self, event: QPaintEvent) -> None:
		'''
		Reinicia o painter deste QWidget, para que ele nao herde as propriedades do
		parent.
		'''
		# super().paintEvent(event)

		opt = QStyleOption()
		opt.initFrom(self)
		p = QPainter(self)
		self.style().drawPrimitive(QStyle.PE_Widget, opt, p, self)

