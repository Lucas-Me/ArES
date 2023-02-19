# IMPORT QT CORE
from qt_core import *

# IMPORT CUSTOM UI
from gui.ui_widgets.ui_dashboard import UI_Dashboard

# Data Manager Page Class
class Dashboard(QWidget):

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		# PROPERTIES
		self.right_menu_width = 200

		# setting UI
		self.ui = UI_Dashboard()
		self.ui.setup_ui(self)
		
		# SIGNALS AND SLOTS
		self.ui.toggle_menu.clicked.connect(self.toggle_menu)

	def toggle_menu(self):
		# objetic animation
		animation = QVariantAnimation(self)

		# check
		w = self.ui.right_menu.width()
		new_width = 0
		if w == 0:
			new_width = self.right_menu_width
			self.ui.right_menu.show()

		else:
			animation.finished.connect(self.ui.right_menu.hide)
			
		# setting up
		animation.setDuration(300)
		animation.setStartValue(w)
		animation.setEndValue(new_width)
		animation.valueChanged.connect(self.ui.right_menu.setFixedWidth)

		# start animation
		animation.start(QVariantAnimation.DeleteWhenStopped)


	def paintEvent(self, event: QPaintEvent) -> None:
		'''
		Reinicia o painter deste QWidget, para que ele nao herde as propriedades do
		parent.
		'''
		# super().paintEvent(event)

		opt = QStyleOption()
		opt.initFrom(self)
		p = QPainter(self)
		self.style().drawPrimitive(QStyle.PE_Widget, opt, p, self)