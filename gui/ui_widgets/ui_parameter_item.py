# IMPORT QT CORE
from qt_core import *

# IMPORT CUSTOM MODULES
from gui.widgets.py_radio_button import PyRadioButton

class UI_ParameterListItem(object):

    def setup_ui(self, parent : QFrame):
        parent.setObjectName("parameter_item")

        # UI PROPERTIES
        background_color = '#ffffff'
        font = 'Microsoft New Tai Lue'
        text_color = '#32495e'

        # SETTING UP PROPERTIES
        parent.setMinimumWidth(parent.item_width)
        parent.setFixedHeight(parent.item_height)

        # MAIN LAYOUT
        self.main_layout = QHBoxLayout(parent)
        self.main_layout.setContentsMargins(10, 0, 10, 0)
        self.main_layout.setSpacing(10)

        # CREATING CHECKBOX
        self.check_box = PyRadioButton(40, 40)

        # Creating Labels
        self.name_label = QLabel(parent.name)
        self.theme_label = QLabel(parent.theme)
        self.unit_label = QLabel(parent.unit)
        #
        self.name_label.setObjectName('name')
        self.theme_label.setObjectName('theme')
        self.unit_label.setObjectName('unit')

        # width and height of objects
        self.theme_label.setFixedWidth(150)
        self.unit_label.setFixedWidth(100)

        # INSERTING WIDGETS IN MAIN LAYOUT
        self.main_layout.addWidget(self.check_box)
        self.main_layout.addWidget(self.name_label)
        self.main_layout.addWidget(self.unit_label)
        self.main_layout.addWidget(self.theme_label)

        # stylesheets
        parent.setStyleSheet(f'''
            #parameter_item {{
                background-color : {background_color};
                border-bottom: 0.5px solid;
                border-color: #dcdcdc;
            }}
            #name, #theme, #unit {{
                font: 500 13pt {font};
                color: {text_color}; 
            }}
            '''
        )

