# IMPORT QT CORE
from qt_core import *

# IMPORT CUSTOM UI
from gui.pages.ui_visualization import UI_DataVisualization
from gui.widgets.dashboard import Dashboard

# Data Manager Page Class
class DataVisualizationScreen(QWidget):

    def __init__(self, parent : QStackedWidget):
        super().__init__(parent = parent)

        # PROPERTIES
        self.tab_widget = TabWidget(parent = self)
        self.data_handles = []
        
        # SETUP UI
        self.ui = UI_DataVisualization()
        self.ui.setup_ui(self)

        # SETTINGS
        self.addDashboard()

    def getDataHandles(self):
        return self.data_handles
    
    def addDashboard(self):
        # creating and updating dashboard
        dashboard = Dashboard(parent = self)
        dashboard.updateItems()

        # inserting dashboard into tab widget
        n = self.tab_widget.count()
        self.tab_widget.addTab(dashboard, f'Tela {n + 1}')

    def updateDataHandles(self, handles : list):
        self.data_handles = handles

        # updating dashboard options
        n = self.tab_widget.count()
        for i in range(n):
            widget = self.tab_widget.widget(i)
            widget.updateItems()

    def paintEvent(self, event: QPaintEvent) -> None:
        '''
        Reinicia o painter deste QWidget, para que ele nao herde as propriedades do
        parent.
        '''
        # super().paintEvent(event)

        opt = QStyleOption()
        opt.initFrom(self)
        p = QPainter(self)
        self.style().drawPrimitive(QStyle.PE_Widget, opt, p, self)


class TabBar(QTabBar):
    def tabSizeHint(self, index):
        s = QTabBar.tabSizeHint(self, index)
        return s

    def paintEvent(self, event):
        painter = QStylePainter(self)
        opt = QStyleOptionTab()

        for i in range(self.count()):
            self.initStyleOption(opt, i)
            painter.drawControl(QStyle.CE_TabBarTabShape, opt)
            painter.save()

            s = opt.rect.size()
            r = QRect(QPoint(), s)
            r.moveCenter(opt.rect.center())
            opt.rect = r

            # c = self.tabRect(i).center()
            # painter.translate(c)
            # painter.translate(-c)
            painter.drawControl(QStyle.CE_TabBarTabLabel, opt);
            painter.restore()


class TabWidget(QTabWidget):
    def __init__(self, *args, **kwargs):
        QTabWidget.__init__(self, *args, **kwargs)
        self.setTabBar(TabBar(self))
        self.setTabPosition(QTabWidget.North)