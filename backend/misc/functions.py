# SCRIPT COM FUNCOES UTEIS PARA O PROGRAMA
# NAO SAO USADAS APENAS PARA UMA FUNCAO EM ESPECIFICO

# IMPORT QT MODULES
from qt_core import *

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

def drawShadow(
	_painter : QPainter,
	_margin : int,
	_radius : float,
	_start : QColor,
	_end : QColor,
	_startPosition : float,
	_endPosition0: float,
	_endPosition1: float,
	_width : float,
	_height : float,
	):
	'''
	DESENHA UMA SOMBRA AO REDOR DE UMA JANELA.
	
	Adapatado de: https://forum.qt.io/topic/66913/draw-shadow-around-a-top-level-framless-qwidget-with-qlineargradient/7.
	'''

	_painter.setPen(Qt.NoPen)

	gradient = QLinearGradient()
	gradient.setColorAt(_startPosition, _start)
	gradient.setColorAt(_endPosition0, _end)

	# right
	right0 = QPointF(_width - _margin, _height / 2)
	right1 = QPointF(_width, _height / 2)
	gradient.setStart(right0)
	gradient.setFinalStop(right1)
	_painter.setBrush(QBrush(gradient))
	_painter.drawRoundedRect(QRectF(QPoint(_width - _margin*_radius, _margin), QPointF(_width, _height - _margin)), 0, 0)

	# left
	left0 = QPointF(_margin, _height / 2)
	left1 = QPointF(0, _height / 2)
	gradient.setStart(left0)
	gradient.setFinalStop(left1)
	_painter.setBrush(QBrush(gradient))
	_painter.drawRoundedRect(QRectF(QPoint(_margin *_radius, _margin), QPointF(0, _height - _margin)), 0, 0)

	# TOP
	top0 = QPointF(_width / 2, _margin)
	top1 = QPointF(_width / 2, 0)
	gradient.setStart(top0)
	gradient.setFinalStop(top1)
	_painter.setBrush(QBrush(gradient))
	_painter.drawRoundedRect(QRectF(QPointF(_width - _margin, 0), QPointF(_margin, _margin)), 0.0, 0.0)

	# BOTTOM
	bottom0 = QPointF(_width / 2, _height - _margin)
	bottom1 = QPointF(_width / 2, _height)
	gradient.setStart(bottom0)
	gradient.setFinalStop(bottom1)
	_painter.setBrush(QBrush(gradient))
	_painter.drawRoundedRect(QRectF(QPointF(_margin, _height - _margin), QPointF(_width - _margin, _height)), 0.0, 0.0)

	# BOTOM RIGHT
	bottomright0 = QPointF(_width - _margin, _height - _margin)
	bottomright1 = QPointF(_width, _height)
	gradient.setStart(bottomright0)
	gradient.setFinalStop(bottomright1)
	gradient.setColorAt(_endPosition1, _end)
	_painter.setBrush(QBrush(gradient))
	_painter.drawRoundedRect(QRectF(bottomright0, bottomright1), 0.0, 0.0)

	# BOTTOM LEFT
	bottomleft0 = QPointF(_margin, _height - _margin)
	bottomleft1 = QPointF(0, _height)
	gradient.setStart(bottomleft0)
	gradient.setFinalStop(bottomleft1)
	gradient.setColorAt(_endPosition1, _end)
	_painter.setBrush(QBrush(gradient))
	_painter.drawRoundedRect(QRectF(bottomleft0, bottomleft1), 0.0, 0.0)

	# TOP LEFT
	topleft0 = QPointF(_margin, _margin)
	topleft1 = QPointF(0, 0)
	gradient.setStart(topleft0)
	gradient.setFinalStop(topleft1)
	gradient.setColorAt(_endPosition1, _end)
	_painter.setBrush(QBrush(gradient))
	_painter.drawRoundedRect(QRectF(topleft0, topleft1), 0.0, 0.0)

	# TOP RIGHT
	topright0 = QPointF(_width - _margin, _margin)
	topright1 = QPointF(_width, 0)
	gradient.setStart(topright0)
	gradient.setFinalStop(topright1)
	gradient.setColorAt(_endPosition1, _end)
	_painter.setBrush(QBrush(gradient))
	_painter.drawRoundedRect(QRectF(topright0, topright1), 0.0, 0.0)

	# Widget
	_painter.setBrush(QBrush("#FFFFFF"));
	_painter.setRenderHint(QPainter.Antialiasing);
	_painter.drawRoundedRect(QRectF(QPointF(_margin, _margin), QPointF(_width - _margin, _height - _margin)), _radius, _radius)
