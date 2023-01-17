# IMPORT QT_CORE
from qt_core import *

# IMPORT CUSTOM MODULES
from gui.widgets.data_manager_qwidget import DataManager

class UI_StackedPages(object):
    def setup_ui(self, parent):
        if not parent.objectName():
            parent.setObjectName(u'app_pages')

        # CREATE PAGE 1
        self.page_1 = QWidget()

        # CREATE PAGE 2
        self.page_2 = DataManager()

        # center label
        self.label = QLabel("Página 1")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # create layout
        self.page_1_layout = QVBoxLayout(self.page_1)
        self.page_1_layout.addWidget(self.label)

        # insert pages into StackedWdiget (parent)
        parent.addWidget(self.page_1)
        parent.addWidget(self.page_2)
