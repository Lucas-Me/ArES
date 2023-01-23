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
        self.login_page = LoginScreen(parent)

        # CREATE PAGE 2
        self.data_page = DataManager()

        # insert pages into StackedWdiget (parent)
        parent.addWidget(self.login_page)
        parent.addWidget(self.data_page)