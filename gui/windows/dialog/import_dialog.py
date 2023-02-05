# IMPORT QT CORE
from qt_core import *

# IMPORT CUSTOM FUNCTIONS
from backend.misc.functions import drawShadow

class ImportDialogSQL(QDialog):
	okClicked = Signal()

	def __init__(self, parent = None):
		super().__init__(parent)
		
		# CONFIGURATIONS
		self.setModal(True)
		self.setObjectName('error_dialog')
		#
		self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint | Qt.NoDropShadowWindowHint)
		self.setAttribute(Qt.WA_TranslucentBackground, True)
		self.setAttribute(Qt.WA_DeleteOnClose, True)
		self.setFixedSize(450, 250)
		#
		self.setup_properties()
		self.setup_stylesheet()
		
		# SIGNALS AND SLOTS
		self.ignore_button.clicked.connect(self.close)
		self.ok_button.clicked.connect(self.okAction)

	def okAction(self):
		self.okClicked.emit()
		self.close()

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
		self.title = QLabel('Erro')
		self.title.setObjectName('title')
		self.title.setFixedSize(w, 40)
		self.title.setAlignment(Qt.AlignmentFlag.AlignLeft)

		# MIDDLE FRAME
		# ///////////////////////////////////////////////////////////
		self.middle_layout = QVBoxLayout()
		self.middle_layout.setSpacing(0)
		self.middle_layout.setContentsMargins(10, 10, 10, 10)

		# MESSAGE
		self.message = QLabel('Não foi possível comunicar-se com o banco de dados')
		self.message.setObjectName("message")
		self.message.setAlignment(Qt.AlignmentFlag.AlignLeft)
		self.message.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
		self.message.setWordWrap(True)

		# description
		self.description = QLabel('Certifique-se de que a conexão com o servidor tenha sido estabelecida.')
		self.description.setObjectName("description")
		self.description.setAlignment(Qt.AlignmentFlag.AlignLeft)
		self.description.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
		self.description.setWordWrap(True)

		# add to middle layout
		self.middle_layout.addWidget(self.message)
		self.middle_layout.addWidget(self.description)

		# BOTTOM FRAME
		# ///////////////////////////////////////////////////////////
		self.bottom_frame = QFrame()
		self.bottom_frame.setFixedSize(w, 50)
		self.bottom_frame.setObjectName('bottom_frame')
		self.bottom_layout = QHBoxLayout(self.bottom_frame)
		self.bottom_layout.setSpacing(10)
		self.bottom_layout.setContentsMargins(10, 10, 10, 10)

		# close button
		self.ok_button = QPushButton("OK")
		self.ok_button.setFixedSize(80, 30)
		self.ok_button.setObjectName('button')

		# cancel button
		self.ignore_button = QPushButton("Ignorar")
		self.ignore_button.setFixedSize(80, 30)
		self.ignore_button.setObjectName('ignore')

		# add to bottom layout
		self.bottom_layout.addItem(QSpacerItem(w - 70, h, QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding))
		self.bottom_layout.addWidget(self.ok_button)
		self.bottom_layout.addWidget(self.ignore_button)

		# ADD TO MAIN LAYOUT
		self.frame_layout.addWidget(self.title)
		self.frame_layout.addLayout(self.middle_layout)
		self.frame_layout.addWidget(self.bottom_frame)
		#
		self.main_layout.addWidget(self.frame)
		self.main_layout.setAlignment(self.frame, Qt.AlignmentFlag.AlignCenter)

	def setup_stylesheet(self):
		self.setStyleSheet('''
			#error_dialog{
				border: 1px solid black;
			}
			#frame{
				background-color: #ffffff;
				border: 1px solid;
				font: 500 14pt 'Microsoft New Tai Lue';
				color: white;
				border-color: #dfdfdf;
			}
			#button{
				background-color: #f53c00;
				border: 1px solid #dfdfdf;
				font: 600 12pt 'Microsoft New Tai Lue';
				text-align: middle;
				color: white;
			}
			#button:hover{
				background-color: #d90438;
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
			#description{
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

