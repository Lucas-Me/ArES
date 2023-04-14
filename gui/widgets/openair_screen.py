# IMPORT MODULES
import os

# IMPORT QT CORE
from qt_core import *

# IMPORT CUSTOM UI
from gui.pages.ui_openairscreen import UI_OpenAirScreen

# IMPORT CUSTOM VARIABLES
import backend.misc.settings as settings

# Data Manager Page Class
class OpenAirScreen(QWidget):

	def __init__(self, parent : QStackedWidget):
		super().__init__(parent = parent)

		# PRIVATE VARIABLES
		self.save_dir = os.path.expanduser("~")
		self.data_dir = os.path.join(self.save_dir, '.ArES', 'temp')
		self.resources_list = ListaSuspensa()

		# SETUP UI
		self.ui = UI_OpenAirScreen()
		self.ui.setup_ui(self)

		# SETTINGS
		self.resources_list.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
		self.resources_list.setFixedWidth(250)

	def paintEvent(self, event: QPaintEvent) -> None:
		'''
		Reinicia o painter deste QWidget, para que ele nao herde as propriedades do
		parent.
		'''
		# super().paintEvent(event)

		opt = QStyleOption()
		opt.initFrom(self)
		p = QPainter(self)
		self.style().drawPrimitive(QStyle.PE_Widget, opt, p, self)


class ListaSuspensaModel(QAbstractListModel):

	def __init__(self):
		super().__init__()
		
		self.active_row = 0
		self.data_objects = ["Rosa dos ventos"]

	def rowCount(self, parent = QModelIndex()) -> int:
		return len(self.data_objects)

	def data(self, index =  QModelIndex(), role: int = ...):
		row = index.row()
		if role == Qt.DisplayRole:
			return self.data_objects[row]
		
		elif role == Qt.BackgroundRole and row == self.active_row:
			return QBrush(QColor('#d9e2f1'))



class ListaSuspensa(QListView):

	rowClicked = Signal(int)
	def __init__(self):
		super().__init__()

		# PROPERTIES
		self.model = ListaSuspensaModel()
		self.left_margin = 25

		# SETTINGS
		self.setModel(self.model)
		self.setItemDelegate(CustomItemDelegate(self))
		self.setSelectionMode(QListView.SelectionMode.NoSelection)
		self.setMinimumHeight(0)
		
		# STYLE
		self.setStyleSheet(f'''
			QListView {{
				font: bold 12pt 'Microsoft New Tai Lue';
				color: #36475f;
				background-color: white;
				border: none;
				border-radius: 5px;			
			}}
			QListView::item{{
				background-color: transparent;
				padding-left: {self.left_margin}px;
			}}
			QListView::item:hover{{
				background-color: #edf0f5;
			}}
		''')

		# signals and slots
		self.clicked.connect(self.toggleFunction)

	def toggleFunction(self, parent: QModelIndex):
		row = parent.row()

		# update active row
		self.model.active_row = row

		# emit signal
		self.rowClicked.emit(row)

class CustomItemDelegate(QStyledItemDelegate):

	def __init__(self, parent):
		super().__init__(parent=parent)


	def sizeHint(self, option: QStyleOptionViewItem, index: QModelIndex) -> QSize:
		return QSize(self.parent().width(), 30)