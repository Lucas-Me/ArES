# IMPORT QT MODULES
from qt_core import *

# IMPORT CUSTOMW WIDGETS
from gui.widgets.chart_menu.legend_level import LegendTopLevel
from gui.widgets.chart_menu.numeric_axis_level import NumericalAxisTopLevel
from gui.widgets.chart_menu.horizontal_axis_level import DateAxisTopLevel, HorizontalAxisTopLevel
from gui.widgets.chart_menu.parameter_level import SeriesTopLevel
from gui.widgets.chart_menu.hline_level import HLineTopLevel

class UI_AbstractMenu(object):
    
	def setupUI(self, parent):

		# NAME
		if not parent.objectName():
			parent.setObjectName('chart_menu')

		# MAIN LAYOUT
		self.right_border_width = 2
		self.main_layout = QVBoxLayout(parent)
		self.main_layout.setContentsMargins(0, 0, self.right_border_width, 0)
		self.main_layout.setSpacing(0)

		# TOP LABEL
		self.top_label = QLabel("Propriedades")
		self.top_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
		self.top_label.setFixedHeight(40)
		self.top_label.setObjectName('top_label')

		# BUTTONS
		self.legend_level = LegendTopLevel(height = parent.item_height)
		self.yaxis_level = NumericalAxisTopLevel(title = "Eixo Vertical", height = parent.item_height)

		# ADD TO MAIN LAYOUT
		self.main_layout.addWidget(self.top_label)
		self.main_layout.addWidget(self.legend_level)
		self.main_layout.addWidget(self.yaxis_level)

		# SETUP STYLE
		self.setup_style(parent)

	def setup_style(self, parent):
		parent.setStyleSheet(f'''
			#chart_menu {{
				background-color: transparent;
				border-right: {self.right_border_width}px solid #36475f;
			}}
			#top_label {{
				background-color: #d9e2f1;
				border: none;
				font: bold 14pt 'Microsoft New Tai Lue';
				color: #36475f;
			}}
		''')

	def setupTimeSeries(self, parent):

		# BUTTONS
		self.xaxis_level = DateAxisTopLevel(height = parent.item_height)
		self.hlines_level = HLineTopLevel(text = 'Linhas horizontais', height=parent.item_height, n = 4)
		self.line_plot_level = SeriesTopLevel(text = 'Gráfico de linha', height = parent.item_height)
		self.bar_plot_level = SeriesTopLevel(text = 'Gráfico de barra', height = parent.item_height)

		# ADD TO MAIN LAYOUT
		self.main_layout.addWidget(self.xaxis_level)
		self.main_layout.addWidget(self.hlines_level)
		self.main_layout.addWidget(self.line_plot_level)
		self.main_layout.addWidget(self.bar_plot_level)

		# ALIGNMENT
		self.main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

	def setupOverpassing(self, parent):
		# BUTTONS
		self.xaxis_level = HorizontalAxisTopLevel(height = parent.item_height)
		self.hline_level = HLineTopLevel(text = 'Limite', height=parent.item_height, n = 1)
		self.plot_level = SeriesTopLevel(text = 'Parâmetros', height = parent.item_height)

		# SETTINGS
		self.hline_level.hlines[0].checkbox.setHidden(True)
		self.hline_level.hlines[0].checkbox.setChecked(True)

		# ADD TO MAIN LAYOUT
		self.main_layout.addWidget(self.xaxis_level)
		self.main_layout.addWidget(self.hline_level)
		self.main_layout.addWidget(self.plot_level)

		# ALIGNMENT
		self.main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
