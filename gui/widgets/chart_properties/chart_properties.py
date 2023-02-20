# IMPORT QT MODULES
from qt_core import *


class ChartProperties(QTreeWidget):
    
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		
		# SETTINGS
		self.setColumnCount(2)
		self.header().setSectionResizeMode(QHeaderView.Stretch)
		self.header().resizeSections()

		# variaveis
		self.items_timeseries = {
			"Eixo Horizontal" : [
				"Intervalo",
				"Unidade",
				"Rotação (°)",
				"Tamanho da fonte"],
			"Eixo Vertical" : ["Número de rótulos", "Valor máximo",
								"Valor mínimo", "Tamanho da fonte"]
		}
		self.items_scatterplot = {
			'Eixo Horizontal' : [
				'Número de rótulos',
				'Valor máximo',
				'Valor mínimo',
				"Tamanho da fonte"
			],
			'Eixo Vertical' : [
				'Número de Rótulos',
				'Valor Máximo',
				'Valor Mínimo',
				"Tamanho da fonte",
			]
		}
		
		# Widgets
		self.intervalo = QSpinBox()
		self.unidade = QComboBox()
		self.rotation_x = QSpinBox()
		self.size_y = QSpinBox()
		self.fontsize_x = QSpinBox()
		self.fontsize_y = QSpinBox()
		self.max_y = QDoubleSpinBox()
		self.min_y = QDoubleSpinBox()
		self.size_x = QSpinBox()
		self.max_x = QDoubleSpinBox()
		self.min_x = QDoubleSpinBox()
		
		# widgets list
		self.widgets = [
			{
				'Eixo Horizontal': [self.intervalo, self.unidade,
									self.rotation_x, self.fontsize_x],
				'Eixo Vertical' : [self.size_y, self.max_y,
									self.min_y, self.fontsize_y]
			},
			{
				'Eixo Horizontal': [self.size_x, self.max_x,
									self.min_x, self.fontsize_x],
				'Eixo Vertical' : [self.size_y, self.max_y,
									self.min_y, self.fontsize_y] 
				}
		]


	def run(self):
		items = self.items_timeseries
		if self.active_scatter: items = self.items_scatterplot
		TreeWidgetItems = []
		widgets = self.widgets[self.active_scatter]
		for key in widgets.keys():
			item = QTreeWidgetItem([key])
			TreeWidgetItems.append(item)

		self.insertTopLevelItems(0, TreeWidgetItems)
		j = 0
		for key, values in widgets.items():
			for i in range(len(values)):
				properties = items[key][i]
				child = QTreeWidgetItem()
				child.setText(0, properties)
				TreeWidgetItems[j].addChild(child)
				self.setItemWidget(child, 1, values[i])

			j += 1
		
		return None
