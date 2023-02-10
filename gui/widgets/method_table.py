# IMPORT QT MODULES
from qt_core import *


# STYLESHEETS
text_color = '#1c1c1c'
font_family = 'Microsoft New Tai Lue'
hover_color = '#e4e4e4'
pressed_color ='#c1c1c1'
radius = 2

header_style= f'''
	QHeaderView::section:checked{{
		background-color: transparent;
	}}
	QHeaderView {{
		background-color: transparent;
		font: 500 12pt {font_family};
		color: {text_color};
	}}
'''

button_style = f'''
	QPushButton{{
		background-color: #fafafa;
		font: 500 12pt {font_family};
		color: {text_color};
		border-radius: {radius}px;
		border: 1px solid #c7c7c7;
	}}
	QPushButton:hover{{
		background-color: {hover_color};
	}}
	QPushButton:pressed{{
		background-color: {pressed_color};
	}}
'''

combobox_style = f'''
	QComboBox {{
		background-color: #fafafa;
		border: 1px solid #c7c7c7;
		border-radius: {radius}px;
		font: 500 10pt {font_family};
		color: {text_color};
	}}
	QComboBox::item:hover {{
		border: 1px solid #fafafa;
		background-color: #009aff;
		color: #fafafa;
	}}
	QComboBox::drop-down {{
		subcontrol-origin: padding;
		subcontrol-position: top right;
		width: 15px;
		border: none;
	}}
'''
# CLASS

class MethodTable(QTableWidget):
	
	rowCountUpdated= Signal()

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		# PROPERTIES
		self.methods = ["Média móvel", "Média aritmética",
						"Média geométrica", "Média harmônica",
						"Máxima"]

		self.groups = ["Data", "Mês e ano", "Ano"]
		self.header_names = ['', 'Método', 'Agrupar']
		self.margins = 2.5

		# WIDGETS
		self.add_button = self.getWidget(type = 'QPushButton', text = '+')
		self.blank_cell1 = QTableWidgetItem()
		self.blank_cell2 = QTableWidgetItem()

		# SETTINGS
		self.setupHeader()
		self.setupTable()
		
		# CONFIGURING WIDGETS
		self.blank_cell1.setFlags(self.blank_cell1.flags() & ~Qt.ItemIsEditable)
		self.blank_cell2.setFlags(self.blank_cell2.flags() & ~Qt.ItemIsEditable)
		self.add_button.setStyleSheet(button_style)

		# Signals and slots
		self.add_button.findChild(QPushButton).clicked.connect(self.createRow)

	def setupHeader(self):
		self.setColumnCount(3)
		self.setHorizontalHeaderLabels(self.header_names)
		#
		self.setColumnWidth(0, 30)
		self.setColumnWidth(1, 130)
		self.setColumnWidth(2, 130)
		header = self.horizontalHeader()
		#
		header.setStyleSheet(header_style)
		header.setSectionResizeMode(QHeaderView.Fixed)

	def setupTable(self):
		self.setRowCount(1)
		self.setCellWidget(0, 0, self.add_button)
		self.setItem(0, 1, self.blank_cell1)
		self.setItem(0, 2, self.blank_cell2)
		self.setShowGrid(False)
		self.verticalHeader().setVisible(False)
		self.resizeColumnToContents(0)
		self.setSelectionMode(QTableWidget.SelectionMode.NoSelection)

	def createRow(self):
		# Inserir linha
		row_position = self.rowCount() - 1
		self.insertRow(row_position)

		# cria widgets
		remove_button = self.getWidget(type = 'QPushButton', text = '-')
		methods_combo = self.getWidget(type = 'QComboBox')
		groupby_combo = self.getWidget(type = 'QComboBox')

		# configura widgets
		methods_combo.findChild(QComboBox).addItems(self.methods)
		groupby_combo.findChild(QComboBox).addItems(["8 horas"])

		# adding to table
		self.setCellWidget(row_position, 0, remove_button)
		self.setCellWidget(row_position, 2, groupby_combo)
		self.setCellWidget(row_position, 1, methods_combo)

		# signals and slots
		remove_button.findChild(QPushButton).clicked.connect(lambda: self.deleteRow(row_position))
		methods_combo.findChild(QComboBox).currentTextChanged.connect(lambda: self.updateMethods(row_position))

		# emit signal
		self.rowCountUpdated.emit()

	def updateMethods(self, row):
		combobox = self.cellWidget(row, 1).findChild(QComboBox)

		is_moving_average = combobox.currentIndex() == 0
		group_combobox = self.cellWidget(row, 2).findChild(QComboBox)
		if is_moving_average:
			group_combobox.clear()
			group_combobox.addItems(["8 horas"])
		
		elif group_combobox.count() == 1:
			group_combobox.clear()
			group_combobox.addItems(self.groups)
		
	def deleteRow(self, row):
		self.removeRow(row)

		# emit signal
		self.rowCountUpdated.emit()

	def getComboBox(self):
		widget = QComboBox()
		widget.setStyleSheet(combobox_style)
		widget.setFixedSize(120, 25)

		return widget

	def getButton(self, text):
		widget = QPushButton(text)
		widget.setStyleSheet(button_style)
		widget.setFixedSize(25, 25)

		return widget

	def getWidget(self, **kwargs):
		cell_widget = QWidget()
		layout = QHBoxLayout(cell_widget)
		layout.setContentsMargins(self.margins,self.margins,self.margins,self.margins)
		layout.setSpacing(0)

		# creating widget
		if kwargs.pop('type') == 'QPushButton':
			widget = self.getButton(kwargs.pop('text'))
		else:
			widget = self.getComboBox()

		layout.addWidget(widget)
		layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

		return cell_widget

	def getMethods(self):
		methods = []
		for row in range(self.rowCount() - 1):
			group_combobox = self.cellWidget(row, 2).findChild(QComboBox)
			method_combobox = self.cellWidget(row, 1).findChild(QComboBox)
			methods.append(
			(method_combobox.currentText(), group_combobox.currentText())
			)

		return methods

	def setMethods(self, methods):
		for row in range(len(methods)):
			self.createRow()
			#
			group_combobox = self.cellWidget(row, 2).findChild(QComboBox)
			method_combobox = self.cellWidget(row, 1).findChild(QComboBox)
			#
			method_combobox.setCurrentText(methods[row][0])
			group_combobox.setCurrentText(methods[row][1])

