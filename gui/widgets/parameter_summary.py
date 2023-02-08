# IMPORTS
import gc

# IMPORT QT CORE
from qt_core import *

# IMPORT UI MODULES
from gui.ui_widgets.ui_parametersummary import UI_ParameterSummary

# IMPORT CUSTOM MODULES
from gui.widgets.parameter_summary_item import ParameterSummaryItem

class ParameterSummary(QListWidget):

	def __init__(self, item_height):
		super().__init__()

		# SETTINGS
		self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
		self.verticalScrollBar().setSingleStep(1)
		self.setVerticalScrollMode(QAbstractItemView.ScrollMode.ScrollPerPixel)
		self.setFocusPolicy(Qt.FocusPolicy.NoFocus)

		# animation
		self.animation = QVariantAnimation(self.verticalScrollBar())

		# PROPERTIES
		self.item_width = self.width()
		self.item_height = item_height
		self.scroll_width = 20

		# setup UI
		self.ui = UI_ParameterSummary()
		self.ui.setup_ui(self)

		# signals and slots
		self.animation.valueChanged.connect(self.moveScroll)

	def addRow(self, **kwargs):
		item_width = self.width() - self.scroll_width
		item_height = self.item_height

		# creating list item and adding to list
		item = QListWidgetItem()
		self.addItem(item)

		# Setting Size Hint to ListWidgetItem
		SizeHint = QSize(self.item_width, self.item_height)
		item.setSizeHint(SizeHint)
		
		# creating ItemWidget
		item_widget = ParameterSummaryItem(
			width = item_width,
			height = item_height,
			first = self.count() == 1,
			**kwargs)
		
	    # setting object QFrame to QlistWidgetItem
		self.setItemWidget(item, item_widget)

	def reset_settings(self):
		# cleaning variables
		self.clear()

		# calling garbage collector
		gc.collect()

	def wheelEvent(self, e: QWheelEvent) -> None:
		self.animation.stop()
		scrollbar = self.verticalScrollBar()
		delta = e.angleDelta().y() // 4
		y = scrollbar.value()
		
		self.animation.setStartValue(y)
		self.animation.setEndValue(y - delta)
		self.animation.setDuration(50)
		self.animation.start()

	def moveScroll(self, i):
		self.verticalScrollBar().setValue(i)

	def resizeEvent(self, e: QResizeEvent) -> None:
		''' Ajusta os itens da lista de acordo com a largura da tabela'''
		item_width = self.width() - self.scroll_width
		for i in range(self.count()):
			item = self.item(i)
			item_widget = self.itemWidget(item)
			#
			item_widget.setFixedWidth(item_width)
			item.setSizeHint(QSize(item_width, item_widget.height()))

		return super().resizeEvent(e)

class ParameterHeader(QFrame):

	def __init__(self, height):
		super().__init__()

		# SETTINGS
		self.setObjectName('header')
		self.setFixedHeight(height)

		# UI
		self.setup_ui()
		self.setup_style()

	def setup_ui(self):
		self.header_layout = QHBoxLayout(self)
		self.header_layout.setContentsMargins(10, 5, 10, 5)
		self.header_layout.setSpacing(10)
		#
		self.parameter_label = QLabel("Parâmetro")
		self.parameter_label.setObjectName("parameter")
		#
		self.station_label = QLabel("Estação")
		self.station_label.setObjectName("station")
		#
		self.enterprise_label = QLabel("Empresa")
		self.enterprise_label.setObjectName("enterprise")
		#
		self.profile_label = QLabel("Perfil")
		self.profile_label.setObjectName("profile")
		self.profile_label.setFixedWidth(80)
		#
		self.header_layout.addWidget(self.parameter_label)
		self.header_layout.addWidget(self.station_label)
		self.header_layout.addWidget(self.enterprise_label)
		self.header_layout.addWidget(self.profile_label)

	def setup_style(self):
		font = 'Microsoft New Tai Lue'
		font_color = '#1c1c1c'

		self.setStyleSheet(f'''
			#header {{
                background-color: transparent;
            }}
			#parameter, #station, #enterprise, #profile {{
                background-color: transparent;
                font: 500 14pt '{font}';
                color: {font_color};
                text-align: left;
            }}	
		''')