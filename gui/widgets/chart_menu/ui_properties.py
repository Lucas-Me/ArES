# IMPORT QT MODULES
from qt_core import *

# IMPORT CUSTOMW WIDGETS
from gui.widgets.chart_menu.buttons import TopLevelButton
from gui.widgets.chart_menu.title_edit import TitleTopLevel

class UI_AbstractMenu(object):
    
	def setupUI(self, parent):

		# NAME
		if not parent.objectName():
			parent.setObjectName('chart_menu')

		# MAIN LAYOUT
		self.right_border_width = 1
		self.main_layout = QVBoxLayout(parent)
		self.main_layout.setContentsMargins(0, 0, self.right_border_width, 0)
		self.main_layout.setSpacing(0)

		# TOP LABEL
		self.top_label = QLabel("Propriedades")
		self.top_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
		self.top_label.setFixedHeight(40)
		self.top_label.setObjectName('top_label')

		# BUTTONS
		self.title_level = TitleTopLevel(height = parent.item_height)
		self.legend_button = TopLevelButton(text = "Legenda", height = parent.item_height)
		self.vaxis_button = TopLevelButton(text = "Eixo Vertical", height = parent.item_height)

		# ADD TO MAIN LAYOUT
		self.main_layout.addWidget(self.top_label)
		self.main_layout.addWidget(self.title_level)
		self.main_layout.addWidget(self.legend_button)
		self.main_layout.addWidget(self.vaxis_button)
		self.main_layout.addItem(QSpacerItem(20, 20, QSizePolicy.MinimumExpanding, QSizePolicy.Expanding))

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

		
