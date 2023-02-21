# IMPORT QT MODULES
from qt_core import *

# IMPORT BUILT-IN MODULES
from copy import deepcopy

# CUSTOM WIDGETS
from gui.widgets.chart_properties.top_level_item import TopLevelItem
from gui.widgets.chart_properties.handles_item import HandlesItem
from gui.widgets.chart_properties.label_edit import LabelEdit
from gui.widgets.chart_properties.property_axis import AxisProperty, LegendProperty
from gui.widgets.chart_properties.date_axis import DateFormatterProperty, DateLocatorProperty, DateLabelProperty

# IMPORT CUSTOM FUNCTIONS
from backend.misc.functions import get_imagepath

class ChartProperties(QTreeWidget):
    
	# bocCliked : Signal -> lista[top level idx, row, status]
	buttonClicked = Signal(list)
	lineEdited = Signal(list)
	spinboxChanged = Signal(list)
	locatorChanged = Signal(dict)
	formatterChanged = Signal(dict)
	labelDateChanged = Signal(dict)
	legendChanged = Signal(list)

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		
		# PROPERTIES
		self.item_height = 35

		# SETTINGS
		self.setColumnCount(1)
		self.header().hide() # esconde o cabecalho
		self.setSelectionMode(QTreeView.SelectionMode.NoSelection)
		
		# FINAL STEPS
		self.setupStyle()
		self.init()

	def resetTopLevelItem(self, index, handles):
		# removing old top level
		name = self.takeTopLevelItem(index).text(0)

		#creating new top level
		tree_item = QTreeWidgetItem([name])
		top_level_widget = TopLevelItem(text = name, height = self.item_height)
		self.insertTopLevelItem(index, tree_item)
		self.setItemWidget(tree_item, 0, top_level_widget)

		# update tree widget
		for i in range(len(handles)):
			widget = HandlesItem(text=handles[i].metadata['alias'], height = self.item_height, row = i, top_level=index)
			child = QTreeWidgetItem()
			tree_item.addChild(child)
			self.setItemWidget(child, 0, widget)

			# SIGNALS AND SLOTS
			widget.toggled.connect(
				lambda x: self.buttonClicked.emit(x)
				)

	def init(self):
		items = ['Gráfico de linha', 'Gráfico de barra', 'Títulos', 'Eixo Vertical', 'Eixo Horizontal', 'Legenda']
		top_level_items = [QTreeWidgetItem([label]) for label in items]
		self.insertTopLevelItems(0, top_level_items)

		# TOP LEVEL WIDGETS
		for item in top_level_items:
			widget = TopLevelItem(text = item.text(0), height = self.item_height)
			self.setItemWidget(item, 0, widget)

		# LABELS EDIT
		# //////////////////////////////////////////////////

		labels = {'Gráfico' : 'title', 'Eixo Vertical' : 'ylabel', 'Eixo Horizontal' : 'xlabel'}
		idx = items.index('Títulos')
		for k, v in labels.items():
			widget = LabelEdit(k, self.item_height, v)
			child = QTreeWidgetItem()
			self.topLevelItem(idx).addChild(child)
			self.setItemWidget(child, 0, widget)

			# SIGNALS
			widget.labelEdited.connect(self.lineEdited.emit)

		# VERTICAL AXIS
		# //////////////////////////////////////////////////

		texts = {'Quantidade' : 'size', 'Máximo' : 'max', 'Mínimo' : 'min', 'Tamanho da fonte' : 'fontsize'}
		idx = items.index('Eixo Vertical')
		for k in texts.keys():
			spinbox = QSpinBox() if texts[k] in ['size', 'fontsize'] else QDoubleSpinBox()
			widget = AxisProperty(height=self.item_height, text = k, property_ = texts[k], spinbox= spinbox)
			child = QTreeWidgetItem()
			self.topLevelItem(idx).addChild(child)
			self.setItemWidget(child, 0, widget)

			# Signals
			widget.valueChanged.connect(self.spinboxChanged.emit)

		# Horizontal Axis (Date
		# //////////////////////////////////////////////////
		idx = items.index('Eixo Horizontal')
		
		# LOCATOR
		widget = DateLocatorProperty(self.item_height)
		child = QTreeWidgetItem()
		self.topLevelItem(idx).addChild(child)
		self.setItemWidget(child, 0, widget)
		widget.locatorChanged.connect(self.locatorChanged.emit)

		# FORMATTER
		widget = DateFormatterProperty(self.item_height)
		child = QTreeWidgetItem()
		self.topLevelItem(idx).addChild(child)
		self.setItemWidget(child, 0, widget)
		widget.formatterChanged.connect(self.formatterChanged.emit)

		# X TICKS ROTATION
		widget = DateLabelProperty("Rotação", 0, 360, 'rotation')
		child = QTreeWidgetItem()
		self.topLevelItem(idx).addChild(child)
		self.setItemWidget(child, 0, widget)
		widget.valueChanged.connect(self.labelDateChanged.emit)

		# X TICKS SIZE
		widget = DateLabelProperty("Tamanho", 0, 50, 'fontsize')
		child = QTreeWidgetItem()
		self.topLevelItem(idx).addChild(child)
		self.setItemWidget(child, 0, widget)
		widget.valueChanged.connect(self.labelDateChanged.emit)
		
		# LEGEND
		# //////////////////////////////////////////////////
		idx = items.index('Legenda')

		# LEGEND COLUMNS
		widget = LegendProperty("Colunas", 0, 50, 'ncol')
		child = QTreeWidgetItem()
		self.topLevelItem(idx).addChild(child)
		self.setItemWidget(child, 0, widget)
		widget.valueChanged.connect(self.legendChanged.emit)

		# LEGEND FONTSIZE
		widget = LegendProperty("Tamanho", 0, 50, 'fontsize')
		child = QTreeWidgetItem()
		self.topLevelItem(idx).addChild(child)
		self.setItemWidget(child, 0, widget)
		widget.valueChanged.connect(self.legendChanged.emit)

	def setupStyle(self):
		branch_closed = get_imagepath('branch_closed.svg', 'gui/images/icons') 
		branch_open = get_imagepath('branch_open.svg', 'gui/images/icons')

		self.setStyleSheet(f'''
			QTreeWidget::item{{
				height: {self.item_height}px;
				padding: 2px 0;
			}}
			QTreeWidget {{ qproperty-indentation: {self.item_height}; }}
			QTreeWidget::branch:has-children:!has-siblings:closed,
			QTreeWidget::branch:closed:has-children:has-siblings {{
				border-image: none;
				image: url({branch_closed});
			}}
			QTreeWidget::branch:open:has-children:!has-siblings,
			QTreeWidget::branch:open:has-children:has-siblings  {{
				border-image: none;
				image: url({branch_open});
			}}
		''')


