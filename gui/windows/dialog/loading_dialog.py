# IMPORT QT CORE
from qt_core import *

# IMPORT CUSTOM FUNCTIONS
from backend.misc.functions import drawShadow, get_imagepath

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


class LoadingWidget(QWidget):

	def __init__(self, width, inner_radius_scale, freq, color, bg_color, span):
		super().__init__()

		# PROPERTIES
		self.ext_radius = width // 2
		self.inner_radius = self.ext_radius / inner_radius_scale
		self.ang_vel = 360 * freq
		self.ang = 0
		self.span = span

		# OTHER PROPERTIES
		self.color = QColor(color)
		self.bg_color = QColor(bg_color)
		self.brush = QBrush(self.color)
		self.brush.setStyle(Qt.SolidPattern)

		# SETTINGS
		self.setFixedSize(width, width)

	def updateTime(self, msecs):
		secs = msecs * 1e-3
		self.ang += self.ang_vel * secs
		self.update()

	def paintEvent(self, event: QPaintEvent) -> None:
		super().paintEvent(event)

		# settings
		startAngle = self.ang  # in degrees
		span = self.span # in degrees

		# Painter
		qp = QPainter()
		qp.begin(self)
		qp.setRenderHint(QPainter.Antialiasing)
		qp.setPen(Qt.NoPen)
		qp.setBrush(self.brush)

		# DRAW PIE
		radius = self.ext_radius
		rect = QRect(0, 0, radius*2, radius*2)
		qp.drawPie(rect, startAngle*16, span*16 )

		# DRAW TRACK
		qp.setBrush(QColor('#e3e8f3'))
		rect = QRect(0, 0, radius*2, radius*2)
		startAngle = startAngle + span
		span = 360 - span
		qp.drawPie(rect, startAngle*16, span*16 )

		# DRAW INTERNAL CIRCLE
		qp.setBrush(self.bg_color)
		radius = self.inner_radius
		qp.drawEllipse(self.rect().center(), radius, radius)

		qp.end()

		