# //////////////////////////////////////////////////////////////////////
#
#               CONFIGURAÇÕES DE PROPRIEDADES DO PROGRAMA.
# 
# ESSA VARIÁVEIS SÃO MODIFICADAS DE ACORDO COM A PREFERENCIA DO USUÁRIO
# E UTILIZADAS EM PROCEDIMENTOS ESPECÍFICO DO SOFTWARE.
# 
# 
# //////////////////////////////////////////////////////////////////////

import os, json

SETTINGS = dict(
    conexao = { # servidor hospedando o banco de dados MySQL
        'servidor' : "BP-J6XCZT3-INEA",
        'database' : 'banco_gear'
    },
    representatividade = { # porcentagem mínima de dados válidos exigidos
        'Horária' : .75,
        'Data' : .75, 
        'Mês e ano' : .75,
        'Ano' : .50
    },
    semiautomatica = { # amostragem da rede semiautomatica
        'data_referencia' : '2017-01-06',
        'frequencia' : 6
    },
    figura = { # Propriedades da figura
        'left' : .1,
        'right' : .9,
        'bottom' : .1,
        'top' : .9,
        'font_family': 'Calibri',
        'font_size' : 15,
        'dpi' : 200
    },
    filtrar =  True, # Ocultar resultados por quantitativo de dados válidos, na figura.
    perfis = {}, # Perfis do usuário
    cores = [['#ffffff']*6 for i in range(2)], # cores personalizadas salvas (legenda)
    version = '1.3.1'
)

# IMPORTAR E ATUALIZAR AS CONFIGURACOES, SE JA EXISTIR.

userhome_directory = os.path.expanduser("~")
ArES_dir = os.path.join(userhome_directory, '.ArES')
fname = os.path.join(ArES_dir, 'config.json')
try:
    # Se o diretorio nao existir, cria ele
    os.makedirs(ArES_dir, exist_ok=True)

    # se o arquivo JSON com as configuracoes existir, provoca um erro
    exists = os.path.isfile(fname)
    if not exists:
        with open(fname, 'w', encoding='utf-8') as f:
            json.dump(SETTINGS, f, ensure_ascii=False, indent=4)

    else:
        raise FileExistsError

except FileExistsError:
    # se o diretorio e o arquivo existirem, importa ele no programa
    with open(fname, 'r', encoding='utf-8') as f:
        existing_data = json.load(f)
    
    version = SETTINGS['version']
    SETTINGS.update(existing_data)
    SETTINGS['version'] = version