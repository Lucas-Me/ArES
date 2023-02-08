# IMPORT QT CORE
from qt_core import *

# IMPORT UI MODULES
from gui.ui_widgets.ui_summary_item import UI_ParameterSummaryItem

# Paramater Selection Widget Class
class ParameterSummaryItem(QFrame):

	def __init__(
		self,
		parameter : str,
		station : str,
		enterprise : str,
		width : int,
		height : int,
		first = False
	):
		super().__init__()

		# PROPERTIES
		self.parameter = parameter
		self.station = station
		self.enterprise = enterprise
		self.enter_color = '#e4e4e4'
		self.leave_color = '#ffffff'
		self.is_first = first

		# CONFIGURATION
		self.setFixedHeight(height)
		self.setMinimumWidth(width)

		# SETUP UI
		self.ui = UI_ParameterSummaryItem()
		self.ui.setup_ui(self)
		self.style_sheet(self.leave_color)

	def adjustColumnWidth(self):
		pass

	def style_sheet(self, color):
		# UI PROPERTIES
		font = 'Microsoft New Tai Lue'
		text_color = '#32495e'
		border_radius = 10

		# stylesheets
		if self.is_first:
			self.setStyleSheet(f'''
				#parameter_item {{
					background-color : {color};
					border-bottom: 1px solid #cccccc;
					border-top-right-radius: {border_radius}px;
					border-top-left-radius: {border_radius}px;
				}}
				#parameter, #station, #enterprise {{
					font: 500 10pt {font};
					color: {text_color}; 
				}}
				''')
		else:
			self.setStyleSheet(f'''
				#parameter_item {{
					background-color : {color};
					border-bottom: 1px solid #cccccc;
				}}
				#parameter, #station, #enterprise {{
					font: 500 10pt {font};
					color: {text_color}; 
				}}
				''')

	def enterEvent(self, event: QEnterEvent) -> None:
		self.style_sheet(self.enter_color)

		return super().enterEvent(event)

	def leaveEvent(self, event: QEvent) -> None:
		self.style_sheet(self.leave_color)

		return super().leaveEvent(event)