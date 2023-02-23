# IMPORT QT_CORE
from qt_core import *

# IMPORT CUSTOM MODULES
from gui.widgets.data_manager_qwidget import DataManager
from gui.widgets.login_screen import LoginScreen
from gui.widgets.processing_screen import ProcessingScreen
from gui.widgets.dashboard import Dashboard

class StackedPages(QStackedWidget):
    
    def __init__(self, parent) -> None:
        super().__init__(parent)

        # PROPERTIES
        self.chart_pages = [] # QWidgets
        self.chart_items = [] # ListWidgetItems

        # SETUP UI
        # CREATE PAGE 1
        self.login_page = LoginScreen(self)

        # CREATE PAGE 2
        self.data_page = DataManager()
        
        # CREATE PAGE 3
        self.process_page = ProcessingScreen(self)

        # insert pages into StackedWdiget (parent)
        self.addWidget(self.login_page)
        self.addWidget(self.data_page)
        self.addWidget(self.process_page)


    def createChartPage(self, item : QListWidgetItem):
        dashboard = Dashboard(parent = self)
        self.chart_pages.append(dashboard)
        self.chart_items.append(item)
        self.addWidget(dashboard)
        
        return dashboard

    def setCurrentWidget(self, w: QWidget) -> None:
        if isinstance(w, QListWidgetItem):
            
            # create if doesn't exist
            try:
                idx = self.chart_items.index(w)

            except ValueError:
                self.createChartPage(w)
                idx = -1

            w = self.chart_pages[idx]

        return super().setCurrentWidget(w)
