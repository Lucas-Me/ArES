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
		self.chart_menu= TimeSeriesMenu(self)
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

	@Slot(list)
	def updateChartElement(self, options):
		# getting args
		top_level_row = options[0]
		child_row = options[1]
		status = options[2]

		# subproducts
		base = 0
		plot_idx = top_level_row - base
		series = self.parent.getHandle(child_row)

		# either add or remove artist
		if status: 

			# check if artist is already present in other format
			tree = self.right_menu
			item = tree.topLevelItem(top_level_row + (-1) ** plot_idx).child(child_row)
			widget = tree.itemWidget(item, 0)
			if widget.button.isChecked():
				widget.button.setChecked(False) # it will remove the artists by itself
			
			# Plot new artist
			if plot_idx == 0:
				self.canvas.plot(series)

			else:
				self.bar_rows.append(child_row)
				self.plotBars()

		else: # remove artist
			if plot_idx == 1:
				del self.bar_rows[self.bar_rows.index(child_row)]
				self.plotBars()

			self.canvas.removePlot(id_ = series.metadata['signature'])

	def plotBars(self):
		list_objects = [self.parent.getHandle(index) for index in self.bar_rows]
		if len(list_objects) > 0:
			self.canvas.barPlot(list_objects)

	def updateItems(self):
		# getting parent handles
		handles = self.parent.getDataHandles()
		
		# # reset tree widget options
		# for i in range(2):
		# 	self.right_menu.resetTopLevelItem(i, handles)

		# reseta o grafico
		self.canvas.resetChart()

		# reset private propertie
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