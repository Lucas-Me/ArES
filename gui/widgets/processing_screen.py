# IMPORT MODULES
import numpy as np
from copy import deepcopy
import os, xlsxwriter

# IMPORT QT CORE
from qt_core import *

# IMPORT CUSTOM UI
from gui.pages.ui_processingscreen import UI_ProcessScreen
from gui.windows.dialog.loading_dialog import LoadingDialog

# IMPORT CUSTOM MODULES
from backend.data_management.methods import Profile
import backend.misc.settings as settings
from gui.windows.dialog.import_dialog import ImportDialog

# IMPORT CUSTOM FUNCTIONS
from backend.data_management import stats
from backend.misc.functions import get_frequency
from backend.data_management.functions import export_to_xlsx

# IMPORT CUSTOM VARIABLES
import backend.misc.settings as settings

# IMPORT DIALOGS
from gui.windows.dialog.import_dialog import ImportDialog

# Data Manager Page Class
class ProcessingScreen(QWidget):

	resultReady = Signal(list)
	def __init__(self, parent : QStackedWidget):
		super().__init__(parent = parent)

		# PRIVATE VARIABLES
		self.save_dir = os.path.expanduser("~")
		self.raw_data = []
		self.processed_data = []
		self.standard_profile = Profile(color = QColor('#fafafa'), name = 'simple')

		# SETUP UI
		self.ui = UI_ProcessScreen()
		self.ui.setup_ui(self)
		self.ui.setup_stylesheet(parent)

		# SETTINGS
		self.laodProfiles() # load pre-existing profile, from earlier sessions

		# SIGNALS AND SLOTS
		self.ui.profile_picker.list.removedProfile.connect(self.resetProfileBox)
		self.ui.profile_picker.list.profileDoubleClicked.connect(self.showProfileEditor)
		self.ui.next_button.clicked.connect(self.processTasks)
		self.ui.export_raw.clicked.connect(lambda: self.export('raw'))
		self.ui.export_modified.clicked.connect(lambda: self.export('modified'))

	def laodProfiles(self):
		profiles = settings.SETTINGS.get('perfis', {})
		if len(profiles) == 0:
			return None
		
		for k, v in profiles.items():
			new_index = self.ui.profile_picker.list.model.rowCount()
			new_profile = Profile(
				color = QColor(v[0]),
				name = k,
				methods = v[1]
			)
			
			# inserting new profile
			self.ui.profile_picker.list.updateProfile(new_index, new_profile)

	def exportStatus(self):
		if len(self.processed_data) > 0:
			self.ui.export_modified.show()
		else:
			self.ui.export_modified.hide()

	@Slot(QDialog)
	def showProfileEditor(self, dialog : QDialog):
		dialog.setParent(self)
		dialog.showWindow()

	def updateDates(self, start_date, end_date):
		fmt = ' %d %b %y'
		text = f"{start_date.strftime(fmt)} - {end_date.strftime(fmt)}"
		self.ui.date_label.setText(text)

	def updateRawData(self, data):
		# reset list
		self.ui.parameter_list.reset_settings()

		# adding to list
		n = len(data)
		for i in range(n):
			item = self.ui.parameter_list.addRow(
				parameter = data[i].metadata['parameter'],
				station = data[i].metadata['name'],
				enterprise = data[i].metadata['enterprise'],
				profile = self.standard_profile
				)

			# SIGNALS
			item.profile_box.pressed.connect(self.profileBoxClicked)

		# SETTING PROPERTIES
		self.raw_data = data

	@Slot(QWidget)
	def profileBoxClicked(self, item):
		# getting properies
		current_profile = item.getProfile()
		profile = self.ui.profile_picker.nextProfile(current_profile)

		# test if None
		if profile is None:
			item.setProfile(self.standard_profile)
		else:
			item.setProfile(profile)

	@Slot(object)
	def resetProfileBox(self, profile):
		target = self.ui.parameter_list
		for row in range(target.count()):
			item = target.item(row)
			item_widget = target.itemWidget(item)
			#
			if item_widget.getProfile() == profile:
				item_widget.setProfile(self.standard_profile)

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

	def processTasks(self):
		'''
		Processos os dados brutos coletados e organizados, e aplica uma transformacao
		a eles, se necessário.
		O resultado fica disponível nesta página, mas também na página de visualização de dados. (Gráfico)

		Fluxo de operacação:
			1. Executar um loop em cada item da lista 'raw_data'
			2. Filtrar por flags e converter unidades [ppb] para [ppm] se necessário
			3. Transformar de acordo com o Perfil especifica pelo usuário. Caso não haja perfil, apena retorna os dados brutos.
		
		Todas essas operacoes sao realizadas em uma Thread separada (vide classe "Worker" abaixo)
		para nao interromper (congelar) o programa principal.
		'''
		# counting the number of rows to process
		n = len(self.raw_data)
		
		# creating regex string to filter values by flags
		regex = self.getRegexString()

		# Retrieving the profiles containing the methods selected by the user
		target_list = self.ui.parameter_list
		methods = [None] * n
		for i in range(n):
			widget = target_list.item(i)
			profile = target_list.itemWidget(widget).getProfile()

			# checking methods
			methods[i] = profile.getMethods()

		# is it necessary to convert [ppb] to [ppm]?
		convert = self.ui.ppb_button.isChecked()

		# create loading dialog
		dialog = LoadingDialog(text = 'Processando dados', parent = self)
		dialog.show()

		# Create a QThread object
		self.thread = QThread()

		# Create a worker object
		self.worker = Worker(
			regex = regex,
			convert = convert,
			raw_data = self.raw_data,
			methods = methods
		)

		# Move worker to the thread
		self.worker.moveToThread(self.thread)

		# Connect signals and slots
		self.thread.started.connect(self.worker.start)
		#
		self.worker.resultReady.connect(self.thread.quit)
		self.worker.resultReady.connect(self.worker.deleteLater)
		self.worker.resultReady.connect(self.handleProcessedResults)
		self.worker.resultReady.connect(lambda: dialog.closeWindow(True))
		#
		self.worker.error.connect(self.thread.quit)
		self.worker.error.connect(self.worker.deleteLater)
		self.worker.error.connect(lambda: dialog.closeWindow(False))
		self.worker.error.connect(self.handleError)
		#
		self.thread.finished.connect(self.thread.deleteLater)

		# Start the thread
		self.thread.start()

	@Slot(list)
	def handleProcessedResults(self, results):
		self.processed_data = results
		self.exportStatus()
		self.resultReady.emit(self.processed_data)

	def handleError(self, error : object):
		# print(type(error))
		# print(error.args)
		# print(error)

		# opens a dialog warning the user about the error
		dialog = ImportDialog(
			title = 'Erro desconhecido',
			message = 'Ocorreu um erro inesperado durante a execução das tarefas.',
			description= '',
			parent = self
		)
		dialog.ignore_button.hide()
		dialog.show()

	def getRegexString(self):
		# GETTING FLAGS TO FILTER BY (# regex)
		# validos = '[V*]\w|^$' # any word that starts with V or any empty character
		validos = '[V*]\w|^$|[<*]|[>*]|[!*]' # any word that starts with V or any empty character or ! or < or > 
		suspeitos = '[?*]\w' # any words that starts with ?
		invalidos = '[I*]\w' # any word that start with I
		#
		flags = [validos, invalidos, suspeitos]
		regex = ''

		# loop through each checkbox
		comboboxes = self.ui.checkbox_flags
		for i in range(len(comboboxes)):
			if comboboxes[i].isChecked():
				regex += flags[i] + '|'

		regex = regex[:-1] # removing last character "|"
		return regex

	def export(self, kind):
		# getting filename and path
		fname, filter = QFileDialog.getSaveFileName(
			parent = self,
			caption = "Salvar tabela como...",
			dir = self.save_dir,
			filter = "Excel files (*.xlsx)",
		)

		# check if fname is valid
		if len(fname) > 0:
			# update save directory
			self.save_dir = os.path.dirname(fname)

			# try to export xlsx file
			try:
				if kind == 'raw':
					export_to_xlsx(files = self.raw_data, kind = kind, fname =  fname)
				else:
					export_to_xlsx(files = self.processed_data, kind = kind, fname = fname)

			# throw an exception if failed
			except xlsxwriter.exceptions.FileCreateError as err:
				dialog = ImportDialog(
					title = 'Erro',
					message = 'Não foi possível salvar a planilha de dados',
					description='Certifique-se de que a planilha não esteja aberta em outro programa',
					parent = self
				)
				dialog.ignore_button.hide()
				dialog.exec()


class Worker(QObject):
	'''
	Worker created in order to run the processTasks methods in the background.
	'''

	resultReady = Signal(list)
	error = Signal(object)

	def __init__(self, **kwargs) -> None:
		super().__init__(kwargs.get('parent', None))
		self.raw_data = deepcopy(kwargs.get('raw_data', None))
		self.regex = deepcopy(kwargs.get('regex'))
		self.convert = deepcopy(kwargs.get('convert'))
		self.methods = deepcopy(kwargs.get('methods'))

		# VARIABLES
		self.formats = {"Data" : "%Y-%m-%d", "Mês e ano": "%Y-%m-01", "Ano" : "%Y-01-01"}
		self.functions = {"Média móvel":stats.media_movel, "Média aritmética":stats.media,
				"Média geométrica" : stats.media_geometrica, "Média harmônica" : stats.media_harmonica,
				"Máxima" : stats.maxima}


	def start(self):
		try:
			# Loop throught each item of "raw_data"
			n = len(self.raw_data)
			processed_data = [None] * n  # new empty array

			for i in range(n):
				# applying flag filter
				filtered_data = self.raw_data[i].filterByFlags(self.regex) # returns a ModifedData object

				# convert PPB to PPM if needed
				filtered_data = self.convertPPB2PPM(filtered_data, self.convert)

				# check if a profile was selected for a given object, and apply if needed.
				final_data = self.runProfile(filtered_data, self.methods[i])

				# updating metadata
				dcopy = filtered_data.metadata.copy()
				del dcopy['frequency']
				final_data.metadata.update(dcopy)

				# finalizing
				processed_data[i] = final_data

			self.resultReady.emit(processed_data)

		except Exception as err:
			self.error.emit(err)

	def runProfile(self, data_object, methods):
		n = len(methods)
		for order in range(n): # if n == 0, will not enter loop anyway
			calc = methods[order][0]
			group = methods[order][1]

			# Critério de representatividade a ser considerado antes de efetuar o cálculo
			threshold = settings.SETTINGS['representatividade']['Horária']

			# se alguma operacao ja tiver sido realizada antes. Dados nao sao mais brutos, tratamento é diferente 
			if order > 0 and methods[order - 1][1] in settings.SETTINGS['representatividade']:
				threshold = settings.SETTINGS['representatividade'][methods[order - 1][1]]

			# Funcao respectiva ao cálculo selecionado
			func = self.functions[calc]

			# Applyng threshold
			data_object.setValues(data_object.maskByThreshold(threshold))
			
			# if "moving avareage" is selected, there is no need the group the data beforehand
			if calc == "Média móvel":
				kwargs = dict(
					func = func,
					date_array = data_object.getDates(),
					dt = np.timedelta64(8, "h")
				)

			else:
				kwargs = dict(
					func = func,
					groupby = True,
					format_ = self.formats[group],
					anual = self.formats[group] == "%Y-01-01" and data_object.metadata['type'] == 'Automática'
				)
				# if it reached here, then there is a need to groupby first

			data_object = data_object.apply(**kwargs)

		data_object.metadata['methods'] = methods
		
		# get frequency of dataset
		data_object.metadata['frequency'] = get_frequency(data_object.getDates())

		return data_object

	def convertPPB2PPM(self, data_object, convert):
		pname = data_object.metadata['parameter'] # get parameter name

		if 'ppb' in pname and convert:
			
			# apply conversion
			data_object.setValues(data_object.getValues() * 1e-3)

			# change parameter unit
			data_object.metadata['parameter'] = pname.replace('ppb', 'ppm')

			# change alias and signature
			data_object.metadata['signature'] = data_object.metadata['signature'].replace('ppb', 'ppm')
			data_object.metadata['alias'] = data_object.metadata['alias'].replace('ppb', 'ppm')

		return data_object