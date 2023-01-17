# IMPORT QT CORE
from qt_core import *

# IMPORT CUSTOM MODULES
from gui.widgets.py_radio_button import PyRadioButton

class UI_ParameterListItem(object):

    def setup_ui(self, parent):
        if not parent.objectName():
            parent.setObjectName("Parameter List")

        # UI PROPERTIES
        background_color = '#ffffff'
        self.frame_color = '#e1e7e8'
        self.text_color = '#2874bf'
        self.bold_color = '#506369'

        # SETTING UP PROPERTIES
        parent.setStyleSheet(
            f'''
            border : none;
            background-color : {background_color};
            left: 100%;
            bottom: 0;
            border-bottom: 0px solid {self.frame_color};
            '''
        )
        parent.setMinimumWidth(parent.item_width)
        parent.setMinimumHeight(parent.item_height - 5)
        parent.setMaximumHeight(parent.item_height - 5)

        # MAIN LAYOUT
        self.main_layout = QHBoxLayout(parent)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        # CREATING CHECKBOX
        self.check_box = PyRadioButton(40, 40)

        # Creating Labels
        self.name_label = QLabel(parent.name)
        self.theme_label = QLabel(parent.theme)
        self.unit_label = QLabel(parent.unit)

        # setting style sheets to labels
        bold_stylesheet = f'''
            color : {self.bold_color};
            font-size: 12pt;
            font-weight: bold;
            font-family : "Microsoft New Tai Lue";
            text-align: left;
            vertical-align: middle;
        '''
        normal_stylesheet = f'''
            color: {self.text_color};
            font-size: 12pt;
            font-weight: 600;
            text-align: left;
            font-family : "Microsoft New Tai Lue";
            vertical-align: middle;
        '''
        self.name_label.setStyleSheet(normal_stylesheet)
        self.theme_label.setStyleSheet(bold_stylesheet)
        self.unit_label.setStyleSheet(bold_stylesheet)

        # width and height of objects
        self.theme_label.setFixedWidth(200)
        self.unit_label.setFixedWidth(100)

        # INSERTING WIDGETS IN MAIN LAYOUT
        self.main_layout.addWidget(self.check_box)
        self.main_layout.addWidget(self.name_label)
        self.main_layout.addWidget(self.unit_label)
        self.main_layout.addWidget(self.theme_label)


