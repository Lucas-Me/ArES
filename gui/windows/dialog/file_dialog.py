# IMPORT QT CORE
from qt_core import *

# IMPORT CUSTOM FUNCTIONS
from backend.misc.functions import drawShadow, get_imagepath

class FileDialog(QDialog):

	def __init__(self, _object, parent = None):
		super().__init__(parent)
		
		# SETTINGS
		self.origin = _object.metadata['signature'][:3].upper()
		self.image = self.imageSetup()
		self.name = _object.metadata['name']
		self.enterprise = _object.metadata['enterprise']

		# CONFIGURATIONS
		self.setModal(True)
		self.setObjectName('file_dialog')
		#
		self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint | Qt.NoDropShadowWindowHint)
		self.setAttribute(Qt.WA_TranslucentBackground, True)
		self.setFixedSize(500, 300)
		#
		self.setup_properties()
		self.setup_stylesheet()
		
		# SIGNALS AND SLOTS
		self.cancel_button.clicked.connect(self.cancelAction)
		self.ignore_button.clicked.connect(self.ignoreAction)
		self.replace_button.clicked.connect(self.replaceAction)
	
	def cancelAction(self):
		self.parent().file_dialog_code = 0
		self.close()

	def replaceAction(self):
		self.replicateCommand()
		self.parent().file_dialog_code = 2
		self.close()

	def ignoreAction(self):
		self.replicateCommand()
		self.parent().file_dialog_code = 1
		self.close()

	def replicateCommand(self):
		self.parent().replicate_command = self.replace_all.isChecked()

	def imageSetup(self):
		if self.origin == 'XLS':
			image = 'icon_xls_file.svg'
		else:
			image = 'icon_sql.svg'
		
		return image

	def setup_properties(self):
		
		# LAYOUT
		self.main_layout = QVBoxLayout(self)
		self.main_layout.setSpacing(0)
		self.main_layout.setContentsMargins(0, 0, 0, 0)

		# FRAME LAYOUR
		self.frame = QFrame()
		self.frame.setObjectName('frame')
		self.frame.setFixedSize(self.width() - 20, self.height() - 20)
		w, h = self.frame.width(), self.frame.height()

		self.frame_layout = QVBoxLayout(self.frame)
		self.frame_layout.setContentsMargins(0, 0, 0, 0)
		self.frame_layout.setSpacing(0)

		# TOP LABEL
		self.title = QLabel('Conflito ao importar')
		self.title.setObjectName('title')
		self.title.setFixedSize(w, 40)
		self.title.setAlignment(Qt.AlignmentFlag.AlignLeft)

		# MIDDLE FRAME
		# ///////////////////////////////////////////////////////////
		self.middle_layout = QVBoxLayout()
		self.middle_layout.setSpacing(0)
		self.middle_layout.setContentsMargins(10, 10, 10, 10)

		# MESSAGE
		self.message = QLabel('O objeto já está aberto no programa.')
		self.message.setObjectName("message")
		self.message.setAlignment(Qt.AlignmentFlag.AlignLeft)
		self.message.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Minimum)
		self.message.setWordWrap(True)

		# PROPERTIES
		self.properties_layout = QHBoxLayout()
		self.properties_layout.setContentsMargins(0, 0, 0, 0)
		self.properties_layout.setSpacing(0)
		#
		self.item_icon = Logo(width = 100, height = 50, image = self.image)
		#
		self.informations = QLabel(f'<b>Nome:</b> {self.name}<br><b>Empresa:</b> {self.enterprise}<br><b>Origem:</b> {self.origin}')
		self.informations.setObjectName('information')
		self.informations.setAlignment(Qt.AlignmentFlag.AlignLeft)
		self.informations.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Expanding)
		self.informations.setWordWrap(True)
		self.informations.setTextFormat(Qt.RichText)
		#
		self.properties_layout.addWidget(self.item_icon)
		self.properties_layout.addWidget(self.informations)
		self.properties_layout.setAlignment(self.item_icon, Qt.AlignmentFlag.AlignCenter)
		self.properties_layout.setAlignment(self.informations, Qt.AlignmentFlag.AlignVCenter)

		# CHECK BUTTON
		self.replace_all = QCheckBox("Fazer isso para os demais conflitos")
		self.replace_all.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Minimum)
		self.replace_all.setObjectName("check_box")

		# add to middle layout
		self.middle_layout.addWidget(self.message)
		self.middle_layout.addLayout(self.properties_layout)
		self.middle_layout.addWidget(self.replace_all)
		self.middle_layout.setAlignment(self.replace_all, Qt.AlignmentFlag.AlignLeft)

		# BOTTOM FRAME
		# ///////////////////////////////////////////////////////////
		self.bottom_frame = QFrame()
		self.bottom_frame.setFixedSize(w, 50)
		self.bottom_frame.setObjectName('bottom_frame')
		self.bottom_layout = QHBoxLayout(self.bottom_frame)
		self.bottom_layout.setSpacing(10)
		self.bottom_layout.setContentsMargins(10, 10, 10, 10)

		# replace
		self.replace_button = QPushButton("Substituir")
		self.replace_button.setFixedSize(80, 30)
		self.replace_button.setObjectName('replace')

		# cancel
		self.cancel_button = QPushButton("Cancelar")
		self.cancel_button.setFixedSize(80, 30)
		self.cancel_button.setObjectName('cancel')

		# ignore
		self.ignore_button = QPushButton("Ignorar")
		self.ignore_button.setFixedSize(80, 30)
		self.ignore_button.setObjectName('ignore')

		# add to bottom layout
		self.bottom_layout.addItem(QSpacerItem(w - 110, 30, QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding))
		self.bottom_layout.addWidget(self.replace_button)
		self.bottom_layout.addWidget(self.ignore_button)
		self.bottom_layout.addWidget(self.cancel_button)

		# ADD TO MAIN LAYOUT
		self.frame_layout.addWidget(self.title)
		self.frame_layout.addLayout(self.middle_layout)
		self.frame_layout.addWidget(self.bottom_frame)
		#
		self.main_layout.addWidget(self.frame)
		self.main_layout.setAlignment(self.frame, Qt.AlignmentFlag.AlignCenter)

	def setup_stylesheet(self):
		self.setStyleSheet('''
			#frame{
				background-color: #ffffff;
				border: 1px solid;
				font: 500 14pt 'Microsoft New Tai Lue';
				color: white;
				border-color: #dfdfdf;
			}
			#replace{
				background-color: #f53c00;
				border: 1px solid #dfdfdf;
				font: 500 12pt 'Microsoft New Tai Lue';
				text-align: middle;
				color: white;
			}
			#replace:hover{
				background-color: #d90438;
			}
			#cancel{
				background-color: #ffffff;
				border: 1px solid #dfdfdf;
				font: 500 12pt 'Microsoft New Tai Lue';
				text-align: middle;
				color: gray;
			}
			#cancel:hover{
				background-color: #e1e1e1;
			}
			#ignore{
				background-color: #ffffff;
				border: 1px solid #dfdfdf;
				font: 500 12pt 'Microsoft New Tai Lue';
				text-align: middle;
				color: gray;
			}
			#ignore:hover{
				background-color: #e1e1e1;
			}
			#check_box{
				font: 500 10pt 'Microsoft New Tai Lue';
			}
			#title{
				background-color: transparent;
				border-bottom: 1px solid;
				border-color: #dfdfdf;
				font: 500 14pt 'Microsoft New Tai Lue';
				color: black;
				padding-left: 10px;
				padding-top: 10px;
			}
			#message{
				background-color: transparent;
				font: 500 12pt 'Microsoft New Tai Lue';
				color: #3874bd;
			}
			#information{
				background-color: transparent;
				font: 500 10pt 'Microsoft New Tai Lue';
				color: black;
			}
			#bottom_frame{
				background-color: #f0f0f0;
				border: 1px solid;
				border-color: #dfdfdf;
			}
		''')

	def paintEvent(self, event: QPaintEvent) -> None:
		painter = QPainter(self)
		drawShadow(
			painter,
			10,
			2.0,
			QColor(120, 120, 120, 32),
			QColor(255, 255, 255, 0),
			0.0,
			1.0,
			0.6,
			self.width(),
			self.height()
		)


class Logo(QWidget):

	def __init__(self, width, height, image):
		super().__init__()

		self.image_name = image

		# properties
		self.setMinimumHeight(height)
		self.setFixedWidth(width)

	def paintEvent(self, event: QPaintEvent) -> None:
		super().paintEvent(event)

		# Painter
		qp = QPainter()
		qp.begin(self)
		qp.setRenderHint(QPainter.Antialiasing)
		qp.setPen(Qt.NoPen)

		# format Path
		icon_path = get_imagepath(self.image_name, 'gui/images/icons')
		icon = QPixmap(icon_path)
		dy = self.height()
		dx = dy / icon.height() *  icon.width()
		icon = icon.scaled(dx, dy, Qt.AspectRatioMode.IgnoreAspectRatio, Qt.TransformationMode.SmoothTransformation)
		
		# positioning in the middle
		x = (self.width() - icon.width()) // 2
		y = (self.height() - icon.height()) // 2

		# scale icon ot dimensions
		qp.drawPixmap(x, y, dx, dy, icon)
		qp.end()

		