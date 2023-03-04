# IMPORT QT CORE
from qt_core import *

class UI_TitleDialog(object):

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
		self.label = QLabel(parent.display_label)
		self.label.setFixedSize(w / 2, 25)
		self.label.setObjectName('label')

		# save button
		self.save_button = QPushButton('Salvar')
		self.save_button.setFixedSize(70, 25)
		self.save_button.setObjectName('save')

		# cancel button
		self.cancel_button = QPushButton('Cancelar')
		self.cancel_button.setFixedSize(70, 25)
		self.cancel_button.setObjectName('cancel')

		# add to header layout
		self.header_layout.addWidget(self.label)
		self.header_layout.addWidget(self.save_button)
		self.header_layout.addWidget(self.cancel_button)
		#
		self.header_layout.setAlignment(self.label, Qt.AlignmentFlag.AlignLeft)
		self.header_layout.setAlignment(self.save_button, Qt.AlignmentFlag.AlignRight)
		self.header_layout.setAlignment(self.cancel_button, Qt.AlignmentFlag.AlignRight)

		# BOTTOM ITEMS
		# ///////////////////////////////////////
		self.item_layout = QHBoxLayout()
		self.item_layout.setContentsMargins(3, 3, 3, 3)
		self.item_layout.setSpacing(5)

		# TEXT
		self.line = QLineEdit(parent.current_title)
		self.line.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
		self.line.setObjectName('label_edit')

		# BOLD
		self.bold = QPushButton('B')
		self.bold.setCheckable(True)
		self.bold.setObjectName('bold_button')
		self.bold.setFixedSize(25, 25)
		self.bold.setChecked(parent.current_fontweight == 'bold')

		# FONTSIZE
		self.fontsize = QSpinBox()
		self.fontsize.setRange(0, 50)
		self.fontsize.setObjectName('fontsize')
		self.fontsize.setFixedSize(40, 25)
		self.fontsize.setValue(parent.current_fontsize)

		# ADD TO MAIN LAYOUT
		self.item_layout.addWidget(self.line)
		self.item_layout.addWidget(self.bold)
		self.item_layout.addWidget(self.fontsize)

		# SETTING UP MAIN LAYOUT
		# ///////////////////////////
		self.frame_layout.addWidget(self.header_frame)
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
			#save, #cancel{{
				background-color: #fafafa;
				font: 500 12pt {font_family};
				color: #4ca0e0;
				border-radius: 4px;
				border: 1px solid #4ca0e0;
			}}
			#save:hover, #cancel:hover, #bold_button:hover{{
				background-color: {hover_color};
			}}
			#save:pressed, #cancel:pressed, #bold_button:pressed{{
				background-color: {pressed_color};
			}}
			#save:disabled, #cancel:disabled{{
				background-color: #dfdfdf;
				color: #8f8f8f;
				border-color: #8f8f8f;
			}}
			#bold_button:checked{{
				background-color: #dfdfdf;
				font: bold 10pt 'Microsoft New Tai Lue';
			}}
			#label {{
				font: bold 13pt {font_family};
				color: {text_color};
			}}
			#header{{
				background-color: transparent;
				border-bottom: 1px solid #c7c7c7;
			}}
			#label_edit{{
				font: normal 10pt 'Microsoft New Tai Lue';
				padding-left: 5px;
			}}
			#bold_button {{
				font: normal 10pt 'Microsoft New Tai Lue';
				color: #4ca0e0;
				border-radius: 4px;
				border: 1px solid #4ca0e0;
			}}
		''')