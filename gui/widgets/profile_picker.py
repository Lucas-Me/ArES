# IMPORTS
import gc
from random import randint

# IMPORT CUSTOM UI
from gui.ui_widgets.ui_profile_picker import UI_ProfilePicker

# IMPORT QT CORE
from qt_core import *

class ProfilePicker(QWidget):
	'''
	Classe responsável pelo widget de gerenciamento de perfis.
	'''

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		# PROPERTIES
		self.list = ListView()

		# SETUP UI
		self.ui = UI_ProfilePicker()
		self.ui.setup_ui(self)

		# SIGNALS AND SLOST
		self.ui.add_button.clicked.connect(self.list.addItem)
		self.ui.remove_button.clicked.connect(self.list.removeItem)


class ProfileModel(QAbstractListModel):
	def __init__(self):
		super().__init__()

		self.profiles = []
		self.colors = []
	
	def rowCount(self, parent = QModelIndex()) -> int:
		return len(self.profiles)

	def data(self, index =  QModelIndex(), role: int = ...):
		if role == Qt.DisplayRole:
			return self.profiles[index.row()]

		elif role == Qt.DecorationRole:
			return self.colors[index.row()]

	def insertRow(self, parent = QModelIndex(), **kwargs) -> bool:
		# count items
		row = self.rowCount()

		# begin
		self.beginInsertRows(parent, row, row)
		self.profiles.insert(row, kwargs.pop('name', f'Perfil {row + 1}'))
		self.colors.insert(row, kwargs.pop('color', QColor(randint(0,255), randint(0,255), randint(0,255))))
		
		# end
		self.endInsertRows()
		return True

	def removeRows(self, parent : list[QModelIndex], **kwargs) -> bool:
		for index in parent:
			row = index.row()
			self.beginRemoveRows(index, row, row)
			del self.profiles[row]
			del self.colors[row]
			self.endRemoveRows()


class ListView(QListView):
	def __init__(self):
		super().__init__()
		self.model = ProfileModel()
		self.setModel(self.model)
		self.setSelectionMode(QListView.SelectionMode.ContiguousSelection)
		self.show()
		
		# STYLE
		self.setStyleSheet(f"font: 500 13pt 'Microsoft New Tai Lue'; color: #1c1c1c;background-color: transparent; border: none;")

		# signals and slots
		self.doubleClicked.connect(self.on_row_changed)

	def on_row_changed(self, current):
		print('Row %d selected' % current.row())

	def addItem(self):
		self.model.insertRow()

	def removeItem(self):
		selected = self.selectedIndexes()
		self.model.removeRows(selected)
		self.clearSelection()