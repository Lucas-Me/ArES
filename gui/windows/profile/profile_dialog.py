# IMPORT QT CORE
from qt_core import *

# IMPORT UI
from gui.windows.profile.ui_profile_dialog import UI_ProfileDialog

class ProfileDialog(QDialog):

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		# PROPERTIES
		self.margins = 10

		# SETTINGS
		self.setModal(True)
		self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)
		# self.setAttribute(Qt.WA_TranslucentBackground, True)
		self.setAttribute(Qt.WA_DeleteOnClose, True)
		self.setFixedSize(400 + self.margins, 200 + self.margins)

		# SETUP UI
		self.ui = UI_ProfileDialog()
		self.ui.setup_ui(self)
