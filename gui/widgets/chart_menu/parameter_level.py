# IMPORT QT MODULES
from qt_core import *

# IMPOORT CUSTOM WIDGETS
from gui.widgets.chart_menu.buttons import TopLevelButton

# IMPORT CUSTOM FUNCTIONS
from backend.misc.functions import get_imagepath

class SeriesTopLevel(QWidget):

	propertyChanged = Signal(dict)
	def __init__(self, text, height, hline = False):
		super().__init__()

		# PROPERTIES
		self.item_height = height
		self.text = text
		self.hline = hline

		# SETUP UI
		self.setupUI()
		self.toggle()

		# SETTINGS
		self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.MinimumExpanding)

		# SIGNALS
		self.top_level.clicked.connect(self.toggle)

	def toggle(self):
		hidden = self.top_level.getStatus()
		active = not hidden
	
		# toggle on (active) or off
		self.top_level.setActive(active)

		# SHOW/HIDDEN widgets
		self.list_view.setHidden(hidden)
		if self.hline:
			self.hline_frame.setHidden(hidden)

		# size policty
		if active:
			self.setMaximumHeight(self.item_height * 100)
		else:
			self.setMaximumHeight(self.item_height)

	def setupUI(self):
		if not self.objectName():
			self.setObjectName("series_top_level")

		self.main_layout = QVBoxLayout(self)
		self.main_layout.setContentsMargins(0, 0, 0, 0)
		self.main_layout.setSpacing(0)

		# OBJECTS
		self.top_level = TopLevelButton(text = self.text, height = self.item_height)
		self.main_layout.addWidget(self.top_level)

		# HORIZONTAL LINE OPTION
		if self.hline:
			self.hline_frame = HorizontalLineProperty(text = 'Faixa Horizontal', vmin = 0, vmax = 10000, height = self.item_height)
			self.main_layout.addWidget(self.hline_frame)

		# PARAMETERS LIST
		self.list_view = SeriesListView()

		# add to layout
		self.main_layout.addWidget(self.list_view)


class HorizontalLineProperty(QFrame):
	
	valueChanged = Signal(int)
	stateChanged = Signal(bool)
	def __init__(self, text, vmin, vmax, height):
		super().__init__()
		
		# SETTINGS
		# self.setMinimumHeight(0)
		self.setFixedHeight(height)

		# PROPERTIES
		self.label = QLabel(text)
		self.spinbox = QSpinBox()
		self.left_margin = 25

		# SETTING WIDGETS
		self.spinbox.setRange(vmin, vmax)

		# SETUP UI
		self.setupUI()
		self.setupStyle()

		# SIGNALS
		self.spinbox.editingFinished.connect(self.emitValue)
		self.checkbox.stateChanged.connect(self.stateChanged.emit)

	def emitValue(self):
		if self.checkbox.isChecked():
			self.valueChanged.emit(self.spinbox.value())

	def setupUI(self):
		self.main_layout = QHBoxLayout(self)
		self.main_layout.setContentsMargins(self.left_margin + 4, 3, 3, 3)
		self.main_layout.setSpacing(5)
		self.setObjectName('item')

		# Checkbox
		self.checkbox = QCheckBox()
		self.checkbox.setObjectName('checkbox')

		# TEXT
		self.label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
		self.label.setObjectName('line')

		# FONTSIZE
		self.spinbox.setObjectName('combobox')

		# ADD TO MAIN LAYOUT
		self.main_layout.addWidget(self.checkbox)
		self.main_layout.addWidget(self.spinbox)
		self.main_layout.addWidget(self.label)

	def setupStyle(self):
		self.setStyleSheet('''
			#item{
				background-color: transparent;
			}
			#spinbox, #line, #checkbox{
				font: normal 10pt 'Microsoft New Tai Lue';
				color: #36475f;
			}
		''')

	def paintEvent(self, event: QPaintEvent) -> None:
		super().paintEvent(event)

		painter = QPainter()
		painter.begin(self)
		
		dx = 2
		x = (self.left_margin - dx) // 2
		y = 0
		dy = self.height()
		painter.fillRect(x, y, dx, dy, QColor('#36475f'))

		painter.end()
		

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
		for i in range(n - 1, -1, -1):
			row = parent[i].row()
			self.beginRemoveRows(parent[i], row, row)
			del self.data_objects[row]
			del self.selected[row]
			self.endRemoveRows()


class SeriesListView(QListView):

	rowClicked = Signal(int, bool)
	def __init__(self):
		super().__init__()

		# PROPERTIES
		self.model = SeriesModel()
		self.left_margin = 25

		# SETTINGS
		self.setModel(self.model)
		self.setItemDelegate(CustomItemDelegate(self))
		self.setSelectionMode(QListView.SelectionMode.NoSelection)
		self.setMinimumHeight(0)
		
		# STYLE
		self.setStyleSheet(f'''
			QListView {{
				font: normal 10pt 'Microsoft New Tai Lue';
				color: #36475f;
				background-color: transparent;
				border: none;			
			}}
			QListView::item{{
				background-color: transparent;
				padding-left: {self.left_margin}px;
			}}
			QListView::item:hover{{
				background-color: #d9e2f1;
			}}
		''')

		# signals and slots
		self.clicked.connect(self.toggleSeries)

	def toggleSeries(self, parent: QModelIndex):
		row = parent.row()
		new_status = not self.getStatus(row)

		# updatin row
		self.setStatus(parent.row(), new_status)

		# emit signal
		self.rowClicked.emit(row, new_status)

	def addItem(self, name):
		self.model.insertRow(name = name)
		
	def removeItems(self):
		n = self.model.rowCount()
		modal_list = [self.model.index(row, 0) for row in range(n)] 
		self.model.removeRows(modal_list)

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

	def setStatus(self, index, status : bool):
		if index >= self.model.rowCount():
			return None
		else:
			self.model.selected[index] = status

		self.update(self.model.index(index, 0))

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
		
class CustomItemDelegate(QStyledItemDelegate):

	def __init__(self, parent):
		super().__init__(parent=parent)


	def sizeHint(self, option: QStyleOptionViewItem, index: QModelIndex) -> QSize:
		return QSize(self.parent().width(), 30)