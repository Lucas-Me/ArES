# IMPORTS
import gc

# IMPORT QT CORE
from qt_core import *

# IMPORT UI MODULES
from gui.ui_widgets.ui_parametersummary import UI_ParameterSummary

class ParameterSummary(QTableWidget):

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		# PROPERTIES
		self.scroll_width = self.verticalScrollBar().height()

		# SETTINGS
		self.setHorizontalHeader(CustomHeader(Qt.Orientation.Horizontal))
		self.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)
		self.setSortingEnabled(True)
		self.setup()

		# setup UI
		self.ui = UI_ParameterSummary()
		self.ui.setup_ui(self)
		self.ui.setup_stylesheet(self)

	def setup(self):
		# disabling grid
		self.setShowGrid(False)

		# disabling vertical header
		verticalHeader = self.verticalHeader()
		verticalHeader.hide()
		verticalHeader.setSectionResizeMode(QHeaderView.Fixed)
		verticalHeader.setDefaultSectionSize(30)

		# settings up columns
		columns = ['Parâmetro', "Estação", 'Empresa', 'Perfil']
		n = len(columns)
		self.setColumnCount(n)
		for i in range(n):
			self.setHorizontalHeaderItem(i, QTableWidgetItem(columns[i]))
		
		self.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)
		# setup font
		self.font = QFont()
		self.font.setFamily("Microsoft New Tai Lue")
		self.font.setPointSize(12)
		
		# deleaget
		self.setItemDelegate(StyledItemDelegate(ncols = self.columnCount()))

	def addRow(self, content : list[str]):
		row = self.rowCount()
		cols = self.columnCount()
		self.insertRow(row)

		for i in range(cols):
			widget_item = self.createItem(content[i], '#ffffff')
			self.setItem(row, i, widget_item)

	def createItem(self, text, color):
		widget_item = QTableWidgetItem()
		#
		widget_item.setText(text)
		widget_item.setBackground(QBrush(QColor(color)))
		widget_item.setFont(self.font)
		widget_item.setTextAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
		
		return widget_item

	def resizeEvent(self, event: QResizeEvent) -> None:
		header = self.horizontalHeader()
		ncols = self.columnCount()
		w = self.width()

		# SETTING EACH COLUMNS WIDTH
		for col in range(ncols):
			width = w * header.getProportions(col) / 100
			self.setColumnWidth(col, width)

		return super().resizeEvent(event)


class CustomHeader(QHeaderView):

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		
		# PROPERTIES
		self.column_proportions = [30, 20, 34, 12] # in percentage

		# SETTINGS
		self.setDefaultAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
		self.setup_style()

	def getProportions(self, col):
		return self.column_proportions[col]

	def setup_style(self):
		# CONSTANTS
		font = 'Microsoft New Tai Lue'
		font_color = '#32495e'

		self.setStyleSheet(f'''
			QHeaderView::section {{
				background-color: transparent;
				border: none;
				font: 500 14pt '{font}';
				color: {font_color};
				padding-left: 4px;
				text-align: left;
				border-bottom: 1px solid #dcdcdc;
				border-top: 1px solid #dcdcdc;
			}}
			QHeaderView::section:checked
			{{
				background-color: red;
			}}
		''')


class StyledItemDelegate(QStyledItemDelegate):

	def __init__(self, ncols, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.max_column = ncols - 1

	def sizeHint(self, option: QStyleOptionViewItem, index):
		return super().sizeHint(option, index)

	def paint(self, painter: QPainter, option: QStyleOptionViewItem, index: QModelIndex) -> None:
		super().paint(painter, option, index)
		
		# setting up informations about cell
		col = index.column()

		# painter and pen
		painter.save()
		pen = QPen(QColor("#dcdcdc"))
		pen.setWidth(pen.width() / 2)
		painter.setPen(pen)
		
		# underline 
		qr = QRect(option.rect)
		qr.setTop(qr.bottom() - pen.width())
		qr.setHeight(pen.width())
		painter.drawRect(qr)

		# if first column
		if col == 0:
			qr = QRect(option.rect)
			qr.setWidth(pen.width())
			painter.drawRect(qr)
		
		# elif last column
		elif col == self.max_column:
			qr = QRect(option.rect)
			qr.setLeft(qr.right() - pen.width())
			qr.setWidth(pen.width())
			painter.drawRect(qr)

		painter.restore()