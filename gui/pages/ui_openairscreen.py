# IMPORT BUILT-IN MODULES
import os

# IMPORT QT_CORE
from qt_core import *

# IMPORT CUSTOM MODULES
from backend.misc.functions import get_imagepath
from gui.widgets.login_screen import Logo
from gui.widgets.py_push_button import ClassicButton

# Data Manager Page UI Class
class UI_OpenAirScreen(object):
    
	def setup_ui(self, parent):

		# FRAME CONSTANTS
		parent.setObjectName(u'openair_page')

		# MAIN LAYOUT
		self.main_layout = QGridLayout(parent)
		self.main_layout.setVerticalSpacing(20)
		self.main_layout.setHorizontalSpacing(20)
		self.main_layout.setContentsMargins(20, 20, 20, 20)
		self.main_layout.setRowStretch(2, 4)

		# R AND SAVE DIRECTORY FOLDERS
		# ///////////////////////////////////////////////////////////
		# icons
		r_icon = Logo(35, 25, get_imagepath('R_logo.svg', 'gui/images/icons'))
		folder_icon = Logo(30, 25, get_imagepath('folder_icon.svg', 'gui/images/icons'))
		
		# Lines
		self.r_directory = ClickableLabel("")
		self.r_directory.setFixedHeight(25)
		self.r_directory.setObjectName('directory')
		self.r_directory.setCursor(Qt.PointingHandCursor)
		#
		self.save_directory = ClickableLabel(os.path.expanduser("~"))
		self.save_directory.setFixedHeight(25)
		self.save_directory.setObjectName('directory')
		self.save_directory.setCursor(Qt.PointingHandCursor)

		# FIGURE PROPERTIES GROUBOX
		# ///////////////////////////////////////////////////////////
		groupbox = QGroupBox("Propriedades da figura")
		groupbox.setFixedSize(320, 80)
		groupbox_layout = QGridLayout(groupbox)
		groupbox_layout.setVerticalSpacing(5)
		groupbox_layout.setHorizontalSpacing(10)
		groupbox_layout.setContentsMargins(10, 5, 10, 5)
		groupbox_layout.setColumnStretch(2, 2)

		# dpi
		dpi_label = QLabel('DPI')
		dpi_label.setObjectName('label')
		self.dpi = QSpinBox()
		self.dpi.setRange(100, 1000)
		self.dpi.setFixedSize(60,15)
		self.dpi.setSingleStep(100)
		self.dpi.setButtonSymbols(QAbstractSpinBox.NoButtons)

		# proporcao
		prop_label = QLabel('Proporção')
		prop_label.setObjectName('label')
		self.proportion = ProportionWidget(
			vmin = 1, vmax = 20,
			width = 60, height = 15, 
			font_color='#d9e2f1',
			bg_color='#394251'
		)

		# resolucao final
		self.final_resolution = QLabel()
		self.final_resolution.setTextFormat(Qt.RichText)
		
		# add to groupbox layout
		groupbox_layout.addWidget(dpi_label, 0, 0)
		groupbox_layout.addWidget(prop_label, 1, 0)
		groupbox_layout.addWidget(self.dpi, 0, 1)
		groupbox_layout.addWidget(self.proportion, 1, 1)
		groupbox_layout.addWidget(self.final_resolution, 0, 2, 2, 1)

		# MODULE OPTIONS FRAME
		# ////////////////////////////////////////////////
		self.module_frame = QFrame()
		self.module_layout = QVBoxLayout(self.module_frame)
		self.module_frame.setStyleSheet('background-color: transparent;border: 1px solid white;border-radius: 3px')

		# EXECUTE BUTTON
		# ////////////////////////////////////////////////
		self.process_button = ClassicButton(
			text = 'Executar',
			icon_allign='right',
			width = 180,
			height = 40,
			icon_width= 40,
			icon_path= 'icon_next_btn.svg',
			paint_icon=False
		)
		self.process_button.setObjectName('process_btn')

		# ADD TO MAIN LAYOUT
		# ///////////////////////////////////////////////////////////
		self.main_layout.addWidget(parent.resources_list, 0, 0, 4, 1)
		self.main_layout.addWidget(r_icon, 0, 1, 1, 1)
		self.main_layout.addWidget(folder_icon, 1, 1, 1, 1)
		self.main_layout.addWidget(self.r_directory, 0, 2, 1, 1)
		self.main_layout.addWidget(self.save_directory, 1, 2, 1, 1)
		self.main_layout.addWidget(groupbox, 0, 3, 2, 1)
		self.main_layout.addWidget(self.module_frame, 2, 1, 1, 3)
		self.main_layout.addWidget(self.process_button, 3, 3, 1, 1, alignment=Qt.AlignmentFlag.AlignRight)

		# SETTING STYLESHEET
		# ////////////////////////////////////////////////
		self.setup_stylesheet(parent)

	def setup_stylesheet(self, parent):
		color_pallette = ['#20252a', '#394251', '#0d7bbd', '#d9e2f1']

		parent.setStyleSheet(f'''
			#openair_page {{
				background-color: {color_pallette[0]};
			}}
			#directory {{
				background-color: {color_pallette[1]};
				color: {color_pallette[-1]};
				font: normal 10pt 'Microsoft New Tai Lue';
				border-radius: 5px;
				vertical-align: middle;
				padding-left: 5px;
			}}
			#label{{
				background-color: transparent;
				color: {color_pallette[-1]};
				font: bold 10pt 'Microsoft New Tai Lue';
			}}
			QLabel{{
				background-color: transparent;
				color: {color_pallette[-1]};
				font: normal 10pt 'Microsoft New Tai Lue';
			}}
			QGroupBox::title {{
				font: bold 10pt 'Microsoft New Tai Lue';
				color: {color_pallette[-1]};
			}}
			QSpinBox {{
				background-color: {color_pallette[1]};
				color: {color_pallette[-1]};
				font: normal 10pt 'Microsoft New Tai Lue';
			}}
			#process_btn {{
                background-color: #ffffff;
                border: 0.5px solid;
                border-color: #dcdcdc;
                border-radius: 5px;
                font: 500 14pt 'Microsoft New Tai Lue';
                color: {color_pallette[2]};
                padding-left: 20px;
                text-align: left;
            }}
            #process_btn:hover {{
                background-color: #fafafa;
            }}
            #process_btn:pressed {{
                background-color: #e4e4e4;
            }}
		''')


class ClickableLabel(QLabel):

	clicked = Signal()
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

	def mousePressEvent(self, ev: QMouseEvent) -> None:
		self.clicked.emit()
		return super().mousePressEvent(ev)
	

class ProportionWidget(QFrame):

	valueChanged = Signal()
	def __init__(self, vmin, vmax, width, height, bg_color = 'transparent', font_color = 'black'):
		super().__init__()

		# creating widgets
		self.width_spinbox = QSpinBox()
		self.height_spinbox = QSpinBox()
		self.label = QLabel(':')
		
		# widgets settings
		self.width_spinbox.setRange(vmin, vmax)
		self.width_spinbox.setValue(4)
		self.width_spinbox.setButtonSymbols(QAbstractSpinBox.NoButtons)
		self.width_spinbox.lineEdit().setAlignment(Qt.AlignmentFlag.AlignRight)
		self.height_spinbox.setRange(vmin, vmax)
		self.height_spinbox.setValue(3)
		self.height_spinbox.setButtonSymbols(QAbstractSpinBox.NoButtons)
		self.height_spinbox.lineEdit().setAlignment(Qt.AlignmentFlag.AlignLeft)
		self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
		self.setFixedSize(width, height)
		self.setObjectName('widget')

		# Layout
		self.main_layout = QHBoxLayout(self)
		self.main_layout.setSpacing(0)
		self.main_layout.setContentsMargins(0, 0, 0, 0)

		# add to main layout
		self.main_layout.addWidget(self.width_spinbox)
		self.main_layout.addWidget(self.label)
		self.main_layout.addWidget(self.height_spinbox)

		# stylesheet
		self.setStyleSheet(f'''
			QSpinBox::QLineEdit {{
				background-color: {bg_color};
				color: {font_color};
				font: normal 12pt 'Microsoft New Tai Lue';
			}}
			QLabel {{
				background-color: {bg_color};
				color: {font_color};
				font: normal 12pt 'Microsoft New Tai Lue';
			}}
		''')

		# SIGNALS AND SLOTS
		self.width_spinbox.valueChanged.connect(lambda: self.valueChanged.emit())
		self.height_spinbox.valueChanged.connect(lambda: self.valueChanged.emit())

	def getHeight(self):
		return self.height_spinbox.value()

	def getWidth(self):
		return self.width_spinbox.value()
	
	def setHeight(self, value):
		self.height_spinbox.setValue(value)

	def setWidth(self, value):
		self.width_spinbox.setValue(value)