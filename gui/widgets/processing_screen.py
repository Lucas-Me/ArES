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
		self.standard_profile = Profile(color = QColor('#fafafa'), name = 'simple')

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
		for i in range(n):
			item = self.ui.parameter_list.addRow(
				parameter = data[i].metadata['parameter'],
				station = data[i].metadata['name'],
				enterprise = data[i].metadata['enterprise'],
				profile = self.standard_profile
				)

			# SIGNALS
			item.profile_box.pressed.connect(self.profileBoxClicked)

		# SETTING PROPERTIES
		self.raw_data = data

	@Slot(QWidget)
	def profileBoxClicked(self, item):
		# getting properies
		current_profile = item.getProfile()
		profile = self.ui.profile_picker.nextProfile(current_profile)

		# test if None
		if profile is None:
			item.setProfile(self.standard_profile)
		else:
			item.setProfile(profile)

	@Slot(object)
	def resetProfileBox(self, profile):
		target = self.ui.parameter_list
		for row in range(target.count()):
			item = target.item(row)
			item_widget = target.itemWidget(item)
			#
			if item_widget.getProfile() == profile:
				item_widget.setProfile(self.standard_profile)

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

