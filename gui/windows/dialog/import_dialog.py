# IMPORT QT CORE
from qt_core import *


class ImportDialogSQL(QDialog):

	def __init__(self, parent = None):
		super().__init__(parent)
		
		# CONFIGURATIONS
		self.setObjectName('error_dialog')
		self.setModal(True)
		self.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog)
		#
		self.setup_properties()
		self.setup_stylesheet()

		# SIGNALS AND SLOTS
		self.button.clicked.connect(self.close)

	def setup_properties(self):
		w, h = (350, 200)
		self.setFixedSize(w, h)

		# LAYOUT
		self.main_layout = QVBoxLayout(self)
		self.main_layout.setSpacing(0)
		self.main_layout.setContentsMargins(0, 0, 0, 0)

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
		self.message = QLabel('Não foi possível comunicar-se com o\nbanco de dados')
		self.message.setObjectName("message")
		self.message.setAlignment(Qt.AlignmentFlag.AlignLeft)
		self.message.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)

		# description
		self.description = QLabel('Certifique-se de que a conexão com o servidor\ntenha sido estabelecida.')
		self.description.setObjectName("description")
		self.description.setAlignment(Qt.AlignmentFlag.AlignLeft)
		self.description.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)

		# add to middle layout
		self.middle_layout.addWidget(self.message)
		self.middle_layout.addWidget(self.description)

		# BOTTOM FRAME
		# ///////////////////////////////////////////////////////////
		self.bottom_frame = QFrame()
		self.bottom_frame.setFixedSize(w, 50)
		self.bottom_frame.setObjectName('bottom_frame')
		self.bottom_layout = QHBoxLayout(self.bottom_frame)
		self.bottom_layout.setSpacing(0)
		self.bottom_layout.setContentsMargins(10, 10, 10, 10)

		# close button
		self.button = QPushButton("OK")
		self.button.setFixedSize(80, 30)
		self.button.setObjectName('button')

		# add to bottom layout
		self.bottom_layout.addWidget(self.button)
		self.bottom_layout.setAlignment(self.button, Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

		# ADD TO MAIN LAYOUT
		self.main_layout.addWidget(self.title)
		self.main_layout.addLayout(self.middle_layout)
		self.main_layout.addWidget(self.bottom_frame)

		# additional configuration

	def setup_stylesheet(self):
		self.setStyleSheet('''
			#error_dialog{
				background-color: #4f67d8;
				border: 1px solid;
				font: 500 14pt 'sans-serif';
				color: white;
				border-color: #000000;
			}
			#button{
				background-color: #f53c00;
				border: none;
				font: 600 14pt 'sans-serif';
				color: white;
				border-radius: 5px;
			}
			#button:hover{
				background-color: #d90438;
			}
			#title{
				background-color: transparent;
				border-bottom: 1px solid;
				border-color: white;
				font: 600 14pt 'sans-serif';
				color: white;
				padding-left: 10px;
				padding-top: 10px;
			}
			#message{
				background-color: transparent;
				font: 600 13pt 'Microsoft New Tai Lue';
				color: white;
			}
			#description{
				background-color: transparent;
				font: 500 11pt 'Microsoft New Tai Lue';
				color: white;
			}
			#bottom_frame{
				background-color: white;
				border: 1px solid;
				border-top: none;
				border-color: #000000;
			}
		''')


