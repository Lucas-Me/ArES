# IMPORT MODULES
import numpy as np

# IMPORT QT CORE
from qt_core import *

# IMPORT CUSTOM UI
from gui.pages.ui_processingscreen import UI_ProcessScreen

# IMPORT CUSTOM MODULES
from gui.widgets.profile_picker import Profile

# IMPORT CUSTOM FUNCTIONS
from backend.data_management import stats


# VARIABLES
formats = {"Data" : "%Y-%m-%d", "Mês e ano": "%Y-%m-01", "Ano" : "%Y-01-01"}
functions = {"Média móvel":stats.media_movel, "Média aritmética":stats.media,
			"Média geométrica" : stats.media_geometrica, "Média harmônica" : stats.media_harmonica,
			"Máxima" : stats.maxima}
frequencies = {"Data" : np.timedelta64(1,'D'), "Mês e ano": np.timedelta64(1,'M'), "Ano" : np.timedelta64(1,'Y')}

# Data Manager Page Class
class ProcessingScreen(QWidget):

	def __init__(self, parent : QStackedWidget):
		super().__init__(parent = parent)

		# PRIVATE VARIABLES
		self.raw_data = []
		self.processed_data = []
		self.standard_profile = Profile(color = QColor('#fafafa'), name = 'simple')

		# SETUP UI
		self.ui = UI_ProcessScreen()
		self.ui.setup_ui(self)
		self.ui.setup_stylesheet(parent)

		# SIGNALS AND SLOTS
		self.ui.profile_picker.list.removedProfile.connect(self.resetProfileBox)
		self.ui.profile_picker.list.profileDoubleClicked.connect(self.showProfileEditor)
		self.ui.next_button.clicked.connect(self.processTasks)

	@Slot(QDialog)
	def showProfileEditor(self, dialog : QDialog):
		dialog.setParent(self)
		dialog.showWindow()

	def updateDates(self, start_date, end_date):
		fmt = '%Y %b %d'
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
		'''
		# creating empty array of shape (N,)
		n = len(self.raw_data)
		processed_data = [None] * n 

		# creating regex string to filter values by flags
		regex = self.getRegexString()

		# Loop throught each item of "raw_data"
		for i in range(n):
			# applying flag filter
			filtered_data = self.raw_data[i].filterByFlags(regex) # returns a ModifedData object

			# convert PPB to PPM if needed
			filtered_data = self.convertPPB2PPM(filtered_data)

			# check if a profile was selected for a given object, and apply if needed.
			final_data = self.runProfile(filtered_data, i)

			# updating metadata
			del filtered_data.metadata['frequency']
			final_data.metadata.update(filtered_data.metadata)

			# finalizing
			processed_data[i] = final_data

		self.processed_data = processed_data

	def getRegexString(self):
		# GETTING FLAGS TO FILTER BY (# regex)
		validos = '[V*]\w|^$' # any word that starts with V or any empty character
		suspeitos = '[?*]\w' # any words that starts with ?
		invalidos = '[I*]\w' # any word that start with I
		#
		flags = [validos, suspeitos, invalidos]
		regex = ''

		# loop through each checkbox
		comboboxes = self.ui.checkbox_flags
		for i in range(len(comboboxes)):
			if comboboxes[i].isChecked():
				regex += flags[i] + '|'

		regex = regex[:-1] # removing last character "|"

		return regex

	def convertPPB2PPM(self, data_object):
		pname = data_object.metadata['parameter'] # get parameter name

		if 'ppb' in pname and self.ui.ppb_button.isChecked():
			
			# apply conversion
			data_object.setValues(data_object.getValues() * 1e-3)

			# change parameter unit
			data_object.metadata['parameter'] = pname.replace('ppb', 'ppm')

		return data_object

	def runProfile(self, data_object, index):
		# PROPERTIES
		target_list = self.ui.parameter_list
		widget = target_list.item(index)
		profile = target_list.itemWidget(widget).getProfile()

		# checking methods
		methods = profile.getMethods()
		n = len(methods)
		for order in range(n): # if n == 0, will not enter loop anyway
			calc = methods[order][0]
			group = methods[order][1]
			#
			threshold = 0 # TESTE
			func = functions[calc]

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
					format_ = formats[group]
				)
				# if it reached here, then there is a need to groupby first

			data_object = data_object.apply(**kwargs)

		data_object.metadata['methods'] = methods
		data_object.metadata['frequency'] = frequencies[methods[-1][1]]
		return data_object

		