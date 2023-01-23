# IMPORT QT CORE
from qt_core import *

# IMPORT BUILT-IN MODULES
from copy import copy

# IMPORT UI MODULES
from gui.ui_widgets.ui_parameter_list import UI_ParameterSelection

# IMPORT CUSTOM MODULES
from gui.widgets.parameter_list_item import ParameterListItem

# Paramater Selection Widget Class
class ParameterSelectionWidget(QListWidget):
    stateChanged = Signal(list)

    def __init__(self, width, item_height):
        super().__init__()

        # configuration
        self.setMinimumWidth(width)
        self.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        # parameters
        self.item_width = self.width()
        self.item_height = item_height
        self.nrows = 0  
        self.signature = ""

        # setup UI
        self.ui = UI_ParameterSelection()
        self.ui.setup_ui(self)

    def set_signature(self, string):
        self.signature = string[:]

    def get_signature(self):
        return self.signature

    def add_item(self, name : str, theme : str, unit : str, selected = False):
        # creating list item and adding to list
        ListItem = QListWidgetItem()
        parameter_frame = ParameterListItem(name, theme, unit, self.item_width, self.item_height, selected)
        n = copy(self.count())
        
        parameter_frame.stateChanged.connect(
            lambda x: self.emit_signal(x, n)
        )
        self.addItem(ListItem)

        # Setting Size Hint to ListWidgetItem
        SizeHint = QSize(self.item_width - 20, self.item_height)
        ListItem.setSizeHint(SizeHint)

        # setting object QFrame to QlistWidgetItem
        self.setItemWidget(ListItem, parameter_frame)
        self.nrows += 1

    def reset_settings(self):
        # cleaning variables
        self.set_signature('')
        self.clear()
        self.nrows = 0

    def emit_signal(self, state, row):
        self.stateChanged.emit([state, row])
