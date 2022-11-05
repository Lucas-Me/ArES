# Esse script realiza as operacoes conforme selecionado pelo usuario no "front-end" do programa
# Operacoes focadas na organização, exportação e importação de dados

import re
import os
import xlrd
import stats
import xlsxwriter
import numpy as np
import matplotlib.dates as mdates
from datetime import datetime, timedelta, date
from data_management import VarDataset, Entity

# Funcoes neste script
__all__ = ["get_dateindex", 'xls2file', "organize",
"save_excel", "rotina_operacoes"]

# ================================== GLOBAIS ========================== #
VARIAVEIS = [
   'Precipitação Pluviométrica', 
   'Velocidade do Vento',
   'Direção do Vento',
   'Temperatura',
   'Radiação Solar',
   'Umidade Relativa',
   'Pressão Atmosférica',
   'Partículas Totais em Suspensão',
   'Partículas Inaláveis (<2,5µm)',
   'Partículas Inaláveis <2,5µm)',
   'Partículas Inaláveis (<2,5µm',
   'Partículas Inaláveis (<10µm)',
   'Partículas Inaláveis (<10µm',
   'Partículas Inaláveis <10µm)',
   'Monóxido de Nitrogênio',
   'Dióxido de Nitrogênio',
   'Óxidos de Nitrogênio',
   'Ozônio',
   'Dióxido de Enxofre', 
   'Monóxido de Carbono',
   'Hidrocarbonetos Totais',
   'Metano',
   'Hidrocarbonetos Não-Metano',
]
VAR_ALIAS = [
   'Precipitação',
   'Vel. Vento',
   'Dir. Vento',
   'Temp',
   'Rad. Solar',
   'UR',
   'Pressao Atm.',
   'PTS',
   'MP2,5',
   'MP2,5',
   'MP2,5',
   'MP10',
   'MP10',
   'MP10',
   'NO',
   'NO2',
   'NOX',
   'O3',
   'SO2',
   'CO',
   'HCT',
   'CH4',
   'HCTnM'
]

# ================================== Funcoes ========================== #


def get_alias(varname : str) -> str:
   '''
   Recebe uma string com o nome de uma variavel e retorna uma outra string com
   a sua abreviação, omitindo a unidade.
   Ex: Hidrocarbonetos Totais (ppb) -> HCT
   '''
   # usando as variaveis globais
   global VARIAVEIS
   global VAR_ALIAS

   # a string é composta pelo nome da variavel e por fim sua unidade.
   words = re.compile('\s+').split(varname)
   varname = ' '.join(words[:-1])
   try:
      alias = VAR_ALIAS[VARIAVEIS.index(str(varname))]
   except:
      alias = varname
   
   return alias


def get_dateindex(tipo, freq:np.timedelta64, start_date:datetime, end_date:datetime, minutos = 0) -> np.array:
   ''' Retorna um array de objetos datetime com o dias/horarios esperados para os registros
   de dados de uma estacao de monitoramento, dado o seu tipo e periodo especificado.
   Frequencia de operacao:
      Automatica (auto) = dados horarios
      Semi-automatica (semi) = dados diarios (6 em 6 dias)
    
   args:
      - tipo: tipo de estacao, para conhecimento da frequencia;
      - start_date: data inicial a ser considerada
      - end_date: data final a ser considerado;
      - parameter: parametro a ser processado em cada estacao.'''

   if isinstance(start_date, date):
      start_date = np.datetime64(start_date)
      end_date = np.datetime64(end_date)
      
   if tipo == "AUTO" or (tipo == "SEMI" and freq != np.timedelta64(6, "D")):
      minutes = np.timedelta64(minutos, "m") # extrai o valor "minutos" no dataset original
      index = np.arange(start_date + minutes, end_date + minutes, freq, dtype =  "datetime64")

   else:
      ref = np.datetime64('2017-01-06') # data que se tem certeza de que tem uma amostragem semi-automatica. Modificar dps.
      index = np.arange(start_date, end_date, np.timedelta64(1, "D"), dtype = "datetime64")
      diff = (index - ref) % freq
      index = index[np.equal(diff.astype('float'), 0)]

   return index


def get_id(string, tipo):
   '''
   Gera uma ID unica para uma estacao e variavel especifica.
   Baseada no municipio, nome da estacao e nome do parametro
   '''
   separa = string.split('-')
   for i in range(len(separa)):
      separa[i] = separa[i].strip()

   Municipio = separa[0]
   Nome = re.compile('\s+').split(separa[1])
   Siglas_nome = ''.join([Nome[i][:3] for i in range(len(Nome))])
   Parametro = separa[-1]
   ID = tipo[0] + Municipio + Parametro + Siglas_nome

   return ID

def organize(parent, start_date:datetime, end_date:datetime, tipo):
   '''
   Reune a serie temporal dos parametros selecionados e referentes a cada estacao
   em um unico objeto (colecao), de forma limpa e organizada.
   Se nenhuma operacao sera feita, apenas use os valores com a frequencia
   padrao dos dados. Estacoes automaticas e semi-automaticas nao podem 
   ser incluidas juntas porque possuem frequencias de operação diferentes.
   
   args:
      - files: lista com os arquivos a serem utilizados (1 por estacao)
      - start_date: data inicial a ser considerado;
      - end_date: data final a ser considerado;

   returns:
      - um unico dataframe contendo a data/hora como linha, nome da estacao
      como coluna e seus valores sao as concentracoes de um dado parametro.
   '''
   # frequencia da serie temporal
   freq = np.timedelta64(1, 'h')
   if not parent.arquivos[0].tipo == "AUTO":
      freq = np.timedelta64(6, "D")

   # preparar dados
   n = len(parent.arquivos)
   minutos = parent.arquivos[0].index[0].item().minute
   new_index = get_dateindex(
      tipo,
      freq, 
      start_date,
      end_date + timedelta(days = 1),
      minutos = minutos
      )
   collection = {}
   parameters = {}
   id_ = {}
   for i in range(n):
      entity = parent.arquivos[i]
      name = entity.nome
      for j in range(len(entity.vars)):
         if entity.vars_selected[j]:
            name_ = name + " - " + get_alias(entity.vars[j])
            collection[name_] = entity.reindex(entity.vars[j], new_index)
            parameters[name_] = entity.vars[j]
            id_[name_] = get_id(name_, parent.arquivos[0].tipo)

   # provoca um erro se nenhum parametro for selecionado
   if len(parameters) == 0:
      raise ValueError

   return VarDataset(parameters, freq.astype('timedelta64[h]'), valores = collection, index = new_index, id = id_)


def xls2file(file_path:str) -> Entity:
   '''Abre o arquivo excel extraido do ATMOS e coleta os dados da estação de monitoramento
   de qualidade do ar. a planilha deve conter informacao de apenas uma estacao, nao de varias.
   
   args:
      - file_path: caminho no computador ate o arquivo.
   
   returns:
      - DataFrame cujas linhas sao a data/hora e coluna sao os parametros. Os valores
      do DataFrame correspondem as concentracoes em uma dada hora de um dado poluente.
   '''
   # abre o arquivo
   xls = xlrd.open_workbook(file_path, logfile=open(os.devnull, 'w'))
   sh = xls.sheet_by_index(0)

   # Informacoes da estacao
   empresa = sh.cell_value(0, 1)
   estacao = sh.cell_value(1, 1)
   nome_estacao = " ".join(estacao.split(" ")[2:])

   # codigo abaixo (1) procura a linha onde o cabecalho "DATA" esta escrito e (2) Identifica os parametros e unidades existentes
   data_index = 0
   for i in range(sh.nrows):
      if sh.cell_value(i, 0) == "Data":
         data_index = i + 1
         break

   #  (2) Identifica os parametros e unidades existentes
   parametros_cols = [] # lista com o indice da coluna de cada parametro
   unidades = [] # lista com numero de unidades por parametro. Ex: um unico parametro pode estar em ppm e microgramas.
   first = True
   for col in range(1, sh.ncols, 2): # Parte do principio que a unidade esta em colunas impares, primeira coluna sera sempre da data.
      value = sh.cell_value(data_index - 4, col)
      if len(value) > 0:
         parametros_cols.append(col)
         if first:
            first = False
            continue
         else:
            unidades.append((col - parametros_cols[-2])//2)

   unidades.append((sh.ncols - parametros_cols[-1])//2) # Compensar para o ultimo parametro.
   variaveis = []
   for i, col in enumerate(parametros_cols):
      basename = sh.cell_value(data_index - 4, col)
      for j in range(unidades[i]):
         # extrai somente a unidade da string: 'Valor [µg/m3]'
         surname = sh.cell_value(data_index - 1, col + j*2).split(" ")[1]
         surname = surname.replace("[", "(").replace("]", ")")
         variaveis.append(basename + " " + surname)
   
   # extraindo os dados, i.e, valores, flags e datas
   valores = {}
   #flags = {}
   dates = np.array([xlrd.xldate_as_datetime(sh.cell_value(row, 0), 0) for row in range(data_index, sh.nrows)], dtype='datetime64')
   for i in range(len(variaveis)):
      # cada variavel contem duas colunas, a primeira: o valor, a segunda: a flag correspondente.
      var_col = 2*i + 1
      var_values = [0]*(sh.nrows - data_index)
      #var_flags = [0]*(sh.nrows - data_index)
      for row in range(data_index, sh.nrows):
         #var_flags[row - data_index] = sh.cell_value(row, var_col + 1)
         cell_value = sh.cell_value(row, var_col)
         if isinstance(cell_value, str):
            cell_value = np.nan
         var_values[row - data_index] = cell_value

      valores[variaveis[i]] = var_values

   # Deduzindo a frequencia dos dados
   horas = dt_guess(dates).astype('timedelta64[h]')
   if horas == 1:
      tipo_estacao = 'AUTO'
   else:
      tipo_estacao = 'SEMI'

   # criando o objeto estacao
   print(nome_estacao, empresa)
   objeto = Entity(
      valores = valores,
      index = dates,
      tipo = tipo_estacao.upper(),
      dt = horas, 
      nome = nome_estacao,
      empresa = empresa
      )

   # Fim
   return objeto

def dt_guess(dates, return_time = True):
   '''
   Adivinha a frequencia dos dados atraves dos seus indices
   '''
   if not return_time:
      dates = mdates.date2num(dates)

   dt = np.roll(dates, 1) - dates
   unique, counts = np.unique(dt, return_counts=True)
   freq = np.asarray((unique, counts)).T
   ii = np.where(freq[:, 1] == np.nanmax(freq[:, 1]))[0][0]
   result = np.abs(freq[ii, 0])

   return result

def save_excel(output : VarDataset, fname : str):
   workbook = xlsxwriter.Workbook(fname)
   worksheet = workbook.add_worksheet()

   # Formatações
   header_fmt = workbook.add_format(dict(bold = True, bg_color = "#9CFAD0", border = 2, align = "center", valign = "center"))
   dados_fmt = workbook.add_format(dict(num_format = "0.00", align = "center", border = 1))
   validacao_fmt = workbook.add_format(
      dict(
         num_format = "0.0%",
         bg_color = "#E5EDE9",
         align = "center",
         border = 1
      )
   )
   metodo = ["Dia", "Mês", "Ano"]
   cell_dateformat = ["dd/mm/yyyy", "mmm/yyyy", "yyyy"]
   cell_dateformat = dict(zip(metodo, cell_dateformat))
   if len(output.agrupar) > 0:
      ultima_operacao = output.agrupar[-1].split(" ")[0]
   else:
      ultima_operacao = " "
   date_fmt = workbook.add_format(
      dict(
         num_format = cell_dateformat.get(ultima_operacao, "dd/mm/yyyy hh:mm"),
         bg_color = "#B6D1C5",
         align = "center",
         border = 1
      )
   )

   ini = 4
   last_columnm = output.shape[1]*2
   worksheet.merge_range(ini - 3, 0, ini - 1, 0, "Datas", header_fmt)
   worksheet.merge_range(ini - 4, 0, ini - 4, last_columnm,
                        "Resultados dos procedimentos realizados", header_fmt)
   estacoes = output.get_columns()

   for col in range(output.shape[1]):
      worksheet.merge_range(ini - 3, 1 + col*2, ini - 3, 2 + col*2, estacoes[col], header_fmt)
      worksheet.merge_range(ini - 2, 1 + col*2, ini - 2, 2 + col*2, output.parametros[estacoes[col]], header_fmt)
      worksheet.write(ini - 1, 1 + col*2, "Valor", header_fmt)
      worksheet.write(ini - 1, 2 + col*2, "Válidos (%)", header_fmt)

   for row in range(output.shape[0]):
      worksheet.write_datetime(ini + row, 0, output.index[row].item(), date_fmt)
      for col in range(output.shape[1]):
         try:
            worksheet.write(ini + row, 1 + col*2, output.valores[estacoes[col]][row], dados_fmt)
         except:
            worksheet.write_formula(ini + row, 1 + col*2, "=NA()")

         worksheet.write(ini + row, 2 + col*2, output.validos[estacoes[col]][row]/100, validacao_fmt)
   
   worksheet.set_column(0, last_columnm, 10)

   # Colunas de procedimentos
   last_columnm
   worksheet.merge_range(0, last_columnm + 2, 0, last_columnm + 4, "Procedimentos realizados", header_fmt)
   worksheet.write(1, last_columnm + 2, "Ordem", header_fmt)
   worksheet.write(1, last_columnm + 3, "Cálculo", header_fmt)
   worksheet.write(1, last_columnm + 4, "Agrupado por", header_fmt)
   fmt = workbook.add_format(dict(bg_color = "#E5EDE9", align = "center", border = 1))
   for i in range(len(output.agrupar)):
      worksheet.write(2 + i, last_columnm + 2, i + 1, fmt)
      worksheet.write(2 + i, last_columnm + 3, output.calculo[i], fmt)
      worksheet.write(2 + i, last_columnm + 4, output.agrupar[i], fmt)
   worksheet.set_column(last_columnm + 2, last_columnm + 4, 10)
   workbook.close()

def rotina_operacoes(parent, tipo):
   ''' 
   Funcao responsavel pela tomada de decisoes
   
   OBS: ESSA COM CERTEZA NAO é A MELHOR ABORDAGEM
         estou aberto a sugestoes.
   '''
   # Preparativos
   # calculos, ou metodos a serem chamados, possivelmente.
   methods = [stats.media_movel, stats.media, stats.media_geometrica, stats.media_harmonica, np.nanmax]
   time_freq = ["Média móvel", "Diária", "Mensal", "Anual"]
   atributos = ["%Y-%m-%d", "%Y-%m-01", "%Y-01-01"]
   atributos_freq = [np.timedelta64(1, 'D'), np.timedelta64(1, 'm'), np.timedelta64(1, 'Y')]
   funcValidos = [stats.dadosValidosDiarios, stats.dadosValidosMensais, stats.dadosValidosAnuais]
   lim = 0
   user_operations = parent.user_operations

   # Realiza os calculos solicitado de acordo com a ordem em que forma inseridos
   # se nao ha solicitacao, o loop for nao sera executado, pois row_track = 0
   for row in range(user_operations.row_track):
      calc_idx = user_operations.cellWidget(row, 1).currentIndex()
      group_idx = user_operations.cellWidget(row, 2).currentIndex()
      
      calc_txt = user_operations.cellWidget(row, 1).currentText()
      group_txt = user_operations.cellWidget(row, 2).currentText()

      # Faz um registro no dataset da operacao que sera realizada.
      parent.ds.calculo.append(calc_txt)
      parent.ds.agrupar.append(group_txt)

      # Extrai somente os validos pro precaucao
      # açao importante caso haja necessidade de realizar + de 1 operacao
      parent.ds.valores = parent.ds.mask_invalidos(lim)
      lim = parent.representatividade[time_freq[group_idx]]

      func = methods[calc_idx]
      if calc_idx == 0:
         # media movel, nao agrupa mesmo se o usuario pedir
         args = dict(date_array = parent.ds.index, dt = np.timedelta64(8, "h"))
         parent.ds = parent.ds.apply(func, map_ = False, kwargs = args)
         continue

      # Outros calculos, agrupa se necessario
      if group_idx > 0:
         idx = group_idx - 1
         new_groups = [x.item().strftime(atributos[idx]) for x in parent.ds.index]
         new_groups = np.array(new_groups, dtype=np.datetime64)
         esperados = funcValidos[idx](parent.ds.index, tipo, parent.ds.freq)
         parent.ds.groupby(new_groups)
         parent.ds.updateValidos({k:stats.porcentagemValidos(v, esperados) for k,v in parent.ds.valores.items()})
         parent.ds = parent.ds.apply(func, map_ = True)
         parent.ds.freq = atributos_freq[idx]

      else:
         parent.ds = parent.ds.apply(func, map_ = False)
         parent.ds.update_index([0])
      

   return parent.ds