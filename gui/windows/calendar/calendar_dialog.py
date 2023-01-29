# IMPORT QT CORE
from qt_core import *

# IMPORT UI MODULES
from gui.windows.calendar.ui_calendar import UI_CalendarWidget

class PyCalendarPicker(QCalendarWidget):

	def __init__(self, parent, order = 0):
		super().__init__(parent = parent)

		# properties
		self.font = QFont("Open Sans", 12)
		self.radius = 10
		self.format = QTextCharFormat()
		self.w = parent.w - 10
		self.h = parent.h - 10
		self.order = order
		self.func = [self.greater_than, self.smaller_than]

		# setup ui
		self.ui = UI_CalendarWidget()
		self.ui.setup_ui(self)

		# setting up date properties
		self.setVerticalHeaderFormat(QCalendarWidget.NoVerticalHeader)
		self.font.setBold(False)
		self.font.setHintingPreference(QFont.PreferDefaultHinting)
		self.font.setStyleStrategy(QFont.PreferAntialias)
		self.format.setFont(self.font)
		self.format.setForeground(QBrush(QColor("#3f40f0")))
		self.setupDateFormat()

		# setting up window properties
		self.setSelectionMode(QCalendarWidget.SelectionMode.SingleSelection)
		self.setWindowFlags(Qt.FramelessWindowHint)
		self.setWindowOpacity(0)

	def setupDateFormat(self):
		self.setHeaderTextFormat(self.format)
		self.format.setForeground(QBrush(QColor("#393b43")))
		self.setWeekdayTextFormat(Qt.DayOfWeek(6), self.format)
		self.setWeekdayTextFormat(Qt.DayOfWeek(7), self.format)

	def paintCell(self, painter: QPainter, rect: QRect, date: QDate) -> None:
		super().paintCell(painter, rect, date)

		# test if same month as shown in calendar
		colors = ['#fb8500', '#393b43']
		same_month = date.month() == self.monthShown()

		pen = QPen(QColor(colors[same_month]))
		pen.setStyle(Qt.PenStyle.SolidLine)
		painter.save()
		painter.beginNativePainting()
		painter.setFont(self.font)
		painter.setPen(pen)
		painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, str(date.day()))
		painter.endNativePainting()
		painter.restore()

		# if date is greater (smaller) than start (end) date
		condition = self.condition(date)
		if condition:
			painter.save()
			painter.setFont(self.font)
			painter.fillRect(rect, QColor("#ededff"))
			pen.setColor(QColor(colors[same_month]))
			painter.setPen(pen)
			painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, str(date.day()))
			painter.restore()

		# if selected date
		if date == self.selectedDate():
			painter.save()
			painter.setFont(self.font)
			painter.fillRect(rect, QColor("#3F40F0"))
			pen.setColor(QColor("#FFFFFF"))
			painter.setPen(pen)
			painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, str(date.day()))
			painter.restore()

	def condition(self, date : QDate):
		idx = not bool(self.order)
		reference = self.parent().reference[idx].selectedDate()
		date = date

		return self.func[idx](date, reference)
	
	def greater_than(self, test, reference):
		return test >= reference and test <= self.selectedDate()

	def smaller_than(self, test, reference):
		return test <= reference and test >= self.selectedDate()


class CalendarWidget(QStackedWidget):

	def __init__(self, parent):
		super().__init__(parent = parent)

		# OBJECTS
		self.w = 400		
		self.h = 250
		self.start_calendar = PyCalendarPicker(self, order = 0)
		self.end_calendar = PyCalendarPicker(self, order = 1)
		self.reference = [self.start_calendar, self.end_calendar]

		# PROPERTIES
		self.start_calendar.setSelectedDate(parent.start_date.date())
		self.end_calendar.setSelectedDate(parent.end_date.date())
		self.setObjectName("calendar_widget")

		# LAYOUT
		self.setContentsMargins(2, 2, 0, 0)
		self.addWidget(self.start_calendar)
		self.addWidget(self.end_calendar)

		# STYLESHEET
		self.setStyleSheet(f'''
			#calendar_widget{{
				background-color: #FFFFFF;
				border: 2px solid;
				border-radius: 10px;
				border-color: black;
			}}
		''')


	def changePage(self, selection):
		options = [self.start_calendar, self.end_calendar]
		self.setCurrentWidget(options[selection])

	def leaveEvent(self, event: QEvent) -> None:
		self.setVisible(False)
		return super().leaveEvent(event)

	def roundCorners(self, radius = 10):		
		path = QPainterPath();
		path.addRoundedRect(self.rect(), radius, radius);
		mask = QRegion(path.toFillPolygon().toPolygon());
		self.setMask(mask);
