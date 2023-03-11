# IMPORT QT MODULES
from qt_core import *
import os, json

# IMPORT UI
from gui.windows.settings.ui_settings import UI_SettingsWindow

# IMPORT CUSTOM FUNCTIONS
from backend.misc.functions import drawShadow

# IMPORT CUSTOM VARIABLES
import backend.misc.settings as settings
from matplotlib import font_manager
import matplotlib as mpl
import numpy as np

class SettingsWindow(QDialog):
    
	def __init__(self, parent = None):
		super().__init__(parent = parent)

		# PROPERTIES
		self.margins = 20
		self.dragPos = QPoint()

		# WINDOW SETTINGS
		self.setFixedSize(400 + self.margins, 350 + self.margins)
		self.setModal(True)
		self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint | Qt.NoDropShadowWindowHint)
		self.setAttribute(Qt.WA_TranslucentBackground, True)
		self.setAttribute(Qt.WA_DeleteOnClose, True)

		# SETUP UI
		self.ui = UI_SettingsWindow()
		self.ui.setup_ui(self)

		# SIGNALS AND SLOTS
		self.ui.btn_exit.clicked.connect(self.close)
		self.ui.btn_connection.clicked.connect(
			lambda: self.updatePage(index = 0, button = self.ui.btn_connection)
			)
		self.ui.btn_criteria.clicked.connect(
			lambda: self.updatePage(index = 1, button = self.ui.btn_criteria)
			)
		self.ui.btn_figure.clicked.connect(
			lambda: self.updatePage(index = 2, button = self.ui.btn_figure)
			)
		self.ui.btn_apply.clicked.connect(self.applyChanges)
		self.ui.btn_save.clicked.connect(self.save_json)

	def save_json(self):
		'''Salva as configurações em um arquivo JSON'''

		# update profile files
		self.updateProfileField()

		# seeking directory
		userhome_directory = os.path.expanduser("~")
		ArES_dir = os.path.join(userhome_directory, '.ArES')
		fname = os.path.join(ArES_dir, 'config.json')

		# saving
		with open(fname, 'w', encoding='utf-8') as f:
			json.dump(settings.SETTINGS, f, ensure_ascii=False, indent=4)
	
	def updateProfileField(self):
		listview = self.parent().ui.pages.process_page.ui.profile_picker.list
		profiles = {}
		for i in range(listview.model.rowCount()):
			profile = listview.getProfile(i)
			profiles[profile.getName()] = [profile.getColor().name(), profile.getMethods()]
	
		settings.SETTINGS['perfis'] = profiles

	def applyChanges(self):
		self.updateSQL()
		self.udpateCriteria()
		self.updateFigure()

	def loadContents(self):
		# BANCO DE DADOS
		self.ui.database_edit.setText(settings.SETTINGS['conexao']['database'])
		self.ui.server_edit.setText(settings.SETTINGS['conexao']['servidor'])

		# CRITERIOS DE VALIDACAO
		self.ui.spinbox_hourly.setValue(settings.SETTINGS['representatividade']['Horária'] * 100)
		self.ui.spinbox_daily.setValue(settings.SETTINGS['representatividade']['Data']  * 100 )
		self.ui.spinbox_monthly.setValue(settings.SETTINGS['representatividade']['Mês e ano']  * 100)
		self.ui.spinbox_yearly.setValue(settings.SETTINGS['representatividade']['Ano']  * 100)
		self.ui.date_edit.setDate(QDate.fromString(settings.SETTINGS['semiautomatica']['data_referencia'], Qt.DateFormat.ISODate))
		self.ui.spinbox_freq.setValue(settings.SETTINGS['semiautomatica']['frequencia'])

		# FIGURA
		self.ui.spinbox_left.setValue(settings.SETTINGS['figura']['left'])
		self.ui.spinbox_right.setValue(settings.SETTINGS['figura']['right'])
		self.ui.spinbox_bottom.setValue(settings.SETTINGS['figura']['bottom'])
		self.ui.spinbox_top.setValue(settings.SETTINGS['figura']['top'])
		self.ui.font_size.setValue(settings.SETTINGS['figura']['font_size'])

		# FAMILY
		families = np.unique(sorted([f.name for f in font_manager.fontManager.afmlist] + [f.name for f in font_manager.fontManager.ttflist]))
		self.ui.font_families.addItems(families)
		self.ui.font_families.setCurrentText(settings.SETTINGS['figura']['font_family'])

	def updateSQL(self):
		login_page = self.parent().ui.pages.login_page

		# if already connected, do not apply and fix the field
		if login_page.sql.get_status():
			self.ui.database_edit.setText(settings.SETTINGS['conexao']['database'])
			self.ui.server_edit.setText(settings.SETTINGS['conexao']['servidor'])
			return None
		
		new_server = self.ui.server_edit.text()
		new_db = self.ui.database_edit.text()

		login_page.sql.configureHost(
			host = new_server,
			db = new_db
		)

		# test connection
		login_page.updateHost()
		login_page.testConnection()

		# update global settings
		settings.SETTINGS['conexao']['database'] = new_db
		settings.SETTINGS['conexao']['servidor'] = new_server

	def udpateCriteria(self):
		# getting new values
		hourly = self.ui.spinbox_hourly.value()
		daily = self.ui.spinbox_daily.value()
		monthly = self.ui.spinbox_monthly.value()
		yearly = self.ui.spinbox_yearly.value()
		ref_date = self.ui.date_edit.date().toPython().strftime('%Y-%m-%d')
		frequency = self.ui.spinbox_freq.value()

		# update global settings
		settings.SETTINGS['representatividade']['Horária'] = hourly / 100
		settings.SETTINGS['representatividade']['Data'] = daily / 100
		settings.SETTINGS['representatividade']['Mês e ano'] = monthly / 100
		settings.SETTINGS['representatividade']['Ano'] = yearly / 100
		settings.SETTINGS['semiautomatica']['data_referencia'] = ref_date
		settings.SETTINGS['semiautomatica']['frequencia'] = frequency

	def updateFigure(self):
		# getting values
		left = self.ui.spinbox_left.value()
		right = self.ui.spinbox_right.value()
		bottom = self.ui.spinbox_bottom.value()
		top = self.ui.spinbox_top.value()
		fontsize = self.ui.font_size.value()
		fontfamily = self.ui.font_families.currentText()

		# update matplotlib standard
		mpl.rcParams.update({
			'font.family': fontfamily,
			'font.size' : fontsize,
			'figure.subplot.bottom' : bottom,
			'figure.subplot.left' : left,
			'figure.subplot.right' : right,
			'figure.subplot.top' : top
			})

		#update charts if open
		for dashboard in self.parent().ui.pages.chart_pages:
			dashboard.canvas.fig.subplots_adjust(
				left = left,
				bottom = bottom,
				top = top,
				right = right
			)

			# atualizando os textos
			dashboard.canvas.updateLegend()
			dashboard.canvas.setTitle()
			dashboard.canvas.setLabel('x')
			dashboard.canvas.setLabel('y')
			dashboard.canvas.setTickParams('y')
			dashboard.canvas.setTickParams('x')
			dashboard.canvas.draw_idle()

		# update global settings
		settings.SETTINGS['figura']['left'] = left
		settings.SETTINGS['figura']['right'] = right
		settings.SETTINGS['figura']['bottom'] = bottom
		settings.SETTINGS['figura']['top'] = top
		settings.SETTINGS['figura']['font_size'] = fontsize
		settings.SETTINGS['figura']['font_family'] = fontfamily

	def show(self) -> None:
		self.adjustPosition()
		self.loadContents()
		return super().show()

	def updatePage(self, index, button : QPushButton):
		self.ui.stacked_widget.setCurrentIndex(index)
		for push_button in self.findChildren(QPushButton):
			if push_button.objectName() in ['connection', 'figure', 'criteria']:
				push_button.setDisabled(False)

		button.setDisabled(True)

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

	def adjustPosition(self) -> None:
		if self.parent() is None:
			return None

		w, h = self.width(), self.height()
		target = self.parent()
		rect = QRect(target.geometry())

		topleft = QPoint()
		topleft.setX((rect.width() - w) / 2 + rect.x())
		topleft.setY((rect.height() - h) / 2 + rect.y())

		rect = QRect(topleft, QSize(w, h))
		self.setGeometry(rect)

	def mousePressEvent(self, event):          
		self.dragPos = event.globalPos()
		self.move_event = True
		
	def mouseMoveEvent(self, event):                          
		if event.buttons() == Qt.LeftButton:
			self.move(self.pos() + event.globalPos() - self.dragPos)
			self.dragPos = event.globalPos()
			event.accept()