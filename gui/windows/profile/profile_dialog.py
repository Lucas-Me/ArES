# IMPORT QT CORE
from qt_core import *

# IMPORT UI
from gui.windows.profile.ui_profile_dialog import UI_ProfileDialog

# IMPORT CUSTOM FUNCTIONS
from backend.misc.functions import drawShadow

# IMPORT CUSTOM MODULES
from backend.data_management.methods import Profile


class ProfileDialog(QDialog):

	profileSaved = Signal(Profile)

	def __init__(self, *args, **kwargs):
		super().__init__(parent = kwargs.pop('parent', None))

		# PROPERTIES
		self.margins = 20
		self.profile = kwargs.pop('profile', Profile())

		# SETTINGS
		self.setModal(True)
		self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint | Qt.NoDropShadowWindowHint)
		self.setAttribute(Qt.WA_TranslucentBackground, True)
		self.setAttribute(Qt.WA_DeleteOnClose, True)
		self.setFixedSize(500 + self.margins, 250 + self.margins)

		# SETUP UI
		self.ui = UI_ProfileDialog()
		self.ui.setup_ui(self)

		# SIGNALS AND SLOTS
		self.ui.table.rowCountUpdated.connect(self.saveStatus)
		self.ui.name.editingFinished.connect(self.saveStatus)
		self.ui.color_selector.color_changed.connect(self.updateColor)
		self.ui.save_button.clicked.connect(self.saveContents)
		self.ui.save_button.clicked.connect(self.close)
		self.ui.cancel_button.clicked.connect(self.close)

		# LOAD CONTENTS
		self.loadContents()
	
	def showWindow(self):
		self.adjustPosition()
		self.show()

	def saveContents(self):
		self.profile.setName(self.ui.name.text())
		self.profile.setMethods(self.ui.table.getMethods())
		self.profile.setColor(self.color)

		# emite o perfil salvo
		self.profileSaved.emit(self.profile) 

	@Slot(QColor)
	def updateColor(self, color : QColor):
		self.color = color
		style = self.ui.color_view.styleSheet()
		index = style.index(';')
		new_style = f'background-color: {self.color.name()}' + style[index:]
		self.ui.color_view.setStyleSheet(new_style)

	def loadContents(self):
		self.ui.name.setText(self.profile.getName())
		# self.nameCheck()
		#
		self.ui.table.setMethods(self.profile.getMethods())
		#
		self.ui.color_selector.set_color(self.profile.getColor())
		self.updateColor(self.profile.getColor())
		self.saveStatus()
		
	def methodCount(self):
		disable = self.ui.table.rowCount() <= 1
		return disable

	def nameCheck(self):
		disable = len(self.ui.name.text()) == 0
		return disable

	@Slot()
	def saveStatus(self):
		condition1 = self.methodCount()
		condition2 = self.nameCheck()
		self.ui.save_button.setDisabled(condition1 or condition2)

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
		self.adjustPosition()

	def adjustPosition(self) -> None:
		if self.parent() is None:
			return None

		w, h = self.width(), self.height()
		target = self.parent()
		rect = QRect(target.geometry())

		topleft = QPoint()
		topleft.setX((rect.width() - w) / 2)
		topleft.setY((rect.height() - h) / 2)

		self.setGeometry(QRect(topleft, QSize(w, h)))
