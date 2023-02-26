# IMPORT QT MODULES
from qt_core import *

# IMPORT CUSTOM WIDGETS
from gui.widgets.chart_menu.buttons import TopLevelButton

class TitleTopLevel(QWidget):

	labelEdited = Signal(list)
	def __init__(self, height):
		super().__init__()

		# PROPERTIES
		self.item_height = height

		# UI
		self.setupUI()
		self.toggle()

		# SIGNALS
		self.top_level.clicked.connect(self.toggle)
		self.figure_title.labelEdited.connect(self.labelEdited.emit)
		self.xaxis_label.labelEdited.connect(self.labelEdited.emit)
		self.yaxis_label.labelEdited.connect(self.labelEdited.emit)

	def toggle(self):
		hidden = self.top_level.getStatus()
		active = not hidden
	
		# toggle on (active) or off
		self.top_level.setActive(active)

		# show/hide widgets
		self.figure_title.setHidden(hidden)
		self.xaxis_label.setHidden(hidden)
		self.yaxis_label.setHidden(hidden)

		# size policty
		if active:
			self.setFixedHeight(self.item_height * 4)
		else:
			self.setFixedHeight(self.item_height)
	
	def setupUI(self):
		if not self.objectName():
			self.setObjectName("title_top_level")

		self.main_layout = QVBoxLayout(self)
		self.main_layout.setContentsMargins(0, 0, 0, 0)
		self.main_layout.setSpacing(0)

		# OBJECTS
		self.top_level = TopLevelButton(text = "Título", height = self.item_height)
		
		# FIGURE LABEL EDIT
		self.figure_title = LabelEdit("Figura", height = self.item_height, prop = 'title')

		# VERTICAL AXIS LABEL EDIT
		self.yaxis_label = LabelEdit("Eixo Vertical", height = self.item_height, prop = 'yaxis')

		# HORIZONTAL AXIS LABEL EDIT
		self.xaxis_label = LabelEdit("Eixo Horizontal", height = self.item_height, prop = 'xaxis')

		# add to layout
		self.main_layout.addWidget(self.top_level)
		self.main_layout.addWidget(self.figure_title)
		self.main_layout.addWidget(self.yaxis_label)
		self.main_layout.addWidget(self.xaxis_label)


class LabelEdit(QWidget):
    
	labelEdited = Signal(list)
	def __init__(self, text, height, prop, *args, **kwargs):
		super().__init__(*args, **kwargs)

		# settings
		self.setFixedHeight(height)

		# PROPERTIES
		self.text = text
		self.property = prop
		self.left_margin = 25

		# SETUP UI
		self.setupUI()
		self.setupStyle()

		# SIGNALS AND SLOTS
		self.line.editingFinished.connect(self.emitSignal)
		self.bold.clicked.connect(self.emitSignal)
		self.fontsize.valueChanged.connect(self.emitSignal)

	def emitSignal(self):
		# texto, negrito, font size, property
		this = [self.line.text(), self.bold.isChecked(), self.fontsize.value(), self.property]
		self.labelEdited.emit(this)

	def setupUI(self):
		self.main_layout = QHBoxLayout(self)
		self.main_layout.setContentsMargins(self.left_margin, 3, 3, 3)
		self.main_layout.setSpacing(5)
		self.setObjectName('item')

		# TEXT
		self.line = QLineEdit()
		self.line.setPlaceholderText(self.text)
		self.line.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
		self.line.setObjectName('label_edit')

		# BOLD
		self.bold = QPushButton('B')
		self.bold.setCheckable(True)
		self.bold.setObjectName('bold_button')
		self.bold.setFixedSize(25, 25)

		# FONTSIZE
		self.fontsize = QSpinBox()
		self.fontsize.setRange(0, 50)
		self.fontsize.setObjectName('fontsize')
		self.fontsize.setFixedSize(40, 25)

		# ADD TO MAIN LAYOUT
		self.main_layout.addWidget(self.line)
		self.main_layout.addWidget(self.bold)
		self.main_layout.addWidget(self.fontsize)

	def setupStyle(self):
		self.setStyleSheet('''
			#item{
				background-color: transparent;
			}
			#label_edit{
				font: normal 10pt 'Microsoft New Tai Lue';
				padding-left: 5px;
			}
			#bold_button {
				font: bold 10pt 'Microsoft New Tai Lue';
			}
		''')

	def paintEvent(self, event: QPaintEvent) -> None:
		super().paintEvent(event)

		painter = QPainter()
		painter.begin(self)
		
		dx = 2
		x = (self.left_margin - dx) // 2
		y = 0
		dy = self.height()
		painter.fillRect(x, y, dx, dy, QColor('#36475f'))

		painter.end()
		