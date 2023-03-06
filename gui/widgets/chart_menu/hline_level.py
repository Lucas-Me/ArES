# IMPORT QT MODULES
from qt_core import *

# IMPOORT CUSTOM WIDGETS
from gui.widgets.chart_menu.buttons import TopLevelButton


class HLineTopLevel(QWidget):
    
    stateChanged = Signal(bool, int)
    valueChanged = Signal(int, int)
    def __init__(self, text, height, n = 4):
        super().__init__()

        # PROPERTIES
        self.item_height = height
        self.text = text
        self.nhlines = n
        self.hlines = [HorizontalLineProperty(height= height, index = i) for i in range(n)]

        # SETUP UI
        self.setupUI()
        self.toggle()

        # SIGNALS
        self.top_level.clicked.connect(self.toggle)

    def toggle(self):
        hidden = self.top_level.getStatus()
        active = not hidden

        # toggle on (active) or off
        self.top_level.setActive(active)

        # SHOW/HIDDEN widgets
        for hline_frame in self.hlines:
            hline_frame.setHidden(hidden)

        # size policty
        if active:
            self.setFixedHeight(self.item_height * (self.nhlines + 1))
        else:
            self.setFixedHeight(self.item_height)

    def setupUI(self):
        if not self.objectName():
            self.setObjectName("series_top_level")

        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        # OBJECTS
        self.top_level = TopLevelButton(text = self.text, height = self.item_height)
        self.main_layout.addWidget(self.top_level)

        # HORIZONTAL LINE OPTION
        for i in range(self.nhlines):
            self.main_layout.addWidget(self.hlines[i])

            # signals
            self.hlines[i].valueChanged.connect(self.valueChanged.emit)
            self.hlines[i].stateChanged.connect(self.stateChanged.emit)


class HorizontalLineProperty(QFrame):

    valueChanged = Signal(int, int)
    stateChanged = Signal(bool, int)
    def __init__(self, height, index):
        super().__init__()
        
        # SETTINGS
        # self.setMinimumHeight(0)
        self.setFixedHeight(height)

        # PROPERTIES
        self.index = index
        self.label = QLabel(f'Faixa Horizontal {index}')
        self.spinbox = QSpinBox()
        self.left_margin = 25

        # SETTING WIDGETS
        self.spinbox.setRange(0, 1000)

        # SETUP UI
        self.setupUI()
        self.setupStyle()

        # SIGNALS
        self.spinbox.editingFinished.connect(self.emitValue)
        self.checkbox.stateChanged.connect(lambda x: self.stateChanged.emit(x, self.index))

    def emitValue(self):
        if self.checkbox.isChecked():
            self.valueChanged.emit(self.spinbox.value(), self.index)

    def setupUI(self):
        self.main_layout = QHBoxLayout(self)
        self.main_layout.setContentsMargins(self.left_margin + 4, 3, 3, 3)
        self.main_layout.setSpacing(5)
        self.setObjectName('item')

        # Checkbox
        self.checkbox = QCheckBox()
        self.checkbox.setObjectName('checkbox')

        # TEXT
        self.label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.label.setObjectName('line')

        # FONTSIZE
        self.spinbox.setObjectName('combobox')

        # ADD TO MAIN LAYOUT
        self.main_layout.addWidget(self.checkbox)
        self.main_layout.addWidget(self.spinbox)
        self.main_layout.addWidget(self.label)

    def setupStyle(self):
        self.setStyleSheet('''
            #item{
                background-color: transparent;
            }
            #spinbox, #line, #checkbox{
                font: normal 10pt 'Microsoft New Tai Lue';
                color: #36475f;
            }
        ''')

    def paintEvent(self, event: QPaintEvent) -> None:
        super().paintEvent(event)

        painter = QPainter()
        painter.begin(self)
        
        dx = 2
        x = (self.left_margin - dx) // 2
        y = 0
        dy = self.height()
        painter.fillRect(x, y, dx, dy, QColor('#36475f'))

        painter.end()
        
