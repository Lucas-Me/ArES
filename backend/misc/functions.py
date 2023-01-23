# SCRIPT COM FUNCOES UTEIS PARA O PROGRAMA
# NAO SAO USADAS APENAS PARA UMA FUNCAO EM ESPECIFICO

# IMPORT MODULES
import os


def get_imagepath(icon_name, folder):
		app_path = os.path.abspath(os.getcwd())
		icons_folder = os.path.join(app_path, folder)

		return os.path.join(icons_folder, icon_name).replace('\\', '/')

def find_unit(parameter_name):
	'''
	Extrai a unidade a partir do nome completo do parametro.
	'''
	reverse = {'}' : '{', ']' : '[', ')' : '('}
	#
	last_char = parameter_name[-1]
	rchar = reverse[last_char]
	start = parameter_name.rfind(rchar)

	return parameter_name[start + 1:-1]