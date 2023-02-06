# IMPORT QT CORE
from qt_core import *

# IMPORT CUSTOM FUNCTIONS
from backend.misc.functions import drawShadow

# IMPORT CUSTOM WIDGETS
from gui.widgets.circular_loading import LoadingWidget

class LoadingDialog(QDialog):

	finished = Signal(bool)
	def __init__(self, text, parent = None):
		super().__init__(parent)
		
		# SETTINGS
		self.description = text
		self.bg_color = 'white'

		# CONFIGURATIONS
		self.setModal(True)
		self.setObjectName('loading_dialog')
		#
		self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint | Qt.NoDropShadowWindowHint)
		self.setAttribute(Qt.WA_TranslucentBackground, True)
		self.setAttribute(Qt.WA_DeleteOnClose, True)
		self.setFixedSize(400, 100)
		#
		self.setup_properties()
		self.setup_stylesheet()

		# SETTING TIMER
		self.timer = QTimer()
		m = 30
		self.timer.timeout.connect(lambda: self.loading.updateTime(m))
		self.timer.start(m)
	
	def closeWindow(self, success):
		self.finished.emit(success)
		self.timer.stop()
		self.timer.deleteLater()
		self.close()

	def updateText(self, text):
		self.description = text
		self.label.setText(text)

	def setup_properties(self):
		
		# LAYOUT
		self.main_layout = QVBoxLayout(self)
		self.main_layout.setSpacing(0)
		self.main_layout.setContentsMargins(0, 0, 0, 0)

		# FRAME LAYOUT
		self.frame = QFrame()
		self.frame.setObjectName('frame')
		self.frame.setFixedSize(self.width() - 20, self.height() - 20)
		w, h = self.frame.width(), self.frame.height()

		self.frame_layout = QHBoxLayout(self.frame)
		margins = 10
		self.frame_layout.setContentsMargins(margins, margins,margins, margins)
		self.frame_layout.setSpacing(margins * 2)

		# LOADING WIDGET
		self.loading = LoadingWidget(
			width = h - margins * 2,
			inner_radius_scale = 1.5,
			color = '#1fbde0',
			bg_color = self.bg_color,
			freq = 1.5,
			span = 80 # in degrees
		)

		# DESCRIPTION LABEL
		self.label = QLabel(self.description)
		self.label.setObjectName('information')
		self.label.setWordWrap(True)
		self.label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

		# ADD TO FRAME LAYOUT
		self.frame_layout.addWidget(self.loading)
		self.frame_layout.addWidget(self.label)
		#
		self.frame_layout.setAlignment(self.loading, Qt.AlignmentFlag.AlignCenter)
		self.frame_layout.setAlignment(self.label, Qt.AlignmentFlag.AlignVCenter)

		# ADD TO MAIN LAYOUT
		self.main_layout.addWidget(self.frame)
		self.main_layout.setAlignment(self.frame, Qt.AlignmentFlag.AlignCenter)

	def setup_stylesheet(self):
		self.setStyleSheet(f'''
			#frame{{
				background-color: {self.bg_color};
				border: 1px solid;
				font: 500 14pt 'Microsoft New Tai Lue';
				color: white;
				border-color: #dfdfdf;
			}}
			#information{{
				background-color: transparent;
				font: 500 13pt 'Microsoft New Tai Lue';
				color: #8396a2;
			}}
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



		