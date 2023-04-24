# IMPORT QT_CORE
from qt_core import *
import gc

# IMPORT CUSTOM MODULES
from gui.widgets.data_manager_screen import DataManager
from gui.widgets.login_screen import LoginScreen
from gui.widgets.processing_screen import ProcessingScreen
from gui.widgets.openair_screen import OpenAirScreen
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

        # CREATE PAGE 4
        self.openair_page = OpenAirScreen(self)

        # insert pages into StackedWdiget (parent)
        self.addWidget(self.login_page)
        self.addWidget(self.data_page)
        self.addWidget(self.process_page)
        self.addWidget(self.openair_page)

    def deleteChartPage(self, widget):
        self.setCurrentIndex(0) # change page to login screen
        index = self.chart_pages.index(widget) # get index of widget to delete

        # delete from menu
        self.menu.charts_list.deleteRow(self.chart_items[index])

        # DELETE 
        del self.chart_items[index]
        del self.chart_pages[index]

        # garbage collector
        gc.collect()

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
        
        # updating openair options
        self.openair_page.updateItems(self.getDataHandles())

    def createChartPage(self, item : QListWidgetItem):
        # creating dashboard
        chart_option = self.menu.charts_list.current_selection
        dashboard = Dashboard(parent = self, option = chart_option)
        dashboard.deleteRequest.connect(lambda: self.deleteChartPage(dashboard))

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
