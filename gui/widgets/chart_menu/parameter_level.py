# IMPORT QT MODULES
from qt_core import *

# IMPOORT CUSTOM WIDGETS
from gui.widgets.chart_menu.buttons import TopLevelButton

# IMPORT CUSTOM FUNCTIONS
from backend.misc.functions import get_imagepath

class SeriesTopLevel(QWidget):

	propertyChanged = Signal(dict)
	def __init__(self, text, height):
		super().__init__()

		# PROPERTIES
		self.item_height = height
		self.text = text

		# SETUP UI
		self.setupUI()
		self.toggle()

		# SETTINGS
		self.setMinimumHeight(self.item_height)

		# SIGNALS
		self.top_level.clicked.connect(self.toggle)

	def toggle(self):
		hidden = self.top_level.getStatus()
		active = not hidden
	
		# toggle on (active) or off
		self.top_level.setActive(active)

		# SHOW/HIDDEN widgets
		self.list_view.setHidden(hidden)

	def setupUI(self):
		if not self.objectName():
			self.setObjectName("series_top_level")

		self.main_layout = QVBoxLayout(self)
		self.main_layout.setContentsMargins(0, 0, 0, 0)
		self.main_layout.setSpacing(0)

		# OBJECTS
		self.top_level = TopLevelButton(text = self.text, height = self.item_height)
		
		# DATE PROPERTIES
		self.list_view = SeriesListView()

		# add to layout
		self.main_layout.addWidget(self.top_level)
		self.main_layout.addWidget(self.list_view)


class SeriesModel(QAbstractListModel):

	def __init__(self):
		super().__init__()

		self.data_objects = [] # contains the name of each objects
		self.selected = [] # contains a bool
		self.checked = QPixmap(get_imagepath('listview_checked.svg', 'gui/images/icons'))
		self.unchecked = QPixmap(get_imagepath('listview_unchecked.svg', 'gui/images/icons'))
	
	def rowCount(self, parent = QModelIndex()) -> int:
		return len(self.data_objects)

	def data(self, index =  QModelIndex(), role: int = ...):
		if role == Qt.DisplayRole:
			return self.data_objects[index.row()]

		elif role == Qt.DecorationRole:
			if self.selected[index.row()]:
				return self.checked
			else:
				return self.unchecked

	def insertRow(self, parent = QModelIndex(), **kwargs) -> bool:
		# count items
		row = self.rowCount()

		# begin
		self.beginInsertRows(parent, row, row)

		# adding to private variable
		self.data_objects.insert(row, kwargs.get('name'))
		self.selected.insert(row, False)
		
		# end
		self.endInsertRows()
		return True

	def removeRows(self, parent : list[QModelIndex], **kwargs) -> bool:
		n = len(parent)
		for i in range(n):
			row = parent[i].row()
			self.beginRemoveRows(parent[i], row, row)
			del self.data_objects[row]
			del self.selected[row]
			self.endRemoveRows()


class SeriesListView(QListView):

	def __init__(self):
		super().__init__()

		# PROPERTIES
		self.model = SeriesModel()
		self.left_margin = 25

		# SETTINGS
		self.setModel(self.model)
		self.setSelectionMode(QListView.SelectionMode.NoSelection)
		self.show()
		self.setMinimumHeight(0)
		
		# STYLE
		self.setStyleSheet(f'''
			QListView {{
				font: normal 10pt 'Microsoft New Tai Lue';
				color: #1c1c1c;
				background-color: transparent;
				border: none;			
			}}
			QListView::item{{
				 padding-left: {self.left_margin}px;
			}}
		''')

		# signals and slots
		self.clicked.connect(self.toggleSeries)

	def toggleSeries(self, parent: QModelIndex):
		row = parent.row()
		current_status = self.getStatus(row)
		self.updateStatus(parent.row(), not current_status)
		self.update(parent)

	def addItem(self, name):
		self.model.insertRow(name = name)
		
	def removeItems(self):
		self.model.removeRows(self.model.persistentIndexList())

	def getIndex(self, *args, **kwargs):
		target = self.model.data_object
		name = kwargs.pop('name', None)

		if name in target:
			return target.index(name)
		else:
			return -1

	def getStatus(self, index):
		n = self.model.rowCount()
		if index == n:
			return None
		else:
			return self.model.selected[index]

	def updateStatus(self, index, status : bool):
		if index >= self.model.rowCount():
			return None
		else:
			self.model.selected[index] = status

	def paintEvent(self, event: QPaintEvent) -> None:
		super().paintEvent(event)

		painter = QPainter()
		painter.begin(self.viewport())
		
		dx = 2
		x = (self.left_margin - dx) // 2
		y = 0
		dy = self.height()
		painter.fillRect(x, y, dx, dy, QColor('#36475f'))

		painter.end()
		