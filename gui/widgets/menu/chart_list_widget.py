# IMPORT QT MODULES
from qt_core import *

# IMPORT MODULES
from copy import copy

# IMPORT CUSTOM WIDGETS
from gui.widgets.menu.buttons import ChartButton, CreateChartButton

class ChartList(QListWidget):

    rowClicked = Signal(object)
    def __init__(self, width):
        super().__init__()

        self.maxrows = 6
        self.item_height = 40

        # SETUP UI
        self.setup_style()

        # SETTINGS
        self.setFixedWidth(width)
        self.setupWidgets()
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        # SIGNALS AND SLOTS
        self.InsertWidget.createRow.connect(self.insertRow)
    
    def setupWidgets(self):
        item = QListWidgetItem()
        item.setSizeHint(QSize(self.width(), self.item_height))
        self.addItem(item)

        # create frame
        self.InsertWidget = CreateChartButton(height = 40)
        self.setItemWidget(item, self.InsertWidget)
    
    @Slot(str)
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

    def setup_style(self):

        self.setStyleSheet('''
            background-color: transparent;
            border: none;
        ''')