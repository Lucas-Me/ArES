# IMPORT QT_CORE
from qt_core import *

# Data Manager Page UI Class
class UI_DataVisualization(object):
    
	def setup_ui(self, parent : QWidget):
		
		if not parent.objectName():
			parent.setObjectName(u'visualization_page')

		# CENTRAL LAYOUT
		self.main_layout = QVBoxLayout(parent)
		self.main_layout.setContentsMargins(0, 0, 0, 0)
		self.main_layout.setSpacing(0)
		
		# ADD TO CENTRAL LAYOUT
		# ///////////////////////////////////////////
		self.main_layout.addWidget(parent.tab_widget)

		# STYlE
		self.setup_stylesheet(parent)

	def setup_stylesheet(self, parent : QWidget):
		# COLORS AND PROPERTIES
		bg_color = '#ededed'
		font = 'Microsoft New Tai Lue'
		radius = 3

		# STYLE
		parent.setStyleSheet(f'''
			QTabWidget::pane {{ /* The tab widget frame */
				border: 1px solid #2a3f54;
			}}
			QTabWidget::tab-bar {{
				left: 5px; /* move to the right by 5px */
			}}
			/* Style the tab using the tab sub-control. Note that
				it reads QTabBar _not_ QTabWidget */
			QTabBar::tab {{
				background: #ffffff;
				font: 500 12pt '{font}';
				color: #2a3f54;
				min-width: 20ex;
				min-height: 8ex;
				border: none;
				border-radius: {radius}px;
			}}
			QTabBar::tab:!selected:hover {{
				background-color: #bfbfbf;
			}}
			QTabBar::tab:selected {{
				border: 1px solid lightgray;
			}}
			QTabBar::tab:!selected {{
				background-color: #ededed;
			}}
		''')
