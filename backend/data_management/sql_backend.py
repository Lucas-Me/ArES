# IMPORT MODULES
import numpy as np
from mysql.connector import Error, MySQLConnection

# Necessarios para evitar erros
from mysql.connector.locales.eng import client_error

# IMPORT QT MODULES
from qt_core import *


class SqlConnection(object):
	'''
	Classe responsavel pela conexão com o banco de dados em MySQL e criação de um
	inventário das estações de qualidade do ar e meteorologia, dado uma fonte de dados.

	Bando de dados utilizado -> MySQL'''

	def __init__(self, host, db) -> None:
		self.cnx = MySQLConnection()
		self.station_enterprises = [] # empresa estacao
		self.station_names = [] # nome estacao
		self.table_names = [] # table_name no sql
		self.table_vars = {} # key = nome estacao, value = [variaveis presentes, campoN]
		self.table_vars_columns = {}
		self.dates = {} # dictionary with dates from every station available

		# CONFIGURATION
		self.configureHost(host, db)

	def configureHost(self, host, db):
		self.cnx.config(host = host, database = db)

	def get_status(self):
		return self.cnx.is_connected()

	def checkConnection(self):
		try:
			ping = self.cnx.ping()

		except:
			raise TimeoutError

		return ping

	def connect(self, username, password):
		code = 1 # code 1 means conection success
		try:
			self.cnx.connect(
				user = username,
				password = password,
			)

		except Error as err:
			print(err)
			code = err.errno

		return code

	def disconnect(self):
		self.cnx.close()

		# reseta tudo
		self.connected = False
		return None

	def atualizar_inventario(self, dialog):
		'''
		Atualiza o inventário da conexão local SQL com base nos headers disponiveis
		no banco de dados "Banco_GEAR"

		Faz isso em uma thread separada, para não congelar o programa.
		'''
		# Create a QThread object
		self.thread = QThread()

		# Create a worker object
		self.worker = Worker(self)

		# Move worker to the thread
		self.worker.moveToThread(self.thread)

		# Connect signals and slots
		self.thread.started.connect(self.worker.start)
		#
		self.worker.resultReady.connect(self.thread.quit)
		self.worker.resultReady.connect(self.worker.deleteLater)
		self.worker.resultReady.connect(self.handleResults)
		self.worker.resultReady.connect(lambda: dialog.closeWindow(True))
		#
		self.worker.errorSQL.connect(self.thread.quit)
		self.worker.errorSQL.connect(self.worker.deleteLater)
		self.worker.errorSQL.connect(lambda: dialog.closeWindow(False))
		#
		self.thread.finished.connect(self.thread.deleteLater)

		# Start the thread
		self.thread.start()

	@Slot(dict)
	def handleResults(self, kwargs):
		self.dates = kwargs.get('dates', None)
		self.station_names = kwargs.get('nomes', None)
		self.station_enterprises = kwargs.get('empresas', None)
		self.table_names = kwargs.get('table_names', None)
		self.table_vars = kwargs.get('table_vars', None)
		self.table_vars_columns = kwargs.get('table_vars_columns', None)
		
	def query_var(self, var_index, station_object, start_date, end_date): # consulta um parametro de uma determinada estacao
		cursor = self.cnx.cursor()

		# properties of station object
		name = station_object.metadata['name']
		coluna = station_object.parameters_cols[var_index]
		idx = self.station_names.index(name)

		# CONSULTA
		# QUERY DATA
		query = (f"SELECT Campo1, Campo{coluna}, Campo{coluna + 1} FROM `{self.table_names[idx]}` "
				f"WHERE Campo1 BETWEEN %s AND %s")
		cursor.execute(query, (start_date, end_date))
		consulta = cursor.fetchall()

		# Fim
		cursor.close()

		return tuple(zip(*consulta))


class Worker(QObject):

	resultReady = Signal(dict)
	reportProgress = Signal(str)
	errorSQL = Signal()

	def __init__(self, connection, parent = None) -> None:
		super().__init__(parent)
		self.connection = connection

	@Slot()
	def start(self):
		try:
			self.run()
		except Error as err:
			self.errorSQL.emit()

		except Exception as err:
			# Apenas para debug
			print(err)

	@Slot()
	def run(self):
		'''Atualiza o inventario utilizando uma nova thread'''
		cursor = self.connection.cnx.cursor()

		# procurar apenas pelas tabelas 'headers' de cada estacao
		query = ("Select TABLE_NAME from INFORMATION_SCHEMA.TABLES"
		" WHERE TABLE_NAME LIKE '%header%'")
		cursor.execute(query)

		headers = [table_name for (table_name,) in cursor]
		cursor.close()
		N = len(headers)

		# le o cabecalho de cada tabela, e extrai as informacoes importantes
		# assume que:
		#     linha 1 -> string empresa responsavel
		#     linha 2 -> string nome da estacao
		#     Linha 3 -> temática de cada variavel
		#     linha 5 -> vazia
		#     linha 4 -> string das variaveis
		#     linha 6 -> string de unidades ou flags
		nomes = [''] * N
		empresas = [''] * N
		table_names = [''] * N
		table_vars = {}
		table_vars_columns =  {}
		dates_ = {}

		for i in range(len(headers)):
			cursor = self.connection.cnx.cursor()

			# extrai nome da empresa e da estacao.
			query = (f"SELECT Campo2 FROM `{headers[i]}` "
					f"WHERE Campo1 in (1, 2)")
			cursor.execute(query)
			empresas[i] = cursor.fetchone()[0]
			nomes[i] = cursor.fetchone()[0]
			table_names[i] = headers[i][:headers[i].find(' header')]

			#  Identifica os parametros e unidades existentes
			parametros_cols = [] # lista com o indice da coluna de cada parametro
			unidades = [] # lista com numero de unidades por parametro.
			first = True

			query = (f"SELECT * FROM `{headers[i]}` "
					f"WHERE Campo1 in (4, 6)")
			cursor.execute(query)
			parametro_line = cursor.fetchone()
			unidade_line = cursor.fetchone()

			# Parte do principio que a unidade esta em colunas impares
			# primeira coluna sera sempre da data.
			parametros_cols = []
			unidades = []
			ncols = len(parametro_line)
			for col in range(1, ncols, 2): 
				value = parametro_line[col]
				if not value is None:
					parametros_cols.append(col)
					if first:
						first = False
						continue
					unidades.append((col - parametros_cols[-2])//2)

			variaveis = []
			unidades.append((ncols - parametros_cols[-1])//2)
			campos = []
			for idx, col in enumerate(parametros_cols):
				basename = parametro_line[col]
				for j in range(unidades[idx]):
					# extrai somente a unidade da string: 'Valor (µg/m3)'
					unidade = unidade_line[col + j*2]
					if unidade is None:
						continue
					surname = unidade.split(" ")[1] 
					variaveis.append(basename + " " + surname)
					campos.append(col + j*2 + 1)
			
			table_vars[nomes[i]] = variaveis
			table_vars_columns[nomes[i]] = campos

			# verifica se ha outra linha a ser lida
			cursor.fetchall()

			# Extract first 24 date
			query = (f"SELECT Campo1 FROM `{table_names[i]}` LIMIT 10")
			cursor.execute(query)
			dates = cursor.fetchall()

			# extract most recent date
			query = (f"SELECT max(Campo1) FROM `{table_names[i]}`")
			cursor.execute(query)
			dates = dates + cursor.fetchall()
			dates_[nomes[i]] = np.array(dates, dtype= 'datetime64')

			# fecha o cursor
			cursor.close()
			self.reportProgress.emit(headers[i])

		results = dict(
			table_names = table_names,
			table_vars = table_vars,
			table_vars_columns =table_vars_columns,
			empresas = empresas,
			nomes = nomes,
			dates = dates_,
		)

		# emite os resultados através de um sinal
		self.resultReady.emit(results)