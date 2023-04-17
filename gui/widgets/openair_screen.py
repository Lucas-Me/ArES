# IMPORT MODULES
import os, subprocess

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
		self.data_dir = os.path.join(os.path.expanduser('~'), '.ArES', 'temp')
		self.resources_list = ListaSuspensa()

		# SETUP UI
		self.ui = UI_OpenAirScreen()
		self.ui.setup_ui(self)

		# SETTINGS
		self.resources_list.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
		self.resources_list.setFixedWidth(200)
		self.searchExecutableDirectory()
		self.updateResolution()

		# SIGNALS AND SLOTS
		self.ui.r_directory.clicked.connect(lambda: self.directorySelection(field = self.ui.r_directory))
		self.ui.save_directory.clicked.connect(lambda: self.directorySelection(field = self.ui.save_directory))
		self.ui.dpi.valueChanged.connect(self.updateResolution)
		self.ui.proportion.valueChanged.connect(self.updateResolution)
		self.ui.process_button.clicked.connect(self.performTask)

	def performTask(self):
		command = os.path.join(self.ui.r_directory.text(), 'Rscript')
		path2script = './/backend//openair//teste_plot.r'
		args = ["--fname", "teste.png","--inputdir", "C:\\Users\\lucassm\\.ArES\\temp"]

		retcode = subprocess.call([command, path2script] + args, shell=True)
		print(retcode)

	def directorySelection(self, field : QLabel):
		current_dir = field.text()
		if not os.path.isdir(current_dir):
			current_dir = os.path.expanduser('~')

		# open window requesting the user to find the directory
		selected_dir = QFileDialog.getExistingDirectory(
			self,
			"Selecione um diretório...",
			dir = current_dir
		)

		# if 'selected' is not a empty string
		if len(selected_dir) > 0:
			field.setText(selected_dir)

	def searchExecutableDirectory(self):
		# R path
		r_path = r"R\R-4.2.3\bin\x64"

		# search in windows folder and user folder
		folders = ["C:\\Program Files", os.path.join(os.path.expanduser('~'), 'AppData\\Local\\Programs')]

		for folder in folders:
			installation_folder = os.path.join(folder, r_path)
			folder_exists = os.path.isdir(installation_folder)
			if folder_exists:
				self.ui.r_directory.setText(installation_folder)
				return None

		# R installation folder has not been encountered, requesting user to insert the right one
		self.ui.r_directory.setText('<Selecione a pasta do executável R>')	

	def updateResolution(self):
		dpi = self.ui.dpi.value()
		x = self.ui.proportion.getWidth()
		y = self.ui.proportion.getHeight()

		height = y * dpi
		width = x * dpi

		# update text
		self.ui.final_resolution.setText(f'''
			<style>
				p {{text-align: center;}}
			</style>
			<body>
				<p>Largura: {width}px<br>Altura: {height}px</p>
			</body>
		'''
		)

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
		self.data_objects = ["Rosa dos ventos", "Rose de poluição", "Resumo"]

	def rowCount(self, parent = QModelIndex()) -> int:
		return len(self.data_objects)

	def data(self, index =  QModelIndex(), role: int = ...):
		row = index.row()
		if role == Qt.DisplayRole:
			return self.data_objects[row]
		
		elif role == Qt.DecorationRole and row == self.active_row:
			return QColor('green')
		

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
				font: bold 10pt 'Microsoft New Tai Lue';
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