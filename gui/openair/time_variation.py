# IMPORT QT CORE
from qt_core import *

# IMPORT CUSTOM MODULES
from gui.widgets.checkable_combobox import CheckableComboBox


class TimeVariationPlot(QWidget):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        # PRIVATE VARIABLES


        # UI
        self.setup_ui()

    def getName(self):
        return self.image_name.text()
    
    def getArgs(self):
        image_name = self.getName()
        sites = ', '.join(self.site_selection.currentData())
        parameters = ', '.join(self.parameter_selection.currentData())
        if len(sites) * len(parameters) * len(image_name) == 0:
            raise KeyError

        args = [
            '--fname', f'{image_name}.png',
            '--sites', f'"{sites}"',
            '--parameters', f'"{parameters}"'
        ]

        return args
        

    def setup_ui(self):
        # UI AND LAYOUTS
        # ////////////////
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(10, 10, 10, 10)
        self.main_layout.setSpacing(10)

        # UNIVERSAL OPTIONS
        # ////////////////
        self.image_name = QLineEdit()
        self.image_name.setPlaceholderText('Nome da figura (ex: variacao_pm10_rio)')

        # site combobox
        self.site_selection = CheckableComboBox()

        # parameter combobox
        self.parameter_selection = CheckableComboBox()

        # ADD TO MAIN LAYOUT
        # ////////////////
        self.main_layout.addWidget(self.image_name, alignment= Qt.AlignmentFlag.AlignTop)
        self.main_layout.addWidget(self.site_selection)
        self.main_layout.addWidget(self.parameter_selection)

        # BOTTOM SPACER
        bottom_spacer = QSpacerItem(20, 20, QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)

        # ADD SPACER TO LAYOUT
        self.main_layout.addItem(bottom_spacer)

        # SET STYLESHEET
        self.setObjectName('module')
        self.setStyleSheet(f'''
            #module {{
                background-color: #efefef;
            }}
        ''')

    def updateOptions(self, options):
        # clean
        self.site_selection.clear()
        self.parameter_selection.clear()

        # add options
        self.site_selection.addItems(options['site'])
        self.parameter_selection.addItems(options['parameter'])

        # updating text
        self.site_selection.updateText()
        self.parameter_selection.updateText()


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