# IMPORT QT CORE
from qt_core import *

# IMPORT CUSTOM MODULES
from gui.openair.abstract_module import AbstractPlot
from gui.widgets.colormap import DiscreteColormap


class WindRose(AbstractPlot):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        # UI
        self.setupUI()

    def setupUI(self):
        # UI AND LAYOUTS
        # ////////////////

        # GROUPBOX "AGRUPAR POR"
        self.groupby_types = GroupBoxTypes()

        # # COLOR AND LEGEND 
        legends_label = QLabel("Esquema de cores")
        legends_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.colormap_edit = DiscreteColormap(colors =['#4331a0',
            '#2670c0',
            '#43c4b5',
            '#b4e97e',
            '#fcf8be',
            '#ecc852',
            '#fa6916',
            '#d31818',
            '#99123f'])

        # # ADD TO MAIN LAYOUT
        # # ////////////////
        self.main_layout.addWidget(self.groupby_types)
        self.main_layout.addWidget(legends_label)
        self.main_layout.addWidget(self.colormap_edit)
        self.main_layout.addItem(QSpacerItem(30, 30, QSizePolicy.Expanding, QSizePolicy.MinimumExpanding))
        
        # REMOVING THE PARAMETER SELECTION
        layout = self.main_layout.takeAt(2)
        for i in reversed(range(layout.count())):
            item = layout.takeAt(i)
            item.widget().deleteLater()

        # # SIZE POLICIES
        # self.colormap_edit.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Minimum)

    def getArgs(self):
        image_name = self.getName()
        sites = ', '.join(self.site_selection.currentData())
        colors = ', '.join(self.colormap_edit.getColors())
        if len(sites) * len(image_name) == 0:
            raise KeyError

        args = [
            '--fname', f'{image_name}.png',
            '--sites', f'"{sites}"',
            # "--ylab", self.ylab.text(),
            # '--normalise', str.upper(str(self.normalise.isChecked())), 
            '--colors', f'"{colors}"',
            '--breaks', f'"{self.colormap_edit.levels.getLevels()}'
        ]

        return args
    
    def getPath(self):

        return './/backend//openair//windrose.r'
    
    def updateOptions(self, options):
        # clean
        self.site_selection.clear()

        # add options
        self.site_selection.addItems(options['site'])

        # updating text
        self.site_selection.updateText()


class GroupBoxTypes(QWidget):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # PRIVATE VARIABLES
        self.objects = []
        self.names = ["Estação", "Ano", "Mês", "Dia da semana", "Estação", "Poluente"]
        self.checked = []

        # SETTINGS
        self.setup_ui()
        self.setup_stylesheet()

    def setup_ui(self):
        # UI
        self.main_layout = QVBoxLayout(self)
        #
        groupbox = QGroupBox("Agrupar por")
        grid = QGridLayout(groupbox)
        grid.setContentsMargins(5, 5, 5, 5)
        grid.setSpacing(2)
        #
        self.main_layout.addWidget(groupbox)

        # RADIOBUTTONS
        for i, name in enumerate(self.names):
            button = QCheckBox(name)
            self.objects.append(button)
            #
            row = i // 2
            col = i % 2
            grid.addWidget(button, row, col)

    def setup_stylesheet(self):

        self.setStyleSheet("""
            QGroupBox {
                border: 1px solid gray;
                border-color: #FF17365D;
                margin-top: 27px;
                font-size: 14px;
                border-bottom-left-radius: 15px;
                border-bottom-right-radius: 15px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top center;
                border-top-left-radius: 15px;
                border-top-right-radius: 15px;
                padding: 5px 150px;
                background-color: #FF17365D;
                color: rgb(255, 255, 255);
            }
        """)
    
    def handleSelections(self, index):
        n = len(self.checked)

        # DISABLING LAST ONE
        if n >= 2:
            prev = self.checked.pop(0)
            self.objects[prev].setChecked(False)
    	
        # MARKING AS TRUE
        self.checked.append(index)
        self.objects[index].setChecked(True)
