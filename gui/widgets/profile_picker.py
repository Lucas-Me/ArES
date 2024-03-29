# IMPORT CUSTOM UI
from gui.ui_widgets.ui_profile_picker import UI_ProfilePicker

# IMPORT CUSTOM WIDGETS
from gui.windows.profile.profile_dialog import ProfileDialog

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

	def nextProfile(self, profile):
		idx = self.list.getIndex(profile = profile)

		return self.list.getProfile(idx + 1)


class ProfileModel(QAbstractListModel):

	def __init__(self):
		super().__init__()

		self.profiles = []
	
	def rowCount(self, parent = QModelIndex()) -> int:
		return len(self.profiles)

	def data(self, index =  QModelIndex(), role: int = ...):
		if role == Qt.DisplayRole:
			return self.profiles[index.row()].name

		elif role == Qt.DecorationRole:
			return self.profiles[index.row()].color
	

	def insertRow(self, parent = QModelIndex(), **kwargs) -> bool:
		# count items
		row = self.rowCount()

		# begin
		self.beginInsertRows(parent, row, row)

		# adding to private variable
		self.profiles.insert(row, kwargs.get('profile'))
		
		# end
		self.endInsertRows()
		return True

	def removeRows(self, parent : list[QModelIndex], **kwargs) -> bool:
		n = len(parent)
		removed = [None]

		for i in range(n):
			row = parent[i].row()
			self.beginRemoveRows(parent[i], row, row)
			removed[i] = self.profiles.pop(row)
			self.endRemoveRows()

		return removed

class ListView(QListView):

	removedProfile = Signal(object)
	profileDoubleClicked = Signal(QDialog)

	def __init__(self):
		super().__init__()
		self.model = ProfileModel()
		self.setModel(self.model)
		self.setSelectionMode(QListView.SelectionMode.ContiguousSelection)
		
		# STYLE
		self.setStyleSheet(f"font: 500 13pt 'Microsoft New Tai Lue'; color: #1c1c1c;background-color: transparent; border: none;")

		# signals and slots
		self.doubleClicked.connect(self.openDialog)

	def openDialog(self, row : QModelIndex):
		if isinstance(row, QModelIndex):
			row = row.row()

		profile = self.getProfile(row)
		dialog = ProfileDialog(profile = profile)
		dialog.profileSaved.connect(lambda x: self.updateProfile(row, x))
		
		# emit signal to show dialog
		self.profileDoubleClicked.emit(dialog)

	def addItem(self):
		dialog = ProfileDialog()
		new_row = self.model.rowCount()
		dialog.profileSaved.connect(lambda x: self.updateProfile(new_row, x))
		
		# emit signal to show dialog
		self.profileDoubleClicked.emit(dialog)

	def removeItem(self):
		selected = self.selectedIndexes()
		removed = self.model.removeRows(selected)
		for prof in removed:
			self.removedProfile.emit(prof)

		self.clearSelection()

	def getIndex(self, *args, **kwargs):
		target = self.model.profiles
		profile = kwargs.pop('profile', None)

		if profile in target:
			return target.index(profile)
		else:
			return -1

	def getProfile(self, index):
		n = self.model.rowCount()
		if index == n:
			return None
		else:
			return self.model.profiles[index]

	def updateProfile(self, index, profile):
		if index >= self.model.rowCount():
			self.model.insertRow(profile = profile)

		else:
			self.model.profiles[index] = profile