# IMPORT QT MODULES
from qt_core import *

# IMPORT BUILT-IN METHODS
from random import randint

class Profile(object):

	def __init__(self, *args, **kwargs):
		
		# PROPERTIES
		self.color = kwargs.pop('color', QColor(randint(0, 255), randint(0, 255), randint(0, 255)))
		self.name = kwargs.pop('name', '')
		self.methods = kwargs.pop('methods', [])

		# VERIFICATIONS
		if not isinstance(self.color, QColor):
			self.color = QColor(self.color)

	def setColor(self, color : QColor):
		self.color = color

	def getColor(self):
		return self.color

	def setName(self, text):
		self.name = text

	def getName(self):
		return self.name

	def setMethods(self, methods : list[tuple[str, str]]):
		self.methods = methods

	def getMethods(self):
		return self.methods