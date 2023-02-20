# IMPORT QT CORE
from qt_core import *

# IMPORT CUSTOM UI
from gui.ui_widgets.ui_dashboard import UI_Dashboard

# CUSTOM WIDGETS
from gui.widgets.chart_properties.top_level_item import TopLevelItem
from gui.widgets.chart_properties.handles_item import HandlesItem

# Data Manager Page Class
class Dashboard(QWidget):

	def __init__(self, parent):
		super().__init__()

		# PROPERTIES
		self.parent = parent

		# setting UI
		self.ui = UI_Dashboard()
		self.ui.setup_ui(self)
		
		# SIGNALS AND SLOTS
		self.ui.toggle_menu.clicked.connect(self.toggle_menu)

	def updateItems(self):
		# getting parent handles
		handles = self.parent.getDataHandles()
		
		# reset tree widget options
		for i in range(2):
			self.ui.right_menu.resetTopLevelItem(i, handles)

	def toggle_menu(self):
		# check
		status = self.ui.right_menu.isHidden()
		if status:
			self.ui.right_menu.show()
		else:
			self.ui.right_menu.hide()


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