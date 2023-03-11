# IMPORT QT MODULES
from qt_core import *

# IMPORT MODULES
from copy import copy
import gc

# IMPORT CUSTOM WIDGETS
from gui.widgets.menu.buttons import ChartButton, CreateChartButton
from gui.windows.dialog.chart.chart_selection import ChartCreationDialog

class ChartList(QListWidget):

    rowClicked = Signal(object)
    def __init__(self, width, parent = None):
        super().__init__()

        self.maxrows = 6
        self.item_height = 40
        self.parent = parent
        self.current_selection = 0

        # SETUP UI
        self.setup_style()

        # SETTINGS
        self.setFixedWidth(width)
        self.setupWidgets()
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        # SIGNALS AND SLOTS
        self.InsertWidget.createRow.connect(self.creationDialog)
    
    def setupWidgets(self):
        item = QListWidgetItem()
        item.setSizeHint(QSize(self.width(), self.item_height))
        self.addItem(item)

        # create frame
        self.InsertWidget = CreateChartButton(height = 40)
        self.setItemWidget(item, self.InsertWidget)
    
    @Slot(str)
    def creationDialog(self, text):
        # getting the type of chart
        self.dialog = ChartCreationDialog(parent = self.parent)
        self.dialog.selection.connect(lambda x: self.handleSelection(text, x))
        self.dialog.show()

    def handleSelection(self, text, add):
        if not add:
            return None
        
        self.current_selection = self.dialog.ui.combobox.currentIndex()
        self.insertRow(text)

    def insertRow(self, text):
        n = copy(self.count())

        # don't create if greater than max
        if n > self.maxrows:
            return None

        # creating QListWidgetItem
        item = QListWidgetItem()
        item.setSizeHint(QSize(self.width(), self.item_height))
        self.insertItem(n - 1, item)
        
        # create widget
        widget = ChartButton(text = text, height = 40)
        self.setItemWidget(item, widget)

        # emit signal
        widget.clicked.connect(
            lambda: self.rowClicked.emit(item)
        )
        widget.click()

    def deleteRow(self, ListWidgetItem : QListWidgetItem):
        # removing from list
        self.removeItemWidget(ListWidgetItem)
        self.takeItem(self.row(ListWidgetItem))

        # Deleting ListWidgetItem
        del ListWidgetItem

        
    def setup_style(self):

        self.setStyleSheet('''
            background-color: transparent;
            border: none;
        ''')