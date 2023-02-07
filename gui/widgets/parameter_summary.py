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

		# configuration
		# self.setFocusPolicy(Qt.FocusPolicy.NoFocus)

		# animation
		self.animation = QVariantAnimation(self.verticalScrollBar())

		# parameters
		self.item_width = self.width()
		self.item_height = item_height

		# setup UI
		self.ui = UI_ParameterSummary()
		self.ui.setup_ui(self)

		# signals and slots
		self.animation.valueChanged.connect(self.moveScroll)

	def addRow(self, **kwargs):
		item_width = self.width() - 20
		item_height = self.item_height

		# creating ItemWidget
		item_widget = ParameterSummaryItem(
			width = item_width,
			height = item_height,
			**kwargs)
		
		# creating list item and adding to list
		item = QListWidgetItem()
		self.addItem(item)
	
		# Setting Size Hint to ListWidgetItem
		SizeHint = QSize(self.width() - 20, self.item_height)
		item.setSizeHint(SizeHint)
		
	    # setting object QFrame to QlistWidgetItem
		self.setItemWidget(item, item_widget)

	def reset_settings(self):
		# cleaning variables
		self.clear()

	def wheelEvent(self, e: QWheelEvent) -> None:
		self.animation.stop()
		scrollbar = self.verticalScrollBar()
		delta = e.angleDelta().y() // 3
		y = scrollbar.value()
		
		self.animation.setStartValue(y)
		self.animation.setEndValue(y - delta)
		self.animation.setDuration(50)
		self.animation.start()

	def moveScroll(self, i):
		self.verticalScrollBar().setValue(i)
