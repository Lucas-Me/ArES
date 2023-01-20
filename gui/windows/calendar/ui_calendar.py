# IMPORT QT CORE
from qt_core import *

# IMPORT BUILT-IN MODULES
import os

# IMPORT CUSTOM FUNCTIONS
from backend.misc.functions import get_icon

# UI CALENDAR
class UI_CalendarWidget(object):

	def setup_ui(self, parent : QCalendarWidget):
		if not parent.objectName():
			parent.setObjectName("Calendar")

		# PROPERTIES
		parent.setGridVisible(False)

		# icons
		next_arrow = get_icon('icon_calendar_next_arrow.svg', 'gui/images/icons')
		prev_arrow = get_icon('icon_calendar_prev_arrow.svg', 'gui/images/icons')
	
		# STYLESHEET
		parent.setStyleSheet(f'''
			#Calendar{{
				background-color: transparent;
			}}
			QCalendarWidget{{
				font: bold 11pt "Microsoft New Tai Lue";
				color: #d0d4ddff;
			}}
			QCalendarWidget QWidget{{
				alternate-background-color: #ffffff;
			}}
			QCalendarWidget QWidget#qt_calendar_navigationbar {{
				background-color: #ffffff;
			}}
			QCalendarWidget QToolButton{{
				background-color: #ffffff;
				font: bold 12pt "Microsoft New Tai Lue";
				color: #000000;
			}}
			QCalendarWidget QToolButton:hover{{
				background-color: #f5f5f5;
				border: none;
			}}
			#qt_calendar_nextmonth{{
				background-color: transparent;
				icon-size: 20px;
				qproperty-icon: url({next_arrow});
			}}
			#qt_calendar_nextmonth:hover{{
				background-color: #d7d7d9;
				border: none;
			}}
			#qt_calendar_prevmonth{{
				background-color: transparent;
				icon-size: 20px;
				qproperty-icon: url({prev_arrow});
			}}
			#qt_calendar_prevmonth:hover{{
				background-color: #d7d7d9;
				border: none;
			}}
			QCalendarWidget QTableView{{
				border-width:0px;
				background-color: #ffffff;
				color: #393b43;
				font: bold 12 pt "Open Sans";
			}}
			QCaldendarWidget QTableView::item{{
				font: bold 12 pt "Open Sans";
				color: #393b43;
			}}
			QCalendarWidget QTableView::item:hover{{
				background-color: #d7d7d9;
			}}
		''')

		# MONTH QMENU
		month_qmenu = parent.findChild(QToolButton, name="qt_calendar_monthbutton").children()[0]
		month_qmenu.setStyleSheet(f'''
			QMenu{{
                  background-color: #ffffff;
                  border-radius: 0px;
				  border: 1px solid;
				  border-color: #aaaeba;
            }}
            QMenu::item {{
                    background-color: transparent;
                    padding:3px 20px;
                    margin:5px 10px;
				  	font: bold 10pt "Microsoft New Tai Lue";
            }}
            QMenu::item:selected {{ background-color: #3f40f0; color: #ffffff; border-radius: 5px;}}
		''')


		# CALENDAR QWIDGET PROPERTIES
		parent.setMaximumHeight(parent.h)
		parent.setMaximumWidth(parent.w)
		parent.setMinimumHeight(parent.h)
		parent.setMinimumWidth(parent.w)