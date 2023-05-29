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
        
        # # xlabel description
        # ylab = QLabel("Legendas do eixo vertical")
        # ylab.setAlignment(Qt.AlignmentFlag.AlignLeft)

        # # XLABEL tagbar
        # self.ylab = QLineEdit()
        # self.ylab.setPlaceholderText("Insira uma legenda... (Ex: Concentração [µg/m3])")

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
        # self.main_layout.addWidget(ylab)
        # self.main_layout.addWidget(self.ylab)
        # self.main_layout.addWidget(self.normalise)
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
            '--colors', f'"{colors}"'
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