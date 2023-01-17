# IMPORT QT CORE
from qt_core import *

# IMPORT MODULES
import os

class UI_PyDateEdit(object):
	
	def setup_ui(self, parent : QFrame):
		if not parent.objectName():
			parent.setObjectName("double_date_edit")

		# LAYOUT
		self.main_layout = QHBoxLayout(parent)
		self.main_layout.setContentsMargins(10, 0, 10, 0)
		self.main_layout.setSpacing(0)

		# spacer
		self.spacer = QSpacerItem(20, 40, QSizePolicy.Expanding, QSizePolicy.Minimum)

		# text label
		self.label = QLabel(' - ')
		self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

		# adding widgets to main layout
		self.main_layout.addWidget(parent.start_date)
		self.main_layout.addWidget(QLabel(' - '))
		self.main_layout.addWidget(parent.end_date)
		self.main_layout.addItem(self.spacer)
		self.main_layout.addWidget(parent.popup_btn)

		# object properties
		r = parent.height() - 10
		parent.popup_btn.setIcon(parent.calendar_icon)
		parent.popup_btn.setFixedSize(QSize(r, r))
		parent.popup_btn.setIconSize(QSize(r, r))
		parent.start_date.setButtonSymbols(QAbstractSpinBox.NoButtons)
		parent.end_date.setButtonSymbols(QAbstractSpinBox.NoButtons)
		#
		parent.popup_btn.setObjectName("popup_button")
		parent.start_date.setObjectName("start_date")
		parent.end_date.setObjectName("end_date")

		# STYLESHEET
		parent.setStyleSheet(f''' 
			#double_date_edit {{
				background-color: #ffffff;
				font: bold 12pt "Microsoft New Tai Lue";
				color: #666666;
				border: solid;
				border-width: 2px;
				border-color: #b7c4c8;
				border-radius: 10px;
			}}
			#double_date_edit:hover {{
				border-color: #5353f1;
			}}
			#popup_button {{
				border: none;
				background-color: 0px;
				margin: 0px 0px 0px 0px;
				border-radius: 2px;
			}}
			#popup_button:pressed{{
				background-color: #f5f5f5;
			}}
			QDateEdit {{
				border: none;
				background-color: transparent;
				font: bold 12pt "Open Sans";
				margin-top: 2px;
			}}
			QLabel {{
				border:none;
				background-color: transparent;
				font: bold 15pt "Open Sans";
			}}
		''')

		

	