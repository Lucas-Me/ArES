from qt_core import *


class ColorCode(QWidget):
	'''A table in which each cell is a color'''

	colorChanged = Signal(QColor)
	def __init__(self, color : QColor):
		super().__init__()

		# PROPERTIES
		self.color_object = color

		# SETTINGS
		self.setupUI()

		# signals and slots
		self.rgb_spinboxes[0].editingFinished.connect(lambda: self.rgbChanged(0))
		self.rgb_spinboxes[1].editingFinished.connect(lambda: self.rgbChanged(1))
		self.rgb_spinboxes[2].editingFinished.connect(lambda: self.rgbChanged(1))
		self.hex_line_edit.editingFinished.connect(self.hexChanged)

	def setupUI(self):
		self.main_layout = QGridLayout(self)
		self.main_layout.setSpacing(5)
		self.main_layout.setContentsMargins(0, 0, 0, 0)

		# OBJECTS
		self.rgb_text = QLabel("RGB")
		self.rgb_text.setObjectName('RGB_TEXT')
		self.hex_text = QLabel("HEX")
		self.hex_text.setObjectName('HEX_TEXT')
		
		# RGB OBJECTS
		self.rgb_frame = QFrame()
		self.rgb_frame.setObjectName("RGB_FRAME")
		self.rgb_layout = QHBoxLayout(self.rgb_frame)
		self.rgb_layout.setContentsMargins(5, 5, 5, 5)
		self.rgb_layout.setSpacing(5)

		# spinbox
		self.rgb_spinboxes = [None] * 3
		rgb_tuple = self.color_object.getRgb()
		for i in range(3):
			spinbox = QSpinBox()
			spinbox.setRange(0, 255)
			spinbox.setValue(rgb_tuple[i])
			spinbox.setButtonSymbols(QAbstractSpinBox.NoButtons)
			self.rgb_spinboxes[i] = spinbox
			self.rgb_layout.addWidget(self.rgb_spinboxes[i])

		# HEX OBJECTS
		self.hex_line_edit = QLineEdit(self.color_object.name())
		self.hex_line_edit.setObjectName("HEX_EDIT")
		self.hex_line_edit.setMaxLength(9)

		# add to main layout
		self.main_layout.addWidget(self.rgb_text, 0, 0)
		self.main_layout.addWidget(self.hex_text, 1, 0)
		self.main_layout.addWidget(self.rgb_frame, 0, 1)
		self.main_layout.addWidget(self.hex_line_edit, 1, 1)

		# setup style
		self.setupStyle()

	def setupStyle(self):
		font = "Microsoft New Tai Lue"
		font_size = 12
		font_color = '#303030'
		self.setStyleSheet(f'''
			#RGB_TEXT, #HEX_TEXT {{
				background-color: transparent;
				font: bold {font_size}pt '{font}';
				color: {font_color};
			}}
			#RGB_FRAME, #HEX_EDIT {{
				background-color: #303030;
				border: 1px solid #dcdcdc;
				border-radius: 5px;
				font: bold {font_size}pt '{font}';
				color: #fcfcfc;
			}}
			QSpinBox {{
				border-width : 0;
				background-color: #303030;
				border: 1px solid #dcdcdc;
				border-radius: 5px;
				font: bold {font_size}pt '{font}';
				color: #fcfcfc;
			}}
		''')

	def rgbChanged(self, row : int):
		current_rgb = list(self.color_object.getRgb())
		current_rgb[row] = self.rgb_spinboxes[row].value()
		self.color_object = QColor.fromRgb(*current_rgb)

		self.updateText(which = 'hex')

	def hexChanged(self):
		current_text = self.hex_line_edit.text()
		try:
			self.color_object = QColor(current_text)
			self.updateText(which = 'rgb')
		except:
			self.hex_line_edit.setText(self.color_object.name())

	
	def updateText(self, which):
		if which == 'hex':
			self.hex_line_edit.setText(self.color_object.name())
		
		elif which == 'rgb':
			current_rgb = self.color_object.getRgb()
			for i in range(3):
				self.rgb_spinboxes[i].setValue(current_rgb[i])

		else:
			self.hex_line_edit.setText(self.color_object.name())
			current_rgb = self.color_object.getRgb()
			for i in range(3):
				self.rgb_spinboxes[i].setValue(current_rgb[i])

			return None

		self.colorChanged.emit(self.color_object)

	def setColor(self, color : QColor):
		self.color_object = color
		self.updateText(which = 'both')