# IMPORT MODULES
import numpy as np


class StationData():
   '''
   Classe responsável por guardar as informações das estações de monitoramento 
   importadas de um arquivo .xls'''
   def __init__(self, *args, **kwargs)  -> None:

      # SETTING UP PROPERTIES
      self.parameters = {} # dicionario cuja chave é uma tupla (array devalor, array de flag)
      self.parameter_theme = {}
      self.dates = np.array([], dtype = 'datetime64')
      self.shape = (0, 0) # 2 dimensoes -> (dates, parameters)
      self.metadata = {'enterprise' : kwargs.get('enterprise', '')} # demais informacoes sobre a estacao

      self.set_name(kwargs.get('name', ''))

   def add_parameter(self, name : str, parameter : tuple[np.array, np.array], theme : str):
      if parameter[0].shape[0] == self.dates.shape[0]:
         self.parameters[name] = parameter
         self.parameter_theme[name] = theme

      self.shape = (self.dates.shape[0], len(self.parameters)) # atualizando shape

   def set_enterprise(self, name : str):
      self.metadata['enterprise'] = name

   def setup_frequency(self):
      dt = np.roll(self.dates, 1) - self.dates
      unique, counts = np.unique(dt, return_counts=True)
      freq = np.asarray((unique, counts)).T
      ii = np.where(freq[:, 1] == np.nanmax(freq[:, 1]))[0][0]
      
      # frequencia de amostragem de unidade de horas
      self.metadata['frequency'] = np.abs(freq[ii, 0]) // np.timedelta64(1, 'h')
      
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


class XlsStationData(StationData):

   def __init__(self, *args, **kwargs):
      super().__init__(*args, **kwargs)

      # Properties
      self.dates = kwargs.get('dates') # array com a data correspondente a cada valor / flag
      self.metadata['source']  = 'xls' # de onde foi importado
      self.metadata['signature'] = 'xls-' + self.metadata['name']

      # Setting up 
      self.setup_frequency()
