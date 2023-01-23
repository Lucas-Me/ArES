# IMPORT QT CORE
from qt_core import *

# IMPORT UI MODULES
from gui.ui_widgets.ui_parameter_item import UI_ParameterListItem

# Paramater Selection Widget Class
class ParameterListItem(QFrame):
    stateChanged = Signal(bool)

    def __init__(
        self,
        name : str,
        theme : str,
        unit : str,
        width : int,
        height : int,
        active : bool = False,
    ):
        super().__init__()

        # properties
        self.name = name
        self.theme = theme
        self.unit = unit
        self.item_width = width
        self.item_height = height

        # setup UI
        self.ui = UI_ParameterListItem()
        self.ui.setup_ui(self)
        self.ui.check_box.setChecked(active)
        self.set_color()

        #
        self.ui.check_box.clicked.connect(self.emit_signal)

    def set_color(self):
        style = self.styleSheet()
        if self.ui.check_box.isChecked():
            self.setStyleSheet(style + f'''
            #parameter_item {{
                background-color : #d0e6ea;
                border-bottom: 1px solid;
                border-color: #000000;
            }}''')
        else:
            self.setStyleSheet(style + f'''
            #parameter_item {{
                background-color : #ffffff;
                border-bottom: 1px solid;
                border-color: #000000;
            }}''')

    def emit_signal(self):
        self.set_color()
        self.stateChanged.emit(self.ui.check_box.isChecked())