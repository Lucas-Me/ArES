# Esse script realiza as operacoes estatisticas necessarias, de acordo com o que foi
# selecionado pelo usuario na interface.

import utilitarios
import numpy as np
import warnings
import datetime

# Funcoes/classes neste script
__all__ = ['medias_geometrica', 'media_harmonica', 'media_movel',"dadosValidosDiarios",
'dadosValidosMensais', 'dadosValidosAnuais', 'porcentagemValidos', 'media']

def dadosValidosDiarios(datas, tipo, freq):
    ini = np.min(datas)
    fim = np.max(datas)
    if isinstance(fim.item(), datetime.date):
        fim = np.datetime64(fim.item())
    else:
        fim = np.datetime64(fim.item().date())
  
    if tipo == "AUTO":
        # 24 dados registrados em um dia.
        index = np.arange(ini, fim, np.timedelta64(1, "D"))
        N_amostras = 24
    else:
        # Semiautomatica. 1 amostragem a cada 6 dias.
        index = datas
        N_amostras = 1

    esperados = np.full(index.shape[0], N_amostras)
    return esperados


def dadosValidosMensais(datas, tipo, freq):
    # datas esta em ordem crescente
    ini = np.min(datas, axis = 0)
    fim = np.max(datas, axis = 0)
    mes_final = fim.item().month
    ano_final = fim.item().year
    if int(mes_final) == 12:
        mes_final = '01'
        ano_final = int(ano_final) + 1
    else:
        mes_final = int(mes_final) + 1
        mes_final = "{}{}".format(mes_final //10, mes_final % 10)

    fim = np.datetime64("{}-{}-01 00:00".format(ano_final, mes_final))

    # Data/horas de amostragem esperada dentro do periodo, por mes.
    index = utilitarios.get_dateindex(tipo, freq, ini, fim)

    # Quantidade de amostragens esperadas por mes e ano.
    criterio = [x.item().strftime("%Y-%m-01") for x in index]
    criterio = np.array(criterio, dtype = np.datetime64)
    N = criterio.shape[0]
    indices = np.unique(criterio, return_index= True)[1]
    esperados = np.append(indices[1:], N) - indices
    return esperados


def dadosValidosAnuais(datas, tipo, freq):
    # datas esta em ordem crescente
    ini = np.datetime64("{}-01-01 00:00".format(np.min(datas).item().year))
    fim = np.datetime64("{}-01-01 00:00".format(np.max(datas).item().year + 1))
    
    # Data/horas de amostragem esperada dentro do periodo, por mes.
    index = utilitarios.get_dateindex(tipo, freq, ini, fim)

    # Quantidade de amostragens esperadas por mes e ano.
    criterio = [x.item().strftime("%Y-01-01") for x in index]
    criterio = np.array(criterio, dtype = np.datetime64)
    N = criterio.shape[0]
    indices = np.unique(criterio, return_index= True)[1]
    esperados = np.append(indices[1:], N) - indices
    
    # Qtd de dados validos na amostra.
    return esperados


def porcentagemValidos(array, esperados):
    def validos(arr):
        return np.count_nonzero(~np.isnan(arr))

    array_ = np.fromiter(map(validos, array), dtype = "float")
    return array_/esperados*100


def media_geometrica(array):
    '''realiza uma media geometrica dada uma serie de dados.
    metodo utilizado a partir da media logaritimica (evita erros de 
    overflow ou underflow de numeros no algoritmo).
    A serie pode conter NaN.'''

    with warnings.catch_warnings():
        warnings.simplefilter("ignore", category=RuntimeWarning)
        media_dos_logaritmos = np.nanmean(np.log(array), axis = 0)

    return np.exp(media_dos_logaritmos)

def media_harmonica(array):
    '''realiza uma media harmonica dada uma serie de dados.
    A serie pode conter NaN.'''
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", category=RuntimeWarning)
        soma = np.nansum(1/array, axis = 0)

    return array.shape[0]/soma


def media_movel(array, date_array, dt = np.timedelta64(8, "h")):
    # Calcula a média móvel, dado um intervalo de tempo (dt) para o calculo.
    # array -> array dos valores
    # date_array -> array de datas
    results = np.full(date_array.shape[0], np.nan)
    validos = np.full(date_array.shape[0], 0)
    last = 0
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", category=RuntimeWarning)
        for n in range(date_array.shape[0]):
            boolarr = date_array[last: n + 1] > (date_array[n] - dt)
            mean_interval = array[last: n + 1][boolarr]
            results[n] = np.nanmean(mean_interval)
            validos[n] = np.count_nonzero(~np.isnan(mean_interval))
            last = n - np.count_nonzero(boolarr) + 1

    validos = validos / mean_interval.shape[0] * 100
    return results, validos


def media(array):
    '''realiza uma media aritmetica dada uma serie de dados.
    A serie pode conter NaN.'''
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", category=RuntimeWarning)
        result = np.nanmean(array, axis = 0)

    return result