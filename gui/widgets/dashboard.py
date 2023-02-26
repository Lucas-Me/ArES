# IMPORT QT CORE
from qt_core import *

# IMPORT CUSTOM UI
from gui.pages.ui_dashboard import UI_Dashboard

# IMPORT CUSTOM WIDGETS
from backend.plot.charts import TimeSeriesCanvas
from gui.widgets.chart_menu.chart_properties import TimeSeriesMenu
from gui.windows.dialog.legend.color_dialog import LegendDialog

# Data Manager Page Class
class Dashboard(QWidget):

	def __init__(self, parent):
		super().__init__()

		# PROPERTIES
		self.parent = parent
		
		self.canvas = TimeSeriesCanvas()
		self.chart_menu = TimeSeriesMenu(self)
		self.bar_rows = []

		# setting UI
		self.ui = UI_Dashboard()
		self.ui.setup_ui(self)
		
		# SIGNALS AND SLOTS
		self.ui.toggle_menu.clicked.connect(self.toggleMenu)
		self.canvas.artistClicked.connect(self.editArtist)

	@Slot(str)
	def editArtist(self, artist_label : str):
		dialog = LegendDialog(parent = self, canvas = self.canvas)
		dialog.loadContents(artist_label)
		dialog.show()

	def updateItems(self):
		# getting parent handles
		handles = self.parent.getDataHandles()
		
		# reset tree widget options
		self.chart_menu.resetSeriesObjects(handles)

		# reseta o grafico
		self.canvas.resetChart()

		# reset private properties
		self.bar_rows.clear()

	def toggleMenu(self):
		status = self.chart_menu.isHidden()
		self.chart_menu.setHidden(not status)

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