# IMPORT QT CORE
from qt_core import *

class UI_ChartDialog(object):

	def setup_ui(self, parent : QDialog):
		if not parent.objectName():
			parent.setObjectName("title_dialog")

		# MAIN LAYOUT
		self.main_layout = QHBoxLayout(parent)
		self.main_layout.setSpacing(0)
		self.main_layout.setContentsMargins(0, 0, 0, 0)

		self.frame = QFrame()
		self.frame.setFixedSize(parent.width() - parent.margins, parent.height() - parent.margins)
		self.frame.setObjectName('frame')
		#
		self.frame_layout = QVBoxLayout(self.frame)
		self.frame_layout.setContentsMargins(10, 10, 10, 10)
		self.frame_layout.setSpacing(10)
		
		# PROPERTIES
		w, h = self.frame.width(), self.frame.height()

		# HEADER
		# /////////////////////////
		self.header_frame = QFrame()
		self.header_frame.setObjectName('header')
		self.header_frame.setFixedHeight(40)

		# header layout
		self.header_layout = QHBoxLayout(self.header_frame)
		self.header_layout.setContentsMargins(0, 0, 0, 0)
		self.header_layout.setSpacing(5)

		# LABELS
		self.label = QLabel("Tipo de gráfico")
		self.label.setFixedSize(w / 2, 25)
		self.label.setObjectName('label')

		# save button
		self.ok_button = QPushButton('Ok')
		self.ok_button.setFixedSize(70, 25)
		self.ok_button.setObjectName('ok')

		# cancel button
		self.cancel_button = QPushButton('Cancelar')
		self.cancel_button.setFixedSize(70, 25)
		self.cancel_button.setObjectName('cancel')

		# add to header layout
		self.header_layout.addWidget(self.label)
		self.header_layout.addWidget(self.ok_button)
		self.header_layout.addWidget(self.cancel_button)
		#
		self.header_layout.setAlignment(self.label, Qt.AlignmentFlag.AlignLeft)
		self.header_layout.setAlignment(self.ok_button, Qt.AlignmentFlag.AlignRight)
		self.header_layout.setAlignment(self.cancel_button, Qt.AlignmentFlag.AlignRight)

		# BOTTOM ITEMS
		# ///////////////////////////////////////
		self.item_layout = QHBoxLayout()
		self.item_layout.setContentsMargins(3, 3, 3, 3)
		self.item_layout.setSpacing(5)

		# COMBOBOX
		self.combobox = QComboBox()
		self.combobox.setObjectName("combobox")
		self.combobox.addItems(parent.options)

		self.item_layout.addWidget(self.combobox)

		# SETTING UP MAIN LAYOUT
		# ///////////////////////////
		self.frame_layout.addWidget(self.header_frame, alignment=Qt.AlignmentFlag.AlignTop)
		self.frame_layout.addLayout(self.item_layout)
		#
		self.main_layout.addWidget(self.frame)
		self.main_layout.setAlignment(self.frame, Qt.AlignmentFlag.AlignCenter)

		# set style
		self.setup_style(parent)

	def setup_style(self, parent : QDialog):
		text_color = '#1c1c1c'
		font_family = 'Microsoft New Tai Lue'
		hover_color = '#e4e4e4'
		pressed_color ='#c1c1c1'

		parent.setStyleSheet(f'''
			#frame{{
				background-color: white;
			}}
			#ok, #cancel{{
				background-color: #fafafa;
				font: 500 12pt {font_family};
				color: #4ca0e0;
				border-radius: 4px;
				border: 1px solid #4ca0e0;
			}}
			#ok:hover, #cancel:hover, #bold_button:hover{{
				background-color: {hover_color};
			}}
			#ok:pressed, #cancel:pressed, #bold_button:pressed{{
				background-color: {pressed_color};
			}}
			#ok:disabled, #cancel:disabled{{
				background-color: #dfdfdf;
				color: #8f8f8f;
				border-color: #8f8f8f;
			}}
			#label {{
				font: bold 13pt {font_family};
				color: {text_color};
			}}
			#header{{
				background-color: transparent;
				border-bottom: 1px solid #c7c7c7;
			}}
			#combobox {{
				font: bold 10pt {font_family};
				color: {text_color};
			}}
		''')