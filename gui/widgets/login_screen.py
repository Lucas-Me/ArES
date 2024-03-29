# IMPORT QT CORE
from qt_core import *

# IMPORT CUSTOM UI
from gui.pages.ui_loginscreen import UI_LoginScreen

# IMPORT CUSTOM MODULES
from backend.data_management.sql_backend import SqlConnection
from gui.windows.dialog.import_dialog import ImportDialog
from gui.windows.dialog.loading_dialog import LoadingDialog

# IMPORT CUSTOM FUCTIONS
from backend.misc.functions import get_imagepath
import backend.misc.settings as settings


# Data Manager Page Class
class LoginScreen(QWidget):

	def __init__(self, parent : QStackedWidget):
		super().__init__(parent = parent)

		# LOGO
		self.logo = Logo(100, 100, image = 'ArES_logo.svg')
		self.profile_image = Logo(120, 120, image = 'profile.svg')

		# SETTINGS
		self.last_refresh = 'Nunca'

		# SETUP CONNECTION
		self.sql = SqlConnection(
			settings.SETTINGS['conexao']['servidor'],
			settings.SETTINGS['conexao']['database']
			) # CONFIGURACOES 

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
		self.ui.refresh_btn.pressed.connect(self.refreshDatabase)

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
		
		# reset the password field
		self.ui.password.setText('')

	def changePage(self, index):
		self.ui.right_frame.setCurrentIndex(index)
		self.ui.greetings_label.setText(f"Olá, {self.ui.username.text()}")
		self.ui.logged_label.setText(
			f'Você está conectado ao {self.sql.cnx._database}'
		)
		self.ui.verification_label.setText(
			f'Última verificação: {self.last_refresh}'
		)

	def refreshDatabase(self):
		'''
		Efetua uma verificação no banco de dados, visando atualizar as informacoes
		sobre as estacoes existentes e suas propriedades (parametros, empresa, etc..)
		'''
		loading_dialog = LoadingDialog(text='Atualizando as informações locais...', parent = self)
		loading_dialog.finished.connect(self.updateRefreshText)
		self.sql.atualizar_inventario(loading_dialog) # update database invenctory
		loading_dialog.show()
	
	@Slot(bool)
	def updateRefreshText(self, success):
		if success:
			self.last_refresh = QDateTime.currentDateTime().toString( 'dd MMM yyyy hh:mm')
			self.ui.verification_label.setText(
				f'Última verificação: {self.last_refresh}'
			)
		else:
			self.disconnectSQL()
			dialog = ImportDialog(
				title = 'Erro',
				message = 'Não foi possível se comunicar com o banco de dados',
				description='Certifique-se de que a conexão esteja estabelecida',
				parent = self
        	)
			dialog.show()

	def disconnectSQL(self):
		self.sql.disconnect()
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

		# format Path
		icon_path = get_imagepath(self.image_name, 'gui/images/icons')
		icon = QPixmap(icon_path)
		dx, dy = self.width(), self.height()

		# scale icon ot dimensions
		icon = icon.scaled(dx, dy, Qt.AspectRatioMode.IgnoreAspectRatio, Qt.TransformationMode.SmoothTransformation)

		qp.drawPixmap(icon.rect(), icon)

		qp.end()

		