# SCRIPT COM FUNCOES UTEIS PARA O PROGRAMA
# NAO SAO USADAS APENAS PARA UMA FUNCAO EM ESPECIFICO

# IMPORT MODULES
import os


def get_icon(icon_name, folder):
		app_path = os.path.abspath(os.getcwd())
		icons_folder = os.path.join(app_path, folder)

		return os.path.join(icons_folder, icon_name).replace('\\', '/')