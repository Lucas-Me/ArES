# IMPORTS
import gc

# IMPORT QT CORE
from qt_core import *

class ProfilePicker(QWidget):
	'''
	Classe responsável pelo widget de gerenciamento de perfis.
	'''

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)