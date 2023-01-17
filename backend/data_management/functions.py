# SCRIPT COM FUNCOES RELACIONADAS AO GERENCIAMENTO DOS DADOS

# IMPORT MODULES
import numpy as np
import os
import xlrd

# IMPORT CUSTOM MODULES
from backend.data_management.data_management import XlsStationData

def xls_reader(file_path : str):
	'''
	Abre o arquivo excel extraido do ATMOS e coleta os dados da estação de monitoramento
	de qualidade do ar e meteorologia. A planilha pode conter informações de uma ou mais
	estações.
   
	args:
		- file_path: caminho no computador ate o arquivo.
   
	returns:
		- Objeto XlsStationData contendo todas as variaveis, flags  e informacoes sobre a estacao
		de monitoramento.
	'''
	# apen file
	xls = xlrd.open_workbook(file_path, logfile = open(os.devnull, 'w'))
	sheet = xls.sheet_by_index(0) # file contains only one sheet
	
	# Properties of the sheet]
	ncols = sheet.ncols
	nrows = sheet.nrows
	sheet_metadata = {}
	
	# Guessing the number of enterprises, stations and themes and its columns. 
	items = ["enterprise_col", "station_col", "theme_col", "parameter_col"]
	for i, j in enumerate([0, 1, 2, 4]):
		row_values = np.array(sheet.row_values(j, start_colx = 1)) # First column is "Data". Not important right now
		filled_cell = np.char.str_len(row_values) > 0 # filtering cells by str len
		name_index = np.arange(1, ncols)[filled_cell]
		names = row_values[filled_cell]

		# Inserting results into sheet_metadata
		sheet_metadata[items[i]] = np.asarray(list(zip(names, name_index)))

		if i > 2:
			# Guessing the parameters cols and its units.
			row_values = np.array(sheet.row_values(7, start_colx = 1)) # First column is "Data". Not important right now
			unit_cells = row_values != 'Flag' # filtering cells by str len
			units = row_values[unit_cells]
			unit_cols = np.arange(1, ncols)[unit_cells]

			sheet_metadata["unit_col"] = np.asarray(list(zip(units, unit_cols)))

	# GETTING DATETIME ARRAYS
	value_idx = 8
	datetime_array = np.array([xlrd.xldate_as_datetime(value, 0) for value in sheet.col_values(0, value_idx)], dtype='datetime64')

	# EXTRACTING PARAMETERS VALUES AND FLAGS
	value_type = np.float32 # precision equals to 4 decimal places, which is sufficient

	station_objects = {}
	for unit, col in sheet_metadata["unit_col"].tolist():
		col = int(col)
		values = np.array(sheet.col_values(col, value_idx), dtype = '<U11')
		values[values == ''] = 'nan' # empty cells are nan
		values = values.astype(value_type)

		# next col contains the flags
		flags = np.array(sheet.col_values(col + 1, value_idx))

		# find properties
		metadata = {}
		for k in sheet_metadata.keys():
			idx = find_previous_nearest(sheet_metadata[k][:, 1].astype(int), col)
			metadata[k[:-4]] = sheet_metadata[k][idx, 0]

		# signature
		upper_name = metadata['station'].upper()
		if "AUTO" in upper_name or "SEMI" in upper_name:
			idx = metadata['station'].find('-')
			metadata['station'] = metadata['station'][idx + 1:].lstrip()
			
		metadata['signature'] = 'xls-' + metadata['station']

		# insertig into object
		complete_name = metadata['parameter'] + " " + unit.split(' ')[-1]

		# Creating station object and setting up properties
		station_object = station_objects.get(metadata['signature'],
		XlsStationData(
			name = metadata['station'], enterprise = metadata['enterprise'], dates = datetime_array
		))
		station_object.add_parameter(
			complete_name, 
			parameter = (values, flags),
			theme = metadata['theme']
			)

		if metadata['signature'] not in station_objects:
			station_objects[metadata['signature']] = station_object

	return station_objects


def find_previous_nearest(array, value):
	array = array - value
	previous = array[array <= 0]
	idx = previous.argmax()
	
	return idx
