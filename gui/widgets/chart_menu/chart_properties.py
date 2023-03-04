# IMPORT QT MODULES
from qt_core import *

# IMPORT CUSTOM WIDGETS
from gui.widgets.chart_menu.ui_properties import UI_AbstractMenu

# IMPORT CUSTOM VARIABLES
import backend.misc.settings as settings


class AbstractChartMenu(QFrame):
    
	def __init__(self, parent : QWidget):
		super().__init__(parent = parent)
		
		# PROPERTIES
		self.item_height = 30

		# SETUP UI
		self.ui = UI_AbstractMenu()
		self.ui.setupUI(self)

		# SIGNALS AND SLOTS
		self.ui.legend_level.propertyChanged.connect(self.updateLegendProperties)
		self.ui.yaxis_level.propertyChanged.connect(self.updateVerticalAxisTicks)

	@Slot(dict)
	def updateVerticalAxisTicks(self, kwargs : dict):
		# updating
		if 'fontsize' in kwargs:
			self.parent().canvas.setTickParams(axis = 'y', **kwargs)
		else:
			self.parent().canvas.setVerticalTicks(**kwargs)
		
		# draw
		self.parent().canvas.draw()

	@Slot(dict)
	def updateLegendProperties(self, kwargs):
		self.parent().canvas.updateLegend(**kwargs)

		# draw
		self.parent().canvas.draw()

	def setupInitialValues(self):
		# canvas settings
		config = self.parent().canvas.getSettings()

		# legend
		self.ui.legend_level.font_size.spinbox.setValue(config['legend-fontsize'])
		self.ui.legend_level.column_count.spinbox.setValue(config['legend-ncol'])

		# Y axis
		self.ui.yaxis_level.vmax.spinbox.setValue(config['yticks-max'])
		self.ui.yaxis_level.vmin.spinbox.setValue(config['yticks-min'])
		self.ui.yaxis_level.total_ticks.spinbox.setValue(config['yticks-size'])
		self.ui.yaxis_level.font_size.spinbox.setValue(config['yaxis-fontsize'])


class TimeSeriesMenu(AbstractChartMenu):

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		# PROPERTIES
		self.bar_rows = []
		self.hline_id = 'Faixa Horizontal'

		# SETUP UI
		self.ui.setupTimeSeries(self)

		# SIGNALS AND SLOTS
		self.ui.xaxis_level.propertyChanged.connect(self.updateDateTicks)
		self.ui.line_plot_level.list_view.rowClicked.connect(self.updateLineElement)
		self.ui.bar_plot_level.list_view.rowClicked.connect(self.updateBarElement)
		self.ui.line_plot_level.hline_frame.stateChanged.connect(self.toggleHLine)
		self.ui.line_plot_level.hline_frame.valueChanged.connect(self.updateHline)
	
	def setupInitialValues(self):
		super().setupInitialValues()

		# get canvas settings
		config = self.parent().canvas.getSettings()

		# X axis
		self.ui.xaxis_level.font_size.spinbox.setValue(config['xaxis-fontsize'])

	@Slot(bool)
	def toggleHLine(self, status : bool):
		if status:
			y = self.ui.line_plot_level.hline_frame.spinbox.value()
			self.parent().canvas.plothline(y, self.hline_id)
		else:
			self.parent().canvas.removePlot(self.hline_id)

	@Slot(int)
	def updateHline(self, value : int):
		# properties
		canvas = self.parent().canvas
		line = canvas.handles[self.hline_id]

		# set value
		line.set_ydata([value, value])

		# draw
		canvas.draw()

	@Slot(dict)
	def updateDateTicks(self, kwargs):
		if 'locator' in kwargs or 'formatter' in kwargs: # update frequency and date format
			self.parent().canvas.setHorizontalTicks(**kwargs)
			
		else: # update fontsize or label rotation
			self.parent().canvas.setTickParams(axis = 'x', **kwargs)

		# draw
		self.parent().canvas.draw()

	def resetSeriesObjects(self, handles):
		# reset bar_rows
		self.bar_rows.clear()

		# getting list
		listview_widgets = [
			self.ui.line_plot_level.list_view,
			self.ui.bar_plot_level.list_view
		]

		for listview in listview_widgets:
			# cleaning list
			listview.removeItems()
	
			# adding elements to list
			for i in range(len(handles)):
				listview.addItem(handles[i].metadata['alias'])
	
	@Slot(int, bool)
	def updateLineElement(self, row : int, add : bool):
		series = self.parent().parent.getHandle(row)
		canvas = self.parent().canvas

		# remove artist if necessary
		if not add:
			canvas.removePlot(id_ = series.metadata['signature'])

		else:
			# add artist, but first check if the same object is already ploted as bars
			listview = self.ui.bar_plot_level.list_view
			if listview.getStatus(row):
				listview.setStatus(row, False)
				self.updateBarElement(row, False)

			# plot new artists
			canvas.plot(series)

		# scaling and drawing
		canvas.autoscaleAxis()
		canvas.draw()

	@Slot(int, bool)
	def updateBarElement(self, row : int, add: bool):
		series = self.parent().parent.getHandle(row)
		canvas = self.parent().canvas

		# either add or remove artist
		if add:
			# add artist, but first check if the same object is already ploted as lines
			listview = self.ui.line_plot_level.list_view
			if listview.getStatus(row):
				listview.setStatus(row, False)
				self.updateLineElement(row, False)
	
			# add bar 
			self.bar_rows.append(row)

		else:
			# remove from canvas
			del self.bar_rows[self.bar_rows.index(row)]
			canvas.removePlot(id_ = series.metadata['signature'])
			
		# plot new artists
		self.plotBars()

		# scaling and drawing
		canvas.autoscaleAxis()
		canvas.draw()

	def plotBars(self):
		if len(self.bar_rows) > 0:
			dashboard = self.parent()
			list_objects = [dashboard.parent.getHandle(index) for index in self.bar_rows]
			dashboard.canvas.barPlot(list_objects)