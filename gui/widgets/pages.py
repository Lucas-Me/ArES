# IMPORT QT_CORE
from qt_core import *

# IMPORT CUSTOM MODULES
from gui.widgets.data_manager_qwidget import DataManager
from gui.widgets.login_screen import LoginScreen
from gui.widgets.processing_screen import ProcessingScreen
from gui.widgets.dashboard import Dashboard

class StackedPages(QStackedWidget):
    '''
    Classe criada para gerenciar as páginas do software, incluindo as páginas dedicadas somente
    aos gráficos.
    '''
    
    def __init__(self, menu, parent = None) -> None:
        super().__init__(parent)

        # PROPERTIES
        self.menu = menu
        self.chart_pages = [] # QWidgets
        self.chart_items = [] # ListWidgetItems
        self.data_handles = [] # List of ModifiedData Objects (data after processing)

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

    def getDataHandles(self):
        return self.data_handles
    
    def getHandle(self, index):
        return self.data_handles[index]

    def updateDataHandles(self, handles : list):
        self.data_handles = handles

        # updating dashboard options
        n = len(self.chart_pages)
        for i in range(n):
            widget = self.chart_pages[i]
            widget.updateItems()

    def createChartPage(self, item : QListWidgetItem):
        # creating dashboard
        chart_option = self.menu.charts_list.current_selection
        dashboard = Dashboard(parent = self, option = chart_option)

        # Storing and inserting it on screen
        self.chart_pages.append(dashboard)
        self.chart_items.append(item)
        self.addWidget(dashboard)

        # update dashboard items
        dashboard.updateItems()
        
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
