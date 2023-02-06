# IMPORT QT CORE
from qt_core import *


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
