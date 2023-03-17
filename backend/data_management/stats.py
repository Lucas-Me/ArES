import numpy as np
import warnings


def media_geometrica(array):
    '''realiza uma media geometrica dada uma serie de dados.
    metodo utilizado a partir da media logaritimica (evita erros de 
    overflow ou underflow de numeros no algoritmo).
    A serie pode conter NaN.'''

    with warnings.catch_warnings():
        warnings.simplefilter("ignore", category=RuntimeWarning)
        array[array <= 0] = np.nan # se houver zeros ou valores negativos, ignora
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

    validos = validos / mean_interval.shape[0]
    return results, validos


def media(array):
    '''realiza uma media aritmetica dada uma serie de dados.
    A serie pode conter NaN.'''
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", category=RuntimeWarning)
        result = np.nanmean(array)

    return result

def maxima(array):
    '''Extrai o valor máximo dada uma serie de dados.
    A serie pode conter NaN.'''
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", category=RuntimeWarning)
        result = np.nanmax(array)

    return result