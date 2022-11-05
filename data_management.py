# Script contem as classes responsaveis pelo armazenamento de dados das estacoes
# e manipulacao/operacao dos valores guardados.

import copy
import warnings
import numpy as np
import utilitarios
from mysql.connector import connect, errorcode, Error

__all__ = ["inventario", "station", "dataset"]


class Entity():
   '''Classe responsável por representar cada estacao/entidade adicionada.
   Deve conter o nome, empreendimento, parametros e seus respectivos dados'''
   def __init__(self, valores : dict, index : np.array, tipo : str, dt, 
                nome : str = "", empresa : str = "") -> None:
      self.vars = list(valores.keys())
      self.nome = nome # nome da estacao
      self.empresa = empresa # Nome da empresa responsavel pela estacoa
      self.valores = valores # Valores referente a cada parametro
      # self.flags = flags # Flags referente a cada parametro
      self.tipo = tipo # Tipo de estacao
      self.dt = dt
      self.index = index # Todas as datas do conjunto de dados
      self.ini = np.min(self.index, axis = 0) # Data inicial
      self.fim = np.max(self.index, axis = 0) # Data final
      self.vars_selected = [0]*len(self.vars) # lista de 0 e 1

   def reindex(self, parameter, new_index):
      # Preparando valores
      values_arr = self.valores[parameter]
      new_arr = np.empty(new_index.shape)
      new_arr[:] = np.nan

      old_inside = np.extract(np.isin(self.index, new_index), values_arr)
      if old_inside.shape[0] > 0:
         indices = np.argwhere(np.isin(new_index, self.index))
         for i in range(indices.shape[0]):
            new_arr[indices[i]] = old_inside[i]

      return new_arr


class VarDataset():
   '''Classe responsavel por armazenar um objeto contendo dados de varias estacoes diferentes,
   referentes a um unico parametro, e realizar as operacoes apropriadas.'''

   def __init__(self, varnames, freq, valores : dict = {}, index : np.array = [], id = {}):
      # inciando propriedades
      self.valores = valores
      self.index = index
      self.shape = (0,0)
      self.validos = {}
      self.calculo = []
      self.agrupar = []
      self.parametros = varnames
      self.freq = freq # frequencia temporal dos dados
      self.ID = id # entra com o nome e recebe o id

      # Operacoes
      self.update_shape()
      self.updateValidos()

   def updateValidos(self, validos = {}):
      if len(validos) == 0:
         # Inicialmente, todos registros sao validos, pois nenhuma operacao foi feita.
         self.validos = {k:np.full(self.shape[0], 100) for k in self.valores.keys()}
      else:
         self.validos = validos

      return None

   def mask_invalidos(self, lim):
      new = {}
      for k, v in self.validos.items():
         new[k] = np.where(v >= lim, self.valores[k], np.nan)

      return new

   def update_shape(self):
      self.shape = (len(self.index), len(self.valores))

   def add(self, name, values):
      self.valores[name] = values
      self.shape = (self.shape[0], len(self.valores))
   
   def update_index(self, index):
      self.index = index
      try:
         N = len(index) if isinstance(index, list) else index.shape[0]
         self.shape = (N, self.shape[1])
         freq = self.index[1] - self.index[0]
         if freq > np.timedelta64(364, 'D'):
            freq = np.timedelta64(1, "Y")
            
         elif freq > np.timedelta64(27, 'D'):
            freq = np.timedelta64(1, "M")

         self.freq = freq

      except:
         self.freq = None
         self.shape = (1, self.shape[1])
   
      return None

   def get_columns(self):
      return list(self.valores.keys())
   
   def copy(self):
      return copy.deepcopy(self)

   def clear(self):
      self.valores.clear()
      self.index = [0]
      self.update_shape()

   def groupby(self, criterio):
      ''' agrupa os elementos de um array de acordo com o criterio especificado.
      util para tarefas que consistem em (1) agrupar e (2) realizar alguma operacao
      
      Como essa funcao funciona como um tipo de reducao, o atributo "index" vai mudar.
      '''
      N = len(criterio) if isinstance(criterio, list) else criterio.shape[0]
      indices = np.unique(criterio, return_index =  True)[1]
      split_idx = np.append(indices, N)[1:]
      self.valores = {k:np.split(v, split_idx)[:-1] for k, v in self.valores.items()}
      self.update_index(np.take(criterio, indices))

   def apply(self, func, map_ = False, kwargs = {}):
      ''' apica uma funcao para os dados de todas as estacoes presentes aqui
      modifica o atributo "index" caso haja uma reducao na qtd de dados.'''
      new_ds = self.copy()
      if map_:
         # Nenhuma reducao
         with warnings.catch_warnings():
            warnings.simplefilter("ignore", category=RuntimeWarning)
            new_ds.valores = {k:np.fromiter(map(func, v, **kwargs), dtype = "float") for k,v in self.valores.items()}
      else:
         for k, v in self.valores.items():
            results = func(v, **kwargs)
            if isinstance(results, tuple):
               new_ds.valores[k] = results[0]
               new_ds.validos[k] = results[1]
            else:
               new_ds.valores[k] = results
               new_ds.validos[k] = np.count_nonzero(~np.isnan(v))/v.shape[0]*100
   
      return new_ds

   def is_empty(self, values):
      '''
      Retorna True se as series de dados de todas as estacoes são compostas
      unicamente por valores NaN, ou seja, estão vazias.
      '''
      result = 0
      for k, v in values.items():
         result += np.count_nonzero(~np.isnan(v))

      return True if result == 0 else False


class EntitySQL(Entity):

   def __init__(self, nome, empresa, index, vars, filename, tipo, parent) -> None:
      super().__init__({}, index, tipo, nome, empresa)
      self.vars = vars
      self.filename = filename
      self.vars_selected = [0]*len(self.vars) # lista de 0 e 1
      self.inventario = parent

   def reindex(self, parameter, new_index):
      # Extraindo os valores do banco de dados
      cursor = self.inventario.cnx.cursor()
      vars_, campos = self.inventario.table_vars[self.nome]
      idx = vars_.index(parameter)
      start = new_index[0].item()
      end = new_index[-1].item()

      # executa a soliitacao
      query_test = (f"SELECT Campo1 "
               f"FROM `{self.filename}` "
               "WHERE Campo1 BETWEEN %s AND %s")
      cursor.execute(query_test, (start, end))
      cursor.fetchall()


      # organiza os dados
      N = cursor.rowcount
      query = (f"SELECT Campo1, Campo{campos[idx]}, Campo{campos[idx] + 1} "
            f"FROM `{self.filename}` "
            "WHERE Campo1 BETWEEN %s AND %s")
      cursor.execute(query, (start, end))
      dates = [''] * N
      values_arr = np.full(N, np.nan)
      i = 0
      for (date, value, flag) in cursor:
         dates[i] = date
         if flag is None or len(flag) == 0 or flag[0] != "I":
            if not value is None:
               values_arr[i] = value
         i += 1
      
      dates = np.array(dates, dtype = np.datetime64)

      # Preparando valores
      new_arr = np.full(new_index.shape, np.nan)
      old_inside = np.extract(np.isin(dates, new_index), values_arr)
      if old_inside.shape[0] > 0:
         indices = np.argwhere(np.isin(new_index, dates))
         for i in range(indices.shape[0]):
            new_arr[indices[i]] = old_inside[i]

      cursor.close()
      return new_arr


class Inventario():
   '''Classe responsavel por criar um inventario do banco de dados de estacoes
   de qualidade do ar e meteorologia, dado uma fonte de dados.
   
   Bando de dados utilizado -> MySQL'''

   def __init__(self, parent) -> None:
      self.parent = parent
      self.host = 'PC-INV109399'
      self.cnx = None
      self.connected = False      
      self.estacao_empresas = [] # empresa estacao
      self.estacao_nomes = [] # nome estacao
      self.table_names = [] # table_name no sql
      self.table_vars = {} # key = nome estacao, value = [variaveis presentes, campoN]
   
   def get_status(self):
      return self.connected

   def connect(self, username, password):
      self.disconnect()
      code = 1
      try:
         self.cnx = connect(
            user = username,
            password = password,
            host = self.host,
            database = 'banco_gear'
         )
         self.connected = True
         self.atualizar_inventario()

      except Error as err:
         code = err.errno

      return code

   def disconnect(self):
      if not self.cnx is None:
         self.cnx.close()

      # reseta tudo
      self.estacao_empresas = [] # empresa estacao
      self.estacao_nomes = [] # nome estacao
      self.table_names = [] # table_name no sql
      self.table_vars = {}
      self.connected = False
      return None

   def atualizar_inventario(self):
      if not self.connected:
         return None

      cursor = self.cnx.cursor()

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
      #     linha 4 -> string das variaveis
      #     linha 6 -> string de unidades ou flags
      nomes = [''] * N
      empresas = [''] * N
      table_names = [''] * N

      for i in range(len(headers)):
         cursor = self.cnx.cursor()

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
         
         self.table_vars[nomes[i]] = [variaveis, campos]

         # verifica se ha outra linha a ser lida e fecha o cursor
         while True:
            try:
               cursor.close()
               break
            except:
               cursor.fetchone()

      self.table_names = table_names
      self.estacao_empresas = empresas
      self.estacao_nomes = nomes
      return None

   def extrair_estacao(self, nome : str) -> EntitySQL:
      cursor = self.cnx.cursor()
      idx = self.estacao_nomes.index(nome)

      # data inicial
      query = (f"SELECT Campo1 FROM `{self.table_names[idx]}` "
               "ORDER BY Campo1 DESC LIMIT 1")
      cursor.execute(query)
      fim = cursor.fetchone()[0]

      # data final
      query = (f"SELECT Campo1 FROM `{self.table_names[idx]}` "
               "ORDER BY Campo1 LIMIT 2")
      cursor.execute(query)
      ini = cursor.fetchone()[0]
      segundo = cursor.fetchone()[0]

      # array de data
      dates = np.array([ini, segundo, fim], dtype = np.datetime64)

      # estimando o tipo de estacao
      dt_horas = utilitarios.dt_guess(dates).astype('timedelta64[h]')
      tipo_estacao = "AUTO"
      if dt_horas != 1:
         tipo_estacao = "SEMI"

      # criando o objeto estacao
      objeto = EntitySQL(
         vars = self.table_vars[nome][0],
         index = dates,
         dt = dt_horas, 
         tipo = tipo_estacao,
         nome = self.estacao_nomes[idx],
         empresa = self.estacao_empresas[idx],
         filename = self.table_names[idx],
         parent = self
         )
      
      # Fim
      cursor.close()
      return objeto
