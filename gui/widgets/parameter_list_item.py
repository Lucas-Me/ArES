# IMPORT QT CORE
from qt_core import *

# IMPORT UI MODULES
from gui.ui_widgets.ui_parameter_item import UI_ParameterListItem

# Paramater Selection Widget Class
class ParameterListItem(QFrame):

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

    def set_color(self, color):
        old_style = self.styleSheet()
        self.setStyleSheet(old_style + f'''
            background-color : {color};
        ''')


    