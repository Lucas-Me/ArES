# IMPORT QT MODULES
from qt_core import *
import datetime

# IMPORT CUSTOM WIDGETS
from gui.widgets.chart_menu.ui_properties import UI_AbstractMenu
from gui.windows.dialog.import_dialog import ImportDialog

# IMPORT MODULES
import matplotlib.dates as mdates

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
		self.ui.legend_level.location.locationChanged.connect(self.updateLegendLocation)
		self.ui.yaxis_level.propertyChanged.connect(self.updateVerticalAxisTicks)
		self.ui.yaxis_level.auto_adjust.clicked.connect(self.setAutoAdjustYaxis)
		self.parent().canvas.yaxisAdjusted.connect(self.setVerticalThreshold)
		
	def setVerticalThreshold(self, vmin, vmax):
		self.ui.yaxis_level.vmax.spinbox.setValue(vmax)
		self.ui.yaxis_level.vmin.spinbox.setValue(vmin)

	def setAutoAdjustYaxis(self, state : bool):
		self.parent().canvas.autoadjust_yaxis = state

	@Slot(dict)
	def updateVerticalAxisTicks(self, kwargs : dict):
		# updating
		if 'fontsize' in kwargs:
			self.parent().canvas.setTickParams(axis = 'y', **kwargs)
		else:
			self.parent().canvas.setVerticalTicks(**kwargs)
		
		# draw
		self.parent().canvas.draw()
	
	@Slot(str)
	def updateLegendLocation(self, location_string):
		self.parent().canvas.updateLegend(loc = location_string)
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

		# SETUP UI
		self.ui.setupTimeSeries(self)

		# SIGNALS AND SLOTS
		self.ui.xaxis_level.propertyChanged.connect(self.updateDateTicks)
		self.ui.line_plot_level.list_view.rowClicked.connect(self.updateLineElement)
		self.ui.bar_plot_level.list_view.rowClicked.connect(self.updateBarElement)
		self.ui.xaxis_level.date_range.dateChanged.connect(self.updateDateLims)
		self.ui.hlines_level.stateChanged.connect(self.toggleHLine)
		self.ui.hlines_level.valueChanged.connect(self.updateHline)
		self.ui.xaxis_level.auto_adjust.clicked.connect(self.setAutoAdjustXaxis)
		self.parent().canvas.xaxisAdjusted.connect(self.setHorizontalThreshold)
		
	def setHorizontalThreshold(self, vmin, vmax):
		if isinstance(vmin, datetime.datetime):
			vmin = vmin.date()
			vmax = vmax.date()

		elif isinstance(vmin, float):
			vmin = mdates.num2date(vmin).date()
			vmax = mdates.num2date(vmax).date()

		self.ui.xaxis_level.date_range.vmin.setDate(QDate(vmin))
		self.ui.xaxis_level.date_range.vmax.setDate(QDate(vmax))

	@Slot(QDate, str)
	def updateDateLims(self, date : QDate, which : str):
		canvas = self.parent().canvas
		kwargs = {which: date.toPython()}
		canvas.setHorizontalLims(**kwargs)

		# draw
		canvas.draw()
	
	@Slot(bool)
	def setAutoAdjustXaxis(self, state : bool):
		self.parent().canvas.autoadjust_xaxis = state

	def setupInitialValues(self):
		super().setupInitialValues()

		# get canvas settings
		config = self.parent().canvas.getSettings()

		# X axis
		self.ui.xaxis_level.font_size.spinbox.setValue(config['xaxis-fontsize'])

		# dates
		vmin, vmax = self.parent().canvas.getXLims()

		self.ui.xaxis_level.date_range.vmin.setDate(QDate(vmin))
		self.ui.xaxis_level.date_range.vmax.setDate(QDate(vmax))


	@Slot(bool, int)
	def toggleHLine(self, status : bool, index : bool):
		hline_id = f'Faixa Horizontal {index + 1}'
		if status:
			y = self.ui.hlines_level.hlines[index].spinbox.value()
			self.parent().canvas.plothline(y, hline_id)
		else:
			self.parent().canvas.removePlot(hline_id)
		
		# atualiza a figura
		self.parent().canvas.draw()

	@Slot(int, int)
	def updateHline(self, value : int, index: int):
		# properties
		id_ = f'Faixa Horizontal {index + 1}'
		canvas = self.parent().canvas
		line = canvas.handles[id_]

		# set value
		lims = [value, value]
		line.set_ydata(lims)
		canvas.ylims[id_] = lims

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

		# drawing
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

		# drawing
		canvas.draw()

	def plotBars(self):
		if len(self.bar_rows) > 0:
			dashboard = self.parent()
			list_objects = [dashboard.parent.getHandle(index) for index in self.bar_rows]
			dashboard.canvas.barPlot(list_objects)


class OverpassingMenu(AbstractChartMenu):

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		# PROPERTIES
		self.bar_rows = []

		# SETUP UI
		self.ui.setupOverpassing(self)

		# SIGNALS AND SLOTS
		self.ui.plot_level.list_view.rowClicked.connect(self.updateBarElement)
		self.ui.hline_level.valueChanged.connect(self.updateHline)
		self.ui.xaxis_level.propertyChanged.connect(self.updateHorizontalTicks)

	def setupInitialValues(self):
		super().setupInitialValues()

		# get canvas settings
		config = self.parent().canvas.getSettings()

		# X axis
		self.ui.xaxis_level.font_size.spinbox.setValue(config['xaxis-fontsize'])

	@Slot(dict)
	def updateHorizontalTicks(self, kwargs):
		self.parent().canvas.setTickParams(axis = 'x', **kwargs)

		# draw
		self.parent().canvas.draw()

	@Slot(int, int)
	def updateHline(self, value : int, index: int):
		# properties
		id_ = 'Faixa Horizontal'
		canvas = self.parent().canvas
		line = canvas.handles[id_]

		# set value
		lims = [value, value]
		line.set_ydata(lims)
		canvas.ylims[id_] = lims

		# update canvas
		self.plotBars()

		# draw
		canvas.autoscaleAxisY()
		canvas.draw_idle()

	@Slot(int, bool)
	def updateBarElement(self, row : int, add: bool):
		canvas = self.parent().canvas

		# either add or remove artist
		if add:
			# add bar 
			self.bar_rows.append(row)

		else:
			# remove from canvas
			del self.bar_rows[self.bar_rows.index(row)]
			
		# plot new artists
		try:
			self.plotBars()
		except IndexError:
			# opens a dialog warning the user about the error
			dialog = ImportDialog(
				title = 'Dados insuficientes',
				message = 'A série de dados precisa conter 2 ou mais valores válidos.',
				description= 'Uma das séries de dados selecionadas contém somente 1 ou nenhum valor válido que atendeu ao critério de representatividade, assim sendo insuficiente para ser visualizada nesse tipo de gráfico',
				parent = self
			)
			dialog.ignore_button.hide()
			dialog.show()

		except Exception as err:
			# opens a dialog warning the user about the error
			dialog = ImportDialog(
				title = 'Erro desconhecido',
				message = 'Ocorreu um erro inesperado durante a execução das tarefas.',
				description= '',
				parent = self
			)
			dialog.ignore_button.hide()
			dialog.show()

		# drawing
		canvas.draw_idle()

	def plotBars(self):
		if len(self.bar_rows) > 0:
			dashboard = self.parent()
			list_objects = [dashboard.parent.getHandle(index) for index in self.bar_rows]
			dashboard.canvas.barPlot(list_objects)

	def resetSeriesObjects(self, handles):
		# reset properties
		self.bar_rows.clear()

		# reset list
		listview = self.ui.plot_level.list_view

		# cleaning list
		listview.removeItems()

		# adding elements to list
		for i in range(len(handles)):
			listview.addItem(handles[i].metadata['alias'])