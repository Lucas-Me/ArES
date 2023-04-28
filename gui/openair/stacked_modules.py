# IMPORT QT CORE
from qt_core import *

# IMPORT PAGES
from gui.openair.time_variation import TimeVariationPlot

class StackedModules(QStackedWidget):

    def __init__(self, parent) -> None:
        super().__init__(parent)

        # PAGES
        self.pages = {
            'TimeVariation' : TimeVariationPlot(parent = self.parent())
        }

        # COMMANDS
        self.initWidgets()
        self.setCurrentWidget('TimeVariation')

    def initWidgets(self):
        for key in self.pages.keys():
            self.addWidget(self.getWidget(key))

    def getWidget(self, key : str):
        return self.pages.get(key, None)
    
    def setCurrentWidget(self, key : str) -> None:
        w = self.getWidget(key)
        return super().setCurrentWidget(w)