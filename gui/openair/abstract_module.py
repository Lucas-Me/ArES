# IMPORT QT MODULE
from qt_core import *

# IMPORT CUSTOM MODULES
from gui.widgets.checkable_combobox import CheckableComboBox


class AbstractPlot(QWidget):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

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
        site_layout = QHBoxLayout()
        site_layout.setContentsMargins(0, 0, 0, 0)
        site_layout.setSpacing(10)
        self.site_selection = CheckableComboBox()
        self.site_selection.lineEdit().setPlaceholderText("Selecione uma ou mais estações")
        self.site_selection.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Fixed)
        site_label = QLabel("Estações")
        site_label.setFixedWidth(80)
        site_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        site_layout.addWidget(site_label)
        site_layout.addWidget(self.site_selection)

        # parameter combobox
        parameter_layout = QHBoxLayout()
        parameter_layout.setContentsMargins(0, 0, 0, 0)
        parameter_layout.setSpacing(10)
        self.parameter_selection = CheckableComboBox()
        self.parameter_selection.lineEdit().setPlaceholderText("Selecione um ou mais parâmetros")
        self.parameter_selection.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Fixed)
        parameter_label = QLabel("Parâmetros")
        parameter_label.setFixedWidth(80)
        parameter_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        parameter_layout.addWidget(parameter_label)
        parameter_layout.addWidget(self.parameter_selection)

        # ADD TO MAIN LAYOUT
        # ////////////////
        self.main_layout.addWidget(self.image_name, alignment= Qt.AlignmentFlag.AlignTop)
        self.main_layout.addLayout(site_layout)
        self.main_layout.addLayout(parameter_layout)

        # border
        label_border = QLabel()
        label_border.setObjectName('border')
        self.main_layout.addWidget(label_border)

        # SET STYLESHEET
        self.setObjectName('module')
        self.setStyleSheet(f'''
            #module {{
                background-color: #efefef;
            }}
            QLabel {{
                color: #000000;
                font: normal 10pt "Microsoft New Tai Lue";
            }}
            #border {{
                border-bottom: 3px solid #dcdcdc;
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