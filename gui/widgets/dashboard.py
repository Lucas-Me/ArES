# IMPORT QT CORE
from qt_core import *

# IMPORT CUSTOM UI
from gui.pages.ui_dashboard import UI_Dashboard

# IMPORT CUSTOM WIDGETS
from backend.plot.charts import TimeSeriesCanvas, OverpassingCanvas
from gui.widgets.chart_menu.chart_properties import TimeSeriesMenu, OverpassingMenu
from gui.windows.dialog.legend.color_dialog import LegendDialog
from gui.windows.dialog.figure_title.title_dialog import TitleEditDialog

# Data Manager Page Class
class Dashboard(QWidget):

	def __init__(self, parent, option):
		super().__init__()

		# PROPERTIES
		self.parent = parent
		
		self.canvas = [TimeSeriesCanvas, OverpassingCanvas][option]()
		self.chart_menu = [TimeSeriesMenu, OverpassingMenu][option](self)

		# setting UI
		self.ui = UI_Dashboard()
		self.ui.setup_ui(self)
		
		# setting up current values
		self.setupChartProperties()
		
		# SIGNALS AND SLOTS
		self.ui.toggle_menu.clicked.connect(self.toggleMenu)
		self.canvas.artistClicked.connect(self.editArtist)
		self.canvas.titleClicked.connect(self.editTitle)

	@Slot(int)
	def editTitle(self, position):
		'''Cria uma janela para que o usuario edite o titulo do eixo X, Y ou da Figura.'''
		 
		# position is {0: left, 1: right, 2: bottom, 3 : top}
		which = ['yaxis', 'yaxis-right', 'xaxis','title']
		display = ['Eixo Vertical', 'Eixo Vertical Secundário', 'Eixo Horizontal', 'Título']

		if position != 1:
			dialog = TitleEditDialog(
				parent = self,
				canvas = self.canvas,
				display = display[position],
				which = which[position]
			)
			dialog.show()

	def setupChartProperties(self):
		self.chart_menu.setupInitialValues()

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