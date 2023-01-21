# IMPORT QT CORE
from qt_core import *

# IMPORT CUSTOM UI
from gui.pages.ui_loginscreen import UI_LoginScreen

# IMPORT CUSTOM MODULES
from backend.data_management.sql_backend import SqlConnection

# IMPORT CUSTOM FUCTIONS
from backend.misc.functions import get_imagepath

# Data Manager Page Class
class LoginScreen(QWidget):

	def __init__(self, parent : QStackedWidget):
		super().__init__(parent = parent)

		# LOGO
		self.logo = Logo(100, 100, image = 'ArES_logo.svg')
		self.profile_image = Logo(100, 100, image = 'profile.svg')

		# SETUP CONNECTION
		self.sql = SqlConnection("PC-INV109399", 'banco_gear')

		# SETUP UI
		self.ui = UI_LoginScreen()
		self.ui.setup_ui(self)
		self.ui.setup_stylesheet()

		# CONFIGURATIONS
		self.updateHost()
		self.testConnection()

		# SIGNALS AND SLOTS
		self.ui.login_btn.pressed.connect(self.connectSQL)
		self.ui.disconnect_btn.pressed.connect(self.disconnectSQL)

	def borderCredentials(self, borders : bool):
		style = '1px solid red' if borders else 'none'
		lines = [self.ui.username, self.ui.password]
		for line in lines:
			line.setStyleSheet(line.styleSheet() + f'border: {style};')

	def connectSQL(self):
		user = self.ui.username.text()
		pswrd = self.ui.password.text()
		code = self.sql.connect(user, pswrd)
		self.borderCredentials(borders = False)
		
		if code == 1:
			# concetion suceeded
			# change the page on the frame
			self.changePage(self.sql.cnx.is_connected())
			pass

		elif code == 1045:
			# WRONG USERNAME OR PASSWORD
			self.borderCredentials(borders = True)
			pass
		
		else:
			print("Nunca vi esse erro na minha vida ")
			print(f'Erro {code}')

		# reset the password field
		self.ui.password.setText('')

	def changePage(self, index):
		self.ui.right_frame.setCurrentIndex(index)
		self.ui.greetings_label.setText(f"Olá, {self.ui.username.text()}")
		self.ui.logged_label.setText(
			f'Você está conectado ao\n{self.sql.cnx._database}'
		)

	def disconnectSQL(self):
		self.sql.cnx.disconnect()
		self.ui.right_frame.setCurrentIndex(0)

	def testConnection(self):
		# CODE 2003 MEANS THE SERVER IS UNAVAILABLE
		available = self.sql.connect('', '') != 2003

		self.borderCredentials(borders = False)
		self.ui.login_btn.setEnabled(available)
		self.updateStatus(available)

	def updateHost(self):
		text = self.sql.cnx._host
		self.ui.host_label.setText(f'Servidor: {text}')

	def updateStatus(self, available):
		status = 'Online' if available else 'Offline'
		self.ui.status_label.setText(
			f'Status: {status}'
		)

	def paintEvent(self, event: QPaintEvent) -> None:
		# super().paintEvent(event)

		opt = QStyleOption()
		opt.initFrom(self)
		p = QPainter(self)
		self.style().drawPrimitive(QStyle.PE_Widget, opt, p, self)

	def resizeEvent(self, event: QResizeEvent) -> None:
		super().resizeEvent(event)
		bkgnd = QImage(get_imagepath('login_splash.jpg', 'gui/images/backgrounds'))
		bkgnd = bkgnd.scaled(self.size())
		palette = self.palette()
		palette.setBrush(QPalette.Window, bkgnd)
		self.setAutoFillBackground(True)
		self.setPalette(palette)


class Logo(QWidget):

	def __init__(self, width, height, image):
		super().__init__()

		self.image_name = image

		# properties
		self.setFixedHeight(height)
		self.setFixedWidth(width)

	def paintEvent(self, event: QPaintEvent) -> None:
		super().paintEvent(event)

		# Painter
		qp = QPainter()
		qp.begin(self)
		qp.setRenderHint(QPainter.Antialiasing)
		qp.setPen(Qt.NoPen)

		rect = QRect(0, 0, self.width(), self.height())

		# format Path
		icon_path =  get_imagepath(self.image_name, 'gui/images/icons')

		# Draw icon
		icon = QPixmap(icon_path)
		qp.drawPixmap(self.rect(), icon)

		qp.end()

		