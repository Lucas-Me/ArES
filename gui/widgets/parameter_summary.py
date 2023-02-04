# IMPORTS
import gc

# IMPORT QT CORE
from qt_core import *

# IMPORT UI MODULES
from gui.ui_widgets.ui_parametersummary import UI_ParameterSummary

class ParameterSummary(QTableWidget):

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		# SETTINGS
		self.setHorizontalHeader(CustomHeader(Qt.Orientation.Horizontal))
		self.setup()

		# setup UI
		self.ui = UI_ParameterSummary()
		self.ui.setup_ui(self)
		self.ui.setup_stylesheet(self)

		# teste
		content = ['Partículas Totais em Suspensão', 'DC - São Bento', 'Refinaria Duque de Caxias', 'Nenhum']
		self.addRow(content)

	def setup(self):
		# disabling grid
		self.setShowGrid(False)

		# disabling vertical header
		self.verticalHeader().hide()

		# settings up columns
		columns = ['Parâmetro', "Estação", 'Empresa', 'Perfil']
		n = len(columns)
		self.setColumnCount(n)
		for i in range(n):
			self.setHorizontalHeaderItem(i, QTableWidgetItem(columns[i]))
		
		self.setColumnWidth(3, 80)

		# setup font
		self.font = QFont()
		self.font.setFamily("Microsoft New Tai Lue")
		self.font.setPointSize(12)
		self.font.setBold(True)
		
		# deleaget
		self.setItemDelegate(StyledItemDelegate(ncols = 4))

	def addRow(self, content : list[str]):
		row = self.rowCount()
		cols = self.columnCount()
		self.insertRow(row)

		for i in range(cols):
			widget_item = self.createItem(content[i], '#fff6e5')
			self.setItem(row, i, widget_item)

	def createItem(self, text, color):
		widget_item = QTableWidgetItem()
		#
		widget_item.setText(text)
		widget_item.setBackground(QBrush(QColor(color)))
		widget_item.setFont(self.font)
		widget_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

		return widget_item


class CustomHeader(QHeaderView):

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		
		# SETTINGS
		# self.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
		self.resizeSections()
		self.setSectionsMovable(True)
		self.setup_style()

	
	def setup_style(self):
		# CONSTANTS
		font = 'Franklin Gothic Demi'
		font_color = '#757d8e'

		self.setStyleSheet(f'''
			QHeaderView::section {{
				background-color: transparent;
				font: 500 14pt '{font}';
				color: {font_color};
				padding-left: 4px;
				border-top: 4px solid #adb3bf;
				border-bottom: 2px solid #adb3bf;
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

	def paint(self, painter: QPainter, option: 'QStyleOptionViewItem', index: QModelIndex) -> None:
		super().paint(painter, option, index)
		
		# setting up informations about cell
		col = index.column()
		
		# painter and pen
		painter.save()
		pen = QPen(QColor("#adb3bf"))
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