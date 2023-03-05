# IMPORT QT CORE
from qt_core import *

# MAIN WINDOW
class UI_SettingsWindow(object):
    
	def setup_ui(self, parent):
		if not parent.objectName():
			parent.setObjectName("settings_window")
		
		# CREATE MAIN LAYOUT
		self.frame_layout = QHBoxLayout(parent)
		self.frame_layout.setContentsMargins(0, 0, 0, 0)
		self.frame_layout.setSpacing(0)

		self.frame = QFrame()
		self.frame.setFixedSize(parent.width() - parent.margins, parent.height() - parent.margins)
		#
		self.main_layout = QHBoxLayout(self.frame)
		self.main_layout.setContentsMargins(0, 0, 0, 0)
		self.main_layout.setSpacing(0)
		#
		self.frame_layout.addWidget(self.frame, alignment=Qt.AlignmentFlag.AlignCenter)

		# LEFT MENU
		# //////////////////////////////////////////////////////////////////////
		self.left_menu = QFrame()
		self.left_menu.setObjectName('menu')
		self.left_menu.setFixedWidth(100)

		# LEFT MENU LAYOUT
		self.left_menu_layout = QVBoxLayout(self.left_menu)
		self.left_menu_layout.setContentsMargins(0, 0, 0, 0)
		self.left_menu_layout.setSpacing(0)

		# CONNECTION BUTTON
		self.btn_connection = QPushButton('Conexão')
		self.btn_connection.setObjectName('connection')
		self.btn_connection.setDisabled(True)
		self.btn_connection.setFixedHeight(30)
		
		# CONNECTION BUTTON
		self.btn_criteria = QPushButton('Critérios')
		self.btn_criteria.setObjectName('criteria')
		self.btn_criteria.setFixedHeight(30)

		# CONNECTION BUTTON
		self.btn_figure = QPushButton('Figura')
		self.btn_figure.setObjectName('figure')
		self.btn_figure.setFixedHeight(30)

		# label version
		self.left_menu_label_version = QLabel("v1.3.0")
		self.left_menu_label_version.setAlignment(Qt.AlignmentFlag.AlignCenter)
		self.left_menu_label_version.setFixedHeight(30)
		self.left_menu_label_version.setObjectName('version')
		
		# adding to layout
		self.left_menu_layout.addWidget(self.btn_connection)
		self.left_menu_layout.addWidget(self.btn_criteria)
		self.left_menu_layout.addWidget(self.btn_figure)
		self.left_menu_layout.addItem(QSpacerItem(100, 30, QSizePolicy.MinimumExpanding, QSizePolicy.Expanding))
		self.left_menu_layout.addWidget(self.left_menu_label_version)

		# CONTENTS AT RIGHT
		# //////////////////////////////////////////////////////////////////////
		self.contents = QFrame()
		self.contents.setObjectName('frame')
		self.contents.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Expanding)

		# CONTENT LAYOUT
		self.contents_layout = QVBoxLayout(self.contents)
		self.contents_layout.setContentsMargins(0, 0, 0, 0)
		self.contents_layout.setSpacing(0)

		# EXIT BUTTON
		self.btn_exit = QPushButton('x')
		self.btn_exit.setObjectName('exit')
		self.btn_exit.setFixedSize(30, 25)

		# PAGES
		self.stacked_widget = QStackedWidget(parent = parent)

		# adding pages
		self.setupPages()

		# BOTTOM BAR
		self.bottom_layout = QHBoxLayout()
		self.bottom_layout.setContentsMargins(10, 5, 10, 5)
		self.bottom_layout.setSpacing(10)

		# BOTTOM BAR BUTTONS
		self.btn_save = QPushButton('Salvar')
		self.btn_save.setObjectName('save')
		self.btn_save.setFixedSize(60, 30)
		#
		self.btn_apply = QPushButton('Aplicar')
		self.btn_apply.setObjectName('apply')
		self.btn_apply.setFixedSize(60, 30)

		# add to bottom bar
		self.bottom_layout.addItem(QSpacerItem(30, 40, QSizePolicy.MinimumExpanding, QSizePolicy.Fixed))
		self.bottom_layout.addWidget(self.btn_save)
		self.bottom_layout.addWidget(self.btn_apply)

		# add to contents layout
		self.contents_layout.addWidget(self.btn_exit, alignment= Qt.AlignmentFlag.AlignRight)
		self.contents_layout.addWidget(self.stacked_widget)
		self.contents_layout.addLayout(self.bottom_layout)

		# ADD TO MAIN LAYOUT
		# ////////////////////////////////////
		self.main_layout.addWidget(self.left_menu)
		self.main_layout.addWidget(self.contents)

		# SETUP STYLE SHEET
		# ////////////////////////////////////
		self.setupStyle(parent)

		
	def setupStyle(self, parent):
		parent.setStyleSheet(f'''
			#top_level_representatividade, #top_level_semi, #top_level_fonts, #top_level_graphwindow {{
				background-color: transparent;
				font: bold 12pt 'Microsoft New Tai Lue';
				color: black;
				border-bottom: 1px solid #e1e1e1;
			}}
			QLabel, QLineEdit{{
				background-color: transparent;
				font: normal 12pt 'Microsoft New Tai Lue';
				color: black;
			}}
			#version{{
				background-color: transparent;
				font: normal 12pt 'Microsoft New Tai Lue';
				text-align: middle;
				color: black;
			}}
			#connection, #figure, #criteria{{
				background-color: #e1e1e1;
				font: normal 12pt 'Microsoft New Tai Lue';
				text-align: middle;
				color: black;
				border: none;
			}}
			#connection:hover, #figure:hover, #criteria:hover{{
				background-color: #d3d3d3;
			}}
			#connection:disabled, #figure:disabled, #criteria:disabled{{
				background-color: #c5c5c5;
			}}
			#menu{{
				background-color: #e1e1e1;
				border: none;
			}}
			#frame{{
				background-color: #ffffff;
				border: none;
			}}
			#exit{{
				background-color: transparent;
				border: none;
				font: normal 14pt 'Calibri';
				color: black;
			}}
			#exit:hover{{
				background-color: #ed4856;
				color: white;
			}}
			#save, #apply{{
				background-color: transparent;
				border: 1px solid #e1e1e1;
				font: normal 12pt 'Microsoft New Tai Lue';
				text-align: middle;
			}}
			#save:hover, #apply:hover{{
				background-color: #e1e1e1;
			}}
			#save:pressed, #apply:pressed{{
				background-color: #c5c5c5;
			}}
		''')

	def setupPages(self):

		# PAGE 1 - SQL CONNECTION
		# ///////////////////////
		self.page_connection = QWidget()
		self.page_connection.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Expanding)
		self.page_connection.setObjectName('connection_page')
		text_height = 30
		
		# layout
		self.layout_page1 = QGridLayout(self.page_connection)
		self.layout_page1.setContentsMargins(10, 10, 10, 10)
		self.layout_page1.setSpacing(10)

		# labels
		self.label_server = QLabel('Servidor')
		self.label_server.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
		self.label_server.setFixedHeight(text_height)

		self.label_database = QLabel('Database')
		self.label_database.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
		self.label_database.setFixedHeight(text_height)

		# line edit
		self.server_edit = QLineEdit()
		self.server_edit.setPlaceholderText("IP ou nome do PC")
		self.server_edit.setFixedHeight(text_height)

		self.database_edit = QLineEdit()
		self.database_edit.setPlaceholderText("banco_gear")
		self.database_edit.setFixedHeight(text_height)

		# add to layout
		self.layout_page1.addWidget(self.label_server, 0, 0)
		self.layout_page1.addWidget(self.label_database, 1, 0)
		self.layout_page1.addWidget(self.server_edit, 0, 1)
		self.layout_page1.addWidget(self.database_edit, 1, 1)
		self.layout_page1.addItem(QSpacerItem(30,30, QSizePolicy.Expanding, QSizePolicy.Expanding), 2, 0, 1, 2)

		# PAGE 2 - CRITERIOS DE REPRESENTATIVIDADE
		# ///////////////////////
		self.page_criteria = QWidget()
		self.page_criteria.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Expanding)
		self.page_criteria.setObjectName('criteria_page')
		text_height = 20
		
		# layout
		self.layout_page2 = QGridLayout(self.page_criteria)
		self.layout_page2.setContentsMargins(10, 10, 10, 10)
		self.layout_page2.setSpacing(5)

		# representatividade
		self.label_validos = QLabel("Representatividade")
		self.label_validos.setAlignment(Qt.AlignmentFlag.AlignCenter)
		self.label_validos.setFixedHeight(text_height)
		self.label_validos.setObjectName('top_level_representatividade')

		# HORARIA
		self.label_hourly = QLabel('Horária')
		self.label_hourly.setAlignment(Qt.AlignmentFlag.AlignCenter)
		self.label_hourly.setFixedHeight(text_height)
		#
		self.spinbox_hourly = QSpinBox()
		self.spinbox_hourly.setFixedSize(100, text_height)
		self.spinbox_hourly.setRange(0, 100)

		# DIARIA
		self.label_daily = QLabel('Diária')
		self.label_daily.setAlignment(Qt.AlignmentFlag.AlignCenter)
		self.label_daily.setFixedHeight(text_height)
		#
		self.spinbox_daily = QSpinBox()
		self.spinbox_daily.setFixedSize(100, text_height)
		self.spinbox_daily.setRange(0, 100)

		# MENSAL
		self.label_monthly = QLabel('Mensal')
		self.label_monthly.setAlignment(Qt.AlignmentFlag.AlignCenter)
		self.label_monthly.setFixedHeight(text_height)
		#
		self.spinbox_monthly = QSpinBox()
		self.spinbox_monthly.setFixedSize(100, text_height)
		self.spinbox_monthly.setRange(0, 100)

		# ANUAL
		self.label_yearly = QLabel('Anual')
		self.label_yearly.setAlignment(Qt.AlignmentFlag.AlignCenter)
		self.label_yearly.setFixedHeight(text_height)
		#
		self.spinbox_yearly = QSpinBox()
		self.spinbox_yearly.setFixedSize(100, text_height)
		self.spinbox_yearly.setRange(0, 100)

		# SEMIAUTOMATICA
		self.label_semi = QLabel("Amostragem semiautomática")
		self.label_semi.setAlignment(Qt.AlignmentFlag.AlignCenter)
		self.label_semi.setFixedHeight(text_height)
		self.label_semi.setObjectName('top_level_semi')

		# DATA DE REFERENCIA
		self.label_date = QLabel('Data de referência')
		self.label_date.setAlignment(Qt.AlignmentFlag.AlignCenter)
		self.label_date.setFixedHeight(text_height)
		#
		self.date_edit = QDateEdit()
		self.date_edit.setFixedSize(100, text_height)

		# FREQUENCIA
		self.label_freq = QLabel('Frequência')
		self.label_freq.setAlignment(Qt.AlignmentFlag.AlignCenter)
		self.label_freq.setFixedHeight(text_height)
		#
		self.spinbox_freq = QSpinBox()
		self.spinbox_freq.setFixedSize(100, text_height)
		self.spinbox_freq.setRange(1, 30)

		# add to layout
		self.layout_page2.addWidget(self.label_validos, 0, 0, 1, 2, alignment=Qt.AlignmentFlag.AlignTop)
		self.layout_page2.addWidget(self.label_hourly, 1, 0)
		self.layout_page2.addWidget(self.label_daily, 2, 0)
		self.layout_page2.addWidget(self.label_monthly, 3, 0)
		self.layout_page2.addWidget(self.label_yearly, 4, 0)
		self.layout_page2.addWidget(self.spinbox_daily, 1, 1)
		self.layout_page2.addWidget(self.spinbox_hourly, 2, 1)
		self.layout_page2.addWidget(self.spinbox_monthly, 3, 1)
		self.layout_page2.addWidget(self.spinbox_yearly, 4, 1)
		self.layout_page2.addItem(QSpacerItem(10, 10, QSizePolicy.Expanding, QSizePolicy.MinimumExpanding), 5, 0, 1, 2)
		self.layout_page2.addWidget(self.label_semi, 6, 0, 1, 2)
		self.layout_page2.addWidget(self.label_date, 7, 0)
		self.layout_page2.addWidget(self.label_freq, 8, 0)
		self.layout_page2.addWidget(self.date_edit, 7, 1)
		self.layout_page2.addWidget(self.spinbox_freq, 8, 1)

		# PAGE 3 - CRITERIOS DE REPRESENTATIVIDADE
		# ///////////////////////
		self.page_figure = QWidget()
		self.page_figure.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Expanding)
		self.page_figure.setObjectName('figure_page')
		text_height = 20
		
		# layout
		self.layout_page3 = QGridLayout(self.page_figure)
		self.layout_page3.setContentsMargins(10, 10, 10, 10)
		self.layout_page3.setSpacing(5)

		# representatividade
		self.label_adjust = QLabel("Janela de gráfico")
		self.label_adjust.setAlignment(Qt.AlignmentFlag.AlignCenter)
		self.label_adjust.setFixedHeight(text_height)
		self.label_adjust.setObjectName('top_level_graphwindow')

		# HORARIA
		self.label_left = QLabel('Canto esquerdo')
		self.label_left.setAlignment(Qt.AlignmentFlag.AlignCenter)
		self.label_left.setFixedHeight(text_height)
		#
		self.spinbox_left = QDoubleSpinBox()
		self.spinbox_left.setFixedSize(100, text_height)
		self.spinbox_left.setRange(0, 1)

		# DIARIA
		self.label_right = QLabel('Canto direito')
		self.label_right.setAlignment(Qt.AlignmentFlag.AlignCenter)
		self.label_right.setFixedHeight(text_height)
		#
		self.spinbox_right = QDoubleSpinBox()
		self.spinbox_right.setFixedSize(100, text_height)
		self.spinbox_right.setRange(0, 1)

		# MENSAL
		self.label_bottom = QLabel('Canto inferior')
		self.label_bottom.setAlignment(Qt.AlignmentFlag.AlignCenter)
		self.label_bottom.setFixedHeight(text_height)
		#
		self.spinbox_bottom = QDoubleSpinBox()
		self.spinbox_bottom.setFixedSize(100, text_height)
		self.spinbox_bottom.setRange(0, 1)

		# ANUAL
		self.label_top = QLabel('Canto superior')
		self.label_top.setAlignment(Qt.AlignmentFlag.AlignCenter)
		self.label_top.setFixedHeight(text_height)
		#
		self.spinbox_top = QDoubleSpinBox()
		self.spinbox_top.setFixedSize(100, text_height)
		self.spinbox_top.setRange(0, 1)

		# SEMIAUTOMATICA
		self.label_fonts = QLabel("Fonte")
		self.label_fonts.setAlignment(Qt.AlignmentFlag.AlignCenter)
		self.label_fonts.setFixedHeight(text_height)
		self.label_fonts.setObjectName('top_level_fonts')

		# Font Family
		self.font_families = QComboBox()
		self.font_families.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.MinimumExpanding)
		#
		self.font_size = QSpinBox()
		self.font_size.setFixedWidth(40)
		self.font_size.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.MinimumExpanding)
		self.font_size.setRange(1, 50)
		#
		self.text_frame = QFrame()
		self.text_frame.setFixedHeight(30)
		self.text_frame_layout = QHBoxLayout(self.text_frame)
		self.text_frame_layout.setContentsMargins(0, 0, 0, 0)
		self.text_frame_layout.setSpacing(5)
		self.text_frame_layout.addWidget(self.font_families)
		self.text_frame_layout.addWidget(self.font_size)

		# add to layout
		self.layout_page3.addWidget(self.label_adjust, 0, 0, 1, 2, alignment=Qt.AlignmentFlag.AlignTop)
		self.layout_page3.addWidget(self.label_left, 1, 0)
		self.layout_page3.addWidget(self.label_right, 2, 0)
		self.layout_page3.addWidget(self.label_bottom, 3, 0)
		self.layout_page3.addWidget(self.label_top, 4, 0)
		self.layout_page3.addWidget(self.spinbox_left, 1, 1)
		self.layout_page3.addWidget(self.spinbox_right, 2, 1)
		self.layout_page3.addWidget(self.spinbox_bottom, 3, 1)
		self.layout_page3.addWidget(self.spinbox_top, 4, 1)
		self.layout_page3.addItem(QSpacerItem(10, 10, QSizePolicy.Expanding, QSizePolicy.MinimumExpanding), 5, 0, 1, 2)
		self.layout_page3.addWidget(self.label_fonts, 6, 0, 1, 2)
		self.layout_page3.addWidget(self.text_frame, 7, 0, 1, 2)

		# ADD TO STACKED WIDGET
		# ////////////////////
		self.stacked_widget.addWidget(self.page_connection)
		self.stacked_widget.addWidget(self.page_criteria)
		self.stacked_widget.addWidget(self.page_figure)
		self.stacked_widget.setCurrentIndex(0)





