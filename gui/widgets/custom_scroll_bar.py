# IMPORT QT CORE
from qt_core import *

# CUSTOM SCROLL BAR
class CustomScrollBar(QScrollBar):

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)