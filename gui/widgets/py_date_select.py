# IMPORT QT CORE
from qt_core import *

# IMPORT UI MODULE
from gui.ui_widgets.ui_date_edit import UI_PyDateEdit

# IMPORT CUSTOM MODULES
from gui.windows.calendar.calendar_dialog import CalendarWidget

# IMPORT BUILT-IN MODULES
import os


class PyDoubleDateEdit(QFrame):

	def __init__(self, parent):
		super().__init__(parent = parent)

		# OBJECTS
		self.calendar_icon = QIcon(self.get_icon('icon_calendar.svg', 'gui/images/icons'))
		self.popup_btn = QToolButton()
		self.end_date = PyDateEdit(QDate().currentDate(), signal = True)
		self.start_date = PyDateEdit(QDate().currentDate().addMonths(-1), signal = False)
		self.calendar_widget = CalendarWidget(self)
		self.dates = [self.start_date.date(), self.end_date.date()]
		self.end_selected = False # False - Start date / True - End date

		# Setting UI
		self.ui = UI_PyDateEdit()
		self.ui.setup_ui(self)
		self.updateSelectedDate()
		
		# PROPERTIES
		self.calendar_widget.setWindowFlag(Qt.FramelessWindowHint | Qt.Window)
		self.start_date.setDisplayFormat("dd MMM yyyy")
		self.end_date.setDisplayFormat("dd MMM yyyy")

		# SIGNAL AND SLOTS
		self.popup_btn.clicked.connect(self.popup_calendar)
		self.start_date.dateChanged.connect(lambda x: self.updateDates(x, False))
		self.end_date.dateChanged.connect(lambda x: self.updateDates(x, True))
		self.start_date.clicked.connect(self.updateSelectedDate)
		self.end_date.clicked.connect(self.updateSelectedDate)
		#
		# LINHAS ABAIXO ESTAO DISPARANDO 2X !!!!!!!!!!!!!!
		self.calendar_widget.start_calendar.clicked.connect(lambda x: self.updateDates(x, False))
		self.calendar_widget.end_calendar.clicked.connect(lambda x: self.updateDates(x, True))

	@Slot(bool)
	def updateSelectedDate(self, selection = False):
		self.selected_date = selection

		colors = ['#26282f', '#b8bdcb']
		old_style = self.styleSheet()
		self.setStyleSheet( old_style + f'''
			#start_date{{
				color: {colors[selection]};
			}}
			#end_date{{
				color: {colors[not selection]};
			}}
		''')

		self.calendar_widget.changePage(int(selection))

	def updateDates(self, new_date, end = False):
		if end:
			if new_date >= self.dates[0]:
				self.dates[1] = new_date

			self.end_date.setDate(self.dates[1])
		
		else:
			if new_date <= self.dates[1]:
				self.dates[0] = new_date

			self.start_date.setDate(self.dates[0])

		self.updateCalendarDates()

	def updateCalendarDates(self):
		widget = self.calendar_widget
		widget.end_calendar.setSelectedDate(self.dates[1])
		widget.start_calendar.setSelectedDate(self.dates[0])

	def popup_calendar(self):
		self.calendar_widget.setVisible(not self.calendar_widget.isVisible())
		self.adjustPopup()

	def adjustPopup(self):
		if not self.calendar_widget.isVisible():
			return None
		
		rect =  QRect(self.geometry())
		bottomLeft = self.mapToGlobal(rect.bottomLeft())

		this_dx = rect.width()
		frame_dx = self.calendar_widget.w
		this_x = bottomLeft.x() - rect.x()
		bottomLeft.setX(this_x + .5 *(this_dx - frame_dx))
		self.calendar_widget.setGeometry(QRect(bottomLeft, QSize(self.calendar_widget.w, self.calendar_widget.h)))
		self.calendar_widget.roundCorners(10)


	def resizeEvent(self, event: QResizeEvent) -> None:
		super().resizeEvent(event)
		self.adjustPopup()

	def moveEvent(self, event: QMoveEvent) -> None:
		# nao funciona
		super().moveEvent(event)
		self.adjustPopup()

	def get_icon(self, icon_name, folder):
		app_path = os.path.abspath(os.getcwd())
		icons_folder = os.path.join(app_path, folder)

		return os.path.join(icons_folder, icon_name).replace('\\', '/')


class PyDateEdit(QDateEdit):
	clicked = Signal(bool)

	def __init__(self, date, signal : bool):
		super().__init__(date)
		self.signal = signal

	def inputMethodQuery(self, arg__1: Qt.InputMethodQuery):
		self.clicked.emit(self.signal)
		return super().inputMethodQuery(arg__1)