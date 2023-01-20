# IMPORT QT_CORE
from qt_core import *

# IMPORT CUSTOM MODULES
from gui.widgets.data_manager_qwidget import DataManager
from gui.widgets.login_screen import LoginScreen

class UI_StackedPages(object):
    def setup_ui(self, parent):
        if not parent.objectName():
            parent.setObjectName(u'app_pages')

        # CREATE PAGE 1
        self.page_1 = LoginScreen()

        # CREATE PAGE 2
        self.page_2 = DataManager()

        # insert pages into StackedWdiget (parent)
        parent.addWidget(self.page_1)
        parent.addWidget(self.page_2)