# IMPORT QT MODULES
from qt_core import *

# IMPORT UI
from gui.windows.settings.ui_settings import UI_SettingsWindow

# IMPORT CUSTOM FUNCTIONS
from backend.misc.functions import drawShadow

# IMPORT CUSTOM VARIABLES
import backend.misc.settings as settings
from matplotlib import font_manager
import numpy as np

class SettingsWindow(QDialog):
    
	def __init__(self, parent = None):
		super().__init__(parent = parent)

		# PROPERTIES
		self.margins = 20

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

	
	def loadContents(self):
		# BANCO DE DADOS
		self.ui.database_edit.setText(settings.SETTINGS['conexao']['database'])
		self.ui.server_edit.setText(settings.SETTINGS['conexao']['servidor'])

		# CRITERIOS DE VALIDACAO
		self.ui.spinbox_hourly.setValue(settings.SETTINGS['representatividade']['Horária'])
		self.ui.spinbox_daily.setValue(settings.SETTINGS['representatividade']['Data'])
		self.ui.spinbox_monthly.setValue(settings.SETTINGS['representatividade']['Mês e ano'])
		self.ui.spinbox_yearly.setValue(settings.SETTINGS['representatividade']['Ano'])
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

	def show(self) -> None:
		self.adjustPosition()
		self.loadContents()
		return super().show()

	def updatePage(self, index, button : QPushButton):
		self.ui.stacked_widget.setCurrentIndex(index)
		for button in self.findChildren(QPushButton):
			if button.objectName() in ['connection', 'figure', 'criteria']:
				button.setDisabled(False)

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
