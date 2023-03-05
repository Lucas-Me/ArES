# //////////////////////////////////////////////////////////////////////
#
#               CONFIGURAÇÕES DE PROPRIEDADES DO PROGRAMA.
# 
# ESSA VARIÁVEIS SÃO MODIFICADAS DE ACORDO COM A PREFERENCIA DO USUÁRIO
# E UTILIZADAS EM PROCEDIMENTOS ESPECÍFICO DO SOFTWARE.
# 
# 
# //////////////////////////////////////////////////////////////////////

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
    version = '1.3.0'
)