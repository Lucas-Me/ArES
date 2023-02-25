# IMPORT QT MODULES
from qt_core import *

# IMPORT CUSTOM WIDGETS
from gui.widgets.chart_menu.ui_properties import UI_AbstractMenu


class AbstractChartMenu(QFrame):
    
	def __init__(self, parent : QWidget):
		super().__init__(parent = parent)
		
		# PROPERTIES
		self.item_height = 30

		# SETUP UI
		self.ui = UI_AbstractMenu()
		self.ui.setupUI(self)

		# SIGNALS AND SLOTS
		self.ui.title_level.labelEdited.connect(self.updateLabel)
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

	@Slot(list)
	def updateLabel(self, options):
		# unpacking args
		kwargs = {
			'label' : options[0],
			'fontweight' : 'bold' if options[1] else 'normal',
			'fontsize' : options[2]
		}

		canvas = self.parent().canvas
		if options[-1] == 'title':
			canvas.setTitle(**kwargs)
		else:
			canvas.setLabel(axis = options[-1][0], **kwargs)


class TimeSeriesMenu(AbstractChartMenu):

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		# SETUP UI
		self.ui.setupTimeSeries(self)

		# SIGNALS AND SLOTS
		self.ui.xaxis_level.propertyChanged.connect(self.updateDateTicks)

	@Slot(dict)
	def updateDateTicks(self, kwargs):
		if 'locator' in kwargs or 'formatter' in kwargs: # update frequency and date format
			self.parent().canvas.setHorizontalTicks(**kwargs)
			
		else: # update fontsize or label rotation
			self.parent().canvas.setTickParams(axis = 'x', **kwargs)

		# draw
		self.parent().canvas.draw()

	def resetSeriesObjects(self, handles):
		# getting list
		listview = self.ui.line_plot_level.list_view

		# cleaning list
		listview.removeItems()

		# adding elements to list
		for i in range(len(handles)):
			listview.addItem(handles[i].metadata['alias'])
			
