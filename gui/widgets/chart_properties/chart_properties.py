# IMPORT QT MODULES
from qt_core import *

# CUSTOM WIDGETS
from gui.widgets.chart_properties.top_level_item import TopLevelItem
from gui.widgets.chart_properties.handles_item import HandlesItem

class ChartProperties(QTreeWidget):
    
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		
		# SETTINGS
		self.setColumnCount(1)
		self.header().hide() # esconde o cabecalho
		self.setSelectionMode(QTreeView.SelectionMode.NoSelection)

		# PROPERTIES

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

		self.setupStyle()
		self.init()

	def resetTopLevelItem(self, index, handles):
		# removing old top level
		name = self.takeTopLevelItem(index).text(0)

		#creating new top level
		tree_item = QTreeWidgetItem([name])
		top_level_widget = TopLevelItem(text = name, height = 30)
		self.insertTopLevelItem(index, tree_item)
		self.setItemWidget(tree_item, 0, top_level_widget)

		# update tree widget
		for i in range(len(handles)):
			widget = HandlesItem(text=handles[i].metadata['alias'], height = 30)
			child = QTreeWidgetItem()
			tree_item.addChild(child)
			self.setItemWidget(child, 0, widget)

	def init(self):
		items = ['Gráfico de linha', 'Gráfico de barra', 'Títulos', 'Eixo Vertical', 'Eixo Horizontal', 'Legenda']
		top_level_items = [QTreeWidgetItem([label]) for label in items]
		self.insertTopLevelItems(0, top_level_items)

		# TOP LEVEL WIDGETS
		for item in top_level_items:
			self.setItemWidget(item, 0, TopLevelItem(text = item.text(0), height = 30))
		

	def setupStyle(self):
		self.setStyleSheet('''
			QTreeWidget::item{
				height: 35px;
			}
		''')


