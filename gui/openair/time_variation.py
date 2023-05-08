# IMPORT QT CORE
from qt_core import *

# IMPORT CUSTOM MODULES
from gui.widgets.tag_bar import ColorTags
from gui.openair.abstract_module import AbstractPlot
from gui.widgets.colormap import ColormapWidget


class TimeVariationPlot(AbstractPlot):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        # UI
        self.setupUI()

        # SIGNALS AND SLOTS
        self.site_selection.dataChanged.connect(lambda: self.checkSelection(True))
        self.parameter_selection.dataChanged.connect(lambda: self.checkSelection(False))

    def checkSelection(self, is_site : bool):
        options = [self.parameter_selection.currentData(), self.site_selection.currentData()]

        # either sites or parameters must have 2 or more objects selected
        if len(options[0]) > 1 and len(options[1]) > 1:
            if is_site:
                self.parameter_selection.clearSelection()
            else:
                self.site_selection.clearSelection()

        # refresh the viewer
        self.legend_properties.updateTags(
            tag_names = options[is_site],
            colors = self.color_list
            )

    def setupUI(self):
        # UI AND LAYOUTS
        # ////////////////
        
        # xlabel description
        ylab = QLabel("Legendas do eixo vertical")
        ylab.setAlignment(Qt.AlignmentFlag.AlignLeft)

        # XLABEL tagbar
        self.ylab = QLineEdit()
        self.ylab.setPlaceholderText("Insira uma legenda... (Ex: Concentração [µg/m3])")

        # normaliza button
        self.normalise = QRadioButton("Normalizar variáveis")
        self.normalise.setChecked(False)
        self.normalise.setToolTip("Divide as variáveis pelos seus valores médios. Ajuda a comparar tendências diurnas entre variáveis com diferentes escalas.")

        # COLOR AND LEGEND 
        legends_label = QLabel("Esquema de cores")
        legends_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.legend_properties = ColorTags()
        self.colormap_edit = ColormapWidget()

        # ADD TO MAIN LAYOUT
        # ////////////////
        self.main_layout.addWidget(ylab)
        self.main_layout.addWidget(self.ylab)
        self.main_layout.addWidget(self.normalise)
        self.main_layout.addWidget(legends_label)
        self.main_layout.addWidget(self.colormap_edit)
        self.main_layout.addItem(QSpacerItem(30, 30, QSizePolicy.Expanding, QSizePolicy.MinimumExpanding))

        # SIZE POLICIES
        self.colormap_edit.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Minimum)

    def getArgs(self):
        super_args = super().getArgs()
        args = super_args + [
            "--ylab", self.ylab.text(),
            '--normalise', str.upper(str(self.normalise.isChecked())), 
        ]

        return args