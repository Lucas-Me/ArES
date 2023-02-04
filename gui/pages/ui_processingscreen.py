# IMPORT QT_CORE
from qt_core import *

# IMPORT CUSTOM MODULES
from backend.misc.functions import get_imagepath
from gui.widgets.parameter_summary import ParameterSummary

# Data Manager Page UI Class
class UI_ProcessScreen(object):
    
    def setup_ui(self, parent):
        
        # FRAME CONSTANTS
        parent.setObjectName(u'process_page')

        # MAIN LAYOUT
        self.main_layout = QGridLayout(parent)
        self.main_layout.setVerticalSpacing(20)
        self.main_layout.setHorizontalSpacing(20)
        self.main_layout.setContentsMargins(30, 30, 30, 30)

        # UPPER LEFT LAYOUT
        # ////////////////////////////////////////////////////////////////
        w = 450
        self.upper_left_layout = QVBoxLayout()
        self.upper_left_layout.setSpacing(10)
        self.upper_left_layout.setContentsMargins(0, 0, 0, 0)
        
        # INFOMARTIVE LABELS
        self.total_loaded_label = QLabel()
        self.total_loaded_label.setFixedSize(w, 50)
        self.total_loaded_label.setObjectName('total_label')

        # SELECTED TIME PERIOD
        self.date_selected_label = QLabel()
        self.date_selected_label.setFixedSize(w, 50)
        self.date_selected_label.setObjectName('date_label')

        # CHECK BOX FOR KIND OF DATA SELECTION (VALID, INVALID, SUSPECT)
        self.check_box_label = QLabel("Incluir dados")
        self.check_box_label.setFixedSize(w, 20)
        self.check_box_label.setObjectName('checkbox_label')

        # CHECKBOXES OF OPTIONS
        texts = ['Válidos', 'Inválidos', 'Suspeitos']
        ids = ['validos', 'invalidos', 'suspeitos']
        self.check_boxes = []

        # ADD TO UPPER LEFT LAYOUT
        self.upper_left_layout.addWidget(self.total_loaded_label)
        self.upper_left_layout.addWidget(self.date_selected_label)
        self.upper_left_layout.addWidget(self.check_box_label)

        for i in range(3):
            check_box = QCheckBox(texts[i])
            check_box.setObjectName(ids[i])
            #
            check_box.setFixedSize(200, 30)
            check_box.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            self.check_boxes.append(check_box)
            #
            self.upper_left_layout.addWidget(check_box)
            self.upper_left_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)

        # LIST LAYOUT
        # //////////////////////////////////////////////////////////////////
        self.list_summary = ParameterSummary()
        
        # MAIN LAYOUT CONFIGURATION
        # ////////////////////////////////////////////////////////////////
        self.main_layout.addLayout(self.upper_left_layout, 0, 0)
        self.main_layout.addWidget(self.list_summary, 1, 0, 1, 2)


    def setup_stylesheet(self, parent):
        # CONSTANTS
        font = 'sans-serif'
        font_color = '#757d8e'
        bg_color = '#F0F0F0'
        border_radius = 10

        checked_path = get_imagepath('checkbox_checked_circle.svg', 'gui/images/icons')
        unchecked_path = get_imagepath('checkbox_unchecked_circle.svg', 'gui/images/icons')

        # UPPER LEFT STYLESHEET
        parent.setStyleSheet(f'''
            #process_page{{
                background-color: {bg_color};
            }}
            #total_label, #date_label {{
                background-color: #ffffff;
                font: 500 16pt '{font}';
                color: {font_color};
                border: 1px solid;
                border-color: {font_color};
                border-radius: {border_radius}px;
                text-align: left;
                padding-left: 10px;
            }}
            #checkbox_label {{
                font: 600 16pt '{font}';
                color: {font_color};
                border: none;
                text-align: left;
                padding-left: 10px;
            }}
            #validos, #invalidos, #suspeitos {{
                background-color: transparent;
                font: 500 14pt '{font}';
                color: {font_color};
                border: 1px solid;
                border-color: {font_color};
                text-align: middle;
                padding-left: 10px;
            }}
            #validos::indicator:checked, #invalidos::indicator:checked, #suspeitos::indicator:checked {{
                image: url({checked_path});
            }}
            #validos:checked, #invalidos:checked, #suspeitos:checked {{
                background-color: #3cd7e8;
                color: white;
            }}
            #validos:checked:hover, #invalidos:checked:hover, #suspeitos:checked:hover {{
                background-color: #1ba5b4;
                color: white;
            }}
            #validos::indicator:unchecked, #invalidos::indicator:unchecked, #suspeitos::indicator:unchecked {{
                image: url({unchecked_path});
            }}
            #validos:unchecked, #invalidos:unchecked, #suspeitos:unchecked {{
                background-color: transparent;
                color: {font_color};
            }}
            #validos:unchecked:hover, #invalidos:unchecked:hover, #suspeitos:unchecked:hover {{
                background-color: white;
                color: {font_color};
            }}
        ''')

    