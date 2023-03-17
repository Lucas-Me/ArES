# IMPORT MODULES
import numpy as np
import re
from copy import copy, deepcopy

# IMPORT CUSTOM FUNCTIONS
from backend.misc.functions import find_unit, get_alias, get_frequency

class StationData(object):
   '''
   Classe responsável por guardar as informações das estações de monitoramento 
   importadas de um arquivo .xls'''
   def __init__(self, *args, **kwargs)  -> None:

      # SETTING UP PROPERTIES
      self.dates = np.array([], dtype = 'datetime64')
      self.shape = (0, 0) # 2 dimensoes -> (dates, parameters)
      self.metadata = {'enterprise' : kwargs.get('enterprise', '')} # demais informacoes sobre a estacao
      self.availability = [] # periodo de dados disponivel

      self.set_name(kwargs.get('name', ''))

   def set_enterprise(self, name : str):
      self.metadata['enterprise'] = name

   def setup_frequency(self):
      # frequencia de amostragem em unidade de horas
      self.metadata['frequency'] = get_frequency(self.dates) // np.timedelta64(1, 'h')
      
      # deduz o tipo de estacao pela frequencia
      if self.metadata['frequency'] == 1:
         self.metadata['type'] = "Automática"
      else:
         self.metadata['type'] = "Semiautomática"

   def set_name(self, name : str):
      upper_name = name.upper()
      if "AUTO" in upper_name or "SEMI" in upper_name:
         idx = name.find('-')
         name = name[idx + 1:].lstrip()
      
      self.metadata['name'] = name

   def setup_availability(self):
      self.availability = [self.dates.min(), self.dates.max()]


class XlsStationData(StationData):

   def __init__(self, *args, **kwargs):
      super().__init__(*args, **kwargs)

      # Properties
      self.parameters = {} # dicionario cuja chave é uma tupla (array devalor, array de flag)
      self.parameter_theme = {}
      self.dates = kwargs.get('dates') # array com a data correspondente a cada valor / flag
      self.metadata['source']  = 'xls' # de onde foi importado
      self.metadata['signature'] = 'xls-' + self.metadata['name']

      # Setting up 
      self.setup_frequency()
      self.setup_availability()

   def add_parameter(self, name : str, parameter : tuple[np.array, np.array], theme : str):
      if parameter[0].shape[0] == self.dates.shape[0]:
         self.parameters[name] = parameter
         self.parameter_theme[name] = theme

      self.shape = (self.dates.shape[0], len(self.parameters)) # atualizando shape


class SQlStationData(StationData):

   def __init__(self, *args, **kwargs):
      super().__init__(*args, **kwargs)

      # Properties
      self.dates = kwargs.get('dates')
      self.metadata['source'] = 'sql'
      self.metadata['signature'] = 'sql-' + self.metadata['name']
      self.parameters_cols = kwargs.get('parameters_cols')
      self.parameters = kwargs.get('parameters')
      #
      self.parameter_theme = {}

      # setting uo
      self.setup_frequency()
      self.setup_availability()
      self.setup_theme(['ppm', 'ppb', 'µg/m3', 'µg/m³'])

   def setup_theme(self, qar_units):
      themes = {}
      for var in self.parameters:
         unit = find_unit(var)
         theme = 'Meteorologia'
         if unit in qar_units:
            theme = 'Qualidade do Ar'

         themes[var] = theme

      self.parameter_theme = themes.copy()


class AbstractData(object):

   def __init__(self, *args, **kwargs):
      # INFO PROPERTIES
      self.metadata = kwargs.get('metadata', {}) # holds info about parameter name, station, enterprise etc.

      # VALUES 
      self.setValues(kwargs.get('values', []))
      self.setDates(kwargs.get('dates', []))

      # SETTINGS
      self.setupAlias()

   def setupAlias(self):
      '''
      Retorna um alias para este objeto, composto por:
      [nome estacao] - [var alias]
      '''
      varname = self.metadata['parameter']
      var_alias = get_alias(varname)

      self.metadata['alias'] = f"{self.metadata['name']} - {var_alias}"
      self.metadata['signature'] = f"{self.metadata['signature'][:3]} - {self.metadata['alias']}" 

   def setValues(self, values):
      values = np.array(values, dtype=float)

      self.values = values

   def getValues(self):
      return self.values

   def setDates(self, dates):
      dates = np.array(dates, dtype = np.datetime64)

      self.dates = dates

   def getDates(self):
      return self.dates
   
   def copy(self):
      return deepcopy(self)

class RawData(AbstractData):

   def __init__(self, *args, **kwargs):
      super().__init__(*args, **kwargs)

      # FLAGS FOR EACH DATE
      self.setFlags(kwargs.get('flags', []))
   
   def filterByFlags(self, flags_regex):
      r = re.compile(flags_regex)
      vmatch = np.vectorize(lambda x:bool(r.match(x)))
      matchs = vmatch(self.flags) # array of booleans, True if condition was met
      #
      filtered_values = np.where(matchs, self.values, np.nan)
      #
      return ModifiedData(
         metadata = self.metadata.copy(),
         values = filtered_values,
         dates = self.dates
      )

   def setFlags(self, flags : np.ndarray):
      '''Handle flags'''

      # setup flags
      self.flags = flags

   def getFlags(self):
      return self.flags
   
class ModifiedData(AbstractData):

   def __init__(self, *args, **kwargs):
      super().__init__(*args, **kwargs)

      # Array de representatividada para cada data, em float (% = float * 100)
      self.representatividade = kwargs.get('representatividade', np.where(np.isnan(self.values), np.nan, 1))

   def maskByThreshold(self, threshold):
      '''
      Mascara os dados de acordo com a representatividade e retorna somente o array de valores
      '''
      values = np.where(self.representatividade < threshold, np.nan, self.values) # nao é uma referencia
      return values

   def apply(self, **kwargs):
      '''
      Apply a function over the whole dataset.
      '''
      new = self.copy()
      if kwargs.pop('groupby', False): # group if True
         new = new.groupby(kwargs.pop('format_'), kwargs.pop('anual', False))
         new.setMetadata(self.metadata)
         return new.apply(**kwargs) # func is still in here

      # From now on, apply the function.
      func = kwargs.pop('func')

      # the ramining items on the dict "kwargs" are arguments for the function "func"
      values, representatividade = func(new.values, **kwargs)

      # setting results to new object and returning it
      new.setValues(values)
      new.setRepresentatividade(representatividade)

      return new

   def groupby(self, format_ : str = "%Y-%m-%d", anual =  False):
      '''
      Agrupa os dados e retorna um novo tipo de objeto.
      -  format - > é o criterio de formatacao dos indices (datas), espera-se que apos a formatacao o array resultante tenham elementos repetidos
      '''
      
      # formatting index (dates)
      formatted_dates = [self.dates[i].item().strftime(format_) for i in range(self.dates.shape[0])]
      formatted_dates = np.array(formatted_dates, dtype ='datetime64')
      grouped = GroupedData(
         values = self.values,
         criteria = formatted_dates,
         original_dates = self.dates,
         anual = anual
      )

      return grouped

   def setRepresentatividade(self, representatividade):
      if not isinstance(representatividade, np.ndarray):
         representatividade = np.array(representatividade)
      
      self.representatividade = representatividade

   def getRepresentatividade(self):
      return self.representatividade

   def setup_frequency(self):
      dt = np.roll(self.dates, 1) - self.dates
      unique, counts = np.unique(dt, return_counts=True)
      freq = np.asarray((unique, counts)).T
      ii = np.where(freq[:, 1] == np.nanmax(freq[:, 1]))[0][0]
      
      # frequencia de amostragem
      self.metadata['frequency'] = np.abs(freq[ii, 0])
      

class GroupedData(object):

      def __init__(self, *args, **kwargs):

         # SETTING UP
         self.setupGroups(**kwargs)

      def setupGroups(self, **kwargs):
         # It jsut works because the criteria array is sorted (ascending)

         values = kwargs.pop('values')
         criteria = kwargs.pop('criteria')
         
         # Creating groups
         dates, index = np.unique(criteria, return_index =  True)
         index = np.append(index, criteria.shape[0])[1:]

         # grouping values
         self.grouped_values = np.split(values, index)[:-1] # last group is empty
         self.unique_dates = dates
         self.anual = kwargs.pop('anual', False)
         if self.anual:
            self.grouped_dates = np.split(kwargs.pop('original_dates'), index)[:-1] # last group is empty

      def setMetadata(self, metadata):
         self.metadata = metadata

      def apply(self, **kwargs):
         # From now on, apply the function.
         func = kwargs.pop('func')

         # the ramining items on the dict "kwargs" are arguments for the function "func"
         values = np.fromiter(map(func, self.grouped_values), dtype = float)
         # representatividade = np.fromiter(map(self.calculateRepresentatividade, self.grouped_values), dtype = float)

         if not self.anual:
            representatividade = np.fromiter(map(self.calculateRepresentatividade, self.grouped_values), dtype = float)
         else:
            representatividade = np.fromiter(map(self.calculateRepresentatividadeAnual, self.grouped_values, self.grouped_dates), dtype = float)

         return ModifiedData(
            values = values,
            dates = self.unique_dates,
            representatividade = representatividade,
            metadata = self.metadata
         )

      def calculateRepresentatividade(self, array):
         return np.count_nonzero(~np.isnan(array)) / array.shape[0]
      
      def calculateRepresentatividadeAnual(self, array : np.ndarray, dates : np.ndarray):
         '''
         Apenas para estações automáticas. Calcula o quantitativo de dados válidos
         segundo o critério estabelecido pela GEAR, ou seja, agrupando cada ano em quadrimestres.
         A representatividade final é o menor quantitativo de dados válidos dos três quadrimestres.
         Ex:
            Jan a Abril: 55% ; Maio a Agosto: 60%; Setembro a Dezembro: 90%;
            No caso acima será eleito o menor percentual como representativo do ano inteiro (55%). 
         '''
         criterio = [(dates[i].item().month - 1) // 4 for i in range(dates.shape[0])]
         index = np.unique(criterio, return_index =  True)[1]
         index = np.append(index, len(criterio))[1:]

         # separa e calcula para cada quadrimestre
         valores = np.split(array, index)[:-1]
         resultados = np.fromiter(map(self.calculateRepresentatividade, valores), dtype = float)

         return np.min(resultados)