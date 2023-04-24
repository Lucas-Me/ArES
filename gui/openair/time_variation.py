# IMPORT QT CORE
from qt_core import *

# IMPORT CUSTOM MODULES
from gui.widgets.checkable_combobox import CheckableComboBox
from gui.widgets.tag_bar import TagBar
from gui.openair.abstract_module import AbstractPlot


class TimeVariationPlot(AbstractPlot):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        # PRIVATE VARIABLES


        # UI
        self.setupUI()

    def setupUI(self):
        # UI AND LAYOUTS
        # ////////////////
        
        # XLABEL tagbar
        self.xlab_tagbar = TagBar()

        # ADD TO MAIN LAYOUT
        # ////////////////
        self.main_layout.addWidget(self.xlab_tagbar)

        # BOTTOM SPACER
        bottom_spacer = QSpacerItem(20, 20, QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)

        # ADD SPACER TO LAYOUT
        self.main_layout.addItem(bottom_spacer)